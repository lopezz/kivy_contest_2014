''' ChiliCard is a Card on the ChiliGrid. 
There are three types:
    - ChiliImage
    - ChiliWord
    - ChiliSound
'''

from kivy.uix.label import Button
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty

# COLOR constants
NONE_COLOR = [0.5, 0.5, 0.5, 1]
OBJECT_COLOR = [1, 0, 0, 1]
WORD_COLOR = [0, 1, 0, 1]
SOUND_COLOR = [0, 0, 1, 1]

class ChiliCard(Button):
    # Status of the card. True if flipped, False otherwise.
    status = BooleanProperty(False)
    # Color of the back of the card
    back_color = ListProperty(NONE_COLOR)
    bac_img = StringProperty('img/back.png')
    # Value of the card (e.g 'horse', 'pear', 'etc')
    value = StringProperty('')
    text = ''

    def flip(self):
        ''' Flip the card '''

    def unflip(self):
        ''' Unflip the card '''



class ChiliImageCard(ChiliCard):
    pass

class ChiliWordCard(ChiliCard):
    pass

class ChiliSoundCard(ChiliCard):
    pass
