from datetime import datetime
import random
from typing import Callable
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from components import (
    scoreForm,
    state,
    fieldButton,
    images,
    BUTTONHEIGHT,
    BUTTONWIDTH,
    collector,
)


def sortAndCutHighScoreList(difficulty: str, stateObj: object):
    stateObj["highScores"][difficulty].sort(key=lambda s: int(s[1]))
    stateObj["highScores"][difficulty].reverse()
    del stateObj["highScores"][difficulty][10:]


def writeStatsToFile(stateInfo: dict, file: str = "statistics.txt"):
    pva = str(stateInfo["gameStarts"].strftime("%Y %B %d %H:%M:%S"))
    dur = str((datetime.now() - stateInfo["gameStarts"]).seconds // 60)
    flagged = stateInfo["scoreInfo"]
    diff = stateInfo["difficultyInfo"]
    totalMines = stateInfo["difficulty"][diff][2]
    turns = stateInfo["gameTurns"]

    newStat = (
        "Game begins: {} , duration: {} min, turns {}, mines flagged"
        " {}/{}, difficulty: {}"
    ).format(pva, dur, turns, flagged, totalMines, diff)
    stateInfo["statistics"].insert(0, newStat)

    with open(file, "w") as filu:
        for i, el in enumerate(stateInfo["statistics"]):
            # last 20 statistics are shown
            if i > 19:
                break
            else:
                filu.write(el + "\n")


def readStatisticsFile(stateInfo: dict, file: str = "statistics.txt"):
    stateInfo["statistics"] = []
    try:
        with open(file) as filu:
            for rivi in filu:
                stateInfo["statistics"].append(rivi.strip())
    except FileNotFoundError:
        print("could not open file {}".format(file))
    except Exception as e:
        print("error {} happened while reading file {}".format(e, file))


def readHighScoresFile(stateInfo: dict, file: str = "scores.csv"):
    easy = []
    normal = []
    hard = []
    try:
        with open(file) as filu:
            for rivi in filu.readlines():
                rivi = rivi.strip().split(";")
                if rivi[0] == "easy":
                    easy.append((rivi[1], rivi[2]))
                elif rivi[0] == "normal":
                    normal.append((rivi[1], rivi[2]))
                elif rivi[0] == "hard":
                    hard.append((rivi[1], rivi[2]))
    except FileNotFoundError:
        print("could not open file {}".format(file))
    except Exception as e:
        print("error {} happened while reading file {}".format(e, file))

    stateInfo["highScores"]["easy"] = easy
    stateInfo["highScores"]["normal"] = normal
    stateInfo["highScores"]["hard"] = hard
    sortAndCutHighScoreList("easy", stateInfo)
    sortAndCutHighScoreList("normal", stateInfo)
    sortAndCutHighScoreList("hard", stateInfo)


def writeFileNewScores(stateInfo: dict, file: str = "scores.csv"):
    with open(file, "w") as filu:
        maxScores = 10
        for i, el in enumerate(stateInfo["highScores"]["easy"]):
            if i < maxScores:
                newline = "easy;{};{}\n".format(el[0], str(el[1]))
                filu.write(newline)
        for i, el in enumerate(stateInfo["highScores"]["normal"]):
            if i < maxScores:
                newline = "normal;{};{}\n".format(el[0], str(el[1]))
                filu.write(newline)
        for i, el in enumerate(stateInfo["highScores"]["hard"]):
            if i < maxScores:
                newline = "hard;{};{}\n".format(el[0], str(el[1]))
                filu.write(newline)


def createGameButton(icon: str, width: int, height: int):
    """
    Creates and returns a gameButton instance from fieldButton class with matching icon string.
     Width and height are args to button and also to icon size.
    """
    button = fieldButton()
    button.setIcon(QIcon(QPixmap(images[icon])))
    button.setIconSize(QSize(width - 5, height - 5))
    button.setFixedSize(width, height)
    return button


def initField(
    stateInfo: dict,
    buttonWidth: int,
    buttonHeight: int,
    buttonCreator: Callable[[str, int, int], QPushButton] = createGameButton,
):
    """
    Initiates minefield buttons with property "position", which is the
    coordinate tuple (y,x) of the button position in the layout. The buttons are added to
    QgridLayout which is returned. The buttons are also added to state fieldButtons list
    for easy manipulation.
    """
    layout = QGridLayout()
    buttonList = []
    for i, row in enumerate(stateInfo["showField"]):
        buttonList.append([])
        for j, el in enumerate(row):
            button = buttonCreator(el, buttonWidth, buttonHeight)
            button.setProperty("position", (i, j))
            layout.addWidget(button, j, i)
            buttonList[-1].append(button)
    stateInfo["fieldButtons"] = buttonList
    return layout


def updateView(stateInfo: dict):
    """When button is pressed updateView is called and the view is updated
    according to values in showField state"""

    for i, row in enumerate(stateInfo["fieldButtons"]):
        for j, el in enumerate(row):
            pos = el.property("position")
            kuva = stateInfo["showField"][pos[0]][pos[1]]
            el.setIcon(QIcon(QPixmap(images[kuva])))
            el.setProperty("position", (i, j))


def getFlagList(stateInfo: dict) -> list:
    """
    Goes through showField list for players flags "l" for mines, puts them in to
    array and returns them.
    """
    flagList = []
    for i, row in enumerate(stateInfo["showField"]):
        for j, el in enumerate(row):
            if el == "l":
                flagList.append((i, j))
    return flagList


def countScore(flags: list) -> int:
    """
    Compares flaglist spots to state field, if flag is planted to same spot where mine is,
    player gets point, if player has planted flag where there is no mine, player loses point.
    """
    score = 0
    for spot in flags:
        if state["field"][spot[0]][spot[1]] == "x":
            score += 1
        else:
            score -= 1
    return score


def initStats(container: QWidget, stateInfo: dict):
    container.removeWidget(stateInfo["statsWidget"])
    stateInfo["statsWidget"].deleteLater()
    newstatsWidget = QWidget()
    newstatsWidget.hide()
    statsLayout = QVBoxLayout()
    for el in stateInfo["statistics"]:
        infoLabel = QLabel(el)
        statsLayout.addWidget(infoLabel)
    newstatsWidget.setLayout(statsLayout)
    container.addWidget(newstatsWidget)
    stateInfo["statsWidget"] = newstatsWidget


def initScores(container: QWidget):
    container.removeWidget(state["scoreWidget"])
    state["scoreWidget"].deleteLater()
    newScoreWidget = QWidget()
    newScoreWidget.hide()
    scoreLayout = QGridLayout()
    scoreLayout.setAlignment(Qt.AlignTop)
    diff1 = QLabel("Easy")
    scoreLayout.addWidget(diff1, 0, 1)
    for i, el in enumerate(state["highScores"]["easy"]):
        text = "{} {}".format(el[0], el[1])
        topPlayer = QLabel(text)
        scoreLayout.addWidget(topPlayer, i + 1, 1)
    diff2 = QLabel("Normal")
    scoreLayout.addWidget(diff2, 0, 2)
    for i, el in enumerate(state["highScores"]["normal"]):
        text = "{} {}".format(el[0], el[1])
        topPlayer = QLabel(text)
        scoreLayout.addWidget(topPlayer, i + 1, 2)
    diff3 = QLabel("Hard")
    scoreLayout.addWidget(diff3, 0, 3)
    for i, el in enumerate(state["highScores"]["hard"]):
        text = "{} {}".format(el[0], el[1])
        topPlayer = QLabel(text)
        scoreLayout.addWidget(topPlayer, i + 1, 3)
    newScoreWidget.setLayout(scoreLayout)
    state["scoreWidget"] = newScoreWidget
    container.addWidget(newScoreWidget)


def endGame():
    for row in state["fieldButtons"]:
        for button in row:
            i, j = button.property("position")
            showImage = state["showField"][i][j]
            fieldImage = state["field"][i][j]
            if showImage != "l" and fieldImage == "x":
                button.setIcon(QIcon(QPixmap(images[fieldImage])))
            button.setEnabled(False)
    flags = getFlagList(state)
    score = countScore(flags)
    state["scoreInfo"] = score
    writeStatsToFile(state)
    readStatisticsFile(state)
    initStats(collector, state)
    checklist = state["highScores"][state["difficultyInfo"]]
    topPlayerCount = len(checklist)
    if topPlayerCount == 0:
        state["scoreForm"].show()
    else:
        lastTopScore = int(checklist[-1][1])
        if topPlayerCount < 10 or lastTopScore < score:
            state["scoreForm"].show()


def floodFill(startX: int, startY: int, stateInfo: dict):
    """
    If square with no mine in it is clicked open, the function opens adjacent squares which have
    no mines.
    """
    checkList = ["1", "2", "3", "4", "5", "6", "7", "8"]

    if stateInfo["field"][startY][startX] == "x":
        stateInfo["fieldButtons"][startY][startX].setIcon(QIcon(QPixmap(images["x"])))
        stateInfo["showField"][startY][startX] = "x"
        endGame()
        return
    elif stateInfo["showField"][startY][startX] != "s":
        return
    floodList = [(startX, startY)]
    height = len(stateInfo["field"]) - 1
    width = len(stateInfo["field"][0]) - 1
    while True:
        element = floodList.pop()
        beginX = element[0] - 1 if element[0] - 1 >= 0 else 0
        endX = element[0] + 1 if element[0] + 1 <= width else width
        beginY = element[1] - 1 if element[1] - 1 >= 0 else 0
        endY = element[1] + 1 if element[1] + 1 <= height else height
        for i in range(beginY, endY + 1):
            for j in range(beginX, endX + 1):
                val = stateInfo["field"][i][j]
                if val == "0":
                    stateInfo["field"][i][j] = "-"  # marks point as checked
                    stateInfo["showField"][i][j] = val
                    floodList.append((j, i))
                elif val in checkList:
                    stateInfo["showField"][i][j] = val
        if not floodList:
            break
    updateView(stateInfo)


def countSurroundingMines(x: int, y: int, field: list) -> int:
    """
    Counts how many mines surrounds the given spot (x,y), the number of mines is returned
    """
    mines = 0
    startX = x - 1 if x - 1 >= 0 else 0
    endX = x + 2 if x + 2 <= len(field[0]) else len(field[0])
    startY = y - 1 if y - 1 >= 0 else 0
    endY = y + 2 if y + 2 <= len(field) else len(field)

    for i in range(startY, endY):
        for j in range(startX, endX):
            if field[i][j] == "x":
                mines += 1
    return mines


def setMines(field2d: list, minesNumber: int):
    """
    Sets mines to the given field, randomly in place - function doesn't return anything.
    """
    unminedSpots = []
    for i in enumerate(field2d):
        for j in enumerate(field2d[i[0]]):
            unminedSpots.append((j[0], i[0]))
    spotsToBeMined = random.sample(unminedSpots, minesNumber)
    for el in spotsToBeMined:
        field2d[el[1]][el[0]] = "x"


def setState(
    width: int,
    height: int,
    mines: int,
    plantMines: Callable[[list, int], None] = setMines,
) -> None:
    """
    Initializes state field and showField lists. Each field element is initialized with ' ' as
    spot with no mines and showField state elements are initialized with 's' as not shown or
    secret. setState function then randomly sets given number of mines to field state using
    setMines function. Field state unmined elements are counted for surrounding mines with
    the help of countSurroundingMines function.
    """
    field = []
    show = []
    for i in range(height):
        field.append([])
        show.append([])
        for j in range(width):
            field[-1].append(" ")
            show[-1].append("s")
    state["field"] = field
    state["showField"] = show
    plantMines(state["field"], mines)
    for i, row in enumerate(state["field"]):
        for j, el in enumerate(row):
            if el == " ":
                state["field"][i][j] = str(countSurroundingMines(j, i, state["field"]))


def changeDifficulty(
    container: QWidget,
    horizontalButtonCount: int,
    verticalButtonCount: int,
    numberOfMines: int,
    stateInfo: dict,
):
    """
    Basically restarts game with wanted dimensions and how many mines wanted. This function
    is used in this app to change difficulty and/or restart the game.
    """
    container.removeWidget(stateInfo["mineFieldWidget"])
    container.removeWidget(stateInfo["scoreForm"])
    stateInfo["mineFieldWidget"].deleteLater()
    stateInfo["scoreForm"].deleteLater()
    stateInfo["mineInfo"] = numberOfMines
    newscoreForm = scoreForm()
    container.addWidget(newscoreForm)
    newscoreForm.hide()
    stateInfo["scoreForm"] = newscoreForm
    newMineField = QWidget()
    setState(horizontalButtonCount, verticalButtonCount, numberOfMines)
    newField = initField(stateInfo, BUTTONWIDTH, BUTTONHEIGHT)
    stateInfo["mineFieldWidget"] = newMineField
    newMineField.setLayout(newField)
    container.addWidget(newMineField)


def getInfoText(number: int):
    text = "Mines left :{}".format(number)
    return text
