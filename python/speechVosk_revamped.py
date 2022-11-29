import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import sys
import json

#print("Display input/output devices")
#print(sd.query_devices())


# get the samplerate - this is needed by the Kaldi recognizer
device_info = sd.query_devices(sd.default.device[0], 'input')
samplerate = int(device_info['default_samplerate'])

# display the default input device
#print("===> Initial Default Device Number:{} Description: {}".format(sd.default.device[0], device_info))

# setup queue and callback function
q = queue.Queue()

def recordCallback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))
    
# build the model and recognizer objects.
print("===> Building model and recognizer objects.  This may take a few minutes.")
model = Model(r"/home/pi/voskModel/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, samplerate)
recognizer.SetWords(False)

print("===> Begin recording. Press Ctrl+C to exit")
try:
    with sd.RawInputStream(dtype='int16', channels=1, callback=recordCallback):
        print("I am listening...")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                recognizerResult = recognizer.Result()
                # convert the recognizerResult string into a dictionary  
                resultDict = json.loads(recognizerResult)
                if not resultDict.get("text", "") == "":
                    #print(recognizerResult)
                    print("I heard: ", resultDict.get("text", ""))
                    print("I am listening...")
                else:
                    print("no input sound")

except KeyboardInterrupt:
    print('===> Finished Recording')
except Exception as e:
    print(str(e))
