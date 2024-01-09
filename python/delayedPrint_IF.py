import sys
from time import sleep

flush = sys.stdout.flush

class DelayedPrint:
    def __init__(self):
        self.printing = False

    def print(self, message):
        chars = set('/-,.:;()')
        delay = .08744
        if any((c in chars) for c in message):
            delay = delay
        else:
            delay = delay - .001
            sys.stdout.write('>')
            flush()
        flush()
        self.printing = True

        for i in range(len(message)):
            sys.stdout.write(message[i])
            flush()
            sleep(delay)
        self.printing = False

    def isPrinting(self):
        return self.printing
