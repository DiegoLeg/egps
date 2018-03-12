import sys
from functools import partial

import os
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QLabel, QPushButton, QMainWindow, QMessageBox, QFileDialog, QIcon, QRadioButton, QProgressBar, \
    QButtonGroup

from audio_module.audio_module import AudioModule
from config import *

INPUT_GROUP = "input"
OUTPUT_GROUP = "output"
PROCESS_GROUP = "process"

b = [2.844, 0.8472, 0.2055]  # numerador
a = [1., -0.1608, 0.5231]  # denominador


class EGPSWindow(QMainWindow):
    def select_file(self):  # defino el boton descargar
        self.audio_mod.stop_rec()
        file_path = str(QFileDialog.getOpenFileName(self, "Elegir archivo"))
        if file_path != "":
            if file_path.endswith(".wav"):
                self.path_label.setText(file_path)
                self.path_label.resize(self.path_label.minimumSizeHint())
                self.audio_mod.load_file(file_path)
            else:
                self.wrong_file_box.exec_()

    def rec_file_save(self):
        file_path = str(QFileDialog.getSaveFileName(self, 'Guardar archivo'))
        if file_path != "" and not self.audio_mod.save_rec(file_path):
            self.no_data_box.exec_()

    def out_file_save(self):
        file_path = str(QFileDialog.getSaveFileName(self, 'Guardar archivo'))
        recorded = self.input_output[PROCESS_GROUP] == "Grabacion"
        tfs = TRANSFER_FUNCTIONS[self.input_output[INPUT_GROUP]] + TRANSFER_FUNCTIONS[self.input_output[OUTPUT_GROUP]]
        if file_path != "" and not self.audio_mod.save_out(file_path, recorded, *tfs):
            self.no_data_box.exec_()

    def out_file_play(self):
        tfs = TRANSFER_FUNCTIONS[self.input_output[INPUT_GROUP]] + TRANSFER_FUNCTIONS[self.input_output[OUTPUT_GROUP]]
        self.audio_mod.play_out(self.input_output[PROCESS_GROUP] == "Grabacion", *tfs)

    def closeEvent(self, event):
        # Overwriten method from parent QWidget. QWidget -> QMainWindow -> EGPSWindow
        event.ignore()
        if self.msg_box.exec_() == QMessageBox.AcceptRole:
            sys.exit()

    def radio_button_clicked(self, text_option, group_option):
        self.input_output[group_option] = text_option
        print(str(self.input_output))

    def __init__(self):
        # Initialize the parent and the audio_module
        super(EGPSWindow, self).__init__()
        self.audio_mod = AudioModule(OUTPUT_FILE_PATH)

        # Title, size and prevent resize
        win_height = 130 + len(TRANSFER_FUNCTIONS) * 40
        self.setWindowTitle("EGPS-1")
        self.setGeometry(70, 70, 600, win_height)
        self.setFixedSize(600, win_height)

        # The function and list of parameters to create the window labels
        labels_func = self.create_label
        nm_px_py_labels = [("Transductor de entrada", 10, 105), ("Grabacion", 400, 120), ("Salida", 400, 330),
                           ("Archivo de entrada", 10, 10), ("Transductor de salida", 200, 105),
                           ("Entrada a procesar", 400, 230)]

        # The function and list of parameters to create the window radio buttons
        in_bq = QButtonGroup(self)
        out_bq = QButtonGroup(self)
        process_bq = QButtonGroup(self)
        radio_buttons_func = self.create_radio_button
        nm_px_py_cb_radio_buttons = [("Archivo de entrada", 405, 255, PROCESS_GROUP, process_bq),
                                     ("Grabacion", 405, 280, PROCESS_GROUP, process_bq)]
        for index, transfer_function in enumerate(TRANSFER_FUNCTIONS.keys()):
            nm_px_py_cb_radio_buttons.append((transfer_function, 30, 125 + index * 40, INPUT_GROUP, in_bq))
            nm_px_py_cb_radio_buttons.append((transfer_function, 220, 125 + index * 40, OUTPUT_GROUP, out_bq))

        # List of parameters and the function to create the window push buttons
        push_buttons_func = self.define_push_button
        nm_px_py_callb_push_buttons = [
            ("", 55, 70, self.audio_mod.stop_file, STOP_IMAGE_PATH, True), ("Elegir archivo", 15, 35, self.select_file),
            ("", 15, 70, self.audio_mod.play_file, PLAY_IMAGE_PATH, True),
            ("", 405, 145, self.audio_mod.rec, REC_IMAGE_PATH, True),
            ("", 445, 145, self.audio_mod.stop_rec, STOP_IMAGE_PATH, True),
            ("", 485, 145, self.audio_mod.play_rec, PLAY_IMAGE_PATH, True),
            ("", 525, 145, self.rec_file_save, SAVE_IMAGE_PATH, True),
            ("", 405, 355, self.out_file_play, PLAY_IMAGE_PATH, True),
            ("", 445, 355, self.audio_mod.stop_out, STOP_IMAGE_PATH, True),
            ("", 485, 355, self.out_file_save, SAVE_IMAGE_PATH, True)
        ]

        # Define a list of tuples with (constructor, list of constructor params) for the different kind of elements.
        elements_constructors = [(labels_func, nm_px_py_labels), (radio_buttons_func, nm_px_py_cb_radio_buttons),
                                 (push_buttons_func, nm_px_py_callb_push_buttons)]

        # Call constructors for the elements with the parameters of the lists
        for const, params_list in elements_constructors:
            for params in params_list:
                const(*params)

        # Select initial radio buttons
        self.input_output = dict()
        self.input_output[INPUT_GROUP] = str(in_bq.buttons()[0].text())
        self.input_output[OUTPUT_GROUP] = str(out_bq.buttons()[1].text())
        self.input_output[PROCESS_GROUP] = str(process_bq.buttons()[0].text())
        in_bq.buttons()[0].setChecked(True)
        out_bq.buttons()[1].setChecked(True)
        process_bq.buttons()[0].setChecked(True)

        # Define quit pop up
        self.msg_box = QMessageBox()
        self.msg_box.setWindowTitle("Salir")
        self.msg_box.setText("Esta seguro que desea salir?")
        self.msg_box.addButton("Si", QMessageBox.AcceptRole)
        self.msg_box.addButton("No", QMessageBox.RejectRole)

        self.wrong_file_box = QMessageBox()
        self.wrong_file_box.setWindowTitle("Error")
        self.wrong_file_box.setText("El archivo tiene formato incorrecto")

        self.no_data_box = QMessageBox()
        self.no_data_box.setWindowTitle("Error")
        self.no_data_box.setText("No se puede usar esa ruta o no hay datos")

        # Create select play file
        self.path_label = QLabel(os.path.abspath(OUTPUT_FILE_PATH), self)
        self.path_label.move(128, 40)
        self.path_label.resize(self.path_label.minimumSizeHint())

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
            btn.setIcon(QIcon(image_path))
        if resize:
            btn.resize(btn.minimumSizeHint())
        # This binds the signal clicked() from the button to the callback.
        self.connect(btn, SIGNAL("clicked()"), callback)

    def create_radio_button(self, text, pos_x, pos_y, group, button_group):
        radio_button = QRadioButton(text, self)
        radio_button.move(pos_x, pos_y)
        # This binds the signal pressed() from the radio button to the radio_button_clicked method.
        self.connect(radio_button, SIGNAL("pressed()"), partial(self.radio_button_clicked, text, group))
        radio_button.resize(radio_button.minimumSizeHint())
        button_group.addButton(radio_button)
