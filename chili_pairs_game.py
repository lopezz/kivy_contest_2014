import csv, os, random
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty
from chili_card import ChiliImageCard, ChiliWordCard, ChiliSoundCard
from kivy.clock import Clock
import time
from chili_helpers import Helper, ShowCardsHelper


class ChiliPairsGame(BoxLayout):

    chiligrid = ObjectProperty(None)
    setlists = list()
    set_loaded = StringProperty('')
    elapsed_time_str = StringProperty('')
    elapsed_time = 0.0
    cards_left = NumericProperty(0) # Cards left in grid
    card_list = ListProperty([])
    showcards_helper = ObjectProperty(None)
    show_remain = NumericProperty(0)    # Remaining showcards helps
    

    def __init__(self, *args, **kwargs):
        super(ChiliPairsGame, self).__init__(*args, **kwargs)
        ''' Finds all the sets available in the card sets
            dir and load them in the setlists variable '''
        sets = os.listdir('card_sets') 
        for i in sets:
            path =''.join(['card_sets/', i])
            set_name = i.split('.')[0]
            self.setlists.append([set_name, path])
        print self.setlists

        # Helpers
        Helper.chiligame = self
        self.showcards_helper = ShowCardsHelper()
        self.show_remain = self.showcards_helper.remaining

    def new_game(self):
        ''' Sets a new game and starts it '''
        # TODO reset values
        self.chiligrid.clear_widgets()
        #pick a random set of cards
        set_id = random.randint(0,len(self.setlists)-1)
        self.set_loaded = self.setlists[set_id][0].capitalize()
        self.load_cards(set_id)
        self.elapsed_time = 0
        self.play()

    def load_cards(self, set_id):
        ''' Reads and loads the cards for the cvs file '''
        cards= open(self.setlists[set_id][1])
        read_cards = list(csv.reader(cards))        
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
        Clock.schedule_interval(self.time_counter, 1.0)
    
    def pause(self):
        ''' Pauses game '''
        Clock.unschedule(self.time_counter)
        pass

    def stop(self):
        ''' Stops game '''
        print "Stop Game"
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
        

    def cards_matched(self, value):
        print "cards matched", value
        if value:
            self.cards_left -= 3
            if self.cards_left == 0:
                self.stop() # End game
