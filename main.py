import mutagen
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.audio import SoundLoader

Builder.load_file('frontend.kv')


class LoadDialog(FloatLayout):
    """Shows the load dialog box"""
    load = ObjectProperty(None)  # initiates self.load()
    cancel = ObjectProperty(None)  # initiates self.dismiss_popup()


class PlayerFunctions(Screen):
    file_selection = ObjectProperty(None)  # store path to selected file

    def dismiss_popup(self):
        """Removes pop up box"""
        self.popup.dismiss()

    def load_track(self):
        """Creates a pop-up instance, using contents of the Dialog box, and opens it"""
        load_window = LoadDialog(load=self.load, cancel=self.dismiss_popup)  # passes load and cancel function to LoadDialog
        self.popup = Popup(title="Load Track",
                           content=load_window,
                           size_hint=(0.9, 0.9))
        self.popup.open()

    def load(self, file_selection):
        """Stores path to selected file to file_selection"""
        self.dismiss_popup()
        self.file_selection = file_selection[0]
        self.sound = SoundLoader.load(self.file_selection) # instantiates sound file into variable
        self.play()

    def play(self):
        """Plays a specified track, and stops the track"""
        if self.sound.state == "stop":
            self.sound.play()
            self.duration()
            self.music_information()
            self.ids.play_pause.text = "Pause"  # changes text from play to pause
        else:
            self.sound.stop()
            self.ids.play_pause.text = "Play"  # changes text from play to pause

    def duration(self):
        """Displays duration of song in hh:mm:ss"""
        min = int(self.sound.length // 60)
        if min >= 60:
            hour = min // 60
            min = min % 60
            sec = int(self.sound.length - ((hour*3600) + (min * 60)))
            self.ids.song_duration.text = str(hour) + ":" + str(min) + ":" + str(sec).zfill(2)
        else:
            sec = int(self.sound.length % 60)
            self.ids.song_duration.text = str(min) + ":" + str(sec).zfill(2)

    def music_information(self):
        """Displays song title, album and artist"""
        song = mutagen.File(str(self.file_selection), easy=True)
        self.ids.title.text = song['title'][0]
        self.ids.album.text = song['album'][0]
        self.ids.artist.text = song['artist'][0]


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


MainApp().run()
