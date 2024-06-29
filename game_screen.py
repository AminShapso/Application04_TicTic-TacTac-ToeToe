import config
from kivy.graphics import Color, Line
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader


class TicTacToeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid_height = 3
        self.grid_width = 3
        self.num_players = 2
        self.max_num_players = len(config.num_players_spinner_values)
        self.starting_player = 0
        self.current_player = 0 + self.starting_player
        self.game_over = False
        self.result_label = Label(text=f"Player {config.player_symbols[self.current_player]}'s turn", font_name=config.global_font, font_size='20sp', size_hint=(1, None))
        self.board = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.scores = {player: 0 for player in range(self.max_num_players)}
        self.colors = self.generate_random_colors()
        self.winning_sequence = []

    def generate_random_colors(self):
        config.generate_random_colors_new(range(self.max_num_players))
        return dict(config.list_of_colors)

    def initialize_game(self, grid_height, grid_width, num_players):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.num_players = num_players
        self.board = [[None for _ in range(grid_width)] for _ in range(grid_height)]
        self.current_player = 0
        self.game_over = False
        self.winning_sequence = []
        self.update_turn_label()
        self.canvas.clear()
        self.draw_grid()

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
            row, col = self.get_clicked_row_col(touch)
            if row is not None and col is not None and self.board[row][col] is None:
                self.board[row][col] = self.current_player
                self.draw_symbol(row, col, self.current_player)
                self.play_sound(self.current_player)
                if self.check_winner(row, col, self.current_player):
                    self.result_label.text = f"Player {config.player_symbols[self.current_player]} wins!"
                    self.scores[self.current_player] += 1
                    self.game_over = True
                    self.draw_winning_line()
                elif self.check_tie():
                    self.result_label.text = "It's a tie!"
                    self.game_over = True
                else:
                    self.current_player = (self.current_player + 1) % self.num_players
                    self.update_turn_label()

        # If the game is over, switch to score screen on next click
        elif self.game_over:
            self.parent.parent.manager.transition.direction = 'left'
            score_screen = self.parent.parent.manager.get_screen('scores')
            score_screen.update_scores(self.scores, self.num_players)
            self.parent.parent.manager.current = 'scores'
            self.parent.parent.reset_game(None)

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

    def play_sound(self, player):
        SoundLoader.load(config.player_sounds[player]).play()

    def draw_symbol(self, row, col, player):
        cell_height = self.height / self.grid_height
        cell_width = self.width / self.grid_width
        with self.canvas:
            r, g, b = self.colors[player]
            Color(r, g, b, 1)
            if player % len(config.player_symbols) == 0:    # symbol = X
                Line(points=[col * cell_width + cell_width * 0.2, row * cell_height + cell_height * 0.2,
                             (col + 1) * cell_width - cell_width * 0.2, (row + 1) * cell_height - cell_height * 0.2], width=2)
                Line(points=[(col + 1) * cell_width - cell_width * 0.2, row * cell_height + cell_height * 0.2,
                             col * cell_width + cell_width * 0.2, (row + 1) * cell_height - cell_height * 0.2], width=2)
            elif player % len(config.player_symbols) == 1:  # symbol = O
                Line(circle=(col * cell_width + cell_width / 2, row * cell_height + cell_height / 2,
                             min(cell_width, cell_height) / 3), width=2)
            elif player % len(config.player_symbols) == 2:  # symbol = □
                Line(rectangle=(col * cell_width + cell_width * 0.2, row * cell_height + cell_height * 0.2,
                                cell_width * 0.6, cell_height * 0.6), width=2)
            elif player % len(config.player_symbols) == 3:  # symbol = △
                Line(points=[col * cell_width + cell_width * 0.5, row * cell_height + cell_height * 0.8,
                             col * cell_width + cell_width * 0.8, row * cell_height + cell_height * 0.2,
                             col * cell_width + cell_width * 0.2, row * cell_height + cell_height * 0.2,
                             col * cell_width + cell_width * 0.5, row * cell_height + cell_height * 0.8], width=2)
            elif player % len(config.player_symbols) == 4:  # symbol = ◇
                Line(points=[col * cell_width + cell_width * 0.5, row * cell_height + cell_height * 0.8,
                             col * cell_width + cell_width * 0.8, row * cell_height + cell_height * 0.5,
                             col * cell_width + cell_width * 0.5, row * cell_height + cell_height * 0.2,
                             col * cell_width + cell_width * 0.2, row * cell_height + cell_height * 0.5,
                             col * cell_width + cell_width * 0.5, row * cell_height + cell_height * 0.8], width=2)
            else:   # symbol = *
                Line(points=[col * cell_width + cell_width * 0.5, row * cell_height + cell_height * 0.8,
                             col * cell_width + cell_width * 0.5, row * cell_height + cell_height * 0.2], width=2)
                Line(points=[col * cell_width + cell_width * 0.2, row * cell_height + cell_height * 0.5,
                             col * cell_width + cell_width * 0.8, row * cell_height + cell_height * 0.5], width=2)
                Line(points=[col * cell_width + cell_width * 0.3, row * cell_height + cell_height * 0.3,
                             col * cell_width + cell_width * 0.7, row * cell_height + cell_height * 0.7], width=2)
                Line(points=[col * cell_width + cell_width * 0.3, row * cell_height + cell_height * 0.7,
                             col * cell_width + cell_width * 0.7, row * cell_height + cell_height * 0.3], width=2)

    def draw_winning_line(self):
        cell_height = self.height / self.grid_height
        cell_width = self.width / self.grid_width
        with self.canvas:
            Color(1, 1, 1, 1)  # White color for the winning line
            for i in range(len(self.winning_sequence) - 1):
                start_row, start_col = self.winning_sequence[i]
                end_row, end_col = self.winning_sequence[i + 1]
                Line(points=[start_col * cell_width + cell_width / 2, start_row * cell_height + cell_height / 2,
                             end_col * cell_width + cell_width / 2, end_row * cell_height + cell_height / 2], width=4)

    def check_winner(self, row, col, symbol):
        if all(self.board[row][c] == symbol for c in range(self.grid_width)):
            self.winning_sequence = [(row, c) for c in range(self.grid_width)]
            return True
        if all(self.board[r][col] == symbol for r in range(self.grid_height)):
            self.winning_sequence = [(r, col) for r in range(self.grid_height)]
            return True
        if row == col and all(self.board[i][i] == symbol for i in range(min(self.grid_height, self.grid_width))):
            self.winning_sequence = [(i, i) for i in range(min(self.grid_height, self.grid_width))]
            return True
        if row + col == self.grid_width - 1 and all(self.board[i][self.grid_width - 1 - i] == symbol for i in range(min(self.grid_height, self.grid_width))):
            self.winning_sequence = [(i, self.grid_width - 1 - i) for i in range(min(self.grid_height, self.grid_width))]
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

        button_layout = BoxLayout(size_hint=(1, None), height=50)
        back_to_menu_button = Button(text='Back to Menu')
        back_to_menu_button.bind(on_press=self.back_to_menu)
        reset_game_button = Button(text='Reset Game')
        reset_game_button.bind(on_press=self.reset_game)
        reset_results_button = Button(text='Reset Results')
        reset_results_button.bind(on_press=self.reset_results)
        view_scores_button = Button(text='View Scores')
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

    def reset_game(self, _):
        self.game.initialize_game(self.game.grid_height, self.game.grid_width, self.game.num_players)

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
