import time
import wave
from PyQt4 import QtGui
from scipy.signal import lfilter as lfilter
from threading import Thread

import librosa as lb
import pyaudio

from config import OUTPUT_FILE_PATH
from sw_hear_ext import SWHear


class AudioModule(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(AudioModule, self).__init__(parent)
        self.ear = SWHear.SWHear(rate=44100, updatesPerSecond=20)
        self.ear.stream_initStop()                  # puedo cambiarlo para que arranque ya con el stream on
        self.p = pyaudio.PyAudio()

    def start(self):                                #deteccion automatica del driver de audio que se usa
        self.ear.stream_start()

    def rec(self):
        formato = pyaudio.paInt16
        canales = 1
        rate = 44100
        chunk = 1024
        record_seconds = 7                          #tiempo de grabacion;poner un getstring para el usuario?
        wave_output_filename = OUTPUT_FILE_PATH

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
        self.stream.stop_stream()

    #def init_thread(self):

    def callback(self, in_data, frame_count, time_info, status):
        data = self.f.readframes(frame_count)
        return (data, pyaudio.paContinue)

    def play_file(self, ):
        # Levanto el archivo wav
        self.f = wave.open(OUTPUT_FILE_PATH, "rb")

        # Abro un stream
        self.stream = self.p.open(format=self.p.get_format_from_width(self.f.getsampwidth()),
                                  channels=self.f.getnchannels(), rate=self.f.getframerate(),
                                  output=True, stream_callback=self.callback)

        self.stream.start_stream()
        while self.stream.is_active():
            time.sleep(0.01)

    def play(self):
        thread = Thread(target=self.play_file)
        thread.setDaemon(True)
        thread.start()



    def process(self):

        #Abro el archivo, y lo convierto en un array de intensidad

        x, samplerate = lb.load(OUTPUT_FILE_PATH,44100)           #si no especifico este samplerate, librosa downsamplea

        # --------------------------------------------------------------------
        #Usando lfilter

        #Defino numerador y denominador de la funcion transferencia del mic


        b = [0.2844, 0.8472, 0.2055]                                   #numerador
        a = [1., -0.1608, 0.5231]                                  #denominador

        #---------------------------------------------------------------------
        #Podria usar sosfilt

        #sos = [a+b]
        #sos = [[1.0, 0.004, 0.816, 1, 1.395, 0.18], [1e-06, 1.395, 0.18, 1, 0.004, 0.816]]

        #filtered = sosfilt(sos,x)
        #y = sos2zpk(sos)           #polos y ceros del sistema

        #---------------------------------------------------------------------

        #Aplico primero el filtro inverso de la transferencia, y despues la transferencia de algun otro mic

        filtered = lfilter(b,a,lfilter(a,b,x))

        #---------------------------------------------------------------------------
        #Guardar en archivo

        lb.output.write_wav('recfile_filtered.wav', filtered, samplerate)

        #sf.write('file_trim2.wav', filtered, samplerate)

        print len(x)
        print x
        print x.dtype

        print len(filtered)
        print filtered()
