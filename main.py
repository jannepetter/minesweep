import sys
from datetime import datetime
from PySide2.QtCore import Qt
from functions import initStats, readStatisticsFile, setState, initField, initScores, readHighScoresFile
from components import menu, state, app, myWindow, collector, buttonHeight, buttonWidth
from components import scoreform, statsWidget, infoBar, scoreWidget, mineFieldWidget


# siisti koodia
# siisti ulkoasua


def main():
    readHighScoresFile()
    readStatisticsFile()
    easy = state['difficulty']['easy']
    state['scoreWidget'] = scoreWidget
    state["statsWidget"] = statsWidget
    state['mineFieldWidget'] = mineFieldWidget
    state['scoreForm'] = scoreform
    wid = myWindow

    fieldWidth = easy[0]
    fieldHeight = easy[1]
    mines = easy[2]
    print('miinoja', mines)
    setState(fieldWidth, fieldHeight, mines)

    mineField = initField(state, buttonWidth, buttonHeight)
    mineFieldWidget.setLayout(mineField)

    collector.addWidget(menu)
    initStats(collector)
    initScores(collector)
    collector.addWidget(infoBar)

    collector.addWidget(mineFieldWidget)
    collector.addWidget(scoreform)
    wid.setLayout(collector)

    wid.setWindowTitle("Minesweep")
    state['gameStarts'] = datetime.now()

    wid.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
