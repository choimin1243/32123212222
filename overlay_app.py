import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap, QGuiApplication
from PyQt5.QtCore import Qt, QPoint

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transparent Overlay")
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()

        self.drawing = False
        self.last_point = QPoint()
        self.mode = "draw"

        self.canvas = QPixmap(self.size())
        self.canvas.fill(Qt.transparent)

        self.initUI()

    def initUI(self):
        self.draw_btn = QPushButton("Draw", self)
        self.draw_btn.move(20, 20)
        self.draw_btn.clicked.connect(lambda: self.set_mode("draw"))

        self.erase_btn = QPushButton("Erase", self)
        self.erase_btn.move(100, 20)
        self.erase_btn.clicked.connect(lambda: self.set_mode("erase"))

        self.capture_btn = QPushButton("Capture", self)
        self.capture_btn.move(180, 20)
        self.capture_btn.clicked.connect(self.capture_screen)

    def set_mode(self, mode):
        self.mode = mode

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.canvas)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.canvas)
            if self.mode == "draw":
                pen = QPen(QColor(255, 0, 0), 3, Qt.SolidLine)
            else:
                pen = QPen(Qt.transparent, 20)
                painter.setCompositionMode(QPainter.CompositionMode_Clear)

            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def capture_screen(self):
        screen = QGuiApplication.primaryScreen()
        screenshot = screen.grabWindow(0)
        screenshot.save("capture.png", "png")
        print("Saved capture.png")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Overlay()
    window.show()
    sys.exit(app.exec_())
