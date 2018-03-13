import pyaudio
import tempfile
import time
import wave
from io import BytesIO
from threading import Thread

from scipy.signal import lfilter as lfilter

import soundfile as sf
from config import OUTPUT_FILE_PATH

# No borrar esta dependencia
import sounddevice as sd


"""Se definen los metodos para el procesamiento del audio"""

class AudioModule:
    def __init__(self, wav_file_path):
        self.py_audio = pyaudio.PyAudio()
        self.wave_in_file = wave.open(wav_file_path, "rb")
        self.in_file_stream = self.py_audio.open(
            format=self.py_audio.get_format_from_width(self.wave_in_file.getsampwidth()),
            channels=self.wave_in_file.getnchannels(), rate=self.wave_in_file.getframerate(),
            output=True, stream_callback=self.play_callback)

        #Se inicia el stream en stop para que no comience a reproducir un audio al abrir la aplicacion
        self.in_file_stream.stop_stream()
        self.in_wav_file_path = wav_file_path

        #Estados de los procesos que se realizan con el stream de audio
        self.out_stream = None
        self.rec_play_stream = None
        self.rec_wave = None
        self.wave_out = None

        #Stream para la grabacion de audio junto con todos sus parametros
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

#-----------------------------------------------------------------------------------------------------------------------
    """Etapa 1: Archivo de entrada"""

    def load_file(self, wav_file_path):
        """
        Metodo para cargar un archivo de audio que se haya grabado previamente con alguno
        de los transductores caracterizados.

        :param wav_file_path: Ruta del archivo de audio a cargar

        """
        self.stop_file()
        self.wave_in_file.close()
        self.wave_in_file = wave.open(wav_file_path, "rb")
        self.in_wav_file_path = wav_file_path

    def play_file(self):
        """
        Se reproduce un archivo de audio previamente cargado creando otro thread

        """
        thread = Thread(target=self.play_file_in_thread)
        thread.setDaemon(True)
        thread.start()

    def play_file_in_thread(self):
        """
        Metodo para la reproduccion de audio en otro thread del algoritmo

        """
        if self.in_file_stream.is_active():
            self.stop_file()
            time.sleep(0.002)
        self.in_file_stream.start_stream()
        while self.in_file_stream.is_active():
            time.sleep(0.001)

    def play_callback(self, in_data, frame_count, time_info, status):
        """
        Se define un callback para la reproduccion de audio

        :param frame_count:

        """
        data = self.wave_in_file.readframes(frame_count)
        return data, pyaudio.paContinue

    def stop_file(self):
        """
        Se define un metodo para detener el stream de audio y rebobinar el archivo que haya sido cargado

        """
        self.in_file_stream.stop_stream()
        self.wave_in_file.rewind()

#-----------------------------------------------------------------------------------------------------------------------
    """Etapa 2: Grabacion"""

    def rec(self):
        """
        Grabacion de un archivo .wav

        """
        self.stop_rec()
        self.rec_frames = []
        self.wave_bytes = BytesIO()
        self.rec_stream.start_stream()

    def rec_callback(self, in_data, frame_count, time_info, status):
        """
        Se define un callback para grabacion de audio

        :param in_data:

        """
        self.rec_frames.append(in_data)
        return in_data, pyaudio.paContinue

    def stop_rec(self):
        """
        Metodo para interrumpir la grabacion de un archivo de audio

        """
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
        """
        Metodo para reproducir el archivo que fue grabado utilizando la interfaz grafica, usando otro thread

        """
        self.stop_rec()

        if self.rec_play_stream:
            thread = Thread(target=self.play_rec_in_thread)
            thread.setDaemon(True)
            thread.start()

    def play_rec_in_thread(self):
        """
        Se define metodo para la grabacion de audio en otro thread del algoritmo

        """
        if self.rec_play_stream.is_active():
            self.stop_rec()
            time.sleep(0.002)
        self.rec_play_stream.start_stream()
        while self.rec_play_stream.is_active():
            time.sleep(0.001)
        self.rec_wave.rewind()

    def play_rec_callback(self, in_data, frame_count, time_info, status):
        """
        Se define un callback para la reproduccion de audio perteneciente al modulo de grabacion

        :param frame_count:

        """
        data = self.rec_wave.readframes(frame_count)
        return data, pyaudio.paContinue

    def save_rec(self, wave_output_filename):
        """
        Metodo para almacenar el archivo de audio que fue grabado

        :param wave_output_filename: Nombre del archivo que se almacena

        """
        if self.rec_frames:

            wave_file = wave.open(wave_output_filename, 'wb')
            wave_file.setnchannels(self.channel)
            wave_file.setsampwidth(self.py_audio.get_sample_size(pyaudio.paInt16))
            wave_file.setframerate(self.rate)
            wave_file.writeframes(b''.join(self.rec_frames))
            wave_file.close()

        return len(self.rec_frames) > 0

#-----------------------------------------------------------------------------------------------------------------------
    """Etapa 3: Salida"""

    def play_out(self, recorded, in_num, in_den, out_num, out_den):
        """
        Reproduccion de la senal de salida una vez filtrada


        :param in_num: Numerador de la funcion de transferencia del transductor a simular
        :param in_den: Denominador de la funcion de transferencia del transductor a simular
        :param out_num: Numerador del sistema inverso correspondiente a la funcion de transferencia del transductor
                        con el que se grabo la senal
        :param out_den: Denominador del sistema inverso correspondiente a la funcion de transferencia del transductor
                        con el que se grabo la senal

        """
        if recorded:
            tf = tempfile.NamedTemporaryFile(suffix=".wav")
            if self.save_rec(tf.name):
                x, sample_rate = sf.read(tf.name)
            else:
                return
        else:
            x, sample_rate = sf.read(self.in_wav_file_path)

        #Procesamiento principal del algoritmo utilizando filtrado inverso
        filtered = lfilter(in_num, in_den, lfilter(out_den, out_num, x))

        #Archivo temporal de audio creado al grabar
        tf = tempfile.NamedTemporaryFile(suffix=".wav")

        sf.write(tf.name, filtered, sample_rate, subtype='PCM_16')

        self.wave_out = wave.open(tf, "rb")

        self.out_stream = self.py_audio.open(
            format=self.py_audio.get_format_from_width(self.wave_in_file.getsampwidth()),
            channels=self.wave_in_file.getnchannels(), rate=self.wave_in_file.getframerate(),
            output=True, stream_callback=self.play_out_callback)
        self.out_stream.stop_stream()

        #Se utiliza otro thread para la reproduccion
        thread = Thread(target=self.play_out_thread)
        thread.setDaemon(True)
        thread.start()

    def play_out_thread(self):
        """
        Metodo para la reproduccion de audio de etapa de salida, en otro thread

        """
        if self.out_stream.is_active():
            self.out_stream()
            time.sleep(0.002)
        self.out_stream.start_stream()
        while self.out_stream.is_active():
            time.sleep(0.001)

    def play_out_callback(self, in_data, frame_count, time_info, status):
        """
        Se define un callback para la reproduccion de audio perteneciente al modulo de salida

        :param frame_count:

        """
        data = self.wave_out.readframes(frame_count)
        return data, pyaudio.paContinue

    def stop_out(self):
        """
        Se define metodo para interrumpir la senal de la etapa de salida de audio

        """
        self.out_stream.stop_stream()

    def save_out(self, filename, recorded, in_num, in_den, out_num, out_den):
        """
        Metodo para guardar el archivo temporal .wav que fue creado

        :param filename: Nombre del archivo
        :param in_num: Numerador de la funcion de transferencia del transductor a simular
        :param in_den: Denominador de la funcion de transferencia del transductor a simular
        :param out_num: Numerador del sistema inverso correspondiente a la funcion de transferencia del transductor
                        con el que se grabo la senal
        :param out_den: Denominador del sistema inverso correspondiente a la funcion de transferencia del transductor
                        con el que se grabo la senal
        """
        if recorded:
            tf = tempfile.NamedTemporaryFile(suffix=".wav")
            if self.save_rec(tf.name):
                x, sample_rate = sf.read(tf.name)
            else:
                return False
        else:
            x, sample_rate = sf.read(self.in_wav_file_path)

        filtered = lfilter(in_num, in_den, lfilter(out_den, out_num, x))
        sf.write(filename, filtered, sample_rate, subtype='PCM_16')
        return True