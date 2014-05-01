from kivy.app import App
from chili_pairs_game import ChiliPairsGame
from chili_grid import ChiliGrid
from chili_card import ChiliCard
from kivy.factory import Factory

class ChiliPairsApp(App):
    def build(self):
        chili_game =  ChiliPairsGame()
        chili_game.new_game()
        return chili_game

if __name__ == '__main__':
    Factory.register('ChiliPairsGame', ChiliPairsGame)
    Factory.register('ChiliGrid', ChiliGrid)
    Factory.register('ChiliCard', ChiliCard)
    ChiliPairsApp().run()