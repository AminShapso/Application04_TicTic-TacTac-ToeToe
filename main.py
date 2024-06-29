# PyPi imports:
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import platform

# .py imports:
from welcome_screen import WelcomeScreen
from game_screen import GameScreen
from scores_screen import ScoresScreen

if platform == "android":
    from jnius import autoclass
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    ActivityInfo = autoclass("android.content.pm.ActivityInfo")
    activity = PythonActivity.mActivity
    activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_USER)


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
# Add themes and sounds
# make vs. Python work
