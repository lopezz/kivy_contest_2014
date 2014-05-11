'''
Helpers user can  use to solve the grid.
'''
from constants import UNFLIPPED
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.event import EventDispatcher
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from chili_card import ChiliWordCard
from constants import FLIPPED
import random

class Helper(EventDispatcher):
    remaining = NumericProperty(2)
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

class GuessObjectView(ModalView):
    ''' Widget for GuessObjectHelper '''
    tinput = TextInput(text='', multiline=False, focus=True)

    def __init__(self, *args, **kwargs):
        super(GuessObjectView, self).__init__(*args, **kwargs)
        bx = BoxLayout(orientation='vertical') 
        bx.add_widget(Label(text='Type Object name in the box below and press Enter'))
        bx.add_widget(self.tinput)
        #bx.add_widget(Button(text='Done'))
        self.add_widget(bx)

    def open(self):
        super(GuessObjectView, self).open()
        self.tinput.focus = True

    def on_enter(self, instance):
        print "text", instance.text
        self.dismiss()


class GuessObjectHelper(Helper):
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
        ''' Returns last flipped card if it's sound or object, 
            otherwise returns None '''
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
        else: # No valid card flipped, end execution.
            self.executing = False

    def on_enter(self, instance):
        ''' Callback when user input text and press enter '''
        value = self.last_card.value
        if instance.text.lower() == value.lower():
            for c in self.chiligame.card_list:  # Unflip all first
                if c.status == FLIPPED and c is not self.last_card:
                    c.unflip()

            for c in self.chiligame.card_list: # Open all the other cards
                if c.value == value and c is not self.last_card:
                    c.flip(by_user=True)

        self.modal.dismiss()
        self.modal.tinput.text = '' # Empty textinput
        self.executing = False
