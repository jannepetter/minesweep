import sys
from datetime import datetime
from PySide2.QtCore import Qt
from functions import setState, initField, initScores, readHighScoresFile
from components import menu, state, app, myWindow, collector, buttonHeight, buttonWidth, infoBar, scoreWidget, mineFieldWidget
from components import scoreform

# tyhjällä score tiedostolla bugi
# tilastowidgetti, vaikka 20 viimesintä peliä sinne
# siisti koodia
# siisti ulkoasua


def main():
    readHighScoresFile('scores.csv')
    easy = state['difficulty']['easy']
    state['scoreWidget'] = scoreWidget
    fieldWidth = easy[0]
    fieldHeight = easy[1]
    mines = easy[2]
    print('miinoja', mines)
    setState(fieldWidth, fieldHeight, mines)
    wid = myWindow
    scoreLayout = initScores(collector)
    scoreWidget.setLayout(scoreLayout)

    mineField = initField(state, buttonWidth, buttonHeight)
    mineFieldWidget.setLayout(mineField)
    state['mineFieldInstance'] = mineField
    state['mineFieldWidget'] = mineFieldWidget

    collector.addWidget(menu)
    collector.addWidget(infoBar)
    collector.setAlignment(menu, Qt.AlignTop)

    collector.addWidget(mineFieldWidget)
    collector.addWidget(scoreWidget)
    collector.addWidget(scoreform)
    state['scoreForm'] = scoreform
    scoreWidget.hide()
    state['scoreWidget'] = scoreWidget
    wid.setLayout(collector)

    wid.setWindowTitle("Minesweep")
    state['gameStarts'] = datetime.now()

    wid.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
