from kivy.uix.gridlayout import GridLayout
from kivy.properties import ReferenceListProperty, NumericProperty, BooleanProperty, ObjectProperty
from chili_card import ChiliCard
from constants import UNFLIPPED, FLIPPED, GUESSED, MAX_FLIPPED_CARDS


class ChiliGrid(GridLayout):
    chiligame = ObjectProperty(None)
    gridsize = ReferenceListProperty(GridLayout.rows, GridLayout.cols)
    # Number of current flipped cards
    num_flipped_cards = NumericProperty(0)
    can_flip_cards = BooleanProperty(True)
    flipped_cards = []
    last_match = False

    def __init__(self, *args, **kwargs):
        super(ChiliGrid, self).__init__(*args, **kwargs)
        #self.bind(last_match=self.chiligame.cards_matched)
    
    def add_card(self, card):
        card.bind(status=self.card_changed)
        self.add_widget(card)
    
    def card_changed(self, card, status):    
        if not card.flip_by_user:
            return

        if status == FLIPPED:
            self.num_flipped_cards += 1 
            print "card", card, "flipped", status
            self.flipped_cards.append(card)
        elif status == UNFLIPPED or status == GUESSED:
            if card in self.flipped_cards:
                self.num_flipped_cards -= 1
                self.flipped_cards.remove(card)

        print "num flipped cards", len(self.flipped_cards)
        if self.num_flipped_cards == MAX_FLIPPED_CARDS:
            print "MAX FLIPPED"
            #user flipped all the allowed number of cards
            self.can_flip_cards = False  # No more flips allowed
            r = self.match_cards()
            if r:
                # Guess all cards in trio
                self.guess_cards()
                self.can_flip_cards = True
            else:
                # Unflip all cards
                self.unflip_cards()
            self.last_match = r
            self.chiligame.cards_matched(self.last_match)
             

    def unflip_cards(self):
        cards = [c for c in self.flipped_cards]  # We need a copy because
                                                 # flipped_cards changes
                                                 # inside 'for' statement.
        for card in cards:
            card.unflip()

    def guess_cards(self):
        cards = [c for c in self.flipped_cards]
        for card in cards:
            card.guess()

    def match_cards(self):
        c1, c2, c3 = self.flipped_cards
        if c1.value == c2.value == c3.value:
            # Mark cards as guessed
            print "guessed"
            return True
        print "not"
        return False
