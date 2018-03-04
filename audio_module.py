import sys
import wave
from PyQt4 import QtGui
from scipy.signal import lfilter as lfilter
from scipy.io.wavfile import read as wavread
import pyaudio
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

    def start(self):
        self.ear = SWHear.SWHear()
        self.ear.stream_start()

    def rec(self):
        formato = pyaudio.paInt16
        canales = 2
        rate = 44100
        chunk = 1024
        record_seconds = 7
        wave_output_filename = "file.wav"

        audio = pyaudio.PyAudio()

        # start Recording
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

        # Sin esta siguiente parte de wavfile, termina la grabacion pero no lo guarda

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
        f = wave.open("file2.wav", "rb")

        # Levanto PyAudio
        p = pyaudio.PyAudio()

        # Abro stream
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)

        # read data
        data = f.readframes(chunk)

        # play stream
        while data:
            stream.write(data)
            data = f.readframes(chunk)

        # stop stream
        stream.stop_stream()
        stream.close()

        # cierro PyAudio
        p.terminate()


    def process(self):

        #Abro el archivo, y lo convierto en un array de intensidad

        [samplerate, x] = wavread("file.wav")  # x es un numpy array of integer, representando los samples

        # escalo de -1.0 -- 1.0

        if x.dtype == 'int16':
            nb_bits = 16                            # -> 16-bit wav
        elif x.dtype == 'int32':
            nb_bits = 32                            # -> 32-bit wav files
        max_nb_bit = float(2 ** (nb_bits - 1))
        samples = x / (max_nb_bit + 1.0)             # samples is a numpy array of float representing the samples
        #return samples


        #transcribir funcion z al denominador y numerador coeficientes

        #lfilter ([1., 2.], [3., 0., 1.], [3., 45., 5., 6., 4., 3., 7., 8., 125., 110., 75.])

        #Aplico la transformada inversa del sistema

        tf1 = lfilter ([1., 2.], [3., 0., 1.], [samples])

        #Aplico la transformada de algun otro mic

        tf2 = lfilter([1., 2.], [1., 0., 3.], [tf1])

        #guardar en archivo (ver el metodo que lo hace#




        #f es el vector de audio que estoy levantando

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = AudioModule()
    form.show()
    form.update()  # start with something
    app.exec_()
    print("DONE")
