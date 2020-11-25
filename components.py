from random import setstate
import sys
from PySide2.QtCore import QObject, Qt
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QApplication, QLabel, QPushButton, QSizePolicy, QStackedWidget, QVBoxLayout, QWidget, QGridLayout, QRadioButton, QHBoxLayout
import functions


state = {
    "field": [],
    "showField": [],
    "fieldButtons": [],
    "mineFieldInstance": {},
    "mineFieldWidget": {},
    "difficulty": {
        "easy": [5, 5, 10],  # width, height, mines
        "normal": [10, 10, 30],
        "hard": [15, 20, 50]
    },
    "mineInfo": 10,          # show how many mines in the field, start with easy
    "hiScores": {
        "easy": [["keksa", "1900"], ["leksa", "1800"], ["jorma", "1700"]],
        "normal": [("jebulis", "11900"), ("lerppu", "11800"), ("jaska", "1700")]
    }
}
buttonHeight = 40
buttonWidth = 40

app = QApplication(sys.argv)
myWindow = QWidget()
collector = QVBoxLayout()
collector.setSpacing(1)
# SetFixedSize is the key to be able to shrink window accordingly
collector.setSizeConstraint(QVBoxLayout.SetFixedSize)

infoBar = QWidget()
infolayout = QHBoxLayout()
infoText = "Mines left: {}".format(state['mineInfo'])
minesCount = QLabel(infoText)
infolayout.addWidget(minesCount)
infoBar.setLayout(infolayout)

scoreWidget = QWidget()
mineFieldWidget = QWidget()


class menuhomma(QWidget):
    def __init__(self):
        super(menuhomma, self).__init__()
        layout = QHBoxLayout()
        self.b1 = QRadioButton("Easy")
        self.b1.setProperty("difficulty", "easy")
        self.b1.setChecked(True)
        self.b1.toggled.connect(lambda: self.setDifficulty(self.b1))
        layout.addWidget(self.b1)
        self.b2 = QRadioButton("Normal")
        self.b2.setProperty("difficulty", "normal")
        self.b2.toggled.connect(lambda: self.setDifficulty(self.b2))
        layout.addWidget(self.b2)
        self.b3 = QRadioButton("Hard")
        self.b3.setProperty("difficulty", "hard")
        self.b3.toggled.connect(lambda: self.setDifficulty(self.b3))
        layout.addWidget(self.b3)
        self.info = infoBar
        self.setLayout(layout)

    def setDifficulty(self, button):
        if button.isChecked():
            print(self.b3.isChecked())
            difficulty = button.property("difficulty")
            if difficulty == "hard":
                hard = state['difficulty']['hard']
                state['mineInfo'] = hard[2]
                text = "Mines left: {}".format(hard[2])
                minesCount.setText(text)
                functions.changeDifficulty(
                    collector, hard[0], hard[1], hard[2])
            if difficulty == "normal":
                normal = state['difficulty']['normal']
                state['mineInfo'] = normal[2]
                text = "Mines left: {}".format(normal[2])
                minesCount.setText(text)
                # scoreWidget.hide()
                functions.changeDifficulty(
                    collector, normal[0], normal[1], normal[2])

            if difficulty == "easy":
                easy = state['difficulty']['easy']
                state['mineInfo'] = easy[2]
                text = "Mines left: {}".format(easy[2])
                minesCount.setText(text)
                functions.changeDifficulty(
                    collector, easy[0], easy[1], easy[2])

        # if self.b3.isChecked():
        #     hard = state['difficulty']['hard']
        #     state['mineInfo'] = hard[2]
        #     text = "Mines left: {}".format(hard[2])
        #     minesCount.setText(text)
        #     functions.changeDifficulty(
        #         collector, hard[0], hard[1], hard[2])
        # if self.b2.isChecked():
        #     normal = state['difficulty']['normal']
        #     state['mineInfo'] = normal[2]
        #     text = "Mines left: {}".format(normal[2])
        #     minesCount.setText(text)
        #     # scoreWidget.hide()
        #     functions.changeDifficulty(
        #         collector, normal[0], normal[1], normal[2])

        # if self.b1.isChecked():
        #     easy = state['difficulty']['easy']
        #     state['mineInfo'] = easy[2]
        #     text = "Mines left: {}".format(easy[2])
        #     minesCount.setText(text)
        #     functions.changeDifficulty(
        #         collector, easy[0], easy[1], easy[2])


menu = menuhomma()


class fieldButton(QPushButton):
    def __init__(self):
        super(fieldButton, self).__init__()

    def mousePressEvent(self, event):
        pos = self.property('position')
        if event.button() == Qt.MouseButton.RightButton:
            if state['showField'][pos[0]][pos[1]] == 's':
                state['mineInfo'] += -1
                minesCount.setText(functions.getInfoText(state['mineInfo']))
                self.setIcon(QIcon(QPixmap(images['l'])))
                state['showField'][pos[0]][pos[1]] = 'l'
                # flags get to 0, game ends
                if state['mineInfo'] <= 0:
                    functions.endGame()
            elif state['showField'][pos[0]][pos[1]] == 'l':
                state['mineInfo'] += 1
                minesCount.setText(functions.getInfoText(state['mineInfo']))
                self.setIcon(QIcon(QPixmap(images['s'])))
                state['showField'][pos[0]][pos[1]] = 's'
        else:
            functions.floodFill(pos[1], pos[0])


images = {
    '1': 'spritet/ruutu_1.png',
    '2': 'spritet/ruutu_2.png',
    '3': 'spritet/ruutu_3.png',
    '4': 'spritet/ruutu_4.png',
    '5': 'spritet/ruutu_5.png',
    '6': 'spritet/ruutu_6.png',
    '7': 'spritet/ruutu_7.png',
    '8': 'spritet/ruutu_8.png',
    'x': 'spritet/ruutu_miina.png',
    's': 'spritet/ruutu_selka.png',
    '0': 'spritet/ruutu_tyhja.png',
    'l': 'spritet/ruutu_lippu.png',

}
