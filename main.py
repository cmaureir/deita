import sys
from PySide2.QtCore import QSize, Slot, QPropertyAnimation, QObject, QByteArray
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
        #self.item_list.setMinimumWidth(256)
        self.item_list.setMaximumWidth(300)
        self.item_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
        self.shown = True

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

        self.show_action = QAction("Hide", self)
        self.show_action.triggered.connect(self.toggle_left)
        self.file_menu.addAction(self.show_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("a nice message to show")

        self.w = DWidget()
        #geometry = app.desktop().availableGeometry(self)
        #self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)
        self.animation = QPropertyAnimation(self.w.item_list, QByteArray(b"maximumWidth"))
        self.setCentralWidget(self.w)

    @Slot()
    def exit_app(self, checked):
        qApp.quit()

    @Slot()
    def toggle_left(self):
        if self.shown:
            self.animation.setDuration(100)
            self.animation.setStartValue(self.w.item_list.width())
            self.animation.setEndValue(0)
            self.animation.start()
            #self.w.item_list.hide()
            self.show_action.setText("Show")
            self.shown = False
        else:
            self.animation.setDuration(100)
            self.animation.setStartValue(0)
            self.animation.setEndValue(300)
            self.animation.start()
            #self.w.item_list.show()
            self.show_action.setText("Hide")
            self.shown = True



def main():
    app = QApplication([])
    w = DWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
