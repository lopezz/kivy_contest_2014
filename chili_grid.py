from kivy.uix.gridlayout import GridLayout
from kivy.properties import ReferenceListProperty
from chili_card import ChiliCard

class ChiliGrid(GridLayout):
    gridsize = ReferenceListProperty(GridLayout.rows, GridLayout.cols)
    
    def add_card(self, card):
        self.add_widget(card)
        
