import sys
import wave
from PyQt4 import QtGui

import pyaudio
import sounddevice as sd

import SWHear


class AudioModule(QtGui.QMainWindow):

    def __init__(self, parent=None):
        # pyqtgraph.setConfigOption('background', 'w') #before loading widget
        super(AudioModule, self).__init__(parent)
        self.ear = SWHear.SWHear(rate=44100, updatesPerSecond=20)
        self.ear.stream_initStop()  # puedo cambiarlo para que arranque ya con el stream on

    def pause(self):
        pass
        # stream.stop_stream()

    def start(self):
        self.ear = SWHear.SWHear()
        self.ear.stream_start()

    def rec(self):
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = 7
        WAVE_OUTPUT_FILENAME = "file.wav"

        audio = pyaudio.PyAudio()

        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        print "recording..."
        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print "finished recording"

        # Termina la grabacion
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Sin esta siguiente parte de wavfile, termina la grabacion pero no lo guarda

        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

    def stop(self):
        # recording = False
        sd.stop()

    def play(self):

        # define stream chunk
        chunk = 1024

        # open a wav format music
        # f = wave.open(r"/home/diego/PycharmProjects/tests/test.wav","rb") #funciona de las dos maneras
        f = wave.open("file.wav", "rb")

        # instantiate PyAudio
        p = pyaudio.PyAudio()

        # open stream
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

        # close PyAudio
        p.terminate()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    form.update()  # start with something
    app.exec_()
    print("DONE")
