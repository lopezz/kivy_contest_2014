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
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty

# COLOR constants
NONE_COLOR = [0, 0, 0, 0]
OBJECT_COLOR = [1, 0, 0, 1]
WORD_COLOR = [0, 1, 0, 1]
SOUND_COLOR = [0, 0, 1, 1]

class ChiliCard(ButtonBehavior, Widget):
    # Status of the card. True if flipped, False otherwise.
    status = BooleanProperty(False)
    # Color of the back of the card
    back_color = ListProperty(OBJECT_COLOR)
    back_img = StringProperty('img/back.png')
    back_widget = ObjectProperty(None)
    # Value of the card (e.g 'horse', 'pear', 'etc')
    value = StringProperty('')
    front_widget = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(ChiliCard, self).__init__(*args, **kwargs)

        self.bind(pos=self.update_pos)
        self.bind(size=self.update_size)

    def flip(self):
        ''' Flip the card '''
        #print "flip"
        self.status = not self.status # Change status
        if self.status:
            # Show contents
            self.remove_widget(self.back_widget)
            self.add_widget(self.front_widget)
        else:
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
