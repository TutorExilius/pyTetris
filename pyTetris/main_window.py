import functools
import time
from itertools import count
from pathlib import Path
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QTimer, QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QSound
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox
from pyTetris.game import Game
import webbrowser


class MainWindow(QMainWindow):
    game_over_signal = pyqtSignal()

    def __init__(self, field_height, field_width, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi(Path(__file__).parent / "ui" / "main_window.ui", self)

        # load background image
        background_image = str(Path(__file__).parent / "ui" / "tetris_backgroung_1.png")
        bg_style = "#centralwidget{ background-color: white; " + f"background-image: url('{background_image}');" + "}"

        # CSS path requires /
        bg_style = bg_style.replace("\\", "/")

        # set background-image
        self.setStyleSheet(bg_style)

        self.default_cell_stylesheet = (
            f"border: 0px; border-top: 1px solid #ccc; border-left: 1px solid #ccc;"
        )

        # Connections
        self.actionAbout_Qt.triggered.connect(self.on_about_qt)
        self.action_Controls.triggered.connect(self.on_controls_dialog)
        self.action_About_pyTetris.triggered.connect(self.on_about_py_tetris)
        self.action_Support_Tutor_Exilius.triggered.connect(self.open_twitch_support_page)

        for h in range(2, field_height):
            for w in range(field_width):
                button = QPushButton()
                button.setFocusPolicy(QtCore.Qt.NoFocus)
                button.setFixedSize(20, 20)
                button.setEnabled(False)
                button.setStyleSheet(self.default_cell_stylesheet)
                self.gridLayout_field.addWidget(button, h, w)

        # TODO: implement setting/options: start with users startlevel
        self.users_start_level = 0

        self.rounds = 0
        self.key_input_lock = False

        self.is_game_over = False
        self.game_timer = QTimer()
        self.game_timer.setInterval(1000)
        self.game_timer.timeout.connect(self.update_game_time)
        self.tetris = None
        self.playing_time_in_seconds = 0
        self.playing_time_in_seconds = 0
        self.start_new_game_timer = QTimer(self.parent())
        self.start_new_game_timer.timeout.connect(
            functools.partial(self.start_game, field_height, field_width, self)
        )

        self.setFixedSize(self.sizeHint())

        # Media Player - to play bye.wav synchronously
        self.player = QMediaPlayer()
        self.player.setVolume(100)
        self.sound_bye = str(Path(__file__).parent / "sounds" / "bye.wav")

    def closeEvent(self, event):
        self.tetris.is_running = False

        # small hack :)
        # DO FIRST: link next close event to self.force_closeEvent(..)
        self.closeEvent = self.force_closeEvent

        # end of playing 'self.sound_bye' will occure next close()
        # --> self.force_closeEvent(..) will be called
        self.player.stateChanged.connect(self.on_bye_played)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.sound_bye)))
        self.player.play()

        event.ignore()

    def open_twitch_support_page(self):
        donate_sound = str(Path(__file__).parent / "sounds" / "donate.wav")
        QSound.play(donate_sound)
        webbrowser.open("https://streamlabs.com/tutorexilius")

    def on_bye_played(self, state):
        if state == QMediaPlayer.StoppedState:
            self.close()

    def force_closeEvent(self, event):
        self.tetris = None
        event.accept()

    def keyPressEvent(self, e):
        if self.key_input_lock:
            return

        self.key_input_lock = True

        # START NEW GAME
        if not self.tetris.is_running:
            if self.is_game_over and e.key() == QtCore.Qt.Key_N:
                self.start_new_game_timer.start()
        else:
            self.tetris.handle_input(e.key())

        self.key_input_lock = False

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

    def on_about_py_tetris(self):
        QMessageBox.about(
            self,
            "About pyTetris 2020",
            """<table style="margin: 6px 18px 6px 12px;">
<tr><td><b>Developer&nbsp;&nbsp;&nbsp;&nbsp;</b></td><td>Tutor Exilius</td><tr>
<tr><td>Source-Code:&nbsp;&nbsp;&nbsp;&nbsp;</td><td>https://github.com/tutorexilius/pyTetris<br>
<tr><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td>https://www.exilius.de<br>
https://www.tutorexilius.de<br>
https://www.twitch.tv/tutorexilius</td></tr>
<tr><td colspan=2></td></tr>
<tr><td><b>Music&nbsp;&nbsp;&nbsp;&nbsp;<br></td><td>Bogozi - Tetris_theme</td></tr>
<tr><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td>Bogozi/CC BY-SA<br>https://creativecommons.org/licenses/by-sa/3.0</td></tr>
<tr><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td>https://commons.wikimedia.org/wiki/File:Tetris_theme.ogg</td></tr></table>""",
        )

    def reset_states(self):
        self.is_game_over = False
        self.playing_time_in_seconds = 0
        self.ui_update_game_time()
        self.on_level_update(0)
        self.on_score_update(0)
        self.on_lines_update(0)
        self.clear_game_over_label()
        self.clear_press_n_label()
        self.start_new_game_timer.stop()

    def start_game(self, field_height, field_width, main_window):
        self.rounds += 1
        self.reset_states()

        self.on_level_update(self.users_start_level)
        self.tetris = Game(field_height, field_width, main_window, self.users_start_level)

        self.game_over_signal.connect(self.tetris.on_game_over)

        self.game_timer.start()
        self.tetris.is_running = True
        self.tetris.player.play()

        while self.tetris.running():
            QApplication.processEvents()

        self.tetris.player.stop()
        self.game_timer.stop()

        # fix: avoid gameover animation, if window is closed by user
        if self.closeEvent != self.force_closeEvent:
            self.game_over_signal.emit()
            self.game_over_animation()
            self.write_press_n()
            self.is_game_over = True

    def game_over_animation(self):
        speed = 0.005

        # fill
        for h in reversed(range(2, self.tetris.height - 1)):
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
        for h in range(2, self.tetris.height - 1):
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

        for row, word in zip([4, 5], ["GAME", "OVER"]):
            for column, letter in zip(count(4), word):
                rgb = "255, 255, 255"
                button = self.gridLayout_field.itemAtPosition(row, column).widget()
                button.setText(letter)
                button.setStyleSheet(f"{font_style} color: rgb({rgb});")

    def clear_game_over_label(self):
        for row, word in zip([4, 5], ["GAME", "OVER"]):
            for column, letter in zip(count(4), word):
                button = self.gridLayout_field.itemAtPosition(row, column).widget()
                button.setText("")
                button.setStyleSheet(
                    f"{self.default_cell_stylesheet} background-color: white;"
                )

    def clear_pause_label(self):
        press_p = [" ", " P", "RE", "SS", "  P", " "]
        for column, letter in reversed(list(zip(count(3), press_p))):
            button = self.gridLayout_field.itemAtPosition(7, column).widget()
            button.setText("")
            button.setStyleSheet(
                f"{self.default_cell_stylesheet} background-color: white;"
            )
            time.sleep(0.015)
            QApplication.processEvents()

        for column, letter in reversed(list(zip(count(3), "PAUSED"))):
            button = self.gridLayout_field.itemAtPosition(5, column).widget()
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
            button = self.gridLayout_field.itemAtPosition(5, column).widget()
            button.setText(letter)
            button.setStyleSheet(f"{font_style} color: rgb({rgb});")

            time.sleep(0.015)
            QApplication.processEvents()

        press_p = [" ", " P", "RE", "SS", "  P", " "]
        for column, letter in zip(count(3), press_p):
            rgb = "170, 240, 60"
            button = self.gridLayout_field.itemAtPosition(7, column).widget()
            button.setText(letter)
            button.setStyleSheet(f"{font_style} color: rgb({rgb}); font-size: 12pt;")

            time.sleep(0.015)
            QApplication.processEvents()

    def clear_press_n_label(self):
        press_p = [" ", " P", "RE", "SS", "  N", " "]
        for column, letter in reversed(list(zip(count(3), press_p))):
            button = self.gridLayout_field.itemAtPosition(7, column).widget()
            button.setText("")
            button.setStyleSheet(
                f"{self.default_cell_stylesheet} background-color: white;"
            )
            time.sleep(0.015)
            QApplication.processEvents()

    def write_press_n(self):
        font_style = (
            "font-size: 10pt; font-weight: bold; background-color: black; border: 0px;"
        )

        press_p = [" ", " P", "RE", "SS", "  N", " "]
        for column, letter in zip(count(3), press_p):
            rgb = "170, 240, 60"
            button = self.gridLayout_field.itemAtPosition(7, column).widget()
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
                try:
                    item = self.gridLayout_field.itemAtPosition(h, w)
                    if item is not None:
                        button = item.widget()
                        if button is not None:
                            self.update_button(button, cell)
                except Exception as e:
                    print("here:", e)

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

        self.frame_next_tetromino.setStyleSheet("background-color: white; border: 3px double black;")

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
