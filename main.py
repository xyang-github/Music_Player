import mutagen
from kivy.app import App
from kivy.core.text import Label
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
# from kivy.core.audio import SoundLoader
from just_playback import Playback

Builder.load_file('frontend.kv')


class LoadDialog(FloatLayout):
    """Shows the load dialog box, that contains file browser"""
    load = ObjectProperty(None)  # initiates self.load_track()
    cancel = ObjectProperty(None)  # initiates self.dismiss_popup()


class MusicPlayer:
    """Methods for loading a track"""
    pause_play_text = StringProperty("")
    file_selection = ObjectProperty(None)  # store path to selected file

    def dismiss_popup(self):
        """Removes pop up box"""
        self.popup.dismiss()

    def load_window(self):
        """Creates a pop-up instance, using contents of the Dialog box, and opens it"""
        load_window = LoadDialog(load=self.load_track, cancel=self.dismiss_popup)  # passes load and cancel function
        # to LoadDialog
        self.popup = Popup(title="Load Track",
                           content=load_window,
                           size_hint=(0.9, 0.9))
        self.popup.open()

    def load_track(self, file_selection):
        """Stores path to selected file to file_selection"""
        self.song = Playback()  # instantiates Playback object for song
        self.file_selection = file_selection[0]  # convert list to string for file path
        self.dismiss_popup()  # closes load_window pop-up once track is selected
        self.song.load_file(self.file_selection)
        self.song.play()
        self.pause_play_text = "Pause"

    def play_pause(self):
        """Toggles between play/resume and pause functions"""
        if self.pause_play_text == "Pause":
            self.song.pause()
            self.pause_play_text = "Play"
        elif self.pause_play_text == "Play":
            self.song.resume()
            self.pause_play_text = "Pause"


    # def duration(self):
    """Displays duration of song in hh:mm:ss"""
    # min = int(self.sound.length // 60)
    # if min >= 60:
    #     hour = min // 60
    #     min = min % 60
    #     sec = int(self.sound.length - ((hour*3600) + (min * 60)))
    #     self.ids.song_duration.text = str(hour) + ":" + str(min) + ":" + str(sec).zfill(2)
    # else:
    #     sec = int(self.sound.length % 60)
    #     self.ids.song_duration.text = str(min) + ":" + str(sec).zfill(2)


# def music_information(self):
#     """Displays song title, album and artist"""
#     song = mutagen.File(str(self.file_selection), easy=True)
#     self.ids.title.text = song['title'][0]
#     self.ids.album.text = song['album'][0]
#     self.ids.artist.text = song['artist'][0]

class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


MainApp().run()
