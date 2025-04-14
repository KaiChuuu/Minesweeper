import sys

from Board import Board

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Minesweeper(QWidget):
    def __init__(self):
        super(Minesweeper, self).__init__()

        self.setFixedSize(2000, 1800)
        self.setStyleSheet("background-color: #1e272e;")
        self.board = Board(20, 20)


        horiLayout = QHBoxLayout()
        horiLayout.addStretch()
        horiLayout.addWidget(self.board)
        horiLayout.addStretch()

        vertLayout = QVBoxLayout()
        vertLayout.addStretch()
        vertLayout.addLayout(horiLayout)
        vertLayout.addStretch()

        self.setLayout(vertLayout)

        self.show()

    def paintEvent(self, event):
        pass

    def startGame(self):
        pass

    def endGame(self):
        pass

if __name__ == "__main__":
    app = QApplication([])

    minesweeper = Minesweeper()

    sys.exit(app.exec_())