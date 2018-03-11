import time
import wave
from scipy.signal import lfilter as lfilter
from threading import Thread

import librosa as lb
import pyaudio
# No borrar esta dependencia
import sounddevice as sd

from config import OUTPUT_FILE_PATH


class AudioModule:
    def __init__(self, wav_file_path):
        self.p = pyaudio.PyAudio()
        self.f = wave.open(wav_file_path, "rb")
        self.stream = self.p.open(format=self.p.get_format_from_width(self.f.getsampwidth()),
                                  channels=self.f.getnchannels(), rate=self.f.getframerate(),
                                  output=True, stream_callback=self.callback)
        self.stream.stop_stream()

    def __del__(self):
        self.stream.close()
        self.p.terminate()

    def callback(self, in_data, frame_count, time_info, status):
        data = self.f.readframes(frame_count)
        return data, pyaudio.paContinue

    def stop(self):
        self.stream.stop_stream()
        self.f.rewind()

    def play_in_thread(self):
        if self.stream.is_active():
            self.stop()
            time.sleep(0.002)
        self.stream.start_stream()
        while self.stream.is_active():
            time.sleep(0.001)

    def play(self):
        thread = Thread(target=self.play_in_thread)
        thread.setDaemon(True)
        thread.start()

    def rec(self):
        formato = pyaudio.paInt16
        canales = 1
        rate = 44100
        chunk = 1024
        record_seconds = 7
        #tiempo de grabacion;poner un getstring para el usuario?
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
