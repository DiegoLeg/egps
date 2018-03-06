import sys
import wave
from PyQt4 import QtGui
from scipy.signal import deconvolve as deconvolve
from scipy.signal import sosfilt as sosfilt
from scipy.signal import lfilter as lfilter
import pyaudio
import librosa as lb
import numpy as np
import sounddevice as sd
import SWHear


class AudioModule(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(AudioModule, self).__init__(parent)
        self.ear = SWHear.SWHear(rate=44100, updatesPerSecond=20)
        self.ear.stream_initStop()                  # puedo cambiarlo para que arranque ya con el stream on

    def pause(self):
        pass
        # stream.stop_stream()

    def start(self):                                #deteccion automatica del driver de audio que se usa
        self.ear = SWHear.SWHear()
        self.ear.stream_start()

    def rec(self):
        formato = pyaudio.paInt16
        canales = 1
        rate = 44100
        chunk = 1024
        record_seconds = 7                          #tiempo de grabacion;poner un getstring para el usuario?
        wave_output_filename = "rec_file.wav"

        audio = pyaudio.PyAudio()

        # Abro el stream para grabar
        stream = audio.open(format=formato, channels=canales,
                            rate=rate, input=True,
                            frames_per_buffer=chunk)
        print "recording..."
        frames = []

        for i in range(0, int(rate / chunk * record_seconds)):
            data = stream.read(chunk)
            frames.append(data)
        print "finished recording"

        # Termina la grabacion
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Guardo el archivo

        waveFile = wave.open(wave_output_filename, 'wb')
        waveFile.setnchannels(canales)
        waveFile.setsampwidth(audio.get_sample_size(formato))
        waveFile.setframerate(rate)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

    def stop(self):
        # recording = False
        sd.stop()

    def play(self):

        chunk = 1024

        # Levanto el archivo wav
        f = wave.open("rec_file.wav", "rb")

        # Levanto PyAudio
        p = pyaudio.PyAudio()

        # Abro un stream
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)

        data = f.readframes(chunk)

        # Reproduzco el stream
        while data:
            stream.write(data)
            data = f.readframes(chunk)

        # Stop stream
        stream.stop_stream()
        stream.close()

        # Cierro PyAudio
        p.terminate()


    def process(self):

        #Abro el archivo, y lo convierto en un array de intensidad

        x, samplerate = lb.load("rec_file.wav",44100)           #si no especifico este samplerate, librosa downsamplea


        #-----------------------------------------------------------------------
        #Usando deconvolve

        #ap_filter = np.array([0.5, 1.0, 0.5])

        #q, r = deconvolve(samples, ap_filter)

        #b, a = convolve (q,ap_filter)

        #print len(q)
        #print q
        #print len(b)
        #print b

        # --------------------------------------------------------------------
        #Usando lfilter

        #Defino numerador y denominador de la funcion transferencia del mic


        b = [2., 1.395, 0.18]                                   #numerador
        a = [1., 0.004, 0.816]                                  #denominador

        #---------------------------------------------------------------------
        #Podria usar sosfilt


        #sos = [a+b]
        #sos = [[1.0, 0.004, 0.816, 1, 1.395, 0.18], [1e-06, 1.395, 0.18, 1, 0.004, 0.816]]

        #filtered = sosfilt(sos,x)
        #y = sos2zpk(sos)           #polos y ceros del sistema

        #---------------------------------------------------------------------

        #Aplico primero el filtro inverso de la transferencia, y despues la transferencia de algun otro mic

        # Aca se aplica la inversa de la funcion transferencia de un mic y luego la funcion transferencia
        # original para verificar que la senal de origen queda igual


        filtered = lfilter(b,a,lfilter(a,b,x))

        #La idea es que lfilter(a,b,x) aplique el filtro inverso del mic MAF por ejemplo (para dejar limpia la senal
        #es decir, para que no tenga influencia de la funcion transferencia del mic) y luego con el lfilter de afuera
        #aplicar otra funcion transferencia, por ejemplo del filtro MCF.

        #Verificar en este paso que la ROC del sistema inverso converja (Sino tira error Audio buffer is not finite everywhere)
        #cuando hay polos fuera del circulo unitario.

        #---------------------------------------------------------------------------
        #Guardar en archivo

        lb.output.write_wav('recfile_filtered.wav', filtered, samplerate)

        #sf.write('file_trim2.wav', filtered, samplerate)

        print len(x)
        print x
        print x.dtype

        print len(filtered)
        print filtered


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = AudioModule()
    form.show()
    form.update()
    app.exec_()
    print("DONE")
