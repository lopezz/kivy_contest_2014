import csv, os, random, time
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty, OptionProperty
from chili_card import ChiliImageCard, ChiliWordCard, ChiliSoundCard
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from chili_helpers import Helper, ShowCardsHelper, GuessObjectHelper
from constants import STOPPED, RUNNING, PAUSED

class ChiliPairsGame(BoxLayout):

    chiligrid = ObjectProperty(None)
    sets_list = list()
    set_loaded = StringProperty('')
    elapsed_time_str = StringProperty('')
    elapsed_time = 0.0
    cards_left = NumericProperty(0) # Cards left in grid
    card_list = ListProperty([])
    showcards_helper = ObjectProperty(ShowCardsHelper())
    guessobj_helper = ObjectProperty(GuessObjectHelper())
    game_status = OptionProperty(STOPPED, options=[STOPPED, RUNNING, PAUSED])
    
    def __init__(self, *args, **kwargs):
        super(ChiliPairsGame, self).__init__(*args, **kwargs)
        ''' Finds all the sets available in the card sets
            dir and load them in the sets_list variable '''
        sets = os.listdir('card_sets') 
        for i in sets:
            path =''.join(['card_sets/', i])
            set_name = i.split('.')[0]
            self.sets_list.append([set_name, path])
        print self.sets_list

        # Helpers
        Helper.chiligame = self
        self.helpers = {'show': self.showcards_helper, 'guess': self.guessobj_helper}

        # Game sound effects
        self.match_sound = SoundLoader.load('sound/match.ogg')
        self.win_sound = SoundLoader.load('sound/win.ogg')

    def new_game(self):
        ''' Sets a new game and starts it '''
        # TODO reset values
        self.chiligrid.clear_widgets()
        #pick a random set of cards
        set_id = random.randint(0,len(self.sets_list)-1)
        self.set_loaded = self.sets_list[set_id][0].capitalize()
        self.load_cards(set_id)
        self.elapsed_time = 0
        self.play()

    def load_cards(self, set_id):
        ''' Reads and loads the cards for the cvs file '''
        cards= open(self.sets_list[set_id][1])
        read_cards = random.sample(list(csv.reader(cards)), 8)  # Pick only 8 'trios'
        cards_to_add = list()
        self.card_list = []

        for row in read_cards:
            cword, cimg, csound = row
            cards_to_add.append(ChiliWordCard(text = cword, value = cword))
            cards_to_add.append(ChiliImageCard(img = cimg, value = cword))
            cards_to_add.append(ChiliSoundCard(sound = csound, value = cword))
            self.card_list.extend(cards_to_add[-3:])
        
        #shuffle the cards in order to randomize their location
        self.cards_left = len(cards_to_add)
        random.shuffle(cards_to_add)
        
        for card in cards_to_add:
            self.chiligrid.add_card(card)
        cards.close()

    def play(self):
        ''' Play/start game '''
        self.game_status = RUNNING
        Clock.schedule_interval(self.time_counter, 1.0)
    
    def pause(self):
        ''' Pauses/unpauses game '''
        if self.game_status == RUNNING:
            Clock.unschedule(self.time_counter)
            self.game_status = PAUSED
            self.chiligrid.can_flip_cards = False
        elif self.game_status == PAUSED:
            self.chiligrid.can_flip_cards = True
            self.play()
        else:
            pass

    def stop(self):
        ''' Stops game '''
        print "Stop Game"
        self.game_status = STOPPED
        Clock.unschedule(self.time_counter)
        # TODO other stuff.

    def show_menu(self):
        ''' Shows main menu '''
        pass

    def hide_menu(self):
        ''' Hides main menu '''
        pass

    def time_counter(self, t):
        self.elapsed_time += 1
        self.elapsed_time_str = time.strftime('%M:%S', time.gmtime(self.elapsed_time))
        
    def use_help(self, helper_name):
        ''' If the help can be used, it is activated '''
        helper = self.helpers[helper_name]
        if helper.can_use():
           helper.activate()


    def cards_matched(self, value):
        print "cards matched", value
        if value:
            self.match_sound.play()
            self.cards_left -= 3
            if self.cards_left == 0:
                self.win_sound.play()
                self.stop() # End game
