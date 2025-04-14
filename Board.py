from Tile import Tile

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Board(QWidget):
    def __init__(self, rows, cols):
        super().__init__()
        self.rows = rows
        self.cols = cols

        # Create Tile Board
        gridLayout = QGridLayout()
        gridLayout.setSpacing(5)
        self.boardUI = []
        for row in range(rows):
            row_tiles = []
            for col in range(cols):
                tile = Tile(0, row, col)
                tile.clicked.connect(self.tileClickHandler(tile))

                gridLayout.addWidget(tile, row, col)
                row_tiles.append(tile)
            self.boardUI.append(row_tiles)

        self.setLayout(gridLayout)

    def tileClickHandler(self, tile):
        def handler():
            if tile.tileStatus == "visible":
                return

            print(f"here {tile.row} : {tile.col}")
            tile.displayValue()
        return handler

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)


    def generateBoard(self, mines, playerLoc):
        pass
