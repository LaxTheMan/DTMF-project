from user_interface import *
from encryption import *
from encoding import *
from communication import *
from settings import *


def receiver():

    #Read wav signal file from directory specified in settings
    signal = read_signal_from_wav(
        f".\\{settings.SAVE_FILE_DIR}\\{settings.SAVE_FILE_NAME}.wav")

    # signal = read_signal_from_wav(f".\\aud\\dtmf_encoded_rec.wav")

    #Decode signal to text
    decoded_text = decode_signal(
        signal, settings.DURATION_SYMBOL, settings.SAMPLE_RATE)

    #Decrypt text
    decrypted_text = decrypt_text(decoded_text)

    #Display final text
    display_output("Output: " + decrypted_text)


if __name__ == "__main__":
    receiver()
