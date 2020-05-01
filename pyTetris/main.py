import sys
from PyQt5.QtWidgets import QApplication
from pyTetris.main_window import MainWindow


def main():
    app = QApplication([])

    main_window = MainWindow(23, 12)
    main_window.start_new_game_timer.start()
    main_window.show()

    sys.exit(app.exec_() or 0)


if __name__ == "__main__":
    main()
