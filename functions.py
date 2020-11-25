from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QGridLayout, QLabel, QWidget
import random
from components import state, fieldButton, myWindow, images, buttonHeight, buttonWidth, collector


def clearLayout(layout):
    '''code by JosBalcaen, pyside2 lacking of basic function to remove
    layout, this does just that'''
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())


def readFile(file):
    scoreList = []
    with open(file) as filu:
        for rivi in file.readlines():
            scoreList.append(rivi.strip().split(';'))
    return scoreList


def writeFileNewScores(file):
    pass


def gameButton(icon: str, width: int, height: int):
    '''
    Creates a gameButton instance with matching icon string. Width and height
     are args to button and also to icon size.
    '''
    button = fieldButton()
    button.setIcon(QIcon(QPixmap(images[icon])))
    button.setIconSize(QSize(width-5, height-5))
    button.setFixedSize(width, height)
    return button


def initField(state, buttonWidth: int, buttonHeight: int, buttonHandler=gameButton):
    '''
    This function needs to be called once. Initiates minefield buttons with property "position",
    which is the coordinate tuple (y,x) of the button position in the layout.
    The button are added to QgridLayout which is returned. The buttons are also added to state
    fieldButtons list with matching property position to manipulate the image of the buttons.
    '''
    layout = QGridLayout()
    buttonList = []
    for i, row in enumerate(state['showField']):
        buttonList.append([])
        for j, el in enumerate(row):
            button = buttonHandler(el, buttonWidth, buttonHeight)
            button.setProperty("position", (i, j))
            layout.addWidget(button, j, i)
            buttonList[-1].append(button)
    state['fieldButtons'] = buttonList
    return layout


def updateView(state=state):
    '''When button is pressed updateView is called and the view is updated
    according to values in showField state'''

    for i, row in enumerate(state['fieldButtons']):
        for j, el in enumerate(row):
            pos = el.property('position')
            kuva = state['showField'][pos[0]][pos[1]]
            el.setIcon(QIcon(QPixmap(images[kuva])))
            el.setProperty("position", (i, j))


def getFlagList():
    flagList = []
    for i, row in enumerate(state['showField']):
        for j, el in enumerate(row):
            if el == 'l':
                flagList.append((i, j))
    return flagList


def countScore(flags):
    score = 0
    for spot in flags:
        if state['field'][spot[0]][spot[1]] == 'x':
            score += 1
        else:
            score -= 1
    return score


def initScores():
    scoreLayout = QGridLayout()
    # scoreLayout.setSizeConstraint(QGridLayout.SetFixedSize)
    for i, el in enumerate(state['hiScores']['easy']):
        text = "{} {}".format(el[0], el[1])
        topPlayer = QLabel(text)
        scoreLayout.addWidget(topPlayer, i, 1)
    return scoreLayout


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
    print('skoore iss', score)


def floodFill(startX: int, startY: int, state=state):
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


def countSurroundingMines(x: int, y: int, field) -> int:
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


def setMines(field2d, minesNumber):
    '''
    Sets mines to the given field, in place - function doesn't return anything.
    '''
    unminedSpots = []
    for y in range(len(field2d)):
        for x in range(len(field2d[y])):
            unminedSpots.append((x, y))
    spotsToBeMined = random.sample(unminedSpots, minesNumber)
    for el in spotsToBeMined:
        field2d[el[1]][el[0]] = 'x'


def setState(width: int, height: int, mines: int) -> None:
    '''
    Needs to be called only once.
    Initializes state field and showField lists. Each field element is initialized with ' ' as
    spot with no mines and showField state elements are initialized with 's' as not shown or
    secret. setState function then randomly sets given number of mines to field state and 
    counts the value of each element how many mines are located in neighbour elements.
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


# def changeDifficulty(container, containerWidth, containerHeight, numberOfMines):
#     clearLayout(state['mineFieldInstance'])
#     setState(containerWidth, containerHeight, numberOfMines)
#     newField = initField(state, buttonWidth, buttonHeight)
#     state['mineFieldInstance'] = newField
#     container.addLayout(newField)

def changeDifficulty(container, containerWidth, containerHeight, numberOfMines):
    clearLayout(state['mineFieldInstance'])
    container.removeWidget(state['mineFieldWidget'])
    newMineField = QWidget()
    setState(containerWidth, containerHeight, numberOfMines)
    newField = initField(state, buttonWidth, buttonHeight)
    state['mineFieldInstance'] = newField
    state['mineFieldWidget'] = newMineField
    newMineField.setLayout(newField)
    container.addWidget(newMineField)


def getInfoText(number):
    text = "Mines left :{}".format(number)
    return text
