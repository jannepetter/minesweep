import sys
from datetime import datetime
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QRadioButton,
    QHBoxLayout,
)
import functions


state = {
    "field": [],  # minefield info
    "showField": [],  # revealed minefield info
    "fieldButtons": [],
    "mineFieldWidget": None,
    "scoreWidget": None,  # scores window
    "statsWidget": None,  # stats window
    "scoreForm": None,  # input form for new highscore
    "difficulty": {
        "easy": [5, 5, 10],  # width, height, mines
        "normal": [10, 10, 30],
        "hard": [15, 20, 50],
    },
    "mineInfo": 10,  # show how many mines in the field, start with easy
    "difficultyInfo": "easy",  # start default as easy
    "scoreInfo": 0,  # when game ends, score gets counted and end up here
    "highScores": {  # list of top scores read from file to here
        "easy": [],
        "normal": [],
        "hard": [],
    },
    "gameStarts": None,  # datetime object
    "gameTurns": 0,
    "statistics": [],
}
BUTTONHEIGHT = 40
BUTTONWIDTH = 40

app = QApplication(sys.argv)
myWindow = QWidget()
collector = QVBoxLayout()
collector.setSpacing(1)
# SetFixedSize is the key to be able to shrink window accordingly
collector.setSizeConstraint(QVBoxLayout.SetFixedSize)

infoBar = QWidget()
infolayout = QHBoxLayout()
infoText = "Mines left: {}".format(state["mineInfo"])
minesCount = QLabel(infoText)
infolayout.addWidget(minesCount)
infoBar.setLayout(infolayout)

scoreWidget = QWidget()
mineFieldWidget = QWidget()
statsWidget = QWidget()


class scoreForm(QWidget):
    def __init__(self):
        super(scoreForm, self).__init__()
        layout = QVBoxLayout()
        self.label = QLabel("New Highscore!")
        self.label2 = QLabel('Enter your name, max 12 characters, ";" not allowed')
        self.nameInput = QLineEdit()
        self.nameInput.setMaxLength(12)
        self.nameInput.setFixedWidth(120)
        self.sButton = QPushButton("Submit")
        self.sButton.setFixedSize(90, 30)
        self.sButton.clicked.connect(lambda: self.submitScore())
        layout.addWidget(self.label)
        layout.addWidget(self.label2)
        layout.addWidget(self.nameInput)
        layout.addWidget(self.sButton)
        self.setLayout(layout)

    def submitScore(self):
        if ";" in self.nameInput.text():
            print("soo soo kielletty merkki")
        else:
            newHighScore = (self.nameInput.text(), str(state["scoreInfo"]))
            state["highScores"][state["difficultyInfo"]].append(newHighScore)
            functions.sortAndCutHighScoreList(state["difficultyInfo"], state)
            functions.writeFileNewScores(state)
            functions.initScores(collector)
            state["scoreInfo"] = 0
            self.nameInput.clear()
            self.setDisabled(True)


scoreform = scoreForm()
scoreform.hide()


class menuWidget(QWidget):
    def __init__(self):
        super(menuWidget, self).__init__()
        bWidth = 55
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignLeft)
        self.b1 = QRadioButton("Easy")
        self.b1.setProperty("difficulty", "easy")
        self.b1.setChecked(True)
        self.b1.toggled.connect(lambda: self.setDifficulty(self.b1))
        layout.addWidget(self.b1, 0, 0)
        self.b2 = QRadioButton("Normal")
        self.b2.setProperty("difficulty", "normal")
        self.b2.toggled.connect(lambda: self.setDifficulty(self.b2))
        layout.addWidget(self.b2, 0, 1)
        self.b3 = QRadioButton("Hard")
        self.b3.setProperty("difficulty", "hard")
        self.b3.toggled.connect(lambda: self.setDifficulty(self.b3))
        layout.addWidget(self.b3, 0, 2)
        self.b4 = QPushButton("Scores")

        self.b4.clicked.connect(lambda: self.toggleScores())
        layout.addWidget(self.b4, 0, 3)
        self.b5 = QPushButton("Restart")
        self.b5.clicked.connect(lambda: self.restartGame())
        self.b6 = QPushButton("Quit")
        self.b6.clicked.connect(lambda: self.quitGame())
        self.b7 = QPushButton("Stats")
        self.b7.clicked.connect(lambda: self.showStats())

        layout.addWidget(self.b5, 1, 0)
        layout.addWidget(self.b6, 1, 1)
        layout.addWidget(self.b7, 1, 2)
        self.setLayout(layout)
        self.b1.setFixedWidth(bWidth)
        self.b2.setFixedWidth(bWidth)
        self.b3.setFixedWidth(bWidth)
        self.b4.setFixedWidth(bWidth)
        self.b5.setFixedWidth(bWidth)
        self.b6.setFixedWidth(bWidth)
        self.b7.setFixedWidth(bWidth)

    def showStats(self):
        statsWindow = state["statsWidget"]
        if statsWindow.isHidden():
            statsWindow.show()
            self.b1.setEnabled(False)
            self.b2.setEnabled(False)
            self.b3.setEnabled(False)
            self.b4.setEnabled(False)
            self.b5.setEnabled(False)
            self.b6.setEnabled(False)
            minesCount.hide()
            state["mineFieldWidget"].hide()
        else:
            statsWindow.hide()
            self.b1.setEnabled(True)
            self.b2.setEnabled(True)
            self.b3.setEnabled(True)
            self.b4.setEnabled(True)
            self.b5.setEnabled(True)
            self.b6.setEnabled(True)
            state["mineFieldWidget"].show()
            minesCount.show()

    def quitGame(self):
        sys.exit()

    def restartGame(self):
        diff = state["difficulty"][state["difficultyInfo"]]
        functions.changeDifficulty(collector, diff[0], diff[1], diff[2], state)
        state["gameStarts"] = datetime.now()
        state["gameTurns"] = 0
        minesCount.setText(functions.getInfoText(state["mineInfo"]))

    def toggleScores(self):
        scoreBoard = state["scoreWidget"]
        if scoreBoard.isHidden():
            scoreBoard.setFixedWidth(state["mineFieldWidget"].width())
            scoreBoard.setFixedHeight(state["mineFieldWidget"].height())
            scoreBoard.show()
            self.b1.setEnabled(False)
            self.b2.setEnabled(False)
            self.b3.setEnabled(False)
            self.b5.setEnabled(False)
            self.b6.setEnabled(False)
            self.b7.setEnabled(False)
            minesCount.hide()
            state["mineFieldWidget"].hide()
        else:
            scoreBoard.hide()
            self.b1.setEnabled(True)
            self.b2.setEnabled(True)
            self.b3.setEnabled(True)
            self.b5.setEnabled(True)
            self.b6.setEnabled(True)
            self.b7.setEnabled(True)
            state["mineFieldWidget"].show()
            minesCount.show()

    def setDifficulty(self, button):
        state["gameStarts"] = datetime.now()
        state["gameTurns"] = 0
        if button.isChecked():
            difficulty = button.property("difficulty")
            if difficulty == "hard":
                hard = state["difficulty"]["hard"]
                state["mineInfo"] = hard[2]
                state["difficultyInfo"] = "hard"
                text = "Mines left: {}".format(hard[2])
                minesCount.setText(text)
                functions.changeDifficulty(collector, hard[0], hard[1], hard[2], state)

            if difficulty == "normal":
                normal = state["difficulty"]["normal"]
                state["mineInfo"] = normal[2]
                state["difficultyInfo"] = "normal"
                text = "Mines left: {}".format(normal[2])
                minesCount.setText(text)
                functions.changeDifficulty(
                    collector, normal[0], normal[1], normal[2], state
                )

            if difficulty == "easy":
                easy = state["difficulty"]["easy"]
                state["mineInfo"] = easy[2]
                state["difficultyInfo"] = "easy"
                text = "Mines left: {}".format(easy[2])
                minesCount.setText(text)
                functions.changeDifficulty(collector, easy[0], easy[1], easy[2], state)


menu = menuWidget()


class fieldButton(QPushButton):
    def mousePressEvent(self, event):
        pos = self.property("position")
        if event.button() == Qt.MouseButton.RightButton:
            if state["showField"][pos[0]][pos[1]] == "s":
                state["mineInfo"] += -1
                minesCount.setText(functions.getInfoText(state["mineInfo"]))
                self.setIcon(QIcon(QPixmap(images["l"])))
                state["showField"][pos[0]][pos[1]] = "l"
                # flags get to 0, game ends
                if state["mineInfo"] <= 0:
                    functions.endGame()
            elif state["showField"][pos[0]][pos[1]] == "l":
                state["mineInfo"] += 1
                minesCount.setText(functions.getInfoText(state["mineInfo"]))
                self.setIcon(QIcon(QPixmap(images["s"])))
                state["showField"][pos[0]][pos[1]] = "s"
        else:
            functions.floodFill(pos[1], pos[0], state)
            state["gameTurns"] += 1


images = {
    "1": "spritet/ruutu_1.png",
    "2": "spritet/ruutu_2.png",
    "3": "spritet/ruutu_3.png",
    "4": "spritet/ruutu_4.png",
    "5": "spritet/ruutu_5.png",
    "6": "spritet/ruutu_6.png",
    "7": "spritet/ruutu_7.png",
    "8": "spritet/ruutu_8.png",
    "x": "spritet/ruutu_miina.png",
    "s": "spritet/ruutu_selka.png",
    "0": "spritet/ruutu_tyhja.png",
    "l": "spritet/ruutu_lippu.png",
}
