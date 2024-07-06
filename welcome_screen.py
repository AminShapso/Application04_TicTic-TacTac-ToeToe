import config
import random
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Number of players layout
        layout.add_widget(Label(text='Number of Players:', size_hint=(0.5, config.widget_height_precentage), height=config.widget_height_pixels))
        num_players_layout = BoxLayout(orientation='horizontal', size_hint=(1, config.widget_height_precentage), height=config.widget_height_pixels)
        self.num_players_spinner = Spinner(
            text='2',  # Default value
            values=config.num_players_spinner_values,
            size_hint=(0.5, 1)
        )
        num_players_layout.add_widget(Label(size_hint=(0.5, 1)))
        num_players_layout.add_widget(self.num_players_spinner)
        layout.add_widget(num_players_layout)

        # Grid layout
        grid_layout = BoxLayout(orientation='horizontal', size_hint=(1, config.widget_height_precentage), height=config.widget_height_pixels)
        grid_layout.add_widget(Label(text='Grid:', size_hint=(0.5, None)))
        grid_layout.add_widget(Label(text='Width', size_hint=(0.25, None)))
        grid_layout.add_widget(Label(text='Height', size_hint=(0.25, None)))
        layout.add_widget(grid_layout)
        grid_layout = BoxLayout(orientation='horizontal', size_hint=(1, config.widget_height_precentage), height=config.widget_height_pixels)
        self.grid_width_spinner = Spinner(
            text='3',  # Default value
            values=config.grid_width_spinner_values,
            size_hint=(0.25, 1)
        )
        self.grid_height_spinner = Spinner(
            text='3',  # Default value
            values=config.grid_height_spinner_values,
            size_hint=(0.25, 1)
        )
        grid_layout.add_widget(Label(size_hint=(0.5, 1)))
        grid_layout.add_widget(self.grid_width_spinner)
        grid_layout.add_widget(self.grid_height_spinner)
        layout.add_widget(grid_layout)

        # Symbol sequence
        symbol_sequence_layout = BoxLayout(orientation='horizontal', size_hint=(1, config.widget_height_precentage), height=config.widget_height_pixels)
        symbol_sequence_layout.add_widget(Label(text='Symbol sequence:', size_hint=(0.5, None)))
        symbol_sequence_layout.add_widget(Label(text='Row', size_hint=(0.1666, None)))
        symbol_sequence_layout.add_widget(Label(text='Column', size_hint=(0.1666, None)))
        symbol_sequence_layout.add_widget(Label(text='Diagonal', size_hint=(0.1666, None)))
        layout.add_widget(symbol_sequence_layout)
        symbol_sequence_layout = BoxLayout(orientation='horizontal', size_hint=(1, config.widget_height_precentage), height=config.widget_height_pixels)
        self.symbol_sequence_row_spinner = Spinner(
            text='3',  # Default value
            values=config.symbol_sequence_spinner_values,
            size_hint=(0.1666, 1)
        )
        self.symbol_sequence_column_spinner = Spinner(
            text='3',  # Default value
            values=config.symbol_sequence_spinner_values,
            size_hint=(0.1666, 1)
        )
        self.symbol_sequence_diagonal_spinner = Spinner(
            text='3',  # Default value
            values=config.symbol_sequence_spinner_values,
            size_hint=(0.1666, 1)
        )
        symbol_sequence_layout.add_widget(Label(size_hint=(0.5, 1)))
        symbol_sequence_layout.add_widget(self.symbol_sequence_row_spinner)
        symbol_sequence_layout.add_widget(self.symbol_sequence_column_spinner)
        symbol_sequence_layout.add_widget(self.symbol_sequence_diagonal_spinner)
        layout.add_widget(symbol_sequence_layout)

        # Start button
        start_button = Button(text='Start Game', size_hint=(1, config.widget_height_precentage), height=config.widget_height_pixels)
        start_button.bind(on_press=self.start_game)

        # Add all widgets to the layout
        layout.add_widget(Image(source='assets/Icon 02.png'))
        layout.add_widget(start_button)

        self.add_widget(layout)

    def start_game(self, _):
        grid_height = int(self.grid_height_spinner.text)
        grid_width = int(self.grid_width_spinner.text)
        try:
            num_players = int(self.num_players_spinner.text)
        except ValueError:
            num_players = 2     # if self.num_players_spinner.text == 'vs. Python'

        game_screen = self.manager.get_screen('game')
        game_screen.game.initialize_game(grid_height, grid_width, num_players)
        game_screen.game.colors = game_screen.game.generate_random_colors()
        random.shuffle(config.player_sounds)
        self.manager.transition.direction = 'left'
        self.manager.current = 'game'
