import sys

from Board import Board

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Minesweeper(QWidget):
    gameDifficulties = { "Beginner": ((9, 9), 10), "Intermediate": ((16, 16), 40), "Expert": ((16, 30), 99), "Custom": ((12, 12), 2)}
    maxCustomBoardSize = 25

    def __init__(self):
        super(Minesweeper, self).__init__()

        menu = self.difficultyMenu()
        customSettingsMenu = self.customMenu()
        gameText = self.gameText()

        self.setFixedSize(2000, 1800)
        self.setStyleSheet("background-color: #1e272e;")

        self.board = None
        self.boardLayout = QHBoxLayout()
        self.boardLayout.addStretch()
        self.boardLayout.addStretch()

        self.startGame(self.gameDifficulties["Beginner"], self.beginnerButton)

        vertLayout = QVBoxLayout()
        vertLayout.addStretch()
        vertLayout.addLayout(menu)
        vertLayout.addLayout(customSettingsMenu)
        vertLayout.addLayout(self.boardLayout)
        vertLayout.addLayout(gameText)
        vertLayout.addStretch()

        self.setLayout(vertLayout)

        self.show()

    def difficultyMenu(self):
        self.defaultButtonStyle = "font-size: 25px; padding: 10px; color: #4c6490; letter-spacing: 1.5px; font-weight: normal"
        self.activeButtonStyle = "font-size: 25px; padding: 10px; color: #bfc7ca; letter-spacing: 1.5px; font-weight: bold"

        self.beginnerButton = QPushButton("Beginner")
        self.beginnerButton.setStyleSheet(self.defaultButtonStyle)
        self.beginnerButton.adjustSize()
        self.beginnerButton.clicked.connect(lambda _, diff="Beginner": self.startGame(self.gameDifficulties[diff], self.beginnerButton))

        self.intermediateButton = QPushButton("Intermediate")
        self.intermediateButton.setStyleSheet(self.defaultButtonStyle)
        self.intermediateButton.adjustSize()
        self.intermediateButton.clicked.connect(lambda _, diff="Intermediate": self.startGame(self.gameDifficulties[diff], self.intermediateButton))

        self.expertButton = QPushButton("Expert")
        self.expertButton.setStyleSheet(self.defaultButtonStyle)
        self.expertButton.adjustSize()
        self.expertButton.clicked.connect(lambda _, diff="Expert": self.startGame(self.gameDifficulties[diff], self.expertButton))

        self.customButton = QPushButton("Custom")
        self.customButton.setStyleSheet(self.defaultButtonStyle)
        self.customButton.adjustSize()
        self.customButton.clicked.connect(self.openCustomSettings)

        horiLayout = QHBoxLayout()
        horiLayout.addStretch()
        horiLayout.addWidget(self.beginnerButton)
        horiLayout.addWidget(self.intermediateButton)
        horiLayout.addWidget(self.expertButton)
        horiLayout.addWidget(self.customButton)
        horiLayout.addStretch()
        return horiLayout

    def customMenu(self):
        inputStyle = "QLineEdit { max-width: 100px; height: 40px; align-items: center; padding: 0px 10px; color: #bfc7ca; font-size: 25px}"

        rowLabel = QLabel("Rows:")
        rowLabel.setStyleSheet(self.activeButtonStyle)

        columnLabel = QLabel("Columns:")
        columnLabel.setStyleSheet(self.activeButtonStyle)

        mineLabel = QLabel("Mines:")
        mineLabel.setStyleSheet(self.activeButtonStyle)

        sizeRange = QIntValidator(1, self.maxCustomBoardSize)

        (row, col), mines = self.gameDifficulties["Custom"]

        self.rowInput = QLineEdit()
        self.rowInput.setText(str(row))
        self.rowInput.setValidator(sizeRange)
        self.rowInput.setStyleSheet(inputStyle)

        self.columnInput = QLineEdit()
        self.columnInput.setText(str(col))
        self.columnInput.setValidator(sizeRange)
        self.columnInput.setStyleSheet(inputStyle)

        self.mineInput = QLineEdit()
        self.mineInput.setText(str(mines))
        self.mineInput.setValidator(QIntValidator())
        self.mineInput.setStyleSheet(inputStyle)

        self.updateCustomButton = QPushButton("Update")
        self.updateCustomButton.setStyleSheet(self.activeButtonStyle)
        self.updateCustomButton.adjustSize()
        self.updateCustomButton.clicked.connect(self.createCustomBoard)

        self.customSettingWidget = QWidget()
        horiLayout = QHBoxLayout()
        horiLayout.addStretch()
        horiLayout.addWidget(rowLabel)
        horiLayout.addWidget(self.rowInput)
        horiLayout.addWidget(columnLabel)
        horiLayout.addWidget(self.columnInput)
        horiLayout.addWidget(mineLabel)
        horiLayout.addWidget(self.mineInput)
        horiLayout.addSpacerItem(QSpacerItem(25, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        horiLayout.addWidget(self.updateCustomButton)
        horiLayout.addStretch()
        horiLayout.setContentsMargins(0, 10, 0, 10)
        self.customSettingWidget.setLayout(horiLayout)

        menuLayout = QHBoxLayout()
        menuLayout.addStretch()
        menuLayout.addWidget(self.customSettingWidget)
        menuLayout.addStretch()

        return menuLayout

    def gameText(self):
        self.endgameLabel = QLabel("")
        self.endgameLabel.setStyleSheet(self.activeButtonStyle)
        self.endgameLabel.adjustSize()

        displayLayout = QHBoxLayout()
        displayLayout.addStretch()
        displayLayout.addWidget(self.endgameLabel)
        displayLayout.addStretch()

        return displayLayout

    def openCustomSettings(self):
        self.startGame(self.gameDifficulties["Custom"], self.customButton)
        self.customSettingWidget.setVisible(True)

    def createCustomBoard(self):
        row, col = int(self.rowInput.text()), int(self.columnInput.text())
        mines = int(self.mineInput.text())
        if mines > row * col:
            mines = row * col - 1
            self.mineInput.setText(str(mines))
        self.startGame(((row, col), mines), self.customButton)
        self.customSettingWidget.setVisible(True)

    def startGame(self, difficulty, difficultyButton):
        self.beginnerButton.setStyleSheet(self.defaultButtonStyle)
        self.intermediateButton.setStyleSheet(self.defaultButtonStyle)
        self.expertButton.setStyleSheet(self.defaultButtonStyle)
        self.customButton.setStyleSheet(self.defaultButtonStyle)

        difficultyButton.setStyleSheet(self.activeButtonStyle)

        boardSize, mines = difficulty

        # Create Board
        if self.board is not None:
            self.board.setParent(None)
            self.board.deleteLater()
            self.board = None

        self.board = Board(boardSize[0], boardSize[1], mines, self.endgameLabel)
        self.boardLayout.insertWidget(1, self.board)

        # Custom Board Settings
        self.customSettingWidget.setVisible(False)

        # Reset Game Text
        self.endgameLabel.setText("")

if __name__ == "__main__":
    app = QApplication([])

    minesweeper = Minesweeper()

    sys.exit(app.exec_())