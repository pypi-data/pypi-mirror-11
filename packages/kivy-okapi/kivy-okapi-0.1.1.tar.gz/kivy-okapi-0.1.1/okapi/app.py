from __future__ import print_function, absolute_import, unicode_literals
from ConfigParser import SafeConfigParser
import codecs

# Kivy
from kivy.app import App
from kivy.core.window import Window

# Okapi
from .screen_manager import ScreenManager


class Okapi(App):
    """Main game class
    """

    INI_PATH = None
    GAME_CLASS = None
    PROJECT_PATH = None
    SCREEN_MANAGER_CLS = ScreenManager

    def get_ini_path(self):
        return "{}/params.ini".format(self.get_project_path())

    def get_project_path(self):
        assert self.PROJECT_PATH is not None, "Must define a project path."
        return self.PROJECT_PATH

    def load_configuration(self, path):
        config = SafeConfigParser()

        with codecs.open(path, 'r', encoding='utf-8') as f:
            config.readfp(f)

        return config

    def get_screen_manager_cls(self, *args, **kwargs):
        assert self.SCREEN_MANAGER_CLS is not None, 'Failed to set a ``SCREEN_MANAGER_CLS`` attr on your App'
        return self.SCREEN_MANAGER_CLS

    def get_screen_manager(self, *args, **kwargs):
        kls = self.get_screen_manager_cls(*args, **kwargs)
        return kls(*args, **kwargs)

    def resize_window(self, window):
        pass

    def build(self):
        self.configuration = self.load_configuration(self.get_ini_path())
        self.root = self.get_screen_manager(
            configuration=self.configuration,
            game_class=self.GAME_CLASS
        )
        self.resize_window(Window)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        return self.root

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.root._on_keyboard_down(keyboard, keycode, text, modifiers)

        # Catch `cmd-w` because I can't stand that that doesn't close the app
        if 'meta' in modifiers and keycode[0] == 119:
            self.close_window()

    def close_window(self):
        Window.close()
