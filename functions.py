from datetime import datetime
from typing import Callable
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout, QWidget
import random
from components import scoreForm, state, fieldButton, images, buttonHeight, buttonWidth, collector


def sortAndCutHighScoreList(difficulty: str, state: object = state):
    state['highScores'][difficulty].sort(
        key=lambda s: int(s[1]))
    state['highScores'][difficulty].reverse()
    del state['highScores'][difficulty][10:]


def writeStatsToFile(state: object, file: str = 'statistics.txt'):
    pva = str(state['gameStarts'].strftime('%Y %B %d %H:%M:%S'))
    dur = str((datetime.now()-state['gameStarts']).seconds//60)
    flagged = state['scoreInfo']
    diff = state['difficultyInfo']
    totalMines = state['difficulty'][diff][2]
    turns = state['gameTurns']

    newStat = 'Game begins: {} , duration: {} min, turns {}, mines flagged {}/{}, difficulty: {}'.format(
        pva, dur, turns, flagged, totalMines, diff
    )
    state['statistics'].insert(0, newStat)

    with open(file, 'w') as filu:
        for i, el in enumerate(state['statistics']):
            # last 20 statistics are shown
            if i > 19:
                break
            else:
                filu.write(el+'\n')


def readStatisticsFile(state: object = state, file: str = 'statistics.txt'):
    state['statistics'] = []
    try:
        with open(file) as filu:
            for rivi in filu:
                state['statistics'].append(rivi.strip())
    except FileNotFoundError:
        print('could not open file {}'.format(file))
    except:
        print('error happened reading file {}'.format(file))


def readHighScoresFile(file: str = 'scores.csv'):
    easy = []
    normal = []
    hard = []
    try:
        with open(file) as filu:
            for rivi in filu.readlines():
                rivi = rivi.strip().split(';')
                if rivi[0] == 'easy':
                    easy.append((rivi[1], rivi[2]))
                elif rivi[0] == 'normal':
                    normal.append((rivi[1], rivi[2]))
                elif rivi[0] == 'hard':
                    hard.append((rivi[1], rivi[2]))
    except FileNotFoundError:
        print('could not open file {}'.format(file))
    except:
        print('error happened reading file {}'.format(file))

    state['highScores']['easy'] = easy
    state['highScores']['normal'] = normal
    state['highScores']['hard'] = hard
    sortAndCutHighScoreList('easy')
    sortAndCutHighScoreList('normal')
    sortAndCutHighScoreList('hard')


def writeFileNewScores(state: object, file: str = 'scores.csv'):
    with open(file, 'w') as filu:
        max = 10
        for i, el in enumerate(state['highScores']['easy']):
            if i < max:
                newline = 'easy;{};{}\n'.format(el[0], str(el[1]))
                filu.write(newline)
        for i, el in enumerate(state['highScores']['normal']):
            if i < max:
                newline = 'normal;{};{}\n'.format(el[0], str(el[1]))
                filu.write(newline)
        for i, el in enumerate(state['highScores']['hard']):
            if i < max:
                newline = 'hard;{};{}\n'.format(el[0], str(el[1]))
                filu.write(newline)


def createGameButton(icon: str, width: int, height: int):
    '''
    Creates and returns a gameButton instance from fieldButton class with matching icon string.
     Width and height are args to button and also to icon size.
    '''
    button = fieldButton()
    button.setIcon(QIcon(QPixmap(images[icon])))
    button.setIconSize(QSize(width-5, height-5))
    button.setFixedSize(width, height)
    return button


def initField(state: object, buttonWidth: int, buttonHeight: int, buttonCreator: Callable[[str, int, int], QPushButton] = createGameButton):
    '''
    Initiates minefield buttons with property "position", which is the 
    coordinate tuple (y,x) of the button position in the layout. The buttons are added to
    QgridLayout which is returned. The buttons are also added to state fieldButtons list
    for easy manipulation.
    '''
    layout = QGridLayout()
    buttonList = []
    for i, row in enumerate(state['showField']):
        buttonList.append([])
        for j, el in enumerate(row):
            button = buttonCreator(el, buttonWidth, buttonHeight)
            button.setProperty("position", (i, j))
            layout.addWidget(button, j, i)
            buttonList[-1].append(button)
    state['fieldButtons'] = buttonList
    return layout


def updateView(state: object = state):
    '''When button is pressed updateView is called and the view is updated
    according to values in showField state'''

    for i, row in enumerate(state['fieldButtons']):
        for j, el in enumerate(row):
            pos = el.property('position')
            kuva = state['showField'][pos[0]][pos[1]]
            el.setIcon(QIcon(QPixmap(images[kuva])))
            el.setProperty("position", (i, j))


def getFlagList(state: object = state) -> list:
    '''
    Goes through showField list for players flags "l" for mines, puts them in to
    array and returns them.
    '''
    flagList = []
    for i, row in enumerate(state['showField']):
        for j, el in enumerate(row):
            if el == 'l':
                flagList.append((i, j))
    return flagList


def countScore(flags: list) -> int:
    '''
    Compares flaglist spots to state field, if flag is planted to same spot where mine is,
    player gets point, if player has planted flag where there is no mine, player loses point.
    '''
    score = 0
    for spot in flags:
        if state['field'][spot[0]][spot[1]] == 'x':
            score += 1
        else:
            score -= 1
    return score


def initStats(container: QWidget, state: object = state):
    container.removeWidget(state["statsWidget"])
    state["statsWidget"].deleteLater()
    newstatsWidget = QWidget()
    newstatsWidget.hide()
    statsLayout = QVBoxLayout()
    for el in state['statistics']:
        infoLabel = QLabel(el)
        statsLayout.addWidget(infoLabel)
    newstatsWidget.setLayout(statsLayout)
    container.addWidget(newstatsWidget)
    state["statsWidget"] = newstatsWidget


def initScores(container: QWidget):
    container.removeWidget(state["scoreWidget"])
    state["scoreWidget"].deleteLater()
    newScoreWidget = QWidget()
    newScoreWidget.hide()
    scoreLayout = QGridLayout()
    scoreLayout.setAlignment(Qt.AlignTop)
    diff1 = QLabel('Easy')
    scoreLayout.addWidget(diff1, 0, 1)
    for i, el in enumerate(state['highScores']['easy']):
        text = "{} {}".format(el[0], el[1])
        topPlayer = QLabel(text)
        scoreLayout.addWidget(topPlayer, i+1, 1)
    diff2 = QLabel('Normal')
    scoreLayout.addWidget(diff2, 0, 2)
    for i, el in enumerate(state['highScores']['normal']):
        text = "{} {}".format(el[0], el[1])
        topPlayer = QLabel(text)
        scoreLayout.addWidget(topPlayer, i+1, 2)
    diff3 = QLabel('Hard')
    scoreLayout.addWidget(diff3, 0, 3)
    for i, el in enumerate(state['highScores']['hard']):
        text = "{} {}".format(el[0], el[1])
        topPlayer = QLabel(text)
        scoreLayout.addWidget(topPlayer, i+1, 3)
    newScoreWidget.setLayout(scoreLayout)
    state['scoreWidget'] = newScoreWidget
    container.addWidget(newScoreWidget)


def endGame():
    for row in state['fieldButtons']:
        for button in row:
            i, j = button.property('position')
            showImage = state['showField'][i][j]
            fieldImage = state['field'][i][j]
            if showImage != 'l' and fieldImage == 'x':
                button.setIcon(
                    QIcon(QPixmap(images[fieldImage])))
            button.setEnabled(False)
    flags = getFlagList()
    score = countScore(flags)
    state['scoreInfo'] = score
    writeStatsToFile(state)
    readStatisticsFile()
    initStats(collector)
    checklist = state['highScores'][state['difficultyInfo']]
    topPlayerCount = len(checklist)
    if topPlayerCount == 0:
        state['scoreForm'].show()
    else:
        lastTopScore = int(checklist[-1][1])
        if topPlayerCount < 10 or lastTopScore < score:
            state['scoreForm'].show()


def floodFill(startX: int, startY: int, state: object = state):
    '''
    If square with no mine in it is clicked open, the function opens adjacent squares which have
    no mines.
    '''
    checkList = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
    if state['field'][startY][startX] == 'x':
        state['fieldButtons'][startY][startX].setIcon(
            QIcon(QPixmap(images['x'])))
        state['showField'][startY][startX] = 'x'
        endGame()
        return
    floodList = [(startX, startY)]
    height = len(state['field'])
    width = len(state['field'][0])
    while True:
        element = floodList.pop()
        beginX = element[0]-1 if element[0]-1 >= 0 else 0
        endX = element[0]+1 if element[0]+1 <= width else width
        beginY = element[1]-1 if element[1]-1 >= 0 else 0
        endY = element[1]+1 if element[1]+1 <= height else height
        for i in range(beginY, endY):
            for j in range(beginX, endX):
                val = state['field'][i][j]
                if val in checkList:
                    state['field'][i][j] = '-'
                    state['showField'][i][j] = val
                    floodList.append((j, i))
        if not floodList:
            break
    updateView()


def countSurroundingMines(x: int, y: int, field: list) -> int:
    '''
    Counts how many mines surrounds the given spot (x,y), the number of mines is returned
    '''
    mines = 0
    startX = x-1 if x-1 >= 0 else 0
    endX = x+2 if x+2 <= len(field[0]) else len(field[0])
    startY = y-1 if y-1 >= 0 else 0
    endY = y+2 if y+2 <= len(field) else len(field)

    for i in range(startY, endY):
        for j in range(startX, endX):
            if field[i][j] == 'x':
                mines += 1
    return mines


def setMines(field2d: list, minesNumber: int):
    '''
    Sets mines to the given field, randomly in place - function doesn't return anything.
    '''
    unminedSpots = []
    for y in range(len(field2d)):
        for x in range(len(field2d[y])):
            unminedSpots.append((x, y))
    spotsToBeMined = random.sample(unminedSpots, minesNumber)
    for el in spotsToBeMined:
        field2d[el[1]][el[0]] = 'x'


def setState(width: int, height: int, mines: int, setMines: Callable[[list, int], None] = setMines) -> None:
    '''
    Initializes state field and showField lists. Each field element is initialized with ' ' as
    spot with no mines and showField state elements are initialized with 's' as not shown or
    secret. setState function then randomly sets given number of mines to field state using
    setMines function. Field state unmined elements are counted for surrounding mines with
    the help of countSurroundingMines function.
    '''
    field = []
    show = []
    for i in range(height):
        field.append([])
        show.append([])
        for j in range(width):
            field[-1].append(' ')
            show[-1].append('s')
    state['field'] = field
    state['showField'] = show
    setMines(state['field'], mines)
    for i, row in enumerate(state['field']):
        for j, el in enumerate(row):
            if el == ' ':
                state['field'][i][j] = str(
                    countSurroundingMines(j, i, state['field']))


def changeDifficulty(container: QWidget, horizontalButtonCount: int, verticalButtonCount: int, numberOfMines: int, state: object = state):
    '''
    Basically restarts game with wanted dimensions and how many mines wanted. This function
    is used in this app to change difficulty and/or restart the game.
    '''
    container.removeWidget(state['mineFieldWidget'])
    container.removeWidget(state['scoreForm'])
    state['mineFieldWidget'].deleteLater()
    state['scoreForm'].deleteLater()
    state['mineInfo'] = numberOfMines
    newscoreForm = scoreForm()
    container.addWidget(newscoreForm)
    newscoreForm.hide()
    state['scoreForm'] = newscoreForm
    newMineField = QWidget()
    setState(horizontalButtonCount, verticalButtonCount, numberOfMines)
    newField = initField(state, buttonWidth, buttonHeight)
    state['mineFieldWidget'] = newMineField
    newMineField.setLayout(newField)
    container.addWidget(newMineField)


def getInfoText(number: int):
    text = "Mines left :{}".format(number)
    return text
