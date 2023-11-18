import sys
from time import sleep

flush = sys.stdout.flush

class DelayedPrint:
    def __init__(self):
        self.printing = False

    def print(self, message):
        #print(len(message))
        #if message.find(','): delay = delay - .00049
        chars = set('/-,.:;()')
        delay = .08745
        if any((c in chars) for c in message):
            delay = delay
        else:
            delay = delay - .001
            sys.stdout.write('>')
            flush()
        #sys.stdout.write(delay)
        flush()
        self.printing = True

        for i in range(len(message)):
            sys.stdout.write(message[i])
            flush()
            sleep(delay)
        #sleep(2)
        self.printing = False

    def isPrinting(self):
        return self.printing
