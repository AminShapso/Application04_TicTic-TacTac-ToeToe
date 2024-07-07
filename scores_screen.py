import config
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen


class ScoresScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Image(source='assets/Icon 02.png', pos=self.pos, size=Window.system_size, opacity=0.5)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.score_label = Label(font_size=config.font_size_big, font_name=config.global_font, halign='center')
        layout.add_widget(self.score_label)

        self.add_widget(layout)

    def update_scores(self, scores, num_players):
        scores_text = 'Overall Scores:\n'
        for index, (player, score) in enumerate(scores.items()):
            if index >= num_players:
                break
            scores_text += f'Player {index + 1:02} ({config.player_symbols[player]}):   {score}\n'
        self.score_label.text = scores_text

    def on_touch_down(self, touch):
        self.manager.transition.direction = 'right'
        self.manager.current = 'game'
