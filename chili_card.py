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
from kivy.core.audio import SoundLoader
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty, OptionProperty
from constants import NONE_COLOR, OBJECT_COLOR, WORD_COLOR, SOUND_COLOR, UNFLIPPED, FLIPPED, GUESSED, BGCOLOR_NORMAL, BGCOLOR_GUESSED


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
    bgcolor = ListProperty(BGCOLOR_NORMAL)

    def __init__(self, *args, **kwargs):
        super(ChiliCard, self).__init__(*args, **kwargs)

        self.value = kwargs['value']
        self.bind(pos=self.update_pos)
        self.bind(size=self.update_size)

    def flip(self, by_user=True):
        ''' Flip the card '''

        if not self.chiligrid.can_flip_cards:
            return

        print "flip", self.value
        self.flip_by_user = by_user
        # Show contents
        self.remove_widget(self.back_widget)
        self.add_widget(self.front_widget)
        self.status = FLIPPED
    
    def unflip(self):
        print "UNFLIP"

        #import pdb
        #pdb.set_trace()
        self.remove_widget(self.front_widget)
        self.add_widget(self.back_widget)
        self.status = UNFLIPPED

    def guess(self):
        print "card GUESSED"
        self.bgcolor = BGCOLOR_GUESSED
        self.status = GUESSED

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
    card_sound=''
    def __init__(self, *args, **kwargs):
        super(ChiliSoundCard, self).__init__(*args, **kwargs)
        self.front_widget = Image(source='img/sound.png')
        self.card_sound = SoundLoader.load(kwargs['sound'])

    def flip(self, by_user=True):
        ''' Flip the card '''
        super(ChiliSoundCard, self).flip(by_user)
        self.play_sound()     
    
    def play_sound(self):
        if self.card_sound.state == 'stop':  # Play only if no sound is being
                                             # played.
            self.card_sound.play()
            print "SOOOUND!!!!"

    def on_touch_up(self, touch):   
        if (self.status==FLIPPED or self.status==GUESSED) \
        and self.collide_point(touch.x, touch.y):           # Play only if the card is
                                                            # already flipped
            self.play_sound()
        else:
            pass
