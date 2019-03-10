#!/bin/python3

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.statusbar = self.statusBar() 
        self.statusbar.showMessage('Ready')
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        
        # create an action located in the file menu
        exitAct = QAction(QIcon('mario.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAct)

        # create a new submenu that has an action
        impMenu = QMenu('Import', self)
        impAct = QAction('Import mail', self)
        impMenu.addAction(impAct)
        fileMenu.addMenu(impMenu)
        
        # create a new action
        newAct = QAction('New', self)
        fileMenu.addAction(newAct)

        # view menu stuff
        viewMenu = menubar.addMenu('View')

        viewStatAct = QAction('View statusbar', self, checkable=True)
        viewStatAct.setStatusTip('View statusbar')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.toggleMenu)
        viewMenu.addAction(viewStatAct)

        exit2Act = QAction(QIcon('mario.png'), 'Exit2', self)
        exit2Act.setShortcut('Ctrl+E')
        exit2Act.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('Exit2')
        self.toolbar.addAction(exit2Act)

        # create a central widget
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        # other stuffffffff soooo booooooring
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Statusbar')

        self.show()

    def toggleMenu(self, state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

    def contextMenuEvent(self, event):
        cmenu = QMenu(self)

        newAct = cmenu.addAction("New")
        openAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        if action == quitAct:
            qApp.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
