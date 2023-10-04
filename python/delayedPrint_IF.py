import sys
from time import sleep

class DelayedPrint:
    def __init__(self):
        self.printing = False

    def print(self, message):
        #print(len(message))
        delay = .08751
        #print(delay)
        self.printing = True

        for i in range(len(message)):
            sys.stdout.write(message[i])
            sys.stdout.flush()
            sleep(delay)
        sleep(1)
        self.printing = False

    def isPrinting(self):
        return self.printing
