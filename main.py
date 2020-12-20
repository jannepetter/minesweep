import sys
from datetime import datetime
from functions import (
    initStats,
    readStatisticsFile,
    setState,
    initField,
    initScores,
    readHighScoresFile,
)
from components import menu, state, app, myWindow, collector, BUTTONHEIGHT, BUTTONWIDTH
from components import scoreform, statsWidget, infoBar, scoreWidget, mineFieldWidget


def main():
    readHighScoresFile(state)
    readStatisticsFile(state)
    easy = state["difficulty"]["easy"]
    state["scoreWidget"] = scoreWidget
    state["statsWidget"] = statsWidget
    state["mineFieldWidget"] = mineFieldWidget
    state["scoreForm"] = scoreform
    wid = myWindow

    fieldWidth = easy[0]
    fieldHeight = easy[1]
    mines = easy[2]
    print("miinoja", mines)
    setState(fieldWidth, fieldHeight, mines)

    mineField = initField(state, BUTTONWIDTH, BUTTONHEIGHT)
    mineFieldWidget.setLayout(mineField)

    collector.addWidget(menu)
    initStats(collector, state)
    initScores(collector)
    collector.addWidget(infoBar)

    collector.addWidget(mineFieldWidget)
    collector.addWidget(scoreform)
    wid.setLayout(collector)

    wid.setWindowTitle("Minesweep")
    state["gameStarts"] = datetime.now()
    wid.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
