import os


line = open("monologi.txt", "r")
print(line.read())

os.system('espeak -p 0 -a 120 -s 120 -v english-us -f "monologi.txt"')
