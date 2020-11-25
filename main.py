import sys

from PySide2.QtCore import Qt
from functions import setState, initField, initScores
from components import menu, state, app, myWindow, collector, buttonHeight, buttonWidth, infoBar, scoreWidget, mineFieldWidget

# testailua normal difficulty valikossa. Laita siinä aluksi toimiin että fieldi
# häviää ja scoret tulee näkyviin. Nyt on ihan sekasin collectorit ja mineFieldwidgetit
# toimii jotenki mutta jossaivaiheessa tulee varmasti kunnon bugeja jos noin jättää
# kokeile QStackedwidget jos ei muuten toimi
# menuun nappi josta toggle kenttä ja scoret
# jäit readfile ja writenewScores funtionssii
# highscore / tilastot ja nimmarinkirjotus
# aika ja lippujen määrä
# joku klikkausääni voi kans olla hyvä
# requirements hommelit


def main():
    easy = state['difficulty']['easy']
    fieldWidth = easy[0]
    fieldHeight = easy[1]
    mines = easy[2]
    print('miinoja', mines)
    setState(fieldWidth, fieldHeight, mines)
    wid = myWindow
    scoreLayout = initScores()
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
    # scoreWidget.hide()
    wid.setLayout(collector)

    wid.setWindowTitle("Simple.. or is it??")

    wid.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
