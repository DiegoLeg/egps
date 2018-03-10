import sys
from PyQt4 import QtGui

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QLabel, QPushButton, QMainWindow

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

    def close_application(self):  # llamo a close_application arriba
        choice = QtGui.QMessageBox.question(self, 'Salir', "Esta seguro que desea salir?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if choice == QtGui.QMessageBox.Yes:
            sys.exit()  # cierra la app al apretar el boton
        else:
            pass

    def closeEvent(self, event):  # defino este nuevo metodo para que aparezca el popup tambien si hago clic en la cruz roja
        event.ignore()
        self.close_application()

    def radio_action(self, pressed):  # defino este nuevo metodo para que el radio button haga una cosa u otra segun si esta apretado o no

        if pressed:
            print ("down")
        else:
            print ("up")

    # ------------------------------------------------------------------
    # Audio Module

    def rec(self):
        self.audio_mod.rec()

    def play(self):
        self.audio_mod.play()

    def stop(self):
        self.audio_mod.stop()

    def process(self):
        self.audio_mod.process()

    # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
    # Defino que quiero que haga cada radiobutton

    def buttonClicked(self, a):  # obtengo la string de que radioButton esta presionado
        sender = self.sender()
        self.statusBar().showMessage(sender.text())
        a = sender.text()
        # print a
        if a == ("MAF"):
            print ("1")  # aca iria lo que quiero que haga una vez presiono en MAF
            # process(MAF)
        elif a == ("MCF"):
            print ("2")
        elif a == ("MVF"):
            print ("3")
        elif a == ("MNF"):
            print ("4")
        elif a == ("MRF"):
            print ("5")
        elif a == ("MT-N"):
            print ("6")
        elif a == ("MT-B"):
            print ("7")
        else:
            print ("DAH")

    def __init__(self):
        super(EGPSWindow, self).__init__()

        self.setGeometry(70, 70, 780, 500)
        self.setWindowTitle("EGPS-1")
        # TODO: desactivar resize
        self.statusBar()  # do not touch
        self.audio_mod = audio_module.AudioModule()

        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(250, 410, 250, 20)

        nm_px_py_labels = [("Transductor de entrada", 80, 60), ("Transductor de salida", 500, 60), ("MAF", 520, 96),
                           ("MCF", 520, 136), ("MVF", 520, 176), ("MNF", 520, 216), ("MRF", 520, 256),
                           ("MT-N", 520, 296), ("MT-B", 520, 336), ("MAF", 520, 96), ("MAF", 520, 96), ("MAF", 520, 96),
                           ("MAF", 520, 96), ("MAF", 520, 96)]
        labels_func = self.create_label

        nm_px_py_callb_radio_buttons = [("MAF", 100, 90, self.buttonClicked), ("MCF", 100, 130, self.buttonClicked),
                                        ("MVF", 100, 170, self.buttonClicked), ("MNF", 100, 210, self.buttonClicked),
                                        ("MRF", 100, 250, self.buttonClicked), ("MT-N", 100, 290, self.buttonClicked),
                                        ("MT-B", 100, 330, self.buttonClicked)]
        radio_buttons_func = self.create_radio_button

        nm_px_py_callb_push_buttons = [
            ("Procesar", 304, 350, self.process, None), ("REC", 254, 190, self.rec, REC_IMAGE_PATH),
            ("STOP", 354, 190, self.stop, STOP_IMAGE_PATH), ("NEW", 304, 140, self.download, NEW_IMAGE_PATH),
            ("PLAY", 304, 240, self.play, PLAY_IMAGE_PATH), ("", 570, 86, self.play, PLAY_IMAGE_PATH, True),
            ("", 570, 126, self.play, PLAY_IMAGE_PATH, True), ("", 570, 166, self.play, PLAY_IMAGE_PATH, True),
            ("", 570, 206, self.play, PLAY_IMAGE_PATH, True), ("", 570, 246, self.play, PLAY_IMAGE_PATH, True),
            ("", 570, 286, self.play, PLAY_IMAGE_PATH, True), ("", 570, 326, self.play, PLAY_IMAGE_PATH, True),
            ("", 610, 86, self.stop, STOP_IMAGE_PATH, True), ("", 610, 126, self.stop, STOP_IMAGE_PATH, True),
            ("", 610, 166, self.stop, STOP_IMAGE_PATH, True), ("", 610, 206, self.stop, STOP_IMAGE_PATH, True),
            ("", 610, 246, self.stop, STOP_IMAGE_PATH, True), ("", 610, 286, self.stop, STOP_IMAGE_PATH, True),
            ("", 610, 326, self.stop, STOP_IMAGE_PATH, True), ("", 650, 86, self.download, SAVE_IMAGE_PATH, True),
            ("", 650, 126, self.download, SAVE_IMAGE_PATH, True), ("", 650, 166, self.download, SAVE_IMAGE_PATH, True),
            ("", 650, 206, self.download, SAVE_IMAGE_PATH, True), ("", 650, 246, self.download, SAVE_IMAGE_PATH, True),
            ("", 650, 286, self.download, SAVE_IMAGE_PATH, True), ("", 650, 326, self.download, SAVE_IMAGE_PATH, True)
        ]
        push_buttons_func = self.define_push_button

        elements_constructors = [(labels_func, nm_px_py_labels), (radio_buttons_func, nm_px_py_callb_radio_buttons),
                                 (push_buttons_func, nm_px_py_callb_push_buttons)]

        for func, params_list in elements_constructors:
            for params in params_list:
                func(*params)

        # method from parent QWidget. QWidget -> QMainWindow -> EGPSWindow
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
        # this binds the signal clicked() from the button to the callback.
        self.connect(btn, SIGNAL("clicked()"), callback)

    def create_radio_button(self, text, pos_x, pos_y, callback):
        radio_button = QtGui.QRadioButton(text, self)
        radio_button.move(pos_x, pos_y)
        self.connect(radio_button, SIGNAL("toggled()"), callback)

