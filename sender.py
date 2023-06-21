from user_interface import *
from encryption import *
from encoding import *
from communication import *
from settings import *


def sender():

    # text = get_user_input()
    text = "ab cd"

    encrypted_text = encrypt_text(text)

    encoded_signal = encode_text(
        encrypted_text, settings.DURATION_SYMBOL, settings.SAMPLE_RATE)
    
    save_signal_as_wav(encoded_signal)

if __name__ == "__main__":
    sender()
