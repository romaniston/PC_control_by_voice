import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

SAMPLE_RATE = 16000

model = Model("model")
rec = KaldiRecognizer(model, SAMPLE_RATE)

def callback(indata, frames, time, status):
    if rec.AcceptWaveform(indata):
        result = json.loads(rec.Result())
        print("I heard:", result.get("text"))

with sd.RawInputStream(
    samplerate=SAMPLE_RATE,
    blocksize=8000,
    dtype="int16",
    channels=1,
    callback=callback
):
    print(" Listening...")
    while True:
        pass
