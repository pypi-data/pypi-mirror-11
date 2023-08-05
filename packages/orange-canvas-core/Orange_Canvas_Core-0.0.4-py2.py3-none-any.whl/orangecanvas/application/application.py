"""
Orange Canvas Application

"""

from PyQt4.QtGui import QApplication

from PyQt4.QtCore import Qt, QUrl, QEvent, pyqtSignal as Signal


class CanvasApplication(QApplication):
    fileOpenRequest = Signal(QUrl)

    def __init__(self, argv):
        QApplication.__init__(self, argv)
        self.setAttribute(Qt.AA_DontShowIconsInMenus, True)

    def event(self, event):
        if event.type() == QEvent.FileOpen:
            self.fileOpenRequest.emit(event.url())

        return QApplication.event(self, event)
