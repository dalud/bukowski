import os
import re
from random import random


class Searcher:
    def __init__(self, path):
        self.dir_path = path
        for file in os.listdir(self.dir_path): print(file)

    def parse(self, content, index):
        # search previous and next punctuation
        start = 0
        end = 0
        # seek start
        for x in range(index, 0, -1):
            if content[x] == "." or content[x] == "!" or content[x] == "?":
                start = x+1
                break
        # seek end
        for x in range(index, len(content)):
            if content[x] == "." or content[x] == "!" or content[x] == "?":
                end = x
                break
        res = content[start:end].replace('"', '').replace('“', '')
        # TODO: remove lines with only numbers
        return self.sanitize(res)

    def find(self, word, played):
        # iterate each file in a directory
        for file in os.listdir(self.dir_path):
            cur_path = os.path.join(self.dir_path, file)
            print(file)
            # check if it is a file
            if os.path.isfile(cur_path):
                with open(cur_path, 'r') as file:                    
                    # read all content of a file and search string
                    content = file.read().lower()
                    for x in range(content.count(word)):
                        i = content.find(word)
                        if not i: continue
                        #print(i)
                        reply = self.parse(content, i)
                        if reply in played:
                            #print("already said")
                            i = content.find(word, i+1)
                            if i > 0: reply = self.parse(content, i)
                            if i < 0: continue
                        if not reply in played: return reply
                        
    def sanitize(self, string):
        reply = []
        for line in string.splitlines():
            #print(line)
            if not line == "" and not line.isdigit():
                reply.append(line)
        return reply
