import os

#dir_path = r'C:\Users\jaakk\OneDrive\Documents\poems'
#word = "cat"

class SearchInFiles:
    def __init__(self, path):
        self.dir_path = path

    def parseSentence(self, content, word):
        # search previous punctuation
        start = 0;
        end = 0;
        # seek start
        for x in range(content.index(word), 0, -1):
            if content[x] == ".":
                start = x+1
                break
        # seek end
        for x in range(content.index(word), len(content)):
            if content[x] == ".":
                end = x
                break
        return content[start:end]

    def search(self, word):
        # iterate each file in a directory
        for file in os.listdir(dir_path):
            print(file)
            cur_path = os.path.join(dir_path, file)
            # check if it is a file
            if os.path.isfile(cur_path):
                with open(cur_path, 'r') as file:
                    # read all content of a file and search string
                    if word in file.read():
                        # rewind and find sentence with matching string
                        file.seek(0)
                        content = file.read()
                        print(parseSentence(content, word))
                        break

