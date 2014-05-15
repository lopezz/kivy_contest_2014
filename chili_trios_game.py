'''
ChiliTriosGame
==============

Root widget where that controls the app state, loads card sets and other
main bits of the app. ChiliTriosGame.new_game starts a new game loaded
the appropiate card set (given by set_id parameter).
'''

import csv
import os
import random
import time
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (ObjectProperty, NumericProperty, StringProperty,
                             ListProperty, OptionProperty)
from chili_card import ChiliImageCard, ChiliWordCard, ChiliSoundCard
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from chili_helpers import Helper, ShowCardsHelper, GuessObjectHelper
from constants import STOPPED, RUNNING, PAUSED
from kivy.uix.popup import Popup
from kivy.factory import Factory


class ChiliTriosGame(BoxLayout):

    ''' Root widget and main class of ChiliTrios app. '''

    chiligrid = ObjectProperty(None)
    ''' Reference to ChiliGrid instance '''

    sets_list = list()
    ''' List of available card sets '''

    set_loaded = StringProperty('')
    current_set_id = -1
    elapsed_time_str = StringProperty('')
    elapsed_time = 0.0
    cards_left = NumericProperty(0)
    ''' Cards left in grid '''

    card_list = ListProperty([])
    showcards_helper = ObjectProperty(ShowCardsHelper())
    ''' ShowCards Helper instance '''

    guessobj_helper = ObjectProperty(GuessObjectHelper())
    ''' GuessObject Helper instance '''

    game_status = OptionProperty(STOPPED, options=[STOPPED, RUNNING, PAUSED])
    ''' State of the game '''

    alert_msg = StringProperty('')

    def __init__(self, *args, **kwargs):
        super(ChiliTriosGame, self).__init__(*args, **kwargs)

        # Create Menu
        cmenu = Factory.ChiliMenu(chiligame=self)
        cmenu.chiligame = self
        self.menu = Popup(title='CHILI TRIOS', content=cmenu,
                          size_hint=(None, None), size=(400, 400),
                          title_size='18sp', separator_height='4dp',
                          separator_color=[0, 0.5, 1, 0.9],
                          auto_dismiss=False)

        # Load sets and create menu buttons for each one.
        sets = os.listdir('card_sets')
        for n, i in enumerate(sets):
            path = ''.join(['card_sets/', i])
            set_name = i.split('.')[0]
            self.sets_list.append([set_name, path])
            # Add setbutton to menu
            set_menubtn = Factory.SetButton(text=set_name.capitalize())
            set_menubtn.set_id = n
            self.menu.content.set_options.add_widget(set_menubtn)

        self.menu.content.set_options.add_widget(
            Factory.SetButton(text="Random"))  # Random button

        # Iinitialize Helpers.
        Helper.chiligame = self
        self.helpers = {
            'show': self.showcards_helper, 'guess': self.guessobj_helper}

        # Game sound effects
        self.match_sound = SoundLoader.load('sound/match.ogg')
        self.win_sound = SoundLoader.load('sound/win.ogg')
        self.forbidden_sound = SoundLoader.load('sound/forbidden.ogg')

    def new_game(self, set_id=-1):
        ''' Sets a new game and starts it '''
        # Reset values
        self.showcards_helper.remaining = 2
        self.guessobj_helper.remaining = 5
        self.chiligrid.reset()
        # Picks a random set of cards
        if set_id == -1:  # -1 is random
            set_id = random.randint(0, len(self.sets_list) - 1)
        self.current_set_id = set_id
        self.set_loaded = self.sets_list[set_id][0].capitalize()
        self.load_cards(set_id)
        self.elapsed_time = 0.0
        self.play()
        print 'game started!'

    def load_cards(self, set_id):
        ''' Reads and loads the cards from csv file. '''
        print "loading ", self.sets_list[set_id]

        with open(self.sets_list[set_id][1]) as cards:
            # Pick only 8 trios.
            read_cards = random.sample(list(csv.reader(cards)), 8)
            cards_to_add = list()
            self.card_list = []

            for row in read_cards:
                cword, cimg, csound = row
                cards_to_add.append(ChiliWordCard(text=cword, value=cword))
                cards_to_add.append(ChiliImageCard(img=cimg, value=cword))
                cards_to_add.append(
                    ChiliSoundCard(sound=csound, value=cword,
                                   image_card=cards_to_add[-1]))
                self.card_list.extend(cards_to_add[-3:])

            # Shuffle the cards in order to randomize their location on
            # the grid.
            self.cards_left = len(cards_to_add)
            random.shuffle(cards_to_add)

            for card in cards_to_add:
                self.chiligrid.add_card(card)

    def play(self):
        ''' Play/start game '''
        self.game_status = RUNNING
        Clock.schedule_interval(self.time_counter, 1.0)

    def pause(self):
        ''' Pauses/resumes game '''
        if self.showcards_helper.executing or self.guessobj_helper.executing:
            self.forbidden_sound.play()
            self.alert_msg = "You cannot pause the game if there is an " +\
                             "active help."
        else:
            if self.game_status == RUNNING:
                Clock.unschedule(self.time_counter)
                self.chiligrid.can_flip_cards = False
                self.menu.content.continue_btn.disabled = False
                self.menu.content.restart_btn.disabled = False
                self.game_status = PAUSED
                self.show_menu()
            elif self.game_status == PAUSED:
                self.chiligrid.can_flip_cards = True
                self.hide_menu()
                self.play()

    def stop(self):
        ''' Stops game '''
        self.game_status = STOPPED
        Clock.unschedule(self.time_counter)
        self.show_menu()

    def restart_game(self):
        ''' Restart the game  with the current set of cards.
            Different cards may be chosen since they are picked randomly '''
        if self.showcards_helper.executing or self.guessobj_helper.executing:
            self.alert_msg = "You cannot restart the game while using a help"
        else:
            self.hide_menu()
            self.new_game(self.current_set_id)

    def show_menu(self):
        ''' Shows main menu '''
        self.menu.open()

    def hide_menu(self):
        ''' Hides main menu '''
        self.menu.dismiss()

    def time_counter(self, t):
        ''' Updates time display '''
        self.elapsed_time += 1
        self.elapsed_time_str = time.strftime(
            '%M:%S', time.gmtime(self.elapsed_time))

    def use_help(self, helper_name):
        ''' If the help can be used, it is activated '''
        helper = self.helpers[helper_name]
        if helper.can_use():
            helper.activate()
        else:
            self.forbidden_sound.play()
            self.alert_msg = "You cannot use that help now"

    def cards_matched(self, value):
        ''' Called when a trio of cards are matched '''
        if value:
            self.match_sound.play()
            self.cards_left -= 3
            if self.cards_left == 0:
                self.win_sound.play()
                self.stop()  # End game
