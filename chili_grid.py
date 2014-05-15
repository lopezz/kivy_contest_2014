'''
ChiliGrid
=========
The grid of cards. It contains a  set of different ChiliCards that the
user can flip in order to match trios. The grid is populated by
ChiliTriosGame in ChiliTriosGame.new_game.
'''

from kivy.uix.gridlayout import GridLayout
from kivy.properties import (ReferenceListProperty, NumericProperty,
                             BooleanProperty, ObjectProperty)
from constants import UNFLIPPED, FLIPPED, GUESSED, MAX_FLIPPED_CARDS
from kivy.clock import Clock


class ChiliGrid(GridLayout):

    ''' ChiliGrid class defines the grid that contains all the cards in the
        set. '''

    chiligame = ObjectProperty(None)
    gridsize = ReferenceListProperty(GridLayout.rows, GridLayout.cols)
    num_flipped_cards = NumericProperty(0)
    ''' Number of current flipped cards. '''

    can_flip_cards = BooleanProperty(True)
    ''' Flag that allows/disallows the card flipping. '''

    flipped_cards = []
    ''' A list contaning the currently flipped cards. '''
    last_match = False

    def __init__(self, *args, **kwargs):
        super(ChiliGrid, self).__init__(*args, **kwargs)

    def reset(self):
        ''' Resets grid. '''
        self.clear_widgets()
        self.can_flip_cards = True
        self.num_flipped_cards = 0
        self.flipped_cards = []

    def add_card(self, card):
        ''' Adds a card to the grid '''

        card.bind(status=self.card_changed)
        self.add_widget(card)

    def card_changed(self, card, status):
        ''' Called when a card status changes '''

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

        if self.num_flipped_cards == MAX_FLIPPED_CARDS:
            print "MAX FLIPPED. Matching ..."
            # user flipped all the allowed number of cards
            self.can_flip_cards = False  # No more flips allowed
            Clock.schedule_once(self.match_cards, 0.5)

    def unflip_cards(self):
        ''' Unflips flipped cards '''
        cards = [c for c in self.flipped_cards]  # We need a copy because
                                                 # flipped_cards changes
                                                 # inside 'for' statement.
        for card in cards:
            card.unflip()

    def guess_cards(self):
        ''' Sets currently flipped cards as guessed '''
        cards = [c for c in self.flipped_cards]
        for card in cards:
            card.guess()

    def match_cards(self, t=0):
        ''' Returns True/False if currently flipped cards match '''
        c1, c2, c3 = self.flipped_cards
        r = False
        if c1.value == c2.value == c3.value:
            # Mark cards as guessed
            r = True
            self.guess_cards()

        else:
            # Unflip all cards
            self.unflip_cards()

        self.can_flip_cards = True
        self.last_match = r
        self.chiligame.cards_matched(self.last_match)

        return r
