import scipy.io.wavfile as wavfile
import numpy as np
import os
import settings


def save_signal_as_wav(signal):
    os.makedirs(f".\\{settings.SAVE_FILE_DIR}", exist_ok=True)
    wavfile.write(
        f".\\{settings.SAVE_FILE_DIR}\\{settings.SAVE_FILE_NAME}.wav", settings.SAMPLE_RATE, signal)
    print(f"Generated wav file: {settings.SAVE_FILE_NAME}.wav under {settings.SAVE_FILE_DIR}")


def read_signal_from_wav(file_name):
    sr, aud = wavfile.read(file_name)

    #Selecting one channel from dual channel audio
    if type(aud[0]) == np.int16:
        return aud
    else:
        return aud[:, 0]


def play_signal(signal):

    return