import os
import shutil
from threading import Thread

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
import PyQt5.QtWidgets
import Links
import sys
from Processor import Processor


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.files = []
        self.processor = Processor(Links.Watermark, Links.Temp)

    def assemble(self):
        uic.loadUi(Links.UI_MAIN, self)
        icon = QIcon(Links.Watermark)

        self.setWindowTitle(Links.Title)
        self.setWindowIcon(icon)
        self.watermark.setStyleSheet(Links.StyleWatermarkBG)

        self.add_image.clicked.connect(self.add_image_def)
        self.remove_image.clicked.connect(self.remove_image_def)
        self.start.clicked.connect(self.start_def)
        self.output_directory_button.clicked.connect(self.save_directory_def)

        self.images.itemClicked.connect(self.set_preview)

        self.watermark_width.valueChanged.connect(self.set_watermark_size)
        self.watermark_height.valueChanged.connect(self.set_watermark_size)

        self.watermark_position_x.valueChanged.connect(self.set_watermark_position)
        self.watermark_position_y.valueChanged.connect(self.set_watermark_position)

    def add_image_def(self):
        file, selected = PyQt5.QtWidgets.QFileDialog.getOpenFileName(
            caption="Select Image",
            filter="*.png *.jpg"
        )

        if selected:
            self.files.append(file)
            icon = QIcon(file)
            label = PyQt5.QtWidgets.QListWidgetItem(icon, file)

            self.images.addItem(label)

    def save_directory_def(self):
        try:
            dir = PyQt5.QtWidgets.QFileDialog.getExistingDirectory()
            self.directory.setText(dir)
            self.processor.save_folder = dir
        except Exception as e:
            print(e)

    def set_preview(self):
        path = self.images.currentItem().text()

        self.processor.generate_preview(path)
        self.preview.setStyleSheet(Links.StylePreviewBG)

    def set_watermark_size(self):
        self.processor.watermark_size = (
            self.watermark_width.value(),
            self.watermark_height.value()
        )

        if self.images.currentItem():
            self.set_preview()

    def set_watermark_position(self):
        self.processor.watermark_position = (
            self.watermark_position_x.value(),
            self.watermark_position_y.value()
        )

        if self.images.currentItem():
            self.set_preview()

    def start_def(self):
        try:
            thread = Thread(
                target=self.processor.start_batch_process,
                args=(self.files, self.update_ui)
            )
            thread.start()

        except Exception as e:
            print(e)

    def update_ui(self, text):
        switch = text == 'START'
        self.start.setEnabled(switch)
        self.start.setText(text)

    def remove_image_def(self):
        selected = self.images.currentItem()

        if selected:
            self.files.remove(selected.text())

            row = self.images.row(selected)
            self.images.takeItem(row)

    def run(self):
        self.show()


def clear_temp_folder():
    folder = Links.Temp
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


app = QtWidgets.QApplication(sys.argv)
window = Window()
window.assemble()
window.run()
app.exec_()
clear_temp_folder()
