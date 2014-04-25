from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty
from chili_card import ChiliImageCard, ChiliWordCard
import csv

class ChiliPairsGame(Widget):

    chiligrid = ObjectProperty(None)
    


    def new_game(self):
        ''' Sets a new game and starts it '''
        # TODO reset values
        self.chiligrid.clear_widgets()
        self.load_cards()
        self.play()

    def load_cards(self):
        ''' Reads and loads the cards for the cvs file '''
        cards= open('card_sets/fruits.csv')
        read_cards = list(csv.reader(cards))
        c=0
        # the set will load 4 times (there's 6 cards in fruits.csv)   
        for i in range(3):
            print i
            for row in read_cards:
                print i
                for col in row:
                    if c==0:
                        self.chiligrid.add_card(ChiliWordCard(text=col))
                        c=1
                    else:
                        self.chiligrid.add_card(ChiliImageCard(img=col))
                        c=0
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
