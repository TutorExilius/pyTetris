import os
import subprocess
from copy import deepcopy
from enum import IntEnum
from random import choice
from PyQt5.QtCore import QTimer, QObject, pyqtSignal

if os.name == "nt":

    def cls():
        subprocess.run("cls", shell=True)


else:

    def cls():
        subprocess.run(["clear"])


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

    def __str__(self):
        lines = ["".join(str(line)) for line in self.brick_matrix]
        return "\n".join(lines)

    def rotate(self, rotation_type, start_index=None):
        if start_index:
            self.rotation_index = start_index

        if self.tetromio_type == TetrominoType.I_BRICK:
            self.brick_matrix = self._rotate_I_brick(rotation_type)
        elif self.tetromio_type == TetrominoType.J_BRICK:
            self.brick_matrix = self._rotate_J_brick(rotation_type)
        elif self.tetromio_type == TetrominoType.L_BRICK:
            self.brick_matrix = self._rotate_L_brick(rotation_type)
        elif self.tetromio_type == TetrominoType.O_BRICK:
            self.brick_matrix = self._rotate_O_brick(rotation_type)
        elif self.tetromio_type == TetrominoType.S_BRICK:
            self.brick_matrix = self._rotate_S_brick(rotation_type)
        elif self.tetromio_type == TetrominoType.T_BRICK:
            self.brick_matrix = self._rotate_T_brick(rotation_type)
        elif self.tetromio_type == TetrominoType.Z_BRICK:
            self.brick_matrix = self._rotate_Z_brick(rotation_type)

    def _rotate_I_brick(self, rotation_type):
        if rotation_type == RotationType.CLOCKWISE:
            self.rotation_index = (self.rotation_index + 1) % 2
        else:
            self.rotation_index = (self.rotation_index - 1) % 2

        t = TetrominoType.I_BRICK.value

        if self.rotation_index == 0:
            return [[0, 0, 0, 0], [0, 0, 0, 0], [t, t, t, t], [0, 0, 0, 0]]
        elif self.rotation_index == 1:
            return [[0, t, 0, 0], [0, t, 0, 0], [0, t, 0, 0], [0, t, 0, 0]]

    def _rotate_J_brick(self, rotation_type):
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

    def _rotate_L_brick(self, rotation_type):
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

    def _rotate_O_brick(self, rotation_type):
        t = TetrominoType.O_BRICK.value

        return [[0, 0, 0, 0], [0, t, t, 0], [0, t, t, 0], [0, 0, 0, 0]]

    def _rotate_S_brick(self, rotation_type):
        if rotation_type == RotationType.CLOCKWISE:
            self.rotation_index = (self.rotation_index + 1) % 2
        else:
            self.rotation_index = (self.rotation_index - 1) % 2

        t = TetrominoType.S_BRICK.value

        if self.rotation_index == 0:
            return [[0, 0, 0], [0, t, t], [t, t, 0]]
        elif self.rotation_index == 1:
            return [[t, 0, 0], [t, t, 0], [0, t, 0]]

    def _rotate_T_brick(self, rotation_type):
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

    def _rotate_Z_brick(self, rotation_type):
        if rotation_type == RotationType.CLOCKWISE:
            self.rotation_index = (self.rotation_index + 1) % 2
        else:
            self.rotation_index = (self.rotation_index - 1) % 2

        t = TetrominoType.Z_BRICK.value

        if self.rotation_index == 0:
            return [[0, 0, 0], [t, t, 0], [0, t, t]]
        elif self.rotation_index == 1:
            return [[0, t, 0], [t, t, 0], [t, 0, 0]]


class Field(QObject):
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
        self.lines_updated.connect(self._update_level)
        self.stamped_tetromino.connect(self._check_complete_lines)
        self.pre_clear.connect(self.main_window._pre_clear_animation)
        self.main_window.soft_dropped.connect(self._on_soft_dropped)

        # https://tetris.wiki/Scoring
        self._line_score_base = [40, 100, 300, 1200]

        # https://tetris.wiki/Tetris_(Game_Boy)
        self._frames_per_second = 59.73
        self._level_speed_frames = [
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

        self._height = height
        self._width = width
        self._cursor = (0, 0)
        self._current_tetromino = None
        self._total_removed_lines = 0
        self._soft_drops = 0
        self._level = 0
        self._score = 0
        self._field = [[0] * self._width for i in range(self._height)]
        self._initialise_field(self._field)

        # self._ignore_actions = False
        self._is_running = False
        self._move_timer = None
        self._collision_detected = False
        self._next_tetromino = Tetromino(choice(list(TetrominoType)))
        self._build_next_tetromino()

    # wonderful site effect here :) ... guess what :D
    def __str__(self):
        # TODO: draw_tetromino auslagern in tetris.update o.ä.
        cls()

        self._update_field()

        next_tetromino = str(self._next_tetromino)

        field_out = (
            "\n".join("".join(str(row)) for row in self._field)
            + "\n\n"
            + next_tetromino
        )

        return field_out.replace("0", " ")

    def _initialise_field(self, field):
        # initialise/draw walls and ground
        for h in range(self._height):
            field[h][0] = -1
            field[h][-1] = -1

        for w in range(self._width):
            field[-1][w] = -2

    def _update_field(self):
        final_field = deepcopy(self._field)
        self._merge_tetromino_with_field(final_field)
        self.field_updated.emit(final_field)

    def _on_soft_dropped(self):
        self._soft_drops += 1

    def pause_game(self, paused):
        if paused:
            self._move_timer.stop()
        else:
            self._move_timer.start()

    def rotate_clockwise_tetromino(self):
        if self._current_tetromino:
            tmp = deepcopy(self._current_tetromino)
            self._current_tetromino.rotate(RotationType.CLOCKWISE)

            # reset rotation
            if not self._is_possible(self._cursor, self._current_tetromino):
                self._current_tetromino = tmp

    def rotate_counter_clockwise_tetromino(self):
        if self._current_tetromino:
            tmp = deepcopy(self._current_tetromino)
            self._current_tetromino.rotate(RotationType.COUNTER_CLOCKWISE)

            # reset rotation
            if not self._is_possible(self._cursor, self._current_tetromino):
                self._current_tetromino = tmp

    def _move(self, action=Action.DOWN):
        h, w = self._cursor

        if action == Action.DOWN:
            h += 1
        elif action == Action.LEFT:
            w -= 1
        elif action == Action.RIGHT:
            w += 1
        elif action == Action.DROP:
            # self._is_dropping = True

            while self._move(Action.DOWN):
                pass

            return

            # self._collision_detected = True
            # return False

        new_pos = (h, w)

        if self._is_possible(new_pos, self._current_tetromino):
            self._cursor = new_pos
            return True
        else:
            if action != Action.LEFT and action != Action.RIGHT:
                self._collision_detected = True
            return False

    def calculate_move_speed(self):
        level = min(self._level, len(self._level_speed_frames) - 1)
        speed_frames = self._level_speed_frames[level]

        return (speed_frames / self._frames_per_second) * 1000  # ms

    def running(self):
        if not self._move_timer:
            self._move_timer = QTimer()
            self._move_timer.timeout.connect(self._move)
            self._move_timer.start(self.calculate_move_speed())
            self._is_running = True
            print("\nTIMER SHOT\n")

        if self._collision_detected:
            self._stamp_tetromino()

            # spawn next tetomino
            self._collision_detected = self._build_next_tetromino()

            return not self._collision_detected and self._is_running

        return self._is_running

    def _build_next_tetromino(self):
        next_tetromino = self._next_tetromino
        self._next_tetromino = Tetromino(choice(list(TetrominoType)))
        if self._spawn(next_tetromino):
            self.next_tetromino_updated.emit(self._next_tetromino)
            return False
        else:
            return True

    def _spawn(self, tetromino, pos=None):
        # https://tetris.fandom.com/wiki/Tetris_Guideline
        # (last visit 2020-03-14)
        self._current_tetromino = tetromino
        tetromino_type = tetromino.tetromio_type

        if pos:
            self._cursor = pos
        else:
            if tetromino_type == TetrominoType.I_BRICK:
                self._cursor = (-2, 4)
            elif tetromino_type == TetrominoType.J_BRICK:
                self._cursor = (-1, 4)
            elif tetromino_type == TetrominoType.L_BRICK:
                self._cursor = (-1, 4)
            elif tetromino_type == TetrominoType.O_BRICK:
                self._cursor = (-1, 4)
            elif tetromino_type == TetrominoType.S_BRICK:
                self._cursor = (-1, 4)
            elif tetromino_type == TetrominoType.T_BRICK:
                self._cursor = (-1, 4)
            elif tetromino_type == TetrominoType.Z_BRICK:
                self._cursor = (-1, 4)
            else:
                raise "UNKNOWN TETROMINO"

        self._is_dropping = False

        return self._is_possible(self._cursor, self._current_tetromino)

    def _is_possible(self, pos, tetromino):
        future_cursor_h, future_cursor_w = pos

        tetromino_h = len(tetromino.brick_matrix)
        tetromino_w = len(tetromino.brick_matrix[0])

        for h in range(tetromino_h):
            for w in range(tetromino_w):
                value = tetromino.brick_matrix[h][w]

                if value != 0:
                    if (future_cursor_h + h) not in range(self._height) or (
                        future_cursor_w + w
                    ) not in range(self._width):
                        return False

                    field_value = self._field[future_cursor_h + h][future_cursor_w + w]

                    if field_value != 0:
                        return False

        return True

    def _stamp_tetromino(self):
        self._merge_tetromino_with_field(self._field)
        self.stamped_tetromino.emit()
        self.score += self._soft_drops
        self._soft_drops = 0

    def _check_complete_lines(self):
        complete_lines = []

        for h in reversed(range(self._height - 1)):
            completed_line = True

            for w in range(1, self._width - 1):
                if self._field[h][w] == 0:
                    completed_line = False
                    break

            if completed_line:
                complete_lines.append(h)

        if len(complete_lines):
            self._remove_complete_lines(complete_lines)

    def _remove_complete_lines(self, complete_lines):
        self._update_field()
        self.main_window._pre_clear_animation(complete_lines)

        new_field = [[0] * self._width for i in range(self._height)]
        self._initialise_field(new_field)

        row_behind = 0
        for h in reversed(range(self._height - 1)):
            if h in complete_lines:
                row_behind += 1
                continue

            for w in range(1, self._width - 1):
                new_field[h + row_behind][w] = self._field[h][w]

        self._field = new_field
        calculated_score = self._line_score_base[len(complete_lines) - 1] * (
            self._level + 1
        )

        self.score += calculated_score
        self.total_removed_lines += len(complete_lines)

    @property
    def total_removed_lines(self):
        return self._total_removed_lines

    @total_removed_lines.setter
    def total_removed_lines(self, value):
        self._total_removed_lines = value
        self.lines_updated.emit(self._total_removed_lines)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        self.score_updated.emit(self._score)

    def _update_level(self):
        old_level = self._level

        self._level = self._total_removed_lines // 10

        if old_level < self._level:
            self.level_updated.emit(self._level)
            self._update_speed()

    def _update_speed(self):
        self._move_timer.setInterval(self.calculate_move_speed())

    def _merge_tetromino_with_field(self, field):
        cursor_h, cursor_w = self._cursor

        tetromino_h = len(self._current_tetromino.brick_matrix)
        tetromino_w = len(self._current_tetromino.brick_matrix[0])

        try:
            for h in range(tetromino_h):
                for w in range(tetromino_w):
                    if (cursor_h + h) in range(self._height) and (
                        cursor_w + w
                    ) in range(self._width):
                        value = self._current_tetromino.brick_matrix[h][w]
                        field_value = field[cursor_h + h][cursor_w + w]

                        if value != 0 and field_value == 0:
                            field[cursor_h + h][cursor_w + w] = value
        except Exception as e:
            print(e)


"""
    def clear_current_tetromino_from_field(self):
        for h in range(4):
            for w in range(4):
                cursor_h, cursor_w = self.cursor
                field_value = self.field[cursor_h + h][cursor_w + w]
                value = self.current_tetromino.brick_matrix[h][w]

                if value != 0 and value == field_value:
                    self.field[cursor_h + h][cursor_w + w] = 0
"""
