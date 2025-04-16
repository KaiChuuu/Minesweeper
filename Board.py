import random
from collections import deque

from Tile import Tile

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Board(QWidget):
    directions = [(0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1)]

    def __init__(self, rows, cols, mines, endgameLabel):
        super().__init__()
        self.rows = rows
        self.cols = cols

        self.firstClick = True
        self.activeBoard = True
        self.availableMoves = rows * cols - mines
        self.mines = mines

        self.endgameLabel = endgameLabel

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
            if tile.tileStatus == "visible" or not self.activeBoard:
                return

            if self.firstClick:
                self.firstClick = False
                self.generateBoard(tile)

            # print(f"clicked tile, {tile.row} : {tile.col}")

            if tile.tileType == "number" and tile.number == 0:
                self.floodFill(tile)
                return

            if tile.tileType == "mine":
                # end game
                self.activeBoard = False
                self.displayMines()
                self.endgameLabel.setText("GAME OVER!")
                print("game over")
                return

            self.availableMoves -= 1
            self.checkAvailableMoves()
            tile.displayValue()

        return handler

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

    def floodFill(self, clickedTile):
        queue = deque()
        queue.append(clickedTile)

        while queue:
            currTile = queue.popleft()

            if currTile.tileStatus == "visible":
                continue

            self.availableMoves -= 1
            currTile.displayValue()

            if currTile.number == 0:
                for dirRow, dirCol in self.directions:
                    newRow = currTile.row + dirRow
                    newCol = currTile.col + dirCol
                    if (0 <= newRow < self.rows and 0 <= newCol < self.cols
                        and self.boardUI[newRow][newCol].tileStatus == "hidden"):
                        queue.append(self.boardUI[newRow][newCol])

        self.checkAvailableMoves()


    def generateBoard(self, playerTile):
        locations = [(r, c) for r in range(self.rows) for c in range(self.cols)]

        playerLoc = (playerTile.row, playerTile.col)
        locations.remove(playerLoc)

        self.mineLoc = random.sample(locations, self.mines)

        for row, col in self.mineLoc:
            self.boardUI[row][col].tileType = "mine"

            for dirRow, dirCol in self.directions:
                curRow = row + dirRow
                curCol = col + dirCol
                if 0 <= curRow < self.rows and 0 <= curCol < self.cols:
                    self.boardUI[curRow][curCol].number += 1

    def checkAvailableMoves(self):
        if self.availableMoves == 0:
            self.activeBoard = False
            self.displayMines()
            self.endgameLabel.setText("YOU WIN!")
            print("you win!")

    def displayMines(self):
        for row, col in self.mineLoc:
            self.boardUI[row][col].displayValue()