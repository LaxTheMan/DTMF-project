from user_interface import *
from encryption import *
from encoding import *
from communication import *
from settings import *


def receiver():

    signal = read_signal_from_wav(
        f".\\{settings.SAVE_FILE_DIR}\\{settings.SAVE_FILE_NAME}.wav")

    # signal = read_signal_from_wav(f".\\aud\\dtmf_encoded_rec.wav")

    decoded_text = decode_signal(
        signal, settings.DURATION_SYMBOL, settings.SAMPLE_RATE)

    decrypted_text = decrypt_text(decoded_text)

    display_output("Output: " + decrypted_text)


if __name__ == "__main__":
    receiver()
