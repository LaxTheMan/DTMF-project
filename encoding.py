import numpy as np
import settings

KEYS = settings.KEYS
F1 = settings.F1
F2 = settings.F2
GOERTZEL_SAMPLES = settings.GOERTZEL_SAMPLES


def encode_text(text, duration_symbol, sample_rate):
    hexstring = text_to_hexstring(text)
    hexstring = "dd" + hexstring + "dd"
    print("Hexstring to be encoded: ", hexstring)
    encoded_signal = np.array([])
    for letter in hexstring:
        for i in range(16):
            if letter == KEYS[i]:
                freq1 = F1[i//4]
                freq2 = F2[i % 4]

        _, wave1 = generate_wave(freq1, duration_symbol, sample_rate)
        _, wave2 = generate_wave(freq2, duration_symbol, sample_rate)
        wave = wave1 + wave2
        encoded_signal = np.concatenate((encoded_signal, wave))

    normalized_signal = np.int16(
        (encoded_signal / encoded_signal.max()) * 32767)
    return normalized_signal


def decode_signal(signal, duration_symbol, sample_rate):
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

    print("Hexstring decoded: ", decoded)
    return hexstring_to_text(decoded)


def text_to_hexstring(text):
    hexstring = ''
    for symbol in text:
        hexstring = hexstring + (format(ord(symbol), "x"))

    return hexstring


def hexstring_to_text(hexstring):
    text = ""
    # print("Hexstring length: ", len(hexstring))
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
