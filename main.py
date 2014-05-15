'''
ChiliTrios is a memory like game where you match trios of different cards
 that represent a common object. Each card in the game can show an
 image (object's appearance), text (object's name) and sound
 (object's name pronunciation).

The important files are:

chili_trios_game.py: Defines root widget and main logic that controls the game.
chili_grid.py: Defines grid widget that contains the cards.
chili_card.py: Defines a ChiliCard and its flavours (image, text and sound).
constants.py: Game constants.
'''
__author__ = "Sebastian Lopez (github.com/lopezz), " +\
             "Jeyson Molina (github.com/jeysonmc)"
__version__ = "1.0"

import os
os.environ['KIVY_AUDIO'] = 'pygame'  # Always use pygame
from kivy.app import App
from chili_trios_game import ChiliTriosGame
from chili_grid import ChiliGrid
from chili_card import ChiliCard
from kivy.factory import Factory
from kivy.config import Config

# Fixes pygame_audio high_pitched sound
from kivy.core.audio.audio_pygame import mixer
mixer.quit()
mixer.pre_init(16384, -16, 2, 1024)  # Changed 44100 to 16384
mixer.init()


class ChiliTriosApp(App):
    ''' Main App '''

    def build(self):
        self.chili_game = ChiliTriosGame()
        return self.chili_game

    def on_start(self):
        self.chili_game.show_menu()

if __name__ == '__main__':
    Config.set('graphics', 'fullscreen', 'auto')
    Factory.register('ChiliTriosGame', ChiliTriosGame)
    Factory.register('ChiliGrid', ChiliGrid)
    Factory.register('ChiliCard', ChiliCard)
    ChiliTriosApp().run()
