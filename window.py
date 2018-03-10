import sys
from PyQt4 import QtGui

from audio_module import audio_module
from config import *


class Window(QtGui.QMainWindow):

    def __init__(self):

        super(Window, self).__init__()                  # parent
        self.setGeometry(70, 70, 780, 500)
        self.setWindowTitle("EGPS-1")

        extractAction = QtGui.QAction("&Salir", self)  # Nombre del submenu representativo de lo que quiero que haga
        extractAction.setShortcut("Ctrl+Q")  # shortcut
        extractAction.setStatusTip("Salir de la app")
        extractAction.triggered.connect(
        self.close_application)                         # lo que quiero que haga ese submenu cuando le haga clic, cerrar la app

        saveFile = QtGui.QAction("Guardar como...", self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip('Guardar Archivo')
        saveFile.triggered.connect(self.file_save)

        self.statusBar()  # do not touch

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&Archivo')                 #Nombre del menu
        fileMenu.addAction(saveFile)
        fileMenu.addAction(extractAction)

        self.audio_mod = audio_module.AudioModule()

        self.home()                                             #Defino home mas abajo

    def home(self):

        label1 = QtGui.QLabel("Transductor de entrada", self)
        label1.move(80, 60)
        label1.resize(label1.minimumSizeHint())

        label2 = QtGui.QLabel("Transductor de salida", self)
        label2.move(500, 60)
        label2.resize(label1.minimumSizeHint())


        self.progress = QtGui.QProgressBar(self)                # hago un progress bar
        self.progress.setGeometry(250, 410, 250, 20)            # dimensiones del progress bar

        self.btn = QtGui.QPushButton("Procesar", self)          # hago un push button que activa el progress bar
        self.btn.move(304, 350)                                 # donde va ubicado el boton
        self.btn.clicked.connect(self.process)                  # que es lo que hace el boton. Tengo que definir un metodo download

        self.btn2 = QtGui.QPushButton("REC", self)
        self.btn2.move(254, 190)
        self.btn2.setIcon(QtGui.QIcon(REC_IMAGE_PATH))
        self.btn2.clicked.connect(self.rec)

        self.btn3 = QtGui.QPushButton("STOP", self)
        self.btn3.move(354, 190)
        self.btn3.setIcon(QtGui.QIcon(STOP_IMAGE_PATH))
        self.btn3.clicked.connect(self.stop)

        self.btn4 = QtGui.QPushButton("NEW", self)
        self.btn4.move(304, 140)
        self.btn4.setIcon(QtGui.QIcon(NEW_IMAGE_PATH))
        self.btn4.clicked.connect(self.download)

        self.btn5 = QtGui.QPushButton("PLAY", self)
        self.btn5.move(304, 240)
        self.btn5.setIcon(QtGui.QIcon(PLAY_IMAGE_PATH))
        self.btn5.clicked.connect(self.play)

        # --------------------------------------------------------------------------------

        # RadioButtons

        radioButton1 = QtGui.QRadioButton("MAF", self)
        radioButton1.move(100, 90)
        radioButton1.toggled.connect(self.buttonClicked)  # accion del radiobutton

        radioButton2 = QtGui.QRadioButton("MCF", self)
        radioButton2.move(100, 130)
        radioButton2.toggled.connect(self.buttonClicked)

        radioButton3 = QtGui.QRadioButton("MVF", self)
        radioButton3.move(100, 170)
        radioButton3.toggled.connect(self.buttonClicked)

        radioButton4 = QtGui.QRadioButton("MNF", self)
        radioButton4.move(100, 210)
        radioButton4.toggled.connect(self.buttonClicked)

        radioButton5 = QtGui.QRadioButton("MRF", self)
        radioButton5.move(100, 250)
        radioButton5.toggled.connect(self.buttonClicked)

        radioButton6 = QtGui.QRadioButton("MT-N", self)
        radioButton6.move(100, 290)
        radioButton6.toggled.connect(self.buttonClicked)

        radioButton7 = QtGui.QRadioButton("MT-B", self)
        radioButton7.move(100, 330)
        radioButton7.toggled.connect(self.buttonClicked)

        # ----------------------------------------------------------------------------------

        # Labels del lado derecho

        output_label1 = QtGui.QLabel("MAF", self)
        output_label1.move(520, 96)
        output_label1.resize(label1.minimumSizeHint())

        output_label2 = QtGui.QLabel("MCF", self)
        output_label2.move(520, 136)
        output_label2.resize(label1.minimumSizeHint())

        output_label3 = QtGui.QLabel("MVF", self)
        output_label3.move(520, 176)
        output_label3.resize(label1.minimumSizeHint())

        output_label4 = QtGui.QLabel("MNF", self)
        output_label4.move(520, 216)
        output_label4.resize(label1.minimumSizeHint())

        output_label5 = QtGui.QLabel("MRF", self)
        output_label5.move(520, 256)
        output_label5.resize(label1.minimumSizeHint())

        output_label6 = QtGui.QLabel("MT-N", self)
        output_label6.move(520, 296)
        output_label6.resize(label1.minimumSizeHint())

        output_label7 = QtGui.QLabel("MT-B", self)
        output_label7.move(520, 336)
        output_label7.resize(label1.minimumSizeHint())

        # ----------------------------------------------------------------------
        # Buttons lado derecho

        self.play_Maf = QtGui.QPushButton("", self)
        self.play_Maf.move(570, 86)
        self.play_Maf.setIcon(QtGui.QIcon(PLAY_IMAGE_PATH))
        self.play_Maf.resize(self.play_Maf.minimumSizeHint())
        self.play_Maf.clicked.connect(self.play)

        self.play_Mcf = QtGui.QPushButton("", self)
        self.play_Mcf.move(570, 126)
        self.play_Mcf.setIcon(QtGui.QIcon(PLAY_IMAGE_PATH))
        self.play_Mcf.resize(self.play_Mcf.minimumSizeHint())
        self.play_Mcf.clicked.connect(self.download)

        self.play_Mvf = QtGui.QPushButton("", self)
        self.play_Mvf.move(570, 166)
        self.play_Mvf.setIcon(QtGui.QIcon(PLAY_IMAGE_PATH))
        self.play_Mvf.resize(self.play_Mvf.minimumSizeHint())
        self.play_Mvf.clicked.connect(self.download)

        self.play_Mnf = QtGui.QPushButton("", self)
        self.play_Mnf.move(570, 206)
        self.play_Mnf.setIcon(QtGui.QIcon(PLAY_IMAGE_PATH))
        self.play_Mnf.resize(self.play_Mnf.minimumSizeHint())
        self.play_Mnf.clicked.connect(self.download)

        self.play_Mrf = QtGui.QPushButton("", self)
        self.play_Mrf.move(570, 246)
        self.play_Mrf.setIcon(QtGui.QIcon(PLAY_IMAGE_PATH))
        self.play_Mrf.resize(self.play_Mrf.minimumSizeHint())
        self.play_Mrf.clicked.connect(self.download)

        self.play_Mtn = QtGui.QPushButton("", self)
        self.play_Mtn.move(570, 286)
        self.play_Mtn.setIcon(QtGui.QIcon(PLAY_IMAGE_PATH))
        self.play_Mtn.resize(self.play_Mtn.minimumSizeHint())
        self.play_Mtn.clicked.connect(self.download)

        self.play_Mtb = QtGui.QPushButton("", self)
        self.play_Mtb.move(570, 326)
        self.play_Mtb.setIcon(QtGui.QIcon(PLAY_IMAGE_PATH))
        self.play_Mtb.resize(self.play_Mtb.minimumSizeHint())
        self.play_Mtb.clicked.connect(self.download)
        # ----------------------------------------------------------------------

        self.stop_Maf = QtGui.QPushButton("", self)
        self.stop_Maf.move(610, 86)
        self.stop_Maf.setIcon(QtGui.QIcon(STOP_IMAGE_PATH))
        self.stop_Maf.resize(self.stop_Maf.minimumSizeHint())
        self.stop_Maf.clicked.connect(self.download)

        self.stop_Mcf = QtGui.QPushButton("", self)
        self.stop_Mcf.move(610, 126)
        self.stop_Mcf.setIcon(QtGui.QIcon(STOP_IMAGE_PATH))
        self.stop_Mcf.resize(self.stop_Mcf.minimumSizeHint())
        self.stop_Mcf.clicked.connect(self.download)

        self.stop_Mvf = QtGui.QPushButton("", self)
        self.stop_Mvf.move(610, 166)
        self.stop_Mvf.setIcon(QtGui.QIcon(STOP_IMAGE_PATH))
        self.stop_Mvf.resize(self.stop_Mvf.minimumSizeHint())
        self.stop_Mvf.clicked.connect(self.download)

        self.stop_Mnf = QtGui.QPushButton("", self)
        self.stop_Mnf.move(610, 206)
        self.stop_Mnf.setIcon(QtGui.QIcon(STOP_IMAGE_PATH))
        self.stop_Mnf.resize(self.stop_Mnf.minimumSizeHint())
        self.stop_Mnf.clicked.connect(self.download)

        self.stop_Mrf = QtGui.QPushButton("", self)
        self.stop_Mrf.move(610, 246)
        self.stop_Mrf.setIcon(QtGui.QIcon(STOP_IMAGE_PATH))
        self.stop_Mrf.resize(self.stop_Mrf.minimumSizeHint())
        self.stop_Mrf.clicked.connect(self.download)

        self.stop_Mtn = QtGui.QPushButton("", self)
        self.stop_Mtn.move(610, 286)
        self.stop_Mtn.setIcon(QtGui.QIcon(STOP_IMAGE_PATH))
        self.stop_Mtn.resize(self.stop_Mtn.minimumSizeHint())
        self.stop_Mtn.clicked.connect(self.download)

        self.stop_Mtb = QtGui.QPushButton("", self)
        self.stop_Mtb.move(610, 326)
        self.stop_Mtb.setIcon(QtGui.QIcon(STOP_IMAGE_PATH))
        self.stop_Mtb.resize(self.stop_Mtb.minimumSizeHint())
        self.stop_Mtb.clicked.connect(self.download)

        # ----------------------------------------------------------------------

        self.save_Maf = QtGui.QPushButton("", self)
        self.save_Maf.move(650, 86)
        self.save_Maf.setIcon(QtGui.QIcon(SAVE_IMAGE_PATH))
        self.save_Maf.resize(self.save_Maf.minimumSizeHint())
        self.save_Maf.clicked.connect(self.file_save)

        self.save_Mcf = QtGui.QPushButton("", self)
        self.save_Mcf.move(650, 126)
        self.save_Mcf.setIcon(QtGui.QIcon(SAVE_IMAGE_PATH))
        self.save_Mcf.resize(self.save_Mcf.minimumSizeHint())
        self.save_Mcf.clicked.connect(self.file_save)

        self.save_Mvf = QtGui.QPushButton("", self)
        self.save_Mvf.move(650, 166)
        self.save_Mvf.setIcon(QtGui.QIcon(SAVE_IMAGE_PATH))
        self.save_Mvf.resize(self.save_Mvf.minimumSizeHint())
        self.save_Mvf.clicked.connect(self.file_save)

        self.save_Mnf = QtGui.QPushButton("", self)
        self.save_Mnf.move(650, 206)
        self.save_Mnf.setIcon(QtGui.QIcon(SAVE_IMAGE_PATH))
        self.save_Mnf.resize(self.save_Mnf.minimumSizeHint())
        self.save_Mnf.clicked.connect(self.file_save)

        self.save_Mrf = QtGui.QPushButton("", self)
        self.save_Mrf.move(650, 246)
        self.save_Mrf.setIcon(QtGui.QIcon(SAVE_IMAGE_PATH))
        self.save_Mrf.resize(self.save_Mrf.minimumSizeHint())
        self.save_Mrf.clicked.connect(self.file_save)

        self.save_Mtn = QtGui.QPushButton("", self)
        self.save_Mtn.move(650, 286)
        self.save_Mtn.setIcon(QtGui.QIcon(SAVE_IMAGE_PATH))
        self.save_Mtn.resize(self.save_Mtn.minimumSizeHint())
        self.save_Mtn.clicked.connect(self.file_save)

        self.save_Mtb = QtGui.QPushButton("", self)
        self.save_Mtb.move(650, 326)
        self.save_Mtb.setIcon(QtGui.QIcon(SAVE_IMAGE_PATH))
        self.save_Mtb.resize(self.save_Mtb.minimumSizeHint())
        self.save_Mtb.clicked.connect(self.file_save)

        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------

        self.show()  # muestra la ventana grafica

    # ----------------------------------------------------------------------

    # Defino los metodos que uso

    def download(self):                                 #defino el boton descargar
        self.completed = 0                              #punto de partida del progress bar
        while self.completed < 100:
            self.completed += 0.001                     # le voy sumando de a estos pasos redefiniendo self.completed
            self.progress.setValue(self.completed)      # seteo el valor como el de self.completed


    def file_save(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Guardar Archivo')
        file = save(name, 'w')

    def close_application(self):  # llamo a close_application arriba

        choice = QtGui.QMessageBox.question(self, 'Salir', "Esta seguro que desea salir?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if choice == QtGui.QMessageBox.Yes:
            sys.exit()                  # cierra la app al apretar el boton
        else:
            pass

    def closeEvent(self, event):        # defino este nuevo metodo para que aparezca el popup tambien si hago clic en la cruz roja
        event.ignore()
        self.close_application()

    def radio_action(self,pressed):      # defino este nuevo metodo para que el radio button haga una cosa u otra segun si esta apretado o no

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
    #---------------------------------------------------------------------------


    # ---------------------------------------------------------------------------
    # Defino que quiero que haga cada radiobutton

    def buttonClicked(self, a):  # obtengo la string de que radioButton esta presionado

        sender = self.sender()
        self.statusBar().showMessage(sender.text())
        a = sender.text()
        # print a
        if a == ("MAF"):
            print ("1")  # aca iria lo que quiero que haga una vez presiono en MAF
            #process(MAF)
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
