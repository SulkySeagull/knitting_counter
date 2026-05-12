import queue
import sys
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import kntting_commands


model = Model("vosk-model-small-en-us-0.15")
sample_rate = 16000
q = queue.Queue()
output_file = open("output.txt", "wb")
rec = KaldiRecognizer(model,sample_rate)

#add exception handling
def callback(indata, frames, time, status):
    q.put(bytes(indata))

print("Listening... please press control Ctrl + C to stop ")
try:
    with sd.RawInputStream(samplerate = sample_rate, blocksize = 1800, dtype = "int16", channels = 1, callback = callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                command = result["text"]
                if "add row" in command:
                    #increment row
                    pass
                
except KeyboardInterrupt:
    print("\nStopped listening")
except Exception as e:
    print("Error: " , e)
    



