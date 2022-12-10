import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import sys
import json

class Ear:
    def __init__(self):
        self.device_info = sd.query_devices(sd.default.device[0], 'input')
        self.samplerate = int(self.device_info['default_samplerate'])
        self.q = queue.Queue()
        print("===> Building model and recognizer objects.  This may take a few minutes.")
        self.model = Model(r"/home/pi/voskModel/vosk-model-small-en-us-0.15")
        self.recognizer = KaldiRecognizer(self.model, self.samplerate)
        self.recognizer.SetWords(False)
        self.listening = False

    def recordCallback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def listen(self, listen):
        self.listening = listen
        try:
            with sd.RawInputStream(dtype='int16', channels=1, callback=self.recordCallback):
                print("I am listening...")
                while self.listening:
                    data = self.q.get()
                    if self.recognizer.AcceptWaveform(data):
                        self.recognizerResult = self.recognizer.Result()
                        self.resultDict = json.loads(self.recognizerResult)
                        if not self.resultDict.get("text", "") == "":
                            print("I heard: ", self.resultDict.get("text", ""))
                            print("I am listening...")
                        else:
                            print("no input sound")

        except Exception as e:
            print(str(e))
