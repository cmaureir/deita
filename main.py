import sys
from PySide2.QtCore import QSize, Slot
from PySide2.QtWidgets import (QApplication, QMainWindow, QHBoxLayout,
                               QWidget, QPushButton, QTabWidget, QListWidget,
                               QListWidgetItem, QSizePolicy, QAction, QStyle)


class DWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        hlayout = QHBoxLayout()

        ##################################################### Left
        self.menu_level = 0
        self.item_list = QListWidget()
        self.fill_main_item_list()
        self.item_list.setMinimumWidth(256)
        self.item_list.setMaximumWidth(300)
        #self.item_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.item_list.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.item_list.itemClicked[QListWidgetItem].connect(self.item_clicked)

        ##################################################### Right
        b = QTabWidget()
        b.addTab(QWidget(), "Primera")
        b.addTab(QWidget(), "Segunda")
        b.setMinimumWidth(768)
        #b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        b.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)


        hlayout.addWidget(self.item_list)
        hlayout.addWidget(b)
        self.setLayout(hlayout)

    @Slot()
    def item_clicked(self, item):
        self.menu_level += 1
        item_text = item.text()

        if self.menu_level < 2:
            self.item_list.clear()

            item = QListWidgetItem("< Back")
            item.setSizeHint(QSize(item.sizeHint().width(), 50))
            self.item_list.addItem(item)

            for i in range(10):
                item = QListWidgetItem("Sub menu {} ({})".format(i, item_text))
                item.setSizeHint(QSize(item.sizeHint().width(), 50))
                self.item_list.addItem(item)
        elif "Back" in item_text:
            self.item_list.clear()
            self.menu_level = 0
            self.fill_main_item_list()


    def fill_main_item_list(self):
        for i in range(10):
            item = QListWidgetItem("Menu {}".format(i))
            item.setSizeHint(QSize(item.sizeHint().width(), 50))
            self.item_list.addItem(item)


class DWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

         # Menu
        self.menu = self.menuBar()
        #icon = self.style().standardIcon(QStyle.SP_BrowserReload)
        #self.file_menu = self.menu.addMenu(icon, "Fileeee")
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("a nice message to show")

        w = DWidget()
        #geometry = app.desktop().availableGeometry(self)
        #self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)
        self.setCentralWidget(w)

    @Slot()
    def exit_app(self, checked):
        qApp.quit()


def main():
    app = QApplication([])
    w = DWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
