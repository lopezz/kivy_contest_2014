''' ChiliCard is a Card on the ChiliGrid. 
There are three types:
    - ChiliImage
    - ChiliWord
    - ChiliSound
'''

from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty, OptionProperty
from constants import NONE_COLOR, OBJECT_COLOR, WORD_COLOR, SOUND_COLOR, UNFLIPPED, FLIPPED, GUESSED


class ChiliCard(Widget):
    # Status of the card. UNFLIPPED, FLIPPED, OR GUESSED
    status = OptionProperty(UNFLIPPED, options=[UNFLIPPED, FLIPPED, GUESSED])
    flip_by_user = BooleanProperty(False)
    # Color of the back of the card
    back_color = ListProperty(OBJECT_COLOR)
    back_img = StringProperty('img/back.png')
    back_widget = ObjectProperty(None)
    # Value of the card (e.g 'horse', 'pear', 'etc')
    value = StringProperty('')
    front_widget = ObjectProperty(None)
    chiligrid = Widget.parent

    def __init__(self, *args, **kwargs):
        super(ChiliCard, self).__init__(*args, **kwargs)

        self.bind(pos=self.update_pos)
        self.bind(size=self.update_size)

    def flip(self, by_user=True):
        ''' Flip the card '''

        if not self.chiligrid.can_flip_cards:
            return

        print "flip"
        self.flip_by_user = by_user
        self.status = FLIPPED
        # Show contents
        self.remove_widget(self.back_widget)
        self.add_widget(self.front_widget)
    
    def unflip(self):
        self.status = UNFLIPPED
        self.remove_widget(self.front_widget)
        self.add_widget(self.back_widget)
    


    def update_pos(self, o, value):
        self.front_widget.pos = value

    def update_size(self, o, value):
        self.front_widget.size = value



class ChiliImageCard(ChiliCard):
    back_color=ListProperty(OBJECT_COLOR)
    def __init__(self, *args, **kwargs):
        super(ChiliImageCard, self).__init__(*args, **kwargs)
        self.front_widget = Image(source=kwargs['img'])
        

class ChiliWordCard(ChiliCard):
    back_color=ListProperty(WORD_COLOR)
    def __init__(self, *args, **kwargs):
        super(ChiliWordCard, self).__init__(*args, **kwargs)
        self.front_widget = Label(text=kwargs['text'], pos=self.pos, size=self.size)

class ChiliSoundCard(ChiliCard):
    back_color=ListProperty(SOUND_COLOR)
    img = StringProperty('') # path of sound
    pass
