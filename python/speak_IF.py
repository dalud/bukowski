import os
from subprocess import Popen

class Mouth:
    def __init__(self):
        self.p = None
        
    def speak(self, sentence):
        if not self.isSpeaking():
            os.system('espeak -p 0 -a 100 -s 105 -v english-us "{0}"'.format(sentence))

    def speakAsync(self, sentence):
        self.p = Popen('espeak -p 0 -a 100 -s 105 -v english-us "{0}"'.format(sentence), shell=True)

    def isSpeaking(self):
        #print(self.p.poll())
        if self.p: return self.p.poll() == None
