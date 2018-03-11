import pyaudio
import time
import wave
from io import BytesIO
from threading import Thread

import librosa as lb
from scipy.signal import lfilter as lfilter

from config import OUTPUT_FILE_PATH

# No borrar esta dependencia
import sounddevice as sd


class AudioModule:
    def __init__(self, wav_file_path):
        self.py_audio = pyaudio.PyAudio()
        self.wave_in_file = wave.open(wav_file_path, "rb")
        self.in_file_stream = self.py_audio.open(
            format=self.py_audio.get_format_from_width(self.wave_in_file.getsampwidth()),
            channels=self.wave_in_file.getnchannels(), rate=self.wave_in_file.getframerate(),
            output=True, stream_callback=self.play_callback)
        self.in_file_stream.stop_stream()

        self.rec_play_stream = None
        self.rec_wave = None

        self.rec_frames = []
        self.wave_bytes = BytesIO()

        self.rate = 44100
        self.chunk = 1024
        self.channel = 1
        self.rec_stream = self.py_audio.open(format=pyaudio.paInt16, channels=self.channel, rate=self.rate, input=True,
                                             frames_per_buffer=self.chunk, stream_callback=self.rec_callback)
        self.rec_stream.stop_stream()
        self.rec_frames = []

    def __del__(self):
        self.in_file_stream.close()
        self.py_audio.terminate()

    def load_file(self, wav_file_path):
        self.stop_file()
        self.wave_in_file.close()
        self.wave_in_file = wave.open(wav_file_path, "rb")

    def play_callback(self, in_data, frame_count, time_info, status):
        data = self.wave_in_file.readframes(frame_count)
        return data, pyaudio.paContinue

    def play_rec_callback(self, in_data, frame_count, time_info, status):
        data = self.rec_wave.readframes(frame_count)
        return data, pyaudio.paContinue

    def rec_callback(self, in_data, frame_count, time_info, status):
        self.rec_frames.append(in_data)
        return in_data, pyaudio.paContinue

    def stop_file(self):
        self.in_file_stream.stop_stream()
        self.wave_in_file.rewind()

    def play_file_in_thread(self):
        if self.in_file_stream.is_active():
            self.stop_file()
            time.sleep(0.002)
        self.in_file_stream.start_stream()
        while self.in_file_stream.is_active():
            time.sleep(0.001)

    def play_rec_in_thread(self):
        if self.rec_play_stream.is_active():
            self.stop_rec()
            time.sleep(0.002)
        self.rec_play_stream.start_stream()
        while self.rec_play_stream.is_active():
            time.sleep(0.001)
        self.rec_wave.rewind()

    def play_file(self):
        thread = Thread(target=self.play_file_in_thread)
        thread.setDaemon(True)
        thread.start()

    def rec(self):
        self.stop_rec()
        self.rec_frames = []
        self.wave_bytes = BytesIO()
        self.rec_stream.start_stream()

    def stop_rec(self):
        if self.rec_play_stream:
            self.rec_play_stream.stop_stream()
            self.wave_bytes.seek(0)

        if self.rec_stream.is_active():
            self.rec_stream.stop_stream()
            w_file = wave.open(self.wave_bytes, "wb")
            w_file.setnchannels(self.channel)
            w_file.setsampwidth(self.py_audio.get_sample_size(pyaudio.paInt16))
            w_file.setframerate(self.rate)
            w_file.writeframes(b''.join(self.rec_frames))
            self.wave_bytes.seek(0)
            self.rec_wave = wave.open(self.wave_bytes, "rb")
            self.rec_play_stream = self.py_audio.open(
                format=self.py_audio.get_format_from_width(self.rec_wave.getsampwidth()),
                channels=self.rec_wave.getnchannels(), rate=self.rec_wave.getframerate(),
                output=True, stream_callback=self.play_rec_callback)
            self.rec_play_stream.stop_stream()

    def play_rec(self):
        self.stop_rec()
        if self.rec_play_stream:
            thread = Thread(target=self.play_rec_in_thread)
            thread.setDaemon(True)
            thread.start()

    def save_rec(self, wave_output_filename):
        if self.rec_frames:
            wave_file = wave.open(wave_output_filename, 'wb')
            wave_file.setnchannels(self.channel)
            wave_file.setsampwidth(self.py_audio.get_sample_size(pyaudio.paInt16))
            wave_file.setframerate(self.rate)
            wave_file.writeframes(b''.join(self.rec_frames))
            wave_file.close()
        return len(self.rec_frames) > 0

    def process(self):

        # Abro el archivo, y lo convierto en un array de intensidad

        x, samplerate = lb.load(OUTPUT_FILE_PATH, 44100)  # si no especifico este samplerate, librosa downsamplea

        # --------------------------------------------------------------------
        # Usando lfilter

        # Defino numerador y denominador de la funcion transferencia del mic

        b = [0.2844, 0.8472, 0.2055]  # numerador
        a = [1., -0.1608, 0.5231]  # denominador

        # ---------------------------------------------------------------------
        # Podria usar sosfilt

        # sos = [a+b]
        # sos = [[1.0, 0.004, 0.816, 1, 1.395, 0.18], [1e-06, 1.395, 0.18, 1, 0.004, 0.816]]

        # filtered = sosfilt(sos,x)
        # y = sos2zpk(sos)           #polos y ceros del sistema

        # ---------------------------------------------------------------------

        # Aplico primero el filtro inverso de la transferencia, y despues la transferencia de algun otro mic

        filtered = lfilter(b, a, lfilter(a, b, x))

        # ---------------------------------------------------------------------------
        # Guardar en archivo

        lb.output.write_wav('recfile_filtered.wav', filtered, samplerate)

        # sf.write('file_trim2.wav', filtered, samplerate)

        print len(x)
        print x
        print x.dtype

        print len(filtered)
        print filtered()
