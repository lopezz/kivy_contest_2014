import csv, os, random
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty
from chili_card import ChiliImageCard, ChiliWordCard, ChiliSoundCard


class ChiliPairsGame(Widget):

    chiligrid = ObjectProperty(None)
    setlists= list()
    
    def __init__(self, *args, **kwargs):
        super(ChiliPairsGame, self).__init__(*args, **kwargs)
        sets=os.listdir('card_sets') 
        for i in sets:
            path=''.join(['card_sets/', i])
            set_name=i.split('.')[0]
            self.setlists.append([set_name, path])
        print self.setlists


    def new_game(self):
        ''' Sets a new game and starts it '''
        # TODO reset values
        self.chiligrid.clear_widgets()
        #pick a random set of cards
        set_id=random.randint(0,len(self.setlists)-1)
        self.load_cards(set_id)
        self.play()

    def load_cards(self, set_id):
        ''' Reads and loads the cards for the cvs file '''
        cards= open(self.setlists[set_id][1])
        read_cards = list(csv.reader(cards))        
        cards_to_add=list()

        for row in read_cards:
            cword, cimg, csound = row
            cards_to_add.append(ChiliWordCard(text=cword, value=cword))
            cards_to_add.append(ChiliImageCard(img=cimg, value=cword))
            cards_to_add.append(ChiliSoundCard(sound=csound, value=cword))
        
        #shuffle the cards in order to randomize their location
        random.shuffle(cards_to_add)
        
        for card in cards_to_add:
            self.chiligrid.add_card(card)
        cards.close()

    def play(self):
        ''' Play/start game '''
        pass

    def pause(self):
        ''' Pauses game '''
        pass

    def stop(self):
        ''' Stops game '''
        pass

    def show_menu(self):
        ''' Shows main menu '''
        pass

    def hides_menu(self):
        ''' Hides main menu '''
        pass

    def cards_matched(self, value):
        print "cards matched", value
        pass
