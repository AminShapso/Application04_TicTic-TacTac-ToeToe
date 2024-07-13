import os
import random
from random import uniform
from kivy.utils import platform


# WelcomeScreen spinner_values
grid_width_spinner_values = [str(i) for i in range(3, 11)]
grid_height_spinner_values = [str(i) for i in range(3, 11)]
symbol_sequence_spinner_values = [str(i) for i in range(3, 11)] + ['Off']
num_players_spinner_values = ['2', '3', '4', '5', '6']


# Globals
dir_path = os.path.dirname(__file__)
assets_path = os.path.join(dir_path, 'assets')
global_font = os.path.join(assets_path, 'arial.ttf')
if platform == "android":
    widget_height_pixels = 80
    widget_height_percentage = 0.05
    font_size_big = 100
    font_size_small = "20sp"
else:
    widget_height_pixels = 35
    widget_height_percentage = None
    font_size_big = 50
    font_size_small = 20
player_symbols = ['X', 'O', '□', 'Δ', '◊', '*']
list_of_colors = None
player_sounds = [f'assets/Audio - Player Sound {i:02}.wav' for i in range(1, 14)]


def generate_random_colors_old(number_of_players):
    global list_of_colors
    list_of_colors = ['#{:06x}'.format(random.randint(0x111111, 0xEEEEEE)) for _ in range(number_of_players)]  # 0 and F are too extreme


def generate_random_colors_new(number_of_players):
    global list_of_colors
    list_of_colors = {}
    for player in number_of_players:
        list_of_colors[player] = (
            uniform(0.4, 0.8),  # Red
            uniform(0.4, 0.8),  # Green
            uniform(0.4, 0.8)   # Blue
        )
