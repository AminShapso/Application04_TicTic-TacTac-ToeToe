import config
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

canvas_image = None


class ScoresScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.score_label = Label(font_size=config.font_size_big, font_name=config.global_font, halign='center', markup=True)
        layout.add_widget(self.score_label)
        self.add_widget(layout)

        Window.bind(size=self.print_canvas)
        self.print_canvas()

    def print_canvas(self, *_):
        global canvas_image
        if canvas_image is not None:
            canvas_image.source = ''
            canvas_image.opacity = 0
        with self.canvas.before:
            canvas_image = Image(source='assets/Icon 02.png', size=Window.system_size, opacity=0.1)


    @staticmethod
    def get_player_color(index):
        r, g, b = config.list_of_colors[index]
        r = round(r * 255)
        g = round(g * 255)
        b = round(b * 255)
        return '#%02x%02x%02x' % (r, g, b)      # player color in hex

    def update_scores(self, scores, num_players):
        scores_text = 'Overall Scores:\n'
        for index, (player, score) in enumerate(scores.items()):
            if index >= num_players:
                break
            scores_text += f'[color={self.get_player_color(index)}]Player {index + 1:02} ({config.player_symbols[index]}):   {score}[/color]\n'
        self.score_label.text = scores_text

    def on_touch_down(self, touch):
        self.manager.transition.direction = 'right'
        self.manager.current = 'game'
