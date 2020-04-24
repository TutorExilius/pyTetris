import functools
import time
from itertools import count
from pathlib import Path
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox
from pyTetris.game import Game


class MainWindow(QMainWindow):
    def __init__(self, field_height, field_width, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi(Path(__file__).parent / "ui" / "main_window.ui", self)

        self.default_cell_stylesheet = (
            "border: 0px; border-top: 1px solid #ccc; border-left: 1px solid #ccc;"
        )

        # Connections
        self.actionAbout_Qt.triggered.connect(self.on_about_qt)
        self.action_Controls.triggered.connect(self.on_controls_dialog)

        for h in range(field_height):
            for w in range(field_width):
                button = QPushButton()
                button.setFocusPolicy(QtCore.Qt.NoFocus)
                button.setFixedSize(20, 20)
                button.setEnabled(False)
                button.setStyleSheet(self.default_cell_stylesheet)
                self.gridLayout_field.addWidget(button, h, w)

        self.game_timer = QTimer()
        self.game_timer.setInterval(1000)
        self.game_timer.timeout.connect(self.update_game_time)

        self.tetris = None
        self.playing_time_in_seconds = 0
        self.playing_time_in_seconds = 0
        self.game_over = False
        self.timer = QTimer(self.parent())
        self.timer.timeout.connect(
            functools.partial(self.start_game, field_height, field_width, self)
        )

        self.setFixedSize(self.sizeHint())

    def closeEvent(self, event):
        self.tetris.is_running = False
        event.accept()

    def keyPressEvent(self, e):
        if not self.tetris.is_running:
            return

        self.tetris.handle_input(e.key())

    def on_about_qt(self):
        QMessageBox.aboutQt(self)

    def on_controls_dialog(self):
        QMessageBox.about(
            self,
            "Controls",
            """<table style="margin: 6px 18px 6px 12px;"><tr><td>Pause:</td><td>&nbsp;&nbsp;&nbsp;</td><td><b>P</b></td></tr>
<tr><td>Left:</td><td>&nbsp;&nbsp;&nbsp;</td><td><b>←, A</b></td></tr>
<tr><td>Right:</td><td>&nbsp;&nbsp;&nbsp;</td><td><b>→, D</b></td></tr>
<tr><td>Soft Drop:</td><td>&nbsp;&nbsp;&nbsp;</td><td><b>↓, S</b></td></tr>
<tr><td>Hard Drop:</td><td>&nbsp;&nbsp;&nbsp;</td><td><b>SPACE</b></td></tr>
<tr><td>Rotate Right:</td><td>&nbsp;&nbsp;&nbsp;</td><td><b>J</b></td></tr>
<tr><td>Rotate Left:</td><td>&nbsp;&nbsp;&nbsp;</td><td><b>K</b></td></tr></table>""",
        )

    def start_game(self, field_height, field_width, main_window):
        self.timer.stop()
        self.tetris = Game(field_height, field_width, main_window)

        self.game_timer.start()
        self.tetris.is_running = True

        while self.tetris.running():
            QApplication.processEvents()

        self.game_timer.stop()

        self.tetris.is_running = False
        self.game_over_animation()

    def game_over_animation(self):
        speed = 0.005

        # fill
        for h in reversed(range(self.tetris.height - 1)):
            if h % 2 == 1:
                _range = range(1, self.tetris.width - 1)
            else:
                _range = reversed(range(1, self.tetris.width - 1))

            for w in _range:
                button = self.gridLayout_field.itemAtPosition(h, w).widget()
                button.setStyleSheet("background-color: black;")

                time.sleep(speed)

            QApplication.processEvents()

        # empty
        for h in range(self.tetris.height - 1):
            if h % 2 == 1:
                _range = range(1, self.tetris.width - 1)
            else:
                _range = reversed(range(1, self.tetris.width - 1))

            for w in _range:
                button = self.gridLayout_field.itemAtPosition(h, w).widget()
                button.setStyleSheet(self.default_cell_stylesheet)
                time.sleep(speed)

            QApplication.processEvents()

        self.write_game_over()

    def write_game_over(self):
        font_style = (
            "font-size: 10pt; font-weight: bold; background-color: black; border: 0px;"
        )

        for row, word in zip([2, 3], ["GAME", "OVER"]):
            for column, letter in zip(count(4), word):
                rgb = "255, 255, 255"
                button = self.gridLayout_field.itemAtPosition(row, column).widget()
                button.setText(letter)
                button.setStyleSheet(f"{font_style} color: rgb({rgb});")

    def clear_pause_label(self):
        press_p = [" ", " P", "RE", "SS", "  P", " "]
        for column, letter in reversed(list(zip(count(3), press_p))):
            button = self.gridLayout_field.itemAtPosition(6, column).widget()
            button.setText("")
            button.setStyleSheet(
                f"{self.default_cell_stylesheet} background-color: white;"
            )
            time.sleep(0.015)
            QApplication.processEvents()

        for column, letter in reversed(list(zip(count(3), "PAUSED"))):
            button = self.gridLayout_field.itemAtPosition(4, column).widget()
            button.setStyleSheet(
                f"{self.default_cell_stylesheet} background-color: white;"
            )
            button.setText("")
            time.sleep(0.015)
            QApplication.processEvents()

    def write_pause(self):
        font_style = (
            "font-size: 10pt; font-weight: bold; background-color: black; border: 0px;"
        )

        for column, letter in zip(count(3), "PAUSED"):
            rgb = "255, 255, 255"
            button = self.gridLayout_field.itemAtPosition(4, column).widget()
            button.setText(letter)
            button.setStyleSheet(f"{font_style} color: rgb({rgb});")

            time.sleep(0.015)
            QApplication.processEvents()

        press_p = [" ", " P", "RE", "SS", "  P", " "]
        for column, letter in zip(count(3), press_p):
            rgb = "170, 240, 60"
            button = self.gridLayout_field.itemAtPosition(6, column).widget()
            button.setText(letter)
            button.setStyleSheet(f"{font_style} color: rgb({rgb}); font-size: 12pt;")

            time.sleep(0.015)
            QApplication.processEvents()

    def pre_clear_animation(self, rows):
        speed = 0.025 - len(rows) * (0.01 / 4.0)

        for h in rows:
            if h % 2 == 1:
                range_ = range(1, self.tetris.width - 1)
            else:
                range_ = reversed(range(1, self.tetris.width - 1))

            for w in range_:
                button = self.gridLayout_field.itemAtPosition(h, w).widget()

                if button:
                    button.setStyleSheet("background-color: black;")
                    time.sleep(speed)
                    QApplication.processEvents()

    def update_game_time(self):
        self.playing_time_in_seconds += 1
        self.ui_update_game_time()

    def ui_update_game_time(self):
        minutes = self.playing_time_in_seconds // 60
        seconds = self.playing_time_in_seconds % 60
        self.label_game_time.setText("Time: {:02d}:{:02d}".format(minutes, seconds))

    def on_next_tetromino_update(self, tetromino):
        self.initialise_next_tetromino_grid(tetromino)

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

    def initialise_next_tetromino_grid(self, tetromino):
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
