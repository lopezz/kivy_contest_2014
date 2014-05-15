'''
ChiliCard
=========

ChiliCard is a Card on the ChiliGrid.
There are three types:
    - ChiliImage: A card that contains an image of the object.
    - ChiliWord: A card that contains the name of the object (text).
    - ChiliSound: A card that contains the pronunciation of object's name.

A ChiliCard is flipped when the user taps on it.
'''

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.properties import (BooleanProperty, ListProperty, StringProperty,
                             ObjectProperty, OptionProperty)
from constants import (OBJECT_COLOR, WORD_COLOR, SOUND_COLOR, UNFLIPPED,
                       FLIPPED, GUESSED, BGCOLOR_NORMAL, BGCOLOR_GUESSED)


class ChiliCard(BoxLayout):

    ''' A card in the game. '''

    status = OptionProperty(UNFLIPPED, options=[UNFLIPPED, FLIPPED, GUESSED])
    ''' Status of the card. UNFLIPPED, FLIPPED, OR GUESSED. '''

    flip_by_user = BooleanProperty(False)
    ''' True if card was flipped by user. '''

    back_color = ListProperty(OBJECT_COLOR)
    ''' Color of the back of the card. '''

    back_img = StringProperty('img/back.png')
    back_widget = ObjectProperty(None)
    ''' Widget that represents the back of the card. '''

    value = StringProperty('')
    ''' Value of the card (e.g 'horse', 'pear', 'etc') '''

    front_widget = ObjectProperty(None)
    ''' Widget that represents the front of the card. '''

    chiligrid = Widget.parent

    bgcolor = ListProperty(BGCOLOR_NORMAL)
    ''' Background color. '''

    def __init__(self, *args, **kwargs):
        super(ChiliCard, self).__init__(*args, **kwargs)

        self.value = kwargs['value']
        self.bind(pos=self.update_pos)
        self.bind(size=self.update_size)

    def flip(self, by_user=True):
        ''' Flip the card '''

        if not self.chiligrid.can_flip_cards:
            return

        self.flip_by_user = by_user
        # Show contents
        self.remove_widget(self.back_widget)
        self.add_widget(self.front_widget)
        self.status = FLIPPED

    def unflip(self):
        ''' Unflips the card. '''

        self.remove_widget(self.front_widget)
        self.add_widget(self.back_widget)
        self.status = UNFLIPPED

    def guess(self):
        ''' Marks card as guessed. '''

        self.bgcolor = BGCOLOR_GUESSED
        self.status = GUESSED

    def update_pos(self, o, value):
        self.front_widget.pos = value

    def update_size(self, o, value):
        self.front_widget.size = value


class ChiliImageCard(ChiliCard):

    ''' Image card. '''

    back_color = ListProperty(OBJECT_COLOR)

    def __init__(self, *args, **kwargs):
        super(ChiliImageCard, self).__init__(*args, **kwargs)
        # Front is an image widget that shows object's image.
        self.front_widget = Image(source=kwargs['img'])

    def guess(self):
        super(ChiliImageCard, self).guess()
        # Transforms card when guessed (add text Label).
        self.add_widget(
            Label(text=self.value, size_hint=(1, 0.2),
                  font_name='fonts/atwriter.ttf'))


class ChiliWordCard(ChiliCard):

    ''' Word card. Shows object's name.'''

    back_color = ListProperty(WORD_COLOR)

    def __init__(self, *args, **kwargs):
        super(ChiliWordCard, self).__init__(*args, **kwargs)
        self.front_widget = Label(
            text=kwargs['text'], pos=self.pos, size=self.size)
        self.front_widget.font_size = 20
        self.front_widget.font_name = 'fonts/atwriter.ttf'

    def guess(self):
        super(ChiliWordCard, self).guess()
        self.clear_widgets()  # Remove front widget
        self.bgcolor = BGCOLOR_NORMAL


class ChiliSoundCard(ChiliCard):

    ''' Sound/Audio Card. Shows an icon that can be tapped to play object's
        name pronunciation. '''

    back_color = ListProperty(SOUND_COLOR)
    card_sound = ''
    image_card = None

    def __init__(self, *args, **kwargs):
        super(ChiliSoundCard, self).__init__(*args, **kwargs)
        self.front_widget = Image(source='img/sound.png')
        self.card_sound = SoundLoader.load(kwargs['sound'])
        self.image_card = kwargs['image_card']  # Matching Image card

    def flip(self, by_user=True):
        super(ChiliSoundCard, self).flip(by_user)

        if not self.chiligrid.can_flip_cards:
            return

        if by_user:
            self.play_sound()

    def play_sound(self):
        ''' Play sound (pronounces name). '''
        if self.card_sound.state == 'stop':  # Play only if no sound is being
                                             # played.
            self.card_sound.play()

    def on_touch_up(self, touch):
        if (self.status == FLIPPED and self.collide_point(touch.x, touch.y))\
                or (self.status == GUESSED and
                    self.image_card.collide_point(touch.x, touch.y)):
        # Play only if the card is already flipped or play if the card
        # is guessed but only when the matching Image card is pressed
            self.play_sound()
        else:
            pass

    def guess(self):
        super(ChiliSoundCard, self).guess()
        self.clear_widgets()
        self.bgcolor = BGCOLOR_NORMAL
