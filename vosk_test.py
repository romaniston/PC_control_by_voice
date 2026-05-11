import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

SAMPLE_RATE = 16000

model = Model("model")

recognizer = KaldiRecognizer(model, SAMPLE_RATE)

def callback(indata, frames, time, status):

    audio_data = bytes(indata)

    if recognizer.AcceptWaveform(audio_data):

        result = json.loads(recognizer.Result())

        text = result.get("text", "").strip()

        if text:
            print("result:", text)

with sd.RawInputStream(
    samplerate=SAMPLE_RATE,
    blocksize=8000,
    dtype="int16",
    channels=1,
    callback=callback
):
    print("I listening")

    while True:
        pass