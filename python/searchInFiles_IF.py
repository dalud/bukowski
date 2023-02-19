import os
import re
from random import random

ponder = ["let me see", "i wonder", "maybe?"]

class Searcher:
    def __init__(self, path):
        self.dir_path = path
        #print(os.listdir(self.dir_path))
        for file in os.listdir(self.dir_path): print(file)

    def parseSentence(self, content, word):
        # search previous punctuation
        start = 0
        end = 0
        # seek start
        for x in range(content.index(word), 0, -1):
            if content[x] == ".":
                start = x+1
                break
        # seek end
        for x in range(content.index(word), len(content)):
            if content[x] == ".":
                end = x+1
                break
        return content[start:end]

    def search(self, word):
        # iterate each file in a directory
        for file in os.listdir(self.dir_path):
            cur_path = os.path.join(self.dir_path, file)
            # check if it is a file
            if os.path.isfile(cur_path):
                with open(cur_path, 'r') as file:
                    # read all content of a file and search string
                    if word in file.read():
                        # rewind and find sentence with matching string
                        file.seek(0)
                        content = file.read()
                        return self.parseSentence(content, word)

    def findNext(self, word, played, mouth):
        mouth.speak(ponder[(int)(random()*len(ponder))])
        for file in os.listdir(self.dir_path):
            for r in re.findall(r"([^.]*?{0}[^.]*\.)".format(word), open(os.path.join(self.dir_path, file)).read()):
                if r not in played:
                    return r

    
