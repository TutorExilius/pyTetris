from copy import deepcopy
from enum import IntEnum
from random import choice

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, QObject, pyqtSignal


class TetrominoType(IntEnum):
    I_BRICK = 1
    J_BRICK = 2
    L_BRICK = 3
    O_BRICK = 4
    S_BRICK = 5
    T_BRICK = 6
    Z_BRICK = 7


class Action(IntEnum):
    LEFT = 1
    RIGHT = 2
    DOWN = 3
    DROP = 4


class RotationType(IntEnum):
    CLOCKWISE = 1
    COUNTER_CLOCKWISE = 2


class Tetromino:
    def __init__(self, tetromio_type):
        self.tetromio_type = tetromio_type
        self.rotation_index = 0
        self.brick_matrix = None
        self.rotate(RotationType.CLOCKWISE, start_index=-1)

    def rotate(self, rotation_type, start_index=None):
        if start_index:
            self.rotation_index = start_index

        if self.tetromio_type == TetrominoType.I_BRICK:
            self.brick_matrix = self.rotate_I_brick(rotation_type)
        elif self.tetromio_type == TetrominoType.J_BRICK:
            self.brick_matrix = self.rotate_J_brick(rotation_type)
        elif self.tetromio_type == TetrominoType.L_BRICK:
            self.brick_matrix = self.rotate_L_brick(rotation_type)
        elif self.tetromio_type == TetrominoType.O_BRICK:
            self.brick_matrix = self.rotate_O_brick(rotation_type)
        elif self.tetromio_type == TetrominoType.S_BRICK:
            self.brick_matrix = self.rotate_S_brick(rotation_type)
        elif self.tetromio_type == TetrominoType.T_BRICK:
            self.brick_matrix = self.rotate_T_brick(rotation_type)
        elif self.tetromio_type == TetrominoType.Z_BRICK:
            self.brick_matrix = self.rotate_Z_brick(rotation_type)

    def rotate_I_brick(self, rotation_type):
        if rotation_type == RotationType.CLOCKWISE:
            self.rotation_index = (self.rotation_index + 1) % 2
        else:
            self.rotation_index = (self.rotation_index - 1) % 2

        t = TetrominoType.I_BRICK.value

        if self.rotation_index == 0:
            return [[0, 0, 0, 0], [0, 0, 0, 0], [t, t, t, t], [0, 0, 0, 0]]
        elif self.rotation_index == 1:
            return [[0, t, 0, 0], [0, t, 0, 0], [0, t, 0, 0], [0, t, 0, 0]]

    def rotate_J_brick(self, rotation_type):
        if rotation_type == RotationType.CLOCKWISE:
            self.rotation_index = (self.rotation_index + 1) % 4
        else:
            self.rotation_index = (self.rotation_index - 1) % 4

        t = TetrominoType.J_BRICK.value

        if self.rotation_index == 0:
            return [[0, 0, 0], [t, t, t], [0, 0, t]]
        elif self.rotation_index == 1:
            return [[0, t, 0], [0, t, 0], [t, t, 0]]
        elif self.rotation_index == 2:
            return [[t, 0, 0], [t, t, t], [0, 0, 0]]
        elif self.rotation_index == 3:
            return [[0, t, t], [0, t, 0], [0, t, 0]]

    def rotate_L_brick(self, rotation_type):
        if rotation_type == RotationType.CLOCKWISE:
            self.rotation_index = (self.rotation_index + 1) % 4
        else:
            self.rotation_index = (self.rotation_index - 1) % 4

        t = TetrominoType.L_BRICK.value

        if self.rotation_index == 0:
            return [[0, 0, 0], [t, t, t], [t, 0, 0]]
        elif self.rotation_index == 1:
            return [[t, t, 0], [0, t, 0], [0, t, 0]]
        elif self.rotation_index == 2:
            return [[0, 0, t], [t, t, t], [0, 0, 0]]
        elif self.rotation_index == 3:
            return [[0, t, 0], [0, t, 0], [0, t, t]]

    def rotate_O_brick(self, rotation_type):
        t = TetrominoType.O_BRICK.value

        return [[0, 0, 0, 0], [0, t, t, 0], [0, t, t, 0], [0, 0, 0, 0]]

    def rotate_S_brick(self, rotation_type):
        if rotation_type == RotationType.CLOCKWISE:
            self.rotation_index = (self.rotation_index + 1) % 2
        else:
            self.rotation_index = (self.rotation_index - 1) % 2

        t = TetrominoType.S_BRICK.value

        if self.rotation_index == 0:
            return [[0, 0, 0], [0, t, t], [t, t, 0]]
        elif self.rotation_index == 1:
            return [[t, 0, 0], [t, t, 0], [0, t, 0]]

    def rotate_T_brick(self, rotation_type):
        if rotation_type == RotationType.CLOCKWISE:
            self.rotation_index = (self.rotation_index + 1) % 4
        else:
            self.rotation_index = (self.rotation_index - 1) % 4

        t = TetrominoType.T_BRICK.value

        if self.rotation_index == 0:
            return [[0, 0, 0], [t, t, t], [0, t, 0]]
        elif self.rotation_index == 1:
            return [[0, t, 0], [t, t, 0], [0, t, 0]]
        elif self.rotation_index == 2:
            return [[0, t, 0], [t, t, t], [0, 0, 0]]
        elif self.rotation_index == 3:
            return [[0, t, 0], [0, t, t], [0, t, 0]]

    def rotate_Z_brick(self, rotation_type):
        if rotation_type == RotationType.CLOCKWISE:
            self.rotation_index = (self.rotation_index + 1) % 2
        else:
            self.rotation_index = (self.rotation_index - 1) % 2

        t = TetrominoType.Z_BRICK.value

        if self.rotation_index == 0:
            return [[0, 0, 0], [t, t, 0], [0, t, t]]
        elif self.rotation_index == 1:
            return [[0, t, 0], [t, t, 0], [t, 0, 0]]


class Game(QObject):
    next_tetromino_updated = pyqtSignal(Tetromino)
    field_updated = pyqtSignal(list)
    score_updated = pyqtSignal(int)
    level_updated = pyqtSignal(int)
    lines_updated = pyqtSignal(int)
    stamped_tetromino = pyqtSignal()
    pre_clear = pyqtSignal(list)

    def __init__(self, height, width, main_window):
        QObject.__init__(self)

        self.main_window = main_window

        # Connections
        self.next_tetromino_updated.connect(self.main_window.on_next_tetromino_update)
        self.field_updated.connect(self.main_window.on_field_update)
        self.score_updated.connect(self.main_window.on_score_update)
        self.level_updated.connect(self.main_window.on_level_update)
        self.lines_updated.connect(self.main_window.on_lines_update)
        self.lines_updated.connect(self.update_level)
        self.stamped_tetromino.connect(self.check_complete_lines)
        self.pre_clear.connect(self.main_window.pre_clear_animation)

        # https://tetris.wiki/Scoring
        self.line_score_base = [40, 100, 300, 1200]

        # https://tetris.wiki/Tetris_(Game_Boy)
        self.frames_per_second = 59.73
        self.level_speed_frames = [
            53,
            49,
            45,
            41,
            37,
            33,
            28,
            22,
            17,
            11,
            10,
            9,
            8,
            7,
            6,
            6,
            5,
            5,
            4,
            4,
            3,
        ]

        self.is_running = False
        self.height = height
        self.width = width
        self.playing_cursor = (0, 0)
        self.current_tetromino = None
        self._total_removed_lines = 0
        self.soft_drops = 0
        self.level = 0
        self._score = 0
        self.field = [[0] * self.width for i in range(self.height)]
        self.initialise_field(self.field)

        self.pause = False
        self.move_timer = None
        self.collision_detected = False
        self.next_tetromino = Tetromino(choice(list(TetrominoType)))
        self.build_next_tetromino()

    def initialise_field(self, field):
        # initialise/draw walls and ground
        for h in range(self.height):
            field[h][0] = -1
            field[h][-1] = -1

        for w in range(self.width):
            field[-1][w] = -2

    def update_field(self):
        final_field = deepcopy(self.field)
        self.merge_tetromino_with_field(final_field)
        self.field_updated.emit(final_field)

    def handle_input(self, key):
        if (key == QtCore.Qt.Key_Left or key == QtCore.Qt.Key_A) and not self.pause:
            self.move(Action.LEFT)
        elif (key == QtCore.Qt.Key_Right or key == QtCore.Qt.Key_D) and not self.pause:
            self.move(Action.RIGHT)
        elif (key == QtCore.Qt.Key_Down or key == QtCore.Qt.Key_S) and not self.pause:
            self.move_timer.stop()
            self.move(Action.DOWN)
            self.move_timer.setInterval(self.calculate_move_speed())
            self.move_timer.start()
            self.soft_drops += 1
        elif key == QtCore.Qt.Key_K and not self.pause:
            self.rotate_clockwise_tetromino()
        elif key == QtCore.Qt.Key_J and not self.pause:
            self.rotate_counter_clockwise_tetromino()
        elif key == QtCore.Qt.Key_Space and not self.pause:
            self.move_timer.stop()
            self.move(Action.DROP)
            self.move_timer.setInterval(self.calculate_move_speed())
            self.move_timer.start()
        elif key == QtCore.Qt.Key_P:
            self.pause_game()
        elif key == QtCore.Qt.Key_N:
            pass

    def pause_game(self):
        self.pause = not self.pause

        if self.pause:
            self.move_timer.stop()
            self.main_window.game_timer.stop()
            self.main_window.write_pause()
        else:
            self.move_timer.start()
            self.main_window.game_timer.start()
            self.main_window.clear_pause_label()

    def rotate_clockwise_tetromino(self):
        if self.current_tetromino:
            tmp = deepcopy(self.current_tetromino)
            self.current_tetromino.rotate(RotationType.CLOCKWISE)

            # reset rotation
            if not self.is_possible(self.playing_cursor, self.current_tetromino):
                self.current_tetromino = tmp

    def rotate_counter_clockwise_tetromino(self):
        if self.current_tetromino:
            tmp = deepcopy(self.current_tetromino)
            self.current_tetromino.rotate(RotationType.COUNTER_CLOCKWISE)

            # reset rotation
            if not self.is_possible(self.playing_cursor, self.current_tetromino):
                self.current_tetromino = tmp

    def move(self, action=Action.DOWN):
        h, w = self.playing_cursor

        if action == Action.DOWN:
            h += 1
        elif action == Action.LEFT:
            w -= 1
        elif action == Action.RIGHT:
            w += 1
        elif action == Action.DROP:
            while self.move(Action.DOWN):
                pass
            return

        new_pos = (h, w)

        if self.is_possible(new_pos, self.current_tetromino):
            self.playing_cursor = new_pos
            return True
        else:
            if action != Action.LEFT and action != Action.RIGHT:
                self.collision_detected = True
            return False

    def calculate_move_speed(self):
        level = min(self.level, len(self.level_speed_frames) - 1)
        speed_frames = self.level_speed_frames[level]

        return (speed_frames / self.frames_per_second) * 1000  # ms

    def running(self):
        if not self.move_timer:
            self.move_timer = QTimer()
            self.move_timer.timeout.connect(self.move)
            self.move_timer.start(self.calculate_move_speed())
            self.update_field()
            self.pause_game()

        if not self.pause:
            self.update_field()

        if self.collision_detected:
            self.stamp_tetromino()

            # spawn next tetomino
            self.collision_detected = self.build_next_tetromino()

            return not self.collision_detected

        return self.is_running

    def build_next_tetromino(self):
        next_tetromino = self.next_tetromino
        self.next_tetromino = Tetromino(choice(list(TetrominoType)))
        if self.spawn(next_tetromino):
            self.next_tetromino_updated.emit(self.next_tetromino)
            return False
        else:
            return True

    def spawn(self, tetromino, pos=None):
        # https://tetris.fandom.com/wiki/Tetris_Guideline
        # (last visit 2020-03-14)
        self.current_tetromino = tetromino
        tetromino_type = tetromino.tetromio_type

        if pos:
            self.playing_cursor = pos
        else:
            if tetromino_type == TetrominoType.I_BRICK:
                self.playing_cursor = (-2, 4)
            elif tetromino_type == TetrominoType.J_BRICK:
                self.playing_cursor = (-1, 4)
            elif tetromino_type == TetrominoType.L_BRICK:
                self.playing_cursor = (-1, 4)
            elif tetromino_type == TetrominoType.O_BRICK:
                self.playing_cursor = (-1, 4)
            elif tetromino_type == TetrominoType.S_BRICK:
                self.playing_cursor = (-1, 4)
            elif tetromino_type == TetrominoType.T_BRICK:
                self.playing_cursor = (-1, 4)
            elif tetromino_type == TetrominoType.Z_BRICK:
                self.playing_cursor = (-1, 4)
            else:
                raise "UNKNOWN TETROMINO"

        return self.is_possible(self.playing_cursor, self.current_tetromino)

    def is_possible(self, pos, tetromino):
        future_cursor_h, future_cursor_w = pos

        tetromino_h = len(tetromino.brick_matrix)
        tetromino_w = len(tetromino.brick_matrix[0])

        for h in range(tetromino_h):
            for w in range(tetromino_w):
                value = tetromino.brick_matrix[h][w]

                if value != 0:
                    if (future_cursor_h + h) not in range(self.height) or (
                        future_cursor_w + w
                    ) not in range(self.width):
                        return False

                    field_value = self.field[future_cursor_h + h][future_cursor_w + w]

                    if field_value != 0:
                        return False

        return True

    def stamp_tetromino(self):
        self.merge_tetromino_with_field(self.field)
        self.stamped_tetromino.emit()
        self.score += self.soft_drops
        self.soft_drops = 0

    def check_complete_lines(self):
        complete_lines = []

        for h in reversed(range(self.height - 1)):
            completed_line = True

            for w in range(1, self.width - 1):
                if self.field[h][w] == 0:
                    completed_line = False
                    break

            if completed_line:
                complete_lines.append(h)

        if len(complete_lines):
            self.remove_complete_lines(complete_lines)

    def remove_complete_lines(self, complete_lines):
        self.update_field()
        self.main_window.pre_clear_animation(complete_lines)

        new_field = [[0] * self.width for i in range(self.height)]
        self.initialise_field(new_field)

        row_behind = 0
        for h in reversed(range(self.height - 1)):
            if h in complete_lines:
                row_behind += 1
                continue

            for w in range(1, self.width - 1):
                new_field[h + row_behind][w] = self.field[h][w]

        self.field = new_field
        calculated_score = self.line_score_base[len(complete_lines) - 1] * (
            self.level + 1
        )

        self.score += calculated_score
        self.total_removed_lines += len(complete_lines)

    @property
    def total_removed_lines(self):
        return self._total_removed_lines

    @total_removed_lines.setter
    def total_removed_lines(self, value):
        self._total_removed_lines = value
        self.lines_updated.emit(self.total_removed_lines)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        self.score_updated.emit(self._score)

    def update_level(self):
        old_level = self.level

        self.level = self.total_removed_lines // 10

        if old_level < self.level:
            self.level_updated.emit(self.level)
            self.update_speed()

    def update_speed(self):
        self.move_timer.setInterval(self.calculate_move_speed())

    def merge_tetromino_with_field(self, field):
        cursor_h, cursor_w = self.playing_cursor

        tetromino_h = len(self.current_tetromino.brick_matrix)
        tetromino_w = len(self.current_tetromino.brick_matrix[0])

        try:
            for h in range(tetromino_h):
                for w in range(tetromino_w):
                    if (cursor_h + h) in range(self.height) and (cursor_w + w) in range(
                        self.width
                    ):
                        value = self.current_tetromino.brick_matrix[h][w]
                        field_value = field[cursor_h + h][cursor_w + w]

                        if value != 0 and field_value == 0:
                            field[cursor_h + h][cursor_w + w] = value
        except Exception as e:
            print(e)
