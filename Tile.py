import math

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Tile(QPushButton):
    tileColor = { 0: "empty", 1: "#191a1c", 2: "#6ac06b", 3: "#fe7c96", 4: "#a172b6", 5: "#e1b43e", 6: "#6fc9cf", 7: "#989a9c", 8: "#cdd6dd"}
    tileSize = 50

    def __init__(self, tileNumber, row, col):
        super().__init__(None)
        self.tileStatus = "hidden"
        self.tileType = "number"
        self.isFlagged = False
        self.number = tileNumber
        self.row = row
        self.col = col
        self.setFixedSize(self.tileSize, self.tileSize)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Default Blank Tile
        if self.tileStatus != "visible":
            # White layer
            painter.setBrush(QColor("#6c757c"))
            painter.drawRect(0, 0, self.tileSize, self.tileSize)

            # Dark layer
            painter.setBrush(QColor('#222b32'))
            painter.drawRect(5, 6, self.tileSize, self.tileSize)

            # Center Grey layer
            painter.setBrush(QColor("#4c555c"))
            painter.drawRect(5, 5, self.tileSize - 10, self.tileSize - 11)

            if self.isFlagged:
                self.drawFlag(painter)
            return

        # Visible Tile
        painter.setBrush(QColor("#384148"))
        painter.drawRect(0, 0, self.tileSize, self.tileSize)

        if self.tileType == "number":
            # Number
            if self.number != 0:
                painter.setFont(QFont('Consolas', self.tileSize // 2, QFont.Bold))
                painter.setPen(QColor(self.tileColor[self.number]))
                painter.drawText(self.rect(), Qt.AlignCenter, str(self.number))

        elif self.tileType == "mine":
            self.drawMine(painter)

    def drawMine(self, painter):
        cx = self.tileSize / 2
        cy = self.tileSize / 2
        center = QPointF(cx, cy)
        radius = self.tileSize * 0.225  # Adjust Mine Center Size

        # Center Circle
        painter.setBrush(QColor("#030000"))
        painter.drawEllipse(center, radius, radius)

        # Spikes
        spikeLen = self.tileSize * 0.3  # Adjust Spike Length
        painter.setPen(QPen(QColor("#030000"), 3))  # Adjust Spike Width
        for angleDeg in range(0, 360, 45):
            angleRad = math.radians(angleDeg)
            dx = math.cos(angleRad) * spikeLen
            dy = math.sin(angleRad) * spikeLen

            endPoint = QPointF(cx + dx, cy + dy)
            painter.drawLine(center, endPoint)

        # Shiny Highlight
        highlightRadius = radius * 0.55  # Adjust Shine Size
        highlightOffset = radius * 0.2  # Offset from center
        highlightCenter = QPointF(cx - highlightOffset, cy - highlightOffset)

        # Outer Gradient on Highlight
        gradient = QRadialGradient(highlightCenter, highlightRadius)
        gradient.setColorAt(0, QColor(255, 255, 255, 180))  # Center Color
        gradient.setColorAt(1, QColor(255, 255, 255, 50))  # Edge Color

        painter.setBrush(gradient)
        painter.drawEllipse(highlightCenter, highlightRadius, highlightRadius)

    def drawFlag(self, painter):
        cx = self.tileSize / 2
        cy = self.tileSize / 2

        poleHeight = self.tileSize * 0.3
        poleWidth = 4
        poleTop = QPointF(cx, cy - poleHeight / 1.75)
        poleBottom = QPointF(cx, cy + poleHeight / 1.5)

        # Pole
        painter.setPen(QPen(QColor("#d6dfe6"), poleWidth))
        painter.drawLine(poleTop, poleBottom)

        # Pole Base
        baseWidth = self.tileSize * 0.4
        painter.drawLine(QPointF(cx - baseWidth / 2, poleBottom.y()),
                         QPointF(cx + baseWidth / 2, poleBottom.y()))

        # Flag
        flagHeight = self.tileSize * 0.3
        flagLength=  self.tileSize * 0.25

        flagTop = QPointF(cx + poleWidth / 2, cy - flagHeight)
        flagMid = QPointF(cx + poleWidth / 2, cy)
        flagTip = QPointF(cx - flagLength, cy - flagHeight / 2)

        triangle = QPolygonF([flagTop, flagMid, flagTip])

        # Flag Gradient
        gradient = QLinearGradient(flagTip, flagMid)
        gradient.setColorAt(0, QColor("#f96b6e"))
        gradient.setColorAt(1, QColor("#f3504e"))

        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(triangle)

    def mousePressEvent(self, event):
        # Handle Right Click
        if event.button() == Qt.MouseButton.RightButton:
            if self.tileStatus == "visible":
                return

            if not self.isFlagged:
                self.isFlagged = True
            else:
                self.isFlagged = False
            self.update()
        # Handle Left Click
        elif event.button() == Qt.MouseButton.LeftButton:
            super().mousePressEvent(event)

    def displayValue(self):
        self.tileStatus = "visible"
        self.update()