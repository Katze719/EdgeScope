import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore

class AreaSelector(QtWidgets.QWidget):
    selection_done = QtCore.pyqtSignal(QtCore.QRect)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bereich auswählen")
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.setWindowOpacity(0.3)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.start = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.is_selecting = False

    def mousePressEvent(self, event):
        self.start = event.pos()
        self.end = event.pos()
        self.is_selecting = True
        self.update()

    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()
        self.is_selecting = False
        self.update()
        rect = QtCore.QRect(self.start, self.end).normalized()
        self.selection_done.emit(rect)
        self.close()

    def paintEvent(self, event):
        if self.is_selecting:
            painter = QtGui.QPainter(self)
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 2))
            rect = QtCore.QRect(self.start, self.end)
            painter.drawRect(rect.normalized())

class OverlayWindow(QtWidgets.QWidget):
    def __init__(self, capture_rect):
        super().__init__()
        self.capture_rect = capture_rect
        self.setWindowTitle("Edge Detection Overlay")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.initUI()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_image)
        self.timer.start(1000)  # Aktualisierung alle 1000ms

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        # Anzeige des Bildes
        self.image_label = QtWidgets.QLabel("Edge Detection Output")
        self.image_label.setStyleSheet("background-color: rgba(0, 0, 0, 150);")
        layout.addWidget(self.image_label)

        # Slider für unteren Schwellenwert
        lower_label = QtWidgets.QLabel("Lower Threshold:")
        lower_label.setStyleSheet("background-color: rgba(0, 0, 0, 150); color: white; padding: 5px;")
        layout.addWidget(lower_label)

        self.lower_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.lower_slider.setMinimum(0)
        self.lower_slider.setMaximum(255)
        self.lower_slider.setValue(50)
        self.lower_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.lower_slider.setTickInterval(5)
        layout.addWidget(self.lower_slider)

        # Slider für oberen Schwellenwert
        upper_label = QtWidgets.QLabel("Upper Threshold:")
        upper_label.setStyleSheet("background-color: rgba(0, 0, 0, 150); color: white; padding: 5px;")
        layout.addWidget(upper_label)

        self.upper_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.upper_slider.setMinimum(0)
        self.upper_slider.setMaximum(255)
        self.upper_slider.setValue(150)
        self.upper_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.upper_slider.setTickInterval(5)
        layout.addWidget(self.upper_slider)

        self.setLayout(layout)
        self.resize(400, 400)
        self.move(100, 100)

    def update_image(self):
        # Screenshot des definierten Bereichs
        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow(0, self.capture_rect.x(), self.capture_rect.y(),
                                         self.capture_rect.width(), self.capture_rect.height())
        # Konvertiere QPixmap zu cv2 Bild
        image = self.qpixmap_to_cv2(screenshot)
        # Konvertiere in Graustufen
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Hole Schwellenwerte von den Slidern
        lower_val = self.lower_slider.value()
        upper_val = self.upper_slider.value()
        # Wende Canny Edge Detection an
        edges = cv2.Canny(gray, lower_val, upper_val)
        # Konvertiere das Ergebnis in QPixmap und zeige es an
        pixmap = self.cv2_to_qpixmap(edges)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def qpixmap_to_cv2(self, qpixmap):
        qimage = qpixmap.toImage()
        qimage = qimage.convertToFormat(QtGui.QImage.Format.Format_RGBA8888)
        width = qimage.width()
        height = qimage.height()
        ptr = qimage.bits()
        ptr.setsize(height * width * 4)
        arr = np.array(ptr).reshape(height, width, 4)
        image = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
        return image

    def cv2_to_qpixmap(self, img):
        # Annahme: img ist ein Graustufenbild
        height, width = img.shape
        bytes_per_line = width
        qimg = QtGui.QImage(img.data, width, height, bytes_per_line, QtGui.QImage.Format_Grayscale8)
        return QtGui.QPixmap.fromImage(qimg)

def main():
    app = QtWidgets.QApplication(sys.argv)
    selector = AreaSelector()
    selector.selection_done.connect(lambda rect: on_area_selected(rect, app))
    selector.show()
    sys.exit(app.exec_())

def on_area_selected(rect, app):
    overlay = OverlayWindow(rect)
    overlay.show()

if __name__ == '__main__':
    main()
