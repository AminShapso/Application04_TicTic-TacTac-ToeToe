# PyPi imports:
import kivy.metrics
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import platform

# .py imports:
from welcome_screen import WelcomeScreen
from game_screen import GameScreen
from scores_screen import ScoresScreen


set_window = [True,                 # to set, or not to set
              1,                    # Refactor screen
              [[1080, 2176, 409],   # 0 = Xiaomi Redmi Note 11S - Portrait
               [2176, 986, 409],    # 1 = Xiaomi Redmi Note 11S - Landscape
               [1080, 2268, 398],   # 2 = Xiaomi Mi Note 10 Pro - Portrait
               [2268, 1080, 398],   # 3 = Xiaomi Mi Note 10 Pro - Landscape
               [1008, 2076, 489],   # 4 = Google Pixel 8 Pro - Portrait
               [2130, 890, 489],    # 5 = Google Pixel 8 Pro - Landscape
               [600, 800, 200]]     # 6 = Custom 01
              [6]]                  # pick from the phones above


if platform == "android":
    from jnius import autoclass
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    ActivityInfo = autoclass("android.content.pm.ActivityInfo")
    activity = PythonActivity.mActivity
    activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_USER)
elif set_window[0]:
    Window.size = int(set_window[2][0] / set_window[1]), int(set_window[2][1] / set_window[1])
    Window.dpi = int(set_window[2][2] / set_window[1])
    # kivy.metrics.Metrics.density = 0.75       # either 0.75, 1, 1.5 or 2
    # kivy.metrics.Metrics.fontscale = 1        #  between 0.8 and 1.2


class TicTacToeApp(App):
    def build(self):
        self.title = "TicTic TacTac ToeToe"
        self.icon = 'assets/Icon 01.png'
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(ScoresScreen(name='scores'))
        return sm


if __name__ == '__main__':
    TicTacToeApp().run()


# Player Sequence - fix check_winner()
# Change beginning player - every new game, a different player starts
# Change colors - to be more colorful
# make the symbols thicker
# draw_symbol - split into different methods: draw_x(), draw_O()

# Finally:
# Add themes and sounds (win, tie, etc.)
# make vs. Python work
