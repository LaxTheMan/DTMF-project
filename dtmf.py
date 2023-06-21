import numpy as np
import scipy.io.wavfile as wavfile
# from scipy.fft import rfft, rfftfreq, irfft

SAMPLE_TEXT = "this is cat"
F1 = [1000, 2000, 3000, 4000]
F2 = [1500, 2500, 3500, 4500]
KEYS = '1', '2', '3', 'a',\
    '4', '5', '6', 'b',\
    '7', '8', '9', 'c',\
    'e', '0', 'f', 'd'
DURATION_SYMBOL = 0.075
SAMPLE_RATE = 44100
GOERTZEL_SAMPLES = 128


def text_to_hexstring(sample_text):
    hexstring = ''
    for symbol in sample_text:
        hexstring = hexstring + (format(ord(symbol), "x"))

    return hexstring


def hexstring_to_text(hexstring):
    text = ""
    print("Hexstring length: ",len(hexstring))
    for i in range(0, len(hexstring), 2):
        hex_byte = hexstring[i:i+2]
        try:
            ascii_char = bytes.fromhex(hex_byte).decode('utf-8')
            if ord(ascii_char) < 128:
                text += ascii_char
        except ValueError:
            continue
    return text


def generate_wave(freq, duration, sample_rate):
    x = np.linspace(0, duration, int(sample_rate*duration), endpoint=False)
    frequencies = x * freq
    y = np.sin((2*np.pi) * frequencies)
    return x, y

# goertzel filter used to extract power of target frequencies
def goertzel_filter(signal, sample_rate, target_frequency, n=None):
    k = int(0.5 + n * target_frequency / sample_rate)
    omega = 2 * np.pi * k / n
    cosine = np.cos(omega)
    sine = np.sin(omega)
    coeff = 2 * cosine
    q0 = 0
    q1 = 0
    q2 = 0
    for i in range(0, n):
        q0 = coeff * q1 - q2 + signal[i]
        q2 = q1
        q1 = q0
    real = q1 - q2 * cosine
    imag = q2 * sine
    magnitude = np.sqrt(real**2 + imag**2)
    return magnitude, real, imag

# encode hexadecimal keys into audio signal
def encode_dtmf(hexstring, duration_symbol, sample_rate):
    encoded_signal = np.array([])
    for letter in hexstring:
        for i in range(16):
            if letter == KEYS[i]:
                f1 = F1[i//4]
                f2 = F2[i % 4]

        _, wave1 = generate_wave(f1, duration_symbol, sample_rate)
        _, wave2 = generate_wave(f2, duration_symbol, sample_rate)
        wave = wave1 + wave2
        encoded_signal = np.concatenate((encoded_signal, wave))

    normalized_signal = np.int16(
        (encoded_signal / encoded_signal.max()) * 32767)
    return normalized_signal

# decode audio signal into hexadecimal keys
def decode_dtmf(signal, duration_symbol, sample_rate):
    decoded = ''
    symbol_samples = int(sample_rate * duration_symbol)
    goertzel_samples = min(GOERTZEL_SAMPLES, symbol_samples)
    for i in range(0, len(signal) - symbol_samples + 1, symbol_samples):
        mags1 = np.array([])
        mags2 = np.array([])
        f1 = 0
        f2 = 0
        for freq in F1:
            mag, _, _ = goertzel_filter(
                signal[i:i+symbol_samples], sample_rate, freq, goertzel_samples)
            mags1 = np.append(mags1, mag)

        for freq in F2:
            mag, _, _ = goertzel_filter(
                signal[i:i+symbol_samples], sample_rate, freq, goertzel_samples)
            mags2 = np.append(mags2, mag)

        for i in range(len(mags1)):
            if mags1[i] == mags1.max():
                f1 = i
                break

        for i in range(len(mags2)):
            if mags2[i] == mags2.max():
                f2 = i
                break

        letter_ind = 4*f1 + f2
        decoded = decoded + KEYS[letter_ind]
    
    # Handle remaining samples
    remaining_samples = len(signal) % symbol_samples
    if remaining_samples > 0:
        mags1 = np.array([])
        mags2 = np.array([])
        f1 = 0
        f2 = 0
        for freq in F1:
            mag, _, _ = goertzel_filter(
                signal[-remaining_samples:], sample_rate, freq, remaining_samples)
            mags1 = np.append(mags1, mag)

        for freq in F2:
            mag, _, _ = goertzel_filter(
                signal[-remaining_samples:], sample_rate, freq, remaining_samples)
            mags2 = np.append(mags2, mag)

        for i in range(len(mags1)):
            if mags1[i] == mags1.max():
                f1 = i
                break

        for i in range(len(mags2)):
            if mags2[i] == mags2.max():
                f2 = i
                break

        letter_ind = 4*f1 + f2
        decoded += KEYS[letter_ind]
    # one extra character gets added to start and end for some reason?
    return decoded[1:-1]

# store signal as wav file
def store_wav(signal, sample_rate):
    print("Generated wav file: dtmf_encoded.wav")
    wavfile.write("dtmf_encoded.wav", sample_rate, signal)

# read left channel of wav file
def read_wav(file_name):
    sr, aud = wavfile.read(file_name)

    if type(aud[0]) == np.int16:
        return aud
    else:
        return aud[:, 0]


hexstring = text_to_hexstring(SAMPLE_TEXT)
print("Sample text:         " + SAMPLE_TEXT)
print("Sample text in hex:  " + hexstring)

signal = encode_dtmf(hexstring, DURATION_SYMBOL, SAMPLE_RATE)

store_wav(signal,SAMPLE_RATE)

read = read_wav("dtmf_encoded_rec.wav")

# recorded audio sample rate should be used for decoding
recorded_sample_rate = 48000

decoded = decode_dtmf(read, DURATION_SYMBOL, recorded_sample_rate)
print("Decoded text in hex: " + decoded)
print("Decoded text:        " + hexstring_to_text(decoded))
print()