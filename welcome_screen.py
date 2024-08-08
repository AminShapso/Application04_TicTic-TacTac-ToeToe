import config
import random
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Image(source='assets/Icon 02.png', pos=self.pos, size=Window.system_size, opacity=0.5)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Number of players layout
        layout.add_widget(Label(text='Number of Players:', font_size=config.font_size_small, size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels))
        self.num_players_spinner = Spinner(text='2', font_size=config.font_size_small, values=config.num_players_spinner_values, size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels)
        layout.add_widget(self.num_players_spinner)
        layout.add_widget(Label(size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels))  # for spacing

        # Ghost player
        layout.add_widget(Label(text='Ghost:', font_size=config.font_size_small, size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels))
        self.vs_ghost_checkbox = CheckBox(active=False, size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels)
        layout.add_widget(self.vs_ghost_checkbox)
        layout.add_widget(Label(size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels))  # for spacing

        # Grid layout
        layout.add_widget(Label(text='Grid:', font_size=config.font_size_small, size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels))
        grid_layout = BoxLayout(orientation='horizontal', size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels)
        grid_layout.add_widget(Label(text='Width', font_size=config.font_size_small, size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels))
        grid_layout.add_widget(Label(text='Height', font_size=config.font_size_small, size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels))
        layout.add_widget(grid_layout)
        grid_layout = BoxLayout(orientation='horizontal', size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels)
        self.grid_width_spinner = Spinner(text='3', font_size=config.font_size_small, values=config.grid_width_spinner_values, size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels)
        self.grid_height_spinner = Spinner(text='3', font_size=config.font_size_small, values=config.grid_height_spinner_values, size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels)
        self.grid_width_spinner.bind(text=self.on_grid_change)
        self.grid_height_spinner.bind(text=self.on_grid_change)
        grid_layout.add_widget(self.grid_width_spinner)
        grid_layout.add_widget(self.grid_height_spinner)
        layout.add_widget(grid_layout)
        layout.add_widget(Label(size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels))  # for spacing

        # Symbol sequence
        layout.add_widget(Label(text='Symbol sequence:', font_size=config.font_size_small, size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels))
        symbol_sequence_layout = BoxLayout(orientation='horizontal', size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels)
        symbol_sequence_layout.add_widget(Label(text='Row', font_size=config.font_size_small, size_hint=(1, 1)))
        symbol_sequence_layout.add_widget(Label(text='Column', font_size=config.font_size_small, size_hint=(1, 1)))
        symbol_sequence_layout.add_widget(Label(text='Diagonal', font_size=config.font_size_small, size_hint=(1, 1)))
        layout.add_widget(symbol_sequence_layout)
        symbol_sequence_layout = BoxLayout(orientation='horizontal', size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels)
        self.symbol_sequence_row_spinner = Spinner(text='3', font_size=config.font_size_small, values=config.symbol_sequence_row_spinner_values, size_hint=(1/3, config.widget_height_percentage), height=config.widget_height_pixels)
        self.symbol_sequence_column_spinner = Spinner(text='3', font_size=config.font_size_small, values=config.symbol_sequence_column_spinner_values, size_hint=(1/3, config.widget_height_percentage), height=config.widget_height_pixels)
        self.symbol_sequence_diagonal_spinner = Spinner(text='3', font_size=config.font_size_small, values=config.symbol_sequence_diagonal_spinner_values, size_hint=(1/3, config.widget_height_percentage), height=config.widget_height_pixels)
        symbol_sequence_layout.add_widget(self.symbol_sequence_row_spinner)
        symbol_sequence_layout.add_widget(self.symbol_sequence_column_spinner)
        symbol_sequence_layout.add_widget(self.symbol_sequence_diagonal_spinner)
        layout.add_widget(symbol_sequence_layout)
        layout.add_widget(Label(size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels))  # for spacing

        # Start button
        layout.add_widget(Label())  # for spacing
        start_button = Button(text='Start Game', font_size=config.font_size_small, size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels)
        start_button.bind(on_press=self.start_game)
        layout.add_widget(start_button)

        # Add all widgets to the layout
        self.add_widget(layout)

    def on_grid_change(self, _, __):
        config.generate_sequence_spinner_values(int(self.grid_height_spinner.text), int(self.grid_width_spinner.text))
        self.symbol_sequence_row_spinner.values = config.symbol_sequence_row_spinner_values
        self.symbol_sequence_column_spinner.values = config.symbol_sequence_column_spinner_values
        self.symbol_sequence_diagonal_spinner.values = config.symbol_sequence_diagonal_spinner_values

    def start_game(self, _):
        game_screen = self.manager.get_screen('game')

        grid_height = int(self.grid_height_spinner.text)
        grid_width = int(self.grid_width_spinner.text)
        num_players = int(self.num_players_spinner.text)
        if self.symbol_sequence_row_spinner.text.isdigit():
            row_sequence = int(self.symbol_sequence_row_spinner.text)
        else:
            row_sequence = 0
        if self.symbol_sequence_column_spinner.text.isdigit():
            column_sequence = int(self.symbol_sequence_column_spinner.text)
        else:
            column_sequence = 0
        if self.symbol_sequence_diagonal_spinner.text.isdigit():
            diagonal_sequence = int(self.symbol_sequence_diagonal_spinner.text)
        else:
            diagonal_sequence = 0

        game_screen.game.vs_ghost = self.vs_ghost_checkbox.active
        game_screen.game.initialize_game(grid_height, grid_width, num_players, row_sequence, column_sequence, diagonal_sequence)
        game_screen.game.colors = config.generate_random_colors()
        random.shuffle(config.player_sounds)
        self.manager.transition.direction = 'left'
        self.manager.current = 'game'
