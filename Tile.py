from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Tile(QPushButton):
    tileStatus = "hidden"
    tileColor = { 0: "empty", 1: "#191a1c", 2: "#6ac06b", 3: "#fe7c96", 4: "#a172b6"}
    tileSize = 50

    def __init__(self, tileNumber, row, col):
        super().__init__(None)
        self.number = tileNumber
        self.row = row
        self.col = col
        self.numberColor = self.tileColor[tileNumber]
        self.setFixedSize(self.tileSize, self.tileSize)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Square
        if self.tileStatus == "visible":
            # Number
            painter.setBrush(QColor("#384148"))
            painter.drawRect(0, 0, self.tileSize, self.tileSize)

            painter.setFont(QFont('Consolas', self.tileSize // 2, QFont.Bold))
            painter.setPen(QColor(self.numberColor))
            painter.drawText(self.rect(), Qt.AlignCenter, str(self.number))
        # Default Blank Tile
        else:
            # White layer
            painter.setBrush(QColor("#6c757c"))
            painter.drawRect(0, 0, self.tileSize, self.tileSize)

            # Dark layer
            painter.setBrush(QColor('#222b32'))
            painter.drawRect(5, 6, self.tileSize, self.tileSize)

            # Center Grey layer
            painter.setBrush(QColor("#4c555c"))
            painter.drawRect(5, 5, self.tileSize - 10, self.tileSize - 11)


    def displayValue(self):
        self.tileStatus = "visible"
        self.update()