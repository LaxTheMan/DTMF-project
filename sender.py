from user_interface import *
from encryption import *
from encoding import *
from communication import *
from settings import *


def sender():

    # text = "ab cd"
    text = get_user_input()

    #Encrypt text
    encrypted_text = encrypt_text(text)

    #Encode text to signal
    encoded_signal = encode_text(
        encrypted_text, settings.DURATION_SYMBOL, settings.SAMPLE_RATE)
    
    #Store audio signal under directory specified in settings
    save_signal_as_wav(encoded_signal)

if __name__ == "__main__":
    sender()
