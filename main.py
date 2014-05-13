import os
os.environ['KIVY_AUDIO'] = 'pygame'  # Always use pygame
from kivy.app import App
from chili_pairs_game import ChiliPairsGame
from chili_grid import ChiliGrid
from chili_card import ChiliCard
from kivy.factory import Factory

# Fixes pygame_audio high_pitched sound
from kivy.core.audio.audio_pygame import mixer
mixer.quit()
mixer.pre_init(16384, -16, 2, 1024) # Changed 44100 to 16384
mixer.init()

class ChiliPairsApp(App):
    def build(self):
        chili_game =  ChiliPairsGame()
        #chili_game.new_game()
        chili_game.show_menu()
        return chili_game

if __name__ == '__main__':
    Factory.register('ChiliPairsGame', ChiliPairsGame)
    Factory.register('ChiliGrid', ChiliGrid)
    Factory.register('ChiliCard', ChiliCard)
    ChiliPairsApp().run()
