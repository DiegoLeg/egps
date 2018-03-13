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

    def __init__(self):
        # Inicializo el parent y audio module
        super(EGPSWindow, self).__init__()
        self.audio_mod = AudioModule(OUTPUT_FILE_PATH)

        # Titulo, tamano y tamano fijo (no resize)
        win_height = 130 + len(TRANSFER_FUNCTIONS) * 40
        self.setWindowTitle("EGPS-1")
        self.setGeometry(70, 70, 600, win_height)
        self.setFixedSize(600, win_height)

        # Funcion y lista de parametros para la creacion de las labels
        labels_func = self.create_label
        nm_px_py_labels = [("Transductor de entrada", 10, 105), ("Grabacion", 400, 120), ("Salida", 400, 330),
                           ("Archivo de entrada", 10, 10), ("Transductor de salida", 200, 105),
                           ("Entrada a procesar", 400, 230)]

        # Funcion y lista de parametros para la creacion de radiobuttons
        in_bq = QButtonGroup(self)
        out_bq = QButtonGroup(self)
        process_bq = QButtonGroup(self)
        radio_buttons_func = self.create_radio_button
        nm_px_py_cb_radio_buttons = [("Archivo de entrada", 405, 255, PROCESS_GROUP, process_bq),
                                     ("Grabacion", 405, 280, PROCESS_GROUP, process_bq)]

        #Creacion de los radio buttons para el grupo de transductores de entrada y de salida
        for index, transfer_function in enumerate(TRANSFER_FUNCTIONS.keys()):
            nm_px_py_cb_radio_buttons.append((transfer_function, 30, 125 + index * 40, INPUT_GROUP, in_bq))
            nm_px_py_cb_radio_buttons.append((transfer_function, 220, 125 + index * 40, OUTPUT_GROUP, out_bq))


        # Funcion y lista de parametros para la creacion de los pushbuttons
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

        # Se define una lista de tuplas con (constructor, lista de parametros del constructor) para los diferentes
        # tipos de elementos
        elements_constructors = [(labels_func, nm_px_py_labels), (radio_buttons_func, nm_px_py_cb_radio_buttons),
                                 (push_buttons_func, nm_px_py_callb_push_buttons)]


        for const, params_list in elements_constructors:
            for params in params_list:
                const(*params)

        # Se eligen los radiobuttons iniciales
        self.input_output = dict()
        self.input_output[INPUT_GROUP] = str(in_bq.buttons()[0].text())
        self.input_output[OUTPUT_GROUP] = str(out_bq.buttons()[1].text())
        self.input_output[PROCESS_GROUP] = str(process_bq.buttons()[0].text())
        in_bq.buttons()[0].setChecked(True)
        out_bq.buttons()[1].setChecked(True)
        process_bq.buttons()[0].setChecked(True)

        # Se define el pop up para salir de la aplicacion
        self.msg_box = QMessageBox()
        self.msg_box.setWindowTitle("Salir")
        self.msg_box.setText("Esta seguro que desea salir?")
        self.msg_box.addButton("Si", QMessageBox.AcceptRole)
        self.msg_box.addButton("No", QMessageBox.RejectRole)

        # Error para formato incorrecto
        self.wrong_file_box = QMessageBox()
        self.wrong_file_box.setWindowTitle("Error")
        self.wrong_file_box.setText("El archivo tiene formato incorrecto")

        # Error para el path file
        self.no_data_box = QMessageBox()
        self.no_data_box.setWindowTitle("Error")
        self.no_data_box.setText("No se puede utilizar la ruta indicada o los datos son inexistentes")

        # Create select play file
        self.path_label = QLabel(os.path.abspath(OUTPUT_FILE_PATH), self)
        self.path_label.move(128, 40)
        self.path_label.resize(self.path_label.minimumSizeHint())

        # Metodo del parent QWidget. QWidget -> QMainWindow -> EGPSWindow

        self.show()

    def select_file(self):
        """
        Se define un metodo para la eleccion de un archivo de audio existente

        """
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
        """
        Metodo para almacenar el archivo que fue grabado en la etapa de grabacion

        """
        file_path = str(QFileDialog.getSaveFileName(self, 'Guardar archivo'))
        if file_path != "" and not self.audio_mod.save_rec(file_path):
            self.no_data_box.exec_()

    def out_file_save(self):
        """
        Metodo para almacenar el archivo que fue procesado en la etapa de salida

        """
        file_path = str(QFileDialog.getSaveFileName(self, 'Guardar archivo'))
        recorded = self.input_output[PROCESS_GROUP] == "Grabacion"
        tfs = TRANSFER_FUNCTIONS[self.input_output[INPUT_GROUP]] + TRANSFER_FUNCTIONS[self.input_output[OUTPUT_GROUP]]
        if file_path != "" and not self.audio_mod.save_out(file_path, recorded, *tfs):
            self.no_data_box.exec_()

    def out_file_play(self):
        """
        Metodo para reproducir el archivo que fue procesado en la etapa de salida

        """
        tfs = TRANSFER_FUNCTIONS[self.input_output[INPUT_GROUP]] + TRANSFER_FUNCTIONS[self.input_output[OUTPUT_GROUP]]
        self.audio_mod.play_out(self.input_output[PROCESS_GROUP] == "Grabacion", *tfs)

    def closeEvent(self, event):
        """
        Metodo para cerrar la ventana principal

        """
        # Overwriten method from parent QWidget. QWidget -> QMainWindow -> EGPSWindow
        event.ignore()
        if self.msg_box.exec_() == QMessageBox.AcceptRole:
            sys.exit()

    def radio_button_clicked(self, text_option, group_option):
        self.input_output[group_option] = text_option
        print(str(self.input_output))


#-----------------------------------------------------------------------------------------------------------------------
    """Creacion de labels, pushbuttons y radiobuttons"""

    def create_label(self, name, pos_x, pos_y):
        """
        Se define un metodo para la creacion de los labels de la interfaz grafica
        :param name: Nombre del label
        :param pos_x: Posicion horizontal
        :param pos_y: Posicion vertical

        """
        label = QLabel(name, self)
        label.move(pos_x, pos_y)
        label.resize(label.minimumSizeHint())

    def define_push_button(self, text, pos_x, pos_y, callback, image_path=None, resize=False):
        """
        Se define un metodo para la creacion de push buttons en la interfaz grafica

        :param text: Texto que muestra el pushbutton
        :param pos_x: Posicion horizontal
        :param pos_y: Posicion Vertical
        :param callback:
        :param image_path: Ruta del icono o imagen asociada al push button
        :param resize: Cambia el tamano del pushbutton
        :return:
        """
        btn = QPushButton(text, self)
        btn.move(pos_x, pos_y)
        if image_path:
            btn.setIcon(QIcon(image_path))
        if resize:
            btn.resize(btn.minimumSizeHint())
        # This binds the signal clicked() from the button to the callback.
        self.connect(btn, SIGNAL("clicked()"), callback)

    def create_radio_button(self, text, pos_x, pos_y, group, button_group):
        """
        Se define un metodo para la creacion de radio buttons

        :param text: Texto que acompana al radio button
        :param pos_x: Posicion horizontal
        :param pos_y: Posicion vertical
        :param group:
        :param button_group:
        :return:
        """
        radio_button = QRadioButton(text, self)
        radio_button.move(pos_x, pos_y)
        # This binds the signal pressed() from the radio button to the radio_button_clicked method.
        self.connect(radio_button, SIGNAL("pressed()"), partial(self.radio_button_clicked, text, group))
        radio_button.resize(radio_button.minimumSizeHint())
        button_group.addButton(radio_button)
