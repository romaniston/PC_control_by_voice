import json
import sounddevice as sd

from vosk import Model, KaldiRecognizer

from commands import (
    sleep_pc,
    shutdown_pc,
    set_volume
)

# --------------------
# CONFIG
# --------------------

SAMPLE_RATE = 16000
WAKE_WORD = "джер"

NUMBERS = {
    "ноль": 0,
    "один": 1,
    "два": 2,
    "три": 3,
    "четыре": 4,
    "пять": 5,
    "шесть": 6,
    "семь": 7,
    "восемь": 8,
    "девять": 9,
    "десять": 10
}

# Ограниченный словарь (ускоряет Vosk)
WORDS = [
    "джер",
    "сон",
    "выключи",
    "компьютер",
    "громкость",
    "ноль",
    "один",
    "два",
    "три",
    "четыре",
    "пять",
    "шесть",
    "семь",
    "восемь",
    "девять",
    "десять"
]

# --------------------
# MODEL
# --------------------

model = Model("model")

recognizer = KaldiRecognizer(
    model,
    SAMPLE_RATE,
    json.dumps(WORDS, ensure_ascii=False)
)

# --------------------
# LOGIC
# --------------------

def handle_command(text: str):

    print("Распознано:", text)

    if not text.startswith(WAKE_WORD):
        return

    command = text.replace(WAKE_WORD, "", 1).strip()

    print("Команда:", command)

    # 🔴 СОН
    if "сон" in command:
        print("→ Сон")
        sleep_pc()

    # 🔴 ВЫКЛЮЧЕНИЕ
    elif "выключ" in command:
        print("→ Выключение")
        shutdown_pc()

    # 🔊 ГРОМКОСТЬ
    elif "громкость" in command:

        for word, number in NUMBERS.items():
            if word in command:
                print(f"→ Громкость {number}")
                set_volume(number)
                break


# --------------------
# MICROPHONE CALLBACK
# --------------------

def callback(indata, frames, time, status):

    audio_data = bytes(indata)

    if recognizer.AcceptWaveform(audio_data):

        result = json.loads(recognizer.Result())

        text = result.get("text", "").strip()

        if text:
            handle_command(text)


# --------------------
# MAIN LOOP
# --------------------

with sd.RawInputStream(
    samplerate=SAMPLE_RATE,
    blocksize=8000,
    dtype="int16",
    channels=1,
    callback=callback
):

    print("🎤 Ассистент запущен")

    while True:
        pass