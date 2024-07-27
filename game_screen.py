import config
import copy
import random
from kivy.core.window import Window
from kivy.graphics import Color, Line
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from kivy.clock import Clock


class TicTacToeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Image(source='assets/Icon 02.png', pos=self.pos, size=Window.system_size, opacity=0.1)
        self.grid_height = 3
        self.grid_width = 3
        self.row_sequence = 3
        self.column_sequence = 3
        self.diagonal_sequence = 3
        self.num_players = 2
        self.max_num_players = len(config.num_players_spinner_values) + 1
        self.starting_player = 0
        self.current_player = self.starting_player
        self.vs_ghost = False
        self.game_over = False
        self.result_label = Label(text=f"Player {config.player_symbols[self.current_player]}'s turn", font_name=config.global_font, font_size=config.font_size_small, size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels)
        self.board = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.scores = {player: 0 for player in range(self.max_num_players)}
        self.colors = config.generate_random_colors()
        self.winning_sequence = []

    def initialize_game(self, grid_height, grid_width, num_players, row_sequence, column_sequence, diagonal_sequence):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.row_sequence = row_sequence
        self.column_sequence = column_sequence
        self.diagonal_sequence = diagonal_sequence
        self.num_players = num_players
        self.initialize_board()

    def initialize_board(self):
        self.board = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.current_player = self.starting_player
        self.game_over = False
        self.winning_sequence = []
        self.update_turn_label()
        self.canvas.clear()
        self.draw_grid()
        self.make_ghost_move()

    def draw_grid(self, *_):
        self.canvas.clear()
        cell_height = self.height / self.grid_height
        cell_width = self.width / self.grid_width
        with self.canvas:
            Color(1, 1, 1, 1)  # White color for grid lines
            for i in range(1, self.grid_height):
                # Horizontal lines
                Line(points=[0, i * cell_height, self.width, i * cell_height], width=1)
            for i in range(1, self.grid_width):
                # Vertical lines
                Line(points=[i * cell_width, 0, i * cell_width, self.height], width=1)

        # Redraw existing symbols
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.board[row][col]:
                    self.draw_symbol(row, col, self.board[row][col])

    def on_touch_down(self, touch):
        if not self.game_over:
            if self.current_player == (self.num_players - 1) and self.vs_ghost:
                row, col = touch
            else:
                row, col = self.get_clicked_row_col(touch)
            if row is not None and col is not None and self.board[row][col] is None:
                self.board[row][col] = self.current_player
                self.draw_symbol(row, col, self.current_player)
                if self.check_winner(row, col, self.current_player):
                    self.result_label.text = f"Player {config.player_symbols[self.current_player]} wins!"
                    self.play_sound(sound_type="results", result="win")
                    self.scores[self.current_player] += 1
                    self.game_over = True
                    self.draw_winning_line()
                elif self.check_tie():
                    self.result_label.text = "It's a tie!"
                    self.play_sound(sound_type="results", result="tie")
                    self.game_over = True
                else:
                    self.play_sound(player=self.current_player, sound_type="players")
                    self.current_player = (self.current_player + 1) % self.num_players
                    self.update_turn_label()
                    self.make_ghost_move()

        # If the game is over, switch to score screen on next click
        elif self.game_over:
            self.starting_player = (self.starting_player + 1) % self.num_players
            self.parent.parent.manager.transition.direction = 'left'
            score_screen = self.parent.parent.manager.get_screen('scores')
            score_screen.update_scores(self.scores, self.num_players)
            self.parent.parent.manager.current = 'scores'
            self.parent.parent.reset_game(None)

    def make_ghost_move(self):
        if self.current_player == (self.num_players - 1) and self.vs_ghost:
            # Clock.usleep(1 * 1000 * 1000)  # 1 second delay
            # Iterate for each grid posiotn, and for each player
            for row in range(self.grid_height):
                for col in range(self.grid_width):
                    for symbol in range(self.num_players):
                        board_copy = copy.deepcopy(self.board)
                        if row is not None and col is not None and self.board[row][col] is None:
                            self.board[row][col] = symbol
                            if self.check_winner(row, col, symbol):
                                self.board = copy.deepcopy(board_copy)
                                self.on_touch_down(touch=(row, col))
                                return None
                        self.board = copy.deepcopy(board_copy)

            # if there is no functional move, make a random move at the corners
            list_grid_corners = [[0, 0], [0, self.grid_width - 1], [self.grid_height - 1, 0], [self.grid_height - 1, self.grid_width - 1]]
            random.shuffle(list_grid_corners)
            for row, col in list_grid_corners:
                if row is not None and col is not None and self.board[row][col] is None:
                    self.on_touch_down(touch=(row, col))
                    return None

            # random move at the middle
            list_width_center_positions = [int(self.grid_width / 2)]
            if self.grid_width % 2 == 0:
                list_width_center_positions.append(int(self.grid_width / 2) - 1)
            list_height_center_positions = [int(self.grid_height / 2)]
            if self.grid_height % 2 == 0:
                list_height_center_positions.append(int(self.grid_height / 2) - 1)
            list_center_positions = [[x, y] for x in list_height_center_positions for y in list_width_center_positions]
            random.shuffle(list_center_positions)
            for row, col in list_center_positions:
                if row is not None and col is not None and self.board[row][col] is None:
                    self.on_touch_down(touch=(row, col))
                    return None

            # random move:
            list_all_positions = [[x, y] for x in range(self.grid_height) for y in range(self.grid_width)]
            random.shuffle(list_all_positions)
            for row, col in list_all_positions:
                if row is not None and col is not None and self.board[row][col] is None:
                    self.on_touch_down(touch=(row, col))
                    return None

    def get_clicked_row_col(self, touch):
        cell_height = self.height / self.grid_height
        cell_width = self.width / self.grid_width
        row = int(touch.y // cell_height)
        col = int(touch.x // cell_width)

        # Check if the click is within the bounds of the game grid
        if 0 <= row < self.grid_height and 0 <= col < self.grid_width:
            return row, col
        else:
            return None, None

    @staticmethod
    def play_sound(sound_type, player=None, result=None):
        match sound_type:
            case "players":
                SoundLoader.load(config.player_sounds[player]).play()
            case "results":
                SoundLoader.load(config.result_sounds[result]).play()

    def draw_symbol(self, row, col, player):
        cell_height = self.height / self.grid_height
        cell_width = self.width / self.grid_width
        with self.canvas:
            r, g, b = self.colors[player]
            Color(r, g, b, 1)
            match player % len(config.player_symbols):
                case 0:
                    self.draw_player_01(row, col, cell_height, cell_width)      # symbol = X
                case 1:
                    self.draw_player_02(row, col, cell_height, cell_width)      # symbol = O
                case 2:
                    self.draw_player_03(row, col, cell_height, cell_width)      # symbol = □
                case 3:
                    self.draw_player_04(row, col, cell_height, cell_width)      # symbol = △
                case 4:
                    self.draw_player_05(row, col, cell_height, cell_width)      # symbol = ◇
                case _:
                    self.draw_player_06(row, col, cell_height, cell_width)      # symbol = *


    @staticmethod
    def draw_player_01(row, col, cell_height, cell_width, pading=0.2, thickness=5):   # symbol = X
        Line(points=[col * cell_width + cell_width * pading, row * cell_height + cell_height * pading,
                     (col + 1) * cell_width - cell_width * pading, (row + 1) * cell_height - cell_height * pading], width=thickness)
        Line(points=[(col + 1) * cell_width - cell_width * pading, row * cell_height + cell_height * pading,
                     col * cell_width + cell_width * pading, (row + 1) * cell_height - cell_height * pading], width=thickness)

    @staticmethod
    def draw_player_02(row, col, cell_height, cell_width, pading=0.2, thickness=5):  # symbol = O
        Line(circle=(col * cell_width + cell_width / 2, row * cell_height + cell_height / 2,
                     min(cell_width, cell_height) / 3), width=thickness)

    @staticmethod
    def draw_player_03(row, col, cell_height, cell_width, pading=0.2, thickness=5):   # symbol = □
        Line(rectangle=(col * cell_width + cell_width * pading, row * cell_height + cell_height * pading,
                        cell_width * (1 - pading * 2), cell_height * (1 - pading * 2)), width=thickness)

    @staticmethod
    def draw_player_04(row, col, cell_height, cell_width, pading=0.2, thickness=5):  # symbol = Δ
        Line(points=[col * cell_width + cell_width * 0.5, row * cell_height + cell_height * (1 - pading),
                     col * cell_width + cell_width * (1 - pading), row * cell_height + cell_height * pading,
                     col * cell_width + cell_width * pading, row * cell_height + cell_height * pading,
                     col * cell_width + cell_width * 0.5, row * cell_height + cell_height * (1 - pading)], width=thickness)

    @staticmethod
    def draw_player_05(row, col, cell_height, cell_width, pading=0.2, thickness=5):   # symbol = ◊
        Line(points=[col * cell_width + cell_width * 0.5, row * cell_height + cell_height * (1 - pading),
                     col * cell_width + cell_width * (1 - pading), row * cell_height + cell_height * 0.5,
                     col * cell_width + cell_width * 0.5, row * cell_height + cell_height * pading,
                     col * cell_width + cell_width * pading, row * cell_height + cell_height * 0.5,
                     col * cell_width + cell_width * 0.5, row * cell_height + cell_height * (1 - pading)], width=thickness)

    @staticmethod
    def draw_player_06(row, col, cell_height, cell_width, pading_1=0.2, pading_2=0.275, thickness=5):   # symbol = ж
        Line(points=[col * cell_width + cell_width * 0.5, row * cell_height + cell_height * (1 - pading_1),
                     col * cell_width + cell_width * 0.5, row * cell_height + cell_height * pading_1], width=thickness)
        Line(points=[col * cell_width + cell_width * pading_1, row * cell_height + cell_height * 0.5,
                     col * cell_width + cell_width * (1 - pading_1), row * cell_height + cell_height * 0.5], width=thickness)
        Line(points=[col * cell_width + cell_width * pading_2, row * cell_height + cell_height * pading_2,
                     col * cell_width + cell_width * (1 - pading_2), row * cell_height + cell_height * (1 - pading_2)], width=thickness)
        Line(points=[col * cell_width + cell_width * pading_2, row * cell_height + cell_height * (1 - pading_2),
                     col * cell_width + cell_width * (1 - pading_2), row * cell_height + cell_height * pading_2], width=thickness)

    def draw_winning_line(self):
        cell_height = self.height / self.grid_height
        cell_width = self.width / self.grid_width
        with self.canvas:
            Color(1, 1, 1, 1)  # White color for the winning line
            start_row, start_col = self.winning_sequence[0]
            end_row, end_col = self.winning_sequence[1]
            Line(points=[start_col * cell_width + cell_width / 2, start_row * cell_height + cell_height / 2, end_col * cell_width + cell_width / 2, end_row * cell_height + cell_height / 2], width=4)

    def check_winner(self, row, col, symbol):
        for c in range(self.grid_width - self.row_sequence + 1):
            if all([self.board[row][i + c] == symbol for i in range(self.row_sequence)]):
                self.winning_sequence = [(row, c), (row, self.row_sequence - 1 + c)]
                return True
        # Check column:
        for r in range(self.grid_height - self.column_sequence + 1):
            if all([self.board[i + r][col] == symbol for i in range(self.column_sequence)]):
                self.winning_sequence = [(r, col), (self.column_sequence - 1 + r, col)]
                return True
        # Check forward diagonal:
        for r, c in zip(range(row - self.diagonal_sequence + 1, row + 1), range(col - self.diagonal_sequence + 1, col + 1)):
            if 0 <= r <= (self.grid_height - self.diagonal_sequence) and 0 <= c <= (self.grid_width - self.diagonal_sequence):
                if all([self.board[r + i][c + i] == symbol for i in range(self.diagonal_sequence)]):
                    self.winning_sequence = [(r, c), (r + self.diagonal_sequence - 1, c + self.diagonal_sequence - 1)]
                    return True
        # Check backward diagonal:
        for r, c in zip(reversed(range(row, row + self.diagonal_sequence)), range(col - self.diagonal_sequence + 1, col + 1)):
            if self.diagonal_sequence - 1 <= r <= self.grid_height - 1 and 0 <= c <= (self.grid_width - self.diagonal_sequence):
                if all([self.board[r - i][c + i] == symbol for i in range(self.diagonal_sequence)]):
                    self.winning_sequence = [(r, c), (r - self.diagonal_sequence + 1, c + self.diagonal_sequence - 1)]
                    return True
        return False

    def check_tie(self):
        return all(self.board[r][c] is not None for r in range(self.grid_height) for c in range(self.grid_width))

    def update_turn_label(self):
        self.result_label.text = f"Player {config.player_symbols[self.current_player]}'s turn"


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        button_layout = BoxLayout(size_hint=(1, config.widget_height_percentage), height=config.widget_height_pixels)
        back_to_menu_button = Button(text='Back to Menu', font_size=config.font_size_small)
        back_to_menu_button.bind(on_press=self.back_to_menu)
        reset_game_button = Button(text='Reset Game', font_size=config.font_size_small)
        reset_game_button.bind(on_press=self.reset_game)
        reset_results_button = Button(text='Reset Results', font_size=config.font_size_small)
        reset_results_button.bind(on_press=self.reset_results)
        view_scores_button = Button(text='View Scores', font_size=config.font_size_small)
        view_scores_button.bind(on_press=self.view_scores)
        button_layout.add_widget(back_to_menu_button)
        button_layout.add_widget(reset_game_button)
        button_layout.add_widget(reset_results_button)
        button_layout.add_widget(view_scores_button)

        self.game = TicTacToeGame()
        self.game.bind(size=self.game.draw_grid)

        layout.add_widget(button_layout)
        layout.add_widget(self.game.result_label)
        layout.add_widget(self.game)

        self.add_widget(layout)

    def back_to_menu(self, _):
        self.manager.transition.direction = 'right'
        self.manager.current = 'welcome'
        self.game.starting_player = 0

    def reset_game(self, _):
        self.game.initialize_board()

    def reset_results(self, _):
        # Reset the scores to 0 for each player
        for symbol in self.game.scores:
            self.game.scores[symbol] = 0

        # Update the result label
        self.game.result_label.text = '  ' + self.game.result_label.text + '\nScores are reset'

    def view_scores(self, _):
        score_screen = self.manager.get_screen('scores')
        score_screen.update_scores(self.game.scores, self.game.num_players)
        self.manager.transition.direction = 'left'
        self.manager.current = 'scores'
