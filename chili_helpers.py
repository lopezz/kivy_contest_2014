'''
Helper
=====

Helpers available to the user.
- ShowCardsHelper: Shows random cards in the grid for several seconds and
then unflips them back.
- GuessObject: If the last flipped card is an Image or Audio card the user
can use this helper and try to guess the object's name and automatically
unflips the remaining cards of the trio.
'''

from constants import UNFLIPPED
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.event import EventDispatcher
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from chili_card import ChiliWordCard
from constants import FLIPPED
import random


class Helper(EventDispatcher):

    ''' Base class for a Helper.
        Inherits from EventDispatcher to allow kivy properties to work. '''

    remaining = NumericProperty(2)
    ''' Remaining uses of the helper. '''
    chiligame = None
    executing = False
    ''' True if helper is currently executing. '''

    def can_use(self):
        ''' Returns True or False if helper can be used or not. '''
        return (not self.executing) and \
               (self.remaining > 0 or self.remaining == -1)

    def activate(self):
        ''' Activates helper's process. '''
        self.executing = True
        self._run()
        if self.remaining > 0:
            self.remaining -= 1

    def _run(self):
        ''' Internal implementation of help process. '''
        print "Override!"
        return


class ShowCardsHelper(Helper):

    ''' Shows N currently unflipped cards during T seconds. '''
    helper_name = "show"
    N = 6
    T = 8
    cards2show = []

    def _run(self):
        unflipped_cards = [
            c for c in self.chiligame.card_list if c.status == UNFLIPPED]
        random.shuffle(unflipped_cards)

        # Show N cards or remaining ones.
        num2show = min(self.N, len(unflipped_cards))

        if not num2show:  # No cards to flip
            self.executing = False
            return

        self.cards2show = unflipped_cards[:num2show]

        for c in self.cards2show:
            c.flip(by_user=False)  # User didn't flip these cards
        Clock.schedule_once(self.unflip_cards, self.T)

    def unflip_cards(self, t):
        for c in self.cards2show:
            c.unflip()
        self.executing = False  # End of execution


class GuessObjectView(ModalView):

    ''' Modal Widget for GuessObjectHelper '''
    tinput = TextInput(text='', multiline=False, focus=True, font_size='30dp')

    def __init__(self, *args, **kwargs):
        super(GuessObjectView, self).__init__(*args, **kwargs)
        bx = BoxLayout(orientation='vertical')
        bx.add_widget(
            Label(text='Type Object name and press Enter', font_size='18dp'))
        bx.add_widget(self.tinput)
        self.add_widget(bx)

    def open(self):
        super(GuessObjectView, self).open()
        self.tinput.focus = True

    def on_enter(self, instance):
        self.dismiss()  # Close popup when users presses Enter.


class GuessObjectHelper(Helper):

    ''' Guess object's name helper. If guessed, remaining unflipped cards
    of trio are flipped '''

    remaining = NumericProperty(5)
    modal = GuessObjectView(size_hint=(0.4, 0.15), auto_dismiss=False)
    last_card = None

    def __init__(self, *args, **kwargs):
        super(GuessObjectHelper, self).__init__(*args, **kwargs)
        self.modal.tinput.bind(on_text_validate=self.on_enter)

    def can_use(self):
        r = super(GuessObjectHelper, self).can_use()
        last_card = self.last_valid_card()
        return r and last_card is not None

    def last_valid_card(self):
        ''' Returns last flipped card if it's sound or image,
            otherwise returns None. '''
        last_card = None
        if self.chiligame.chiligrid.num_flipped_cards:
            last_card = self.chiligame.chiligrid.flipped_cards[-1]
        else:
            return None

        if isinstance(last_card, ChiliWordCard):
            return None

        return last_card

    def _run(self):
        last_card = self.last_valid_card()
        if last_card is not None:
            self.last_card = last_card
            self.modal.open()  # Show modal
        else:  # No valid card flipped, end execution.
            self.executing = False

    def on_enter(self, instance):
        ''' Callback when user inputs text and presses Enter key. '''
        value = self.last_card.value
        if instance.text.lower() == value.lower():
            for c in self.chiligame.card_list:  # Unflip all first
                if c.status == FLIPPED and c is not self.last_card:
                    c.unflip()

            for c in self.chiligame.card_list:  # Open all the other cards
                if c.value == value and c is not self.last_card:
                    c.flip(by_user=True)

        self.modal.dismiss()
        self.modal.tinput.text = ''  # Empty textinput
        self.executing = False
