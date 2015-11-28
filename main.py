import argparse
import sys

from PyQt4 import QtGui

import tutorial2
import tutorial3
import tutorial4
import tutorial5
import tutorial7
import tutorial8


TUTORIAL_CANVAS = {
    "tutorial2": tutorial2.Canvas,
    "tutorial3": tutorial3.Canvas,
    "tutorial4": tutorial4.Canvas,
    "tutorial5": tutorial5.Canvas,
    "tutorial7": tutorial7.Canvas,
    "tutorial8": tutorial8.Canvas,
}


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("tutorials", nargs="+", help="Tutorials to display",
                        choices=TUTORIAL_CANVAS.keys())
    return parser.parse_args()


class TutorialList(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TutorialList, self).__init__(parent)
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

    def append(self, widget):
        self.layout().addWidget(widget)


class MainWindow(QtGui.QMainWindow):
    def __init__(self, tutorials):
        super(MainWindow, self).__init__()
        tutorial_list = TutorialList()
        self.setCentralWidget(tutorial_list)
        for each_tutorial in tutorials:
            tutorial_list.append(TUTORIAL_CANVAS[each_tutorial]())


def main():
    app = QtGui.QApplication(["OpenGL Tutorial"])
    arguments = parse_arguments()
    main_window = MainWindow(arguments.tutorials)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
