import sys
from PyQt4 import QtGui
from functools import partial

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QLabel, QPushButton, QMainWindow, QMessageBox

from audio_module import audio_module
from config import *


class EGPSWindow(QMainWindow):

    def download(self):  # defino el boton descargar
        self.completed = 0  # punto de partida del progress bar
        while self.completed < 100:
            self.completed += 0.001  # le voy sumando de a estos pasos redefiniendo self.completed
            self.progress.setValue(self.completed)  # seteo el valor como el de self.completed

    def file_save(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Guardar Archivo')
        file = save(name, 'w')

    def closeEvent(self, event):
        # Overwriten method from parent QWidget. QWidget -> QMainWindow -> EGPSWindow
        event.ignore()
        if self.msg_box.exec_() == QMessageBox.AcceptRole:
            sys.exit()

    def radio_button_clicked(self, option):
        self.statusBar().showMessage(option)
        print(option)

    def __init__(self):
        # Initialize the parent and the audio_module
        super(EGPSWindow, self).__init__()
        self.audio_mod = audio_module.AudioModule()

        # Title, size and prevent resize
        self.setWindowTitle("EGPS-1")
        self.setGeometry(70, 70, 780, 500)
        self.setFixedSize(780, 500)

        self.statusBar()  # do not touch
        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(250, 410, 250, 20)

        # The function and list of parameters to create the window labels
        labels_func = self.create_label
        nm_px_py_labels = [("Transductor de entrada", 80, 60), ("Transductor de salida", 500, 60), ("MAF", 520, 96),
                           ("MCF", 520, 136), ("MVF", 520, 176), ("MNF", 520, 216), ("MRF", 520, 256),
                           ("MT-N", 520, 296), ("MT-B", 520, 336), ("MAF", 520, 96), ("MAF", 520, 96), ("MAF", 520, 96),
                           ("MAF", 520, 96), ("MAF", 520, 96)]

        # The function and list of parameters to create the window radio buttons
        radio_buttons_func = self.create_radio_button
        nm_px_py_callb_radio_buttons = [("MAF", 100, 90,), ("MCF", 100, 130), ("MVF", 100, 170), ("MNF", 100, 210),
                                        ("MRF", 100, 250), ("MT-N", 100, 290), ("MT-B", 100, 330)]


        # List of parameters and the function to create the window push buttons
        push_buttons_func = self.define_push_button
        nm_px_py_callb_push_buttons = [
            ("Procesar", 304, 350, self.audio_mod.process, None), ("REC", 254, 190, self.audio_mod.rec, REC_IMAGE_PATH),
            ("STOP", 354, 190, self.audio_mod.stop, STOP_IMAGE_PATH), ("NEW", 304, 140, self.download, NEW_IMAGE_PATH),
            ("", 650, 126, self.download, SAVE_IMAGE_PATH, True), ("", 650, 166, self.download, SAVE_IMAGE_PATH, True),
            ("", 650, 206, self.download, SAVE_IMAGE_PATH, True), ("", 650, 246, self.download, SAVE_IMAGE_PATH, True),
            ("", 650, 286, self.download, SAVE_IMAGE_PATH, True), ("", 650, 326, self.download, SAVE_IMAGE_PATH, True),
            ("PLAY", 304, 240, self.audio_mod.play, PLAY_IMAGE_PATH),
            ("", 570, 86, self.audio_mod.play, PLAY_IMAGE_PATH, True),
            ("", 570, 126, self.audio_mod.play, PLAY_IMAGE_PATH, True),
            ("", 570, 166, self.audio_mod.play, PLAY_IMAGE_PATH, True),
            ("", 570, 206, self.audio_mod.play, PLAY_IMAGE_PATH, True),
            ("", 570, 246, self.audio_mod.play, PLAY_IMAGE_PATH, True),
            ("", 570, 286, self.audio_mod.play, PLAY_IMAGE_PATH, True),
            ("", 570, 326, self.audio_mod.play, PLAY_IMAGE_PATH, True),
            ("", 610, 86, self.audio_mod.stop, STOP_IMAGE_PATH, True),
            ("", 610, 126, self.audio_mod.stop, STOP_IMAGE_PATH, True),
            ("", 610, 166, self.audio_mod.stop, STOP_IMAGE_PATH, True),
            ("", 610, 206, self.audio_mod.stop, STOP_IMAGE_PATH, True),
            ("", 610, 246, self.audio_mod.stop, STOP_IMAGE_PATH, True),
            ("", 610, 286, self.audio_mod.stop, STOP_IMAGE_PATH, True),
            ("", 610, 326, self.audio_mod.stop, STOP_IMAGE_PATH, True),
            ("", 650, 86, self.download, SAVE_IMAGE_PATH, True)
        ]

        # Define a list of tuples with (constructor, list of constructor params) for the different kind of elements.
        elements_constructors = [(labels_func, nm_px_py_labels), (radio_buttons_func, nm_px_py_callb_radio_buttons),
                                 (push_buttons_func, nm_px_py_callb_push_buttons)]

        # Call constructors for the elements with the parameters of the lists
        for const, params_list in elements_constructors:
            for params in params_list:
                const(*params)

        # Define quit pop up
        self.msg_box = QMessageBox()
        self.msg_box.setWindowTitle("Salir")
        self.msg_box.setText("Esta seguro que desea salir?")
        self.msg_box.addButton("Si", QMessageBox.AcceptRole)
        self.msg_box.addButton("No", QMessageBox.RejectRole)

        # Method from parent QWidget. QWidget -> QMainWindow -> EGPSWindow
        self.show()

    def create_label(self, name, pos_x, pos_y):
        label = QLabel(name, self)
        label.move(pos_x, pos_y)
        label.resize(label.minimumSizeHint())

    def define_push_button(self, text, pos_x, pos_y, callback, image_path=None, resize=False):
        btn = QPushButton(text, self)
        btn.move(pos_x, pos_y)
        if image_path:
            btn.setIcon(QtGui.QIcon(image_path))
        if resize:
            btn.resize(btn.minimumSizeHint())
        # This binds the signal clicked() from the button to the callback.
        self.connect(btn, SIGNAL("clicked()"), callback)

    def create_radio_button(self, text, pos_x, pos_y):
        radio_button = QtGui.QRadioButton(text, self)
        radio_button.move(pos_x, pos_y)
        # This binds the signal pressed() from the radio button to the radio_button_clicked method.
        self.connect(radio_button, SIGNAL("pressed()"), partial(self.radio_button_clicked, text))
