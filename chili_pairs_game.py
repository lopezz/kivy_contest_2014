from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty
from chili_card import ChiliImageCard

class ChiliPairsGame(Widget):

    chiligrid = ObjectProperty(None)
    


    def new_game(self):
        ''' Sets a new game and starts it '''
        # TODO reset values
        self.chiligrid.clear_widgets()
        for i in range(4 * 6):
            #self.chiligrid.add_card(ChiliWordCard(text='Test card'))
            self.chiligrid.add_card(ChiliImageCard(img='img/pear.png'))
            #self.chiligrid.add_card(ChiliSoundCard(img='ruta'))
        self.play()

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
