#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)
        vbox.addStretch(1)

        btn1 = QPushButton("Button 1", self)
        btn2 = QPushButton("Button 2", self)
        self.lbl = QLabel("starting text", self)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(btn1)
        vbox2.addWidget(btn2)
        vbox2.addWidget(self.lbl)
        vbox2.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addLayout(vbox2)
        hbox.addStretch(1)

        self.setLayout(hbox)

        # now add events
        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        sld.valueChanged.connect(lcd.display)
       
        x = 0
        y = 0

        self.text = "x: {0}, y: {1}".format(x, y)

        self.label = QLabel(self.text, self)
        vbox.addWidget(self.label)

        self.setMouseTracking(True)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Signal and slot')
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()

        text = "x: {0}, y: {1}".format(x, y)
        self.label.setText(text)

    def buttonClicked(self):
        sender = self.sender()
        self.lbl.setText(sender.text() + ' was pressed')
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
