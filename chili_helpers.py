'''
Helpers user can  use to solve the grid.
'''
from constants import UNFLIPPED
from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty
from kivy.event import EventDispatcher
import random

class Helper(EventDispatcher):
    remaining = NumericProperty(2)
    # remaining = NumericProperty(0)
    # remaining = 2
    chiligame = None
    executing = False

    def can_use(self):
        return (not self.executing) and (self.remaining > 0 or self.remaining == -1)

    def activate(self):
        self.executing = True
        self._run()
        if self.remaining > 0:
            self.remaining -= 1

    def _run(self):
        ''' Internal implementation of help process'''
        print "Override!"
        return


class ShowCardsHelper(Helper):
    ''' Show N cards during T seconds '''
    helper_name = "show"
    N = 6
    T = 8
    cards2show = []

    def _run(self):
        unflipped_cards = [c for c in self.chiligame.card_list if c.status == UNFLIPPED]
        random.shuffle(unflipped_cards)

        num2show = min(self.N, len(unflipped_cards))  # Show N cards or remaining ones.

        if not num2show: # No cards to flip
            self.executing = False
            return

        self.cards2show = unflipped_cards[:num2show]
        
        for c in self.cards2show:
            c.flip(by_user=False) # User didn't flip these cards
            # TODO custom bground color
        Clock.schedule_once(self.unflip_cards, self.T)


    def unflip_cards(self, t):
        for c in self.cards2show:
            c.unflip()
        self.executing = False  # End of execution
