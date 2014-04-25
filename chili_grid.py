from kivy.uix.gridlayout import GridLayout
from kivy.properties import ReferenceListProperty, NumericProperty, BooleanProperty
from chili_card import ChiliCard
from constants import UNFLIPPED, FLIPPED, GUESSED, MAX_FLIPPED_CARDS


class ChiliGrid(GridLayout):

    gridsize = ReferenceListProperty(GridLayout.rows, GridLayout.cols)
    # Number of current flipped cards
    num_flipped_cards = NumericProperty(0)
    can_flip_cards = BooleanProperty(True)
    flipped_cards = []

    def __init__(self, *args, **kwargs):
        super(ChiliGrid, self).__init__(*args, **kwargs)
    
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
        elif status == UNFLIPPED:
            self.num_flipped_cards -= 1
            self.flipped_cards.append(card)

        if self.num_flipped_cards == MAX_FLIPPED_CARDS:
            #user flipped all the allowed number of cards
            self.can_flip_cards = False  # No more flips allowed
            # TODO check trio

        print "total flipped cards", self.num_flipped_cards
