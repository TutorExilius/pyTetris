import functools
import time
from itertools import count
from pathlib import Path
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox
from pyTetris.tetris import Field, cls, Action


class MainWindow(QMainWindow):
    soft_dropped = pyqtSignal()

    def __init__(self, field_height, field_width, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi(Path(__file__).parent / "ui" / "main_window.ui", self)

        self.default_cell_stylesheet = (
            "border: 0px; border-top: 1px solid #ccc; border-left: 1px solid #ccc;"
        )

        # Connections
        self.actionAbout_Qt.triggered.connect(self._on_about_qt)

        for h in range(field_height):
            for w in range(field_width):
                button = QPushButton()
                button.setFocusPolicy(QtCore.Qt.NoFocus)
                button.setFixedSize(20, 20)
                button.setEnabled(False)
                self.gridLayout_field.addWidget(button, h, w)

        self._playing_time_in_seconds = 0
        self._playing_time_in_seconds = 0
        self._pause = False
        self._game_over = False
        self.timer = QTimer(self.parent())
        self.timer.timeout.connect(
            functools.partial(self._start_game, field_height, field_width, self)
        )

        self.setFixedSize(self.sizeHint())

        self.keyPressEvent = self.keyPressEvent

    def closeEvent(self, event):
        self._field._is_running = False
        event.accept()

    def keyPressEvent(self, e):
        if self._game_over:
            return

        if not self._field._is_dropping:
            if (
                e.key() == QtCore.Qt.Key_Left or e.key() == QtCore.Qt.Key_A
            ) and not self._pause:
                self._move_left()
            elif (
                e.key() == QtCore.Qt.Key_Right or e.key() == QtCore.Qt.Key_D
            ) and not self._pause:
                self._move_right()
            elif (
                e.key() == QtCore.Qt.Key_Down or e.key() == QtCore.Qt.Key_S
            ) and not self._pause:
                self._move_down()
                self.soft_dropped.emit()
            elif e.key() == QtCore.Qt.Key_X and not self._pause:
                self._rotate_clockwise()
            elif e.key() == QtCore.Qt.Key_Y and not self._pause:
                self._rotate_counterclockwise()
            elif e.key() == QtCore.Qt.Key_Space and not self._pause:
                self._drop()
            elif e.key() == QtCore.Qt.Key_P:
                self._pause_game()

    def _on_about_qt(self):
        QMessageBox.aboutQt(self)

    def _start_game(self, field_height, field_width, main_window):
        self.timer.stop()
        self._field = Field(field_height, field_width, main_window)

        game_timer = QTimer()
        game_timer.setInterval(1000)
        game_timer.timeout.connect(self._update_game_time)
        game_timer.start()

        while self._field.running():
            if not self._pause:
                print(self._field)
                if not game_timer.isActive():
                    game_timer.start()
            else:
                game_timer.stop()

            QApplication.processEvents()

        game_timer.stop()
        self._game_over = True
        self._game_over_animation()

        cls()
        print("Game over")

    def _pause_game(self):
        self._pause = not self._pause
        self._field.pause_game(self._pause)

        if self._pause:
            self._write_pause()
        else:
            self._clear_pause_label()

    def _move_left(self):
        self._field._move(Action.LEFT)

    def _move_right(self):
        self._field._move(Action.RIGHT)

    def _move_down(self):
        self._field._move_timer.stop()
        self._field._move(Action.DOWN)
        self._field._move_timer.setInterval(self._field.calculate_move_speed())
        self._field._move_timer.start()

    def _drop(self):
        self._field._move_timer.stop()
        self._field._move(Action.DROP)
        self._field._move_timer.setInterval(self._field.calculate_move_speed())
        self._field._move_timer.start()

    def _game_over_animation(self):
        speed = 0.005

        # fill
        for h in reversed(range(self._field._height - 1)):
            if h % 2 == 1:
                _range = range(1, self._field._width - 1)
            else:
                _range = reversed(range(1, self._field._width - 1))

            for w in _range:
                button = self.gridLayout_field.itemAtPosition(h, w).widget()
                button.setStyleSheet("background-color: black;")

                time.sleep(speed)

            QApplication.processEvents()

        # empty
        for h in range(self._field._height - 1):
            if h % 2 == 1:
                _range = range(1, self._field._width - 1)
            else:
                _range = reversed(range(1, self._field._width - 1))

            for w in _range:
                button = self.gridLayout_field.itemAtPosition(h, w).widget()
                button.setStyleSheet(self.default_cell_stylesheet)
                time.sleep(speed)

            QApplication.processEvents()

        self._write_game_over()

    def _write_game_over(self):
        font_style = (
            "font-size: 10pt; font-weight: bold; background-color: black; border: 0px;"
        )

        for row, word in zip([3, 4], ["GAME", "OVER"]):
            for column, letter in zip(count(4), word):
                # ranges = [(25, 220), (50, 180), (25, 220)]
                # rgb = ", ".join(str(random.randint(min, max)) for min, max in ranges)
                rgb = "255, 255, 255"
                button = self.gridLayout_field.itemAtPosition(row, column).widget()
                button.setText(letter)
                button.setStyleSheet(f"{font_style} color: rgb({rgb});")

                # effect = QGraphicsDropShadowEffect()
                # effect.setBlurRadius(3)
                # effect.setColor(QColor.fromRgb(127, 127, 127))
                # button.setGraphicsEffect(effect)

                # time.sleep(0.035)
                # QApplication.processEvents()

    def _clear_pause_label(self):
        for column, letter in reversed(list(zip(count(3), "PAUSED"))):
            button = self.gridLayout_field.itemAtPosition(4, column).widget()
            button.setStyleSheet(
                f"{self.default_cell_stylesheet} background-color: white;"
            )
            button.setText("")
            time.sleep(0.015)
            QApplication.processEvents()

    def _write_pause(self):
        font_style = (
            "font-size: 10pt; font-weight: bold; background-color: black; border: 0px;"
        )

        for column, letter in zip(count(3), "PAUSED"):
            rgb = "255, 255, 255"
            button = self.gridLayout_field.itemAtPosition(4, column).widget()
            button.setText(letter)
            button.setStyleSheet(f"{font_style} color: rgb({rgb});")

            # effect = QGraphicsDropShadowEffect()
            # effect.setBlurRadius(3)
            # effect.setColor(QColor.fromRgb(127, 127, 127))
            # button.setGraphicsEffect(effect)

            time.sleep(0.015)
            QApplication.processEvents()

    def _pre_clear_animation(self, rows):
        speed = 0.025 - len(rows) * (0.01 / 4.0)

        for h in rows:
            if h % 2 == 1:
                _range = range(1, self._field._width - 1)
            else:
                _range = reversed(range(1, self._field._width - 1))

            for w in _range:
                button = self.gridLayout_field.itemAtPosition(h, w).widget()

                if button:
                    button.setStyleSheet("background-color: black;")
                    time.sleep(speed)
                    QApplication.processEvents()

    def _rotate_clockwise(self):
        self._field.rotate_clockwise_tetromino()

    def _rotate_counterclockwise(self):
        self._field.rotate_counter_clockwise_tetromino()

    def _update_game_time(self):
        self._playing_time_in_seconds += 1
        self._ui_update_game_time()

    def _ui_update_game_time(self):
        minutes = self._playing_time_in_seconds // 60
        seconds = self._playing_time_in_seconds % 60
        self.label_game_time.setText("Time: {:02d}:{:02d}".format(minutes, seconds))

    def on_next_tetromino_update(self, tetromino):
        self._initialise_next_tetromino_grid(tetromino)

        for h, line in enumerate(tetromino.brick_matrix):
            for w, cell in enumerate(line):
                try:
                    button = self.gridLayout_next_tetromino.itemAtPosition(
                        h, w
                    ).widget()

                    self.update_button(button, cell, False)
                except Exception as e:
                    print(e)

    def on_field_update(self, field):
        for h, rows in enumerate(field):
            for w, cell in enumerate(rows):
                # if cell == -1 or cell == -2:
                #     continue

                try:
                    button = self.gridLayout_field.itemAtPosition(h, w).widget()

                    self.update_button(button, cell)
                except Exception as e:
                    print(e)

    def on_score_update(self, value):
        self.label_score_value.setText(str(value))

    def on_level_update(self, value):
        self.label_lvl_value.setText(str(value))

    def on_lines_update(self, value):
        self.label_lines_value.setText(str(value))

    def _initialise_next_tetromino_grid(self, tetromino):
        # the widget is deleted when its parent is deleted.
        # Important note: You need to loop backwards because removing
        # things from the beginning shifts items and changes the order of items in the layout.
        while self.gridLayout_next_tetromino.count():
            button = self.gridLayout_next_tetromino.takeAt(0).widget()
            self.gridLayout_next_tetromino.removeWidget(button)
            button.setParent(None)
            button.deleteLater()

        tetromino_h = len(tetromino.brick_matrix)
        tetromino_w = len(tetromino.brick_matrix[0])

        for h in range(tetromino_h):
            for w in range(tetromino_w):
                button = QPushButton()
                button.setFocusPolicy(QtCore.Qt.NoFocus)
                button.setFixedSize(17, 17)
                button.setEnabled(True)
                button.setStyleSheet("border: 0px;")
                self.gridLayout_next_tetromino.addWidget(button, h, w)

        self.frame_next_tetromino.setStyleSheet("border: 3px double black;")

    def update_button(self, button, cell_value, draw_frame=True):
        stylesheet = []

        if cell_value > 0:
            stylesheet.append("border: 0px")
        elif cell_value == 0:
            if draw_frame:
                stylesheet.append(self.default_cell_stylesheet)
            else:
                stylesheet.append("border: 0px")

        if cell_value == -2:
            stylesheet.append("background-color: black")
        if cell_value == -1:
            stylesheet.append("background-color: black")
        if cell_value == 0:
            stylesheet.append("background-color: white")
        if cell_value == 1:
            stylesheet.append(
                "background-color: qlineargradient( x1:0 y1:0, x2:1 y2:1, stop:0 red, stop:1 #750000)"
            )
        elif cell_value == 2:
            stylesheet.append(
                "background-color: qlineargradient( x1:0 y1:0, x2:1 y2:1, stop:0 orange, stop:1 #755500)"
            )
        elif cell_value == 3:
            stylesheet.append(
                "background-color: qlineargradient( x1:0 y1:0, x2:1 y2:1, stop:0 #5555ff, stop:1 #222285)"
            )
        elif cell_value == 4:
            stylesheet.append("background-color: green")
            stylesheet.append(
                "background-color: qlineargradient( x1:0 y1:0, x2:1 y2:1, stop:0 #55ff55, stop:1 #228522)"
            )
        elif cell_value == 5:
            stylesheet.append(
                "background-color: qlineargradient( x1:0 y1:0, x2:1 y2:1, stop:0 magenta, stop:1 #750075)"
            )
        elif cell_value == 6:
            stylesheet.append(
                "background-color: qlineargradient( x1:0 y1:0, x2:1 y2:1, stop:0 yellow, stop:1 #757500)"
            )
        elif cell_value == 7:
            stylesheet.append(
                "background-color: qlineargradient( x1:0 y1:0, x2:1 y2:1, stop:0 #00b6be, stop:1 #006d84)"
            )

        button.setStyleSheet("; ".join(stylesheet))

    # def _reset_gridLayout_next_tetromino(self):
    #     for i in range(self.gridLayout_field.count()):
    #         button = self.gridLayout_field.itemAt(i).widget()
    #         button.setStyleSheet("")
