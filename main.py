from kivy.app import App
from chili_pairs_game import ChiliPairsGame

class ChiliPairsApp(App):
    def build(self):
        return ChiliPairsGame()

if __name__ == '__main__':
    ChiliPairsApp().run()