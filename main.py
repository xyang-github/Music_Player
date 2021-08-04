import datetime
import mutagen
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from just_playback import Playback
from kivy.core.window import Window

Window.size = (400, 600)

Builder.load_file('frontend.kv')


class LoadDialog(FloatLayout):
    """Shows the load dialog box, that contains file browser"""
    load = ObjectProperty(None)  # initiates self.load_track()
    cancel = ObjectProperty(None)  # initiates self.dismiss_popup()


class MusicPlayer(Screen):
    """Methods for loading a track"""
    pause_play_text = StringProperty("")
    file_selection = ObjectProperty(None)  # store path to selected file

    def dismiss_popup(self):
        """Removes pop up box"""
        self.popup.dismiss()

    def load_window(self):
        """Creates a pop-up instance, using contents of the Dialog box, and opens it"""
        load_window = LoadDialog(load=self.load_track, cancel=self.dismiss_popup)  # passes load and
        # cancel function to LoadDialog
        self.popup = Popup(title="Load Track",
                           content=load_window,
                           size_hint=(0.9, 0.9))
        self.popup.open()

    def load_track(self, file_selection):
        """Stores path to selected file to file_selection"""
        self.song = Playback()  # instantiates Playback object for song
        self.file_selection = file_selection[0]  # stores path list as string
        self.dismiss_popup()  # closes load_window pop-up once track is selected
        self.song.load_file(self.file_selection)
        self.ids.play_pause.disabled = False
        self.song.play()
        self.music_information()
        self.ids.play_pause.background_normal = "images/Pause-normal.png"

    def play_pause(self):
        """Toggles between play/resume and pause functions"""
        if self.ids.play_pause.background_normal == "images/Pause-normal.png":
            self.song.pause()
            self.ids.play_pause.background_normal = "images/Play-normal.png"
            self.ids.play_pause.background_down = "images/Play-down.png"
        elif self.ids.play_pause.background_normal == "images/Play-normal.png":
            self.song.resume()
            self.ids.play_pause.background_normal = "images/Pause-normal.png"
            self.ids.play_pause.background_down = "images/Pause-down.png"

    def song_position(self, dt):
        """Displays duration of song in hh:mm:ss, and updates slider"""
        current_pos = datetime.timedelta(seconds=self.song.curr_pos)  # current song position
        current_pos = str(current_pos)[:7]

        track_length = datetime.timedelta(seconds=self.song.duration)  # total duration of song
        track_length = str(track_length)[:7]

        self.ids.current_position.text = f"{current_pos} | {track_length}"  # updates text
        self.ids.song_slider.value = int(self.song.curr_pos)  # updates slider position

    def change_position(self):
        """Syncs position of song with slider position"""
        self.song.seek(self.ids.song_slider.value)

    def music_information(self):
        """Displays song duration, title, album and artist"""

        # Calls on clock module to repeatedly update audio slider
        if self.song.active:
            self.ids.song_slider.max = int(self.song.duration)
            Clock.schedule_interval(self.song_position, 0.5)

        song = mutagen.File(self.file_selection)  # music tag information

        try:
            self.ids.title.text = str(song['TIT2'])  # title
        except KeyError:
            self.ids.title.text = "Unknown Title"

        try:
            self.ids.album.text = str(song['TALB'])  # album
        except KeyError:
            self.ids.album.text = "Unknown Album"

        try:
            self.ids.artist.text = str(song['TPE1'])  # artist
        except KeyError:
            self.ids.artist.text = "Unknown Artist"

        try:
            artwork = song.tags['APIC:'].data  # Extract album cover
            with open('images/album_cover.jpg', 'wb') as img:
                img.write(artwork)
            self.ids.album_art.source = "images/album_cover.jpg"
        except KeyError:
            self.ids.album_art.source = "images/default_cover.png"
        self.ids.album_art.reload()  # refreshes images when changing tracks

        # Create an animated title that scrolls horizontally
        scrolling_effect = Animation(x=-400, opacity=0, duration=7)
        scrolling_effect += Animation(pos=(0,0), opacity=1, duration=2)
        scrolling_effect.start(self.ids.title)


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


MainApp().run()
