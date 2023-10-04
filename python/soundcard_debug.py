from amplitude_IF import Output
from arduinoIF import Arduino
from time import sleep

output = Output()
arduino = Arduino()
arduino.connect()


while True:
    #print(output.read())
    arduino.write('p'+str(output.read()))
