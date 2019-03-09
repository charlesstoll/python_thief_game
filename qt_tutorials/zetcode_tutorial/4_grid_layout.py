#!/bin/python3

import sys
from PyQt5.QtWidgets import *

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        names = ['Cls', 'Bck', '', 'Close', 
                '7', '8', '9', '/', 
                '4', '5', '6', '*', 
                '1', '2', '3', '-', 
                '0', '.', '=', '+']

        positions = [(i, j) for i in range(5) for j in range(4)]
        for position, name in zip(positions, names):
            if name == '':
                continue
            button = QPushButton(name)
            grid.addWidget(button, *position)

        grid.setSpacing(5)

        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid.addWidget(title, 5, 0)
        grid.addWidget(titleEdit, 5, 1, 1, 3)
        
        grid.addWidget(author, 6, 0)
        grid.addWidget(authorEdit, 6, 1, 1, 3)

        grid.addWidget(review, 7, 0)
        grid.addWidget(reviewEdit, 7, 1, 5, 3)

        self.move(300, 150)
        self.setWindowTitle('Calc')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
