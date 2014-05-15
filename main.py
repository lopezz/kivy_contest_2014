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
