import os
import random
from kivy.utils import platform


# GameScreen default values
default_vs_ghost = False
default_num_players = 2
default_grid_width = 3
default_grid_height = 3
default_sequence_row = 3
default_sequence_column = 3
default_sequence_diagonal = 3

# GameScreen max values
max_sequence_row = 3
max_sequence_column = 3
max_sequence_diagonal = 3

# WelcomeScreen spinner_values
grid_width_spinner_values = [str(i) for i in range(3, 11)]
grid_height_spinner_values = [str(i) for i in range(3, 11)]
symbol_sequence_row_spinner_values = [str(i) for i in range(2, default_sequence_row + 1)] + ['Off']
symbol_sequence_column_spinner_values = [str(i) for i in range(2, default_sequence_column + 1)] + ['Off']
symbol_sequence_diagonal_spinner_values = [str(i) for i in range(2, min(default_sequence_row, default_sequence_column) + 1)] + ['Off']
num_players_spinner_values = ['2', '3', '4', '5', '6']

# Globals
dir_path = os.path.dirname(__file__)
assets_path = os.path.join(dir_path, 'assets')
global_font = os.path.join(assets_path, 'arial.ttf')
if platform == "android":
    widget_height_pixels = 80
    widget_height_percentage = 1
    font_size_big = 80
    font_size_small = "14sp"
    # widget_height_pixels = 180
    # widget_height_percentage = 0.1
    # font_size_big = 200
    # font_size_small = "30sp"
else:
    widget_height_pixels = 35
    widget_height_percentage = None
    font_size_big = 50
    font_size_small = 20
player_symbols = ['X', 'O', '□', 'Δ', '◊', '#']
list_of_colors = None
player_sounds = [f'assets/Audio - Player Sound {i:02}.wav' for i in range(1, 14)]
result_sounds = {'win': 'assets/Audio - Game won.wav', 'tie': 'assets/Audio - Game tie.wav'}


def generate_random_colors():
    global list_of_colors
    list_of_colors = {}
    for player in range(len(num_players_spinner_values) + 1):
        list_of_colors[player] = (
            random.randint(30, 230) / 255,  # Red
            random.randint(30, 230) / 255,  # Green
            random.randint(30, 230) / 255   # Blue
        )
    return list_of_colors


def generate_sequence_spinner_values(grid_height, grid_width):
    global symbol_sequence_row_spinner_values, symbol_sequence_column_spinner_values, symbol_sequence_diagonal_spinner_values
    global max_sequence_row, max_sequence_column, max_sequence_diagonal
    max_sequence_row = grid_width
    max_sequence_column = grid_height
    max_sequence_diagonal = min(grid_height, grid_width)
    symbol_sequence_row_spinner_values = [str(i) for i in range(2, max_sequence_row + 1)] + ['Off']
    symbol_sequence_column_spinner_values = [str(i) for i in range(2, max_sequence_column + 1)] + ['Off']
    symbol_sequence_diagonal_spinner_values = [str(i) for i in range(2, max_sequence_diagonal + 1)] + ['Off']
