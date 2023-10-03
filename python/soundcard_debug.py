#import pasimple
from amplitude_IF import Output

output = Output()
while True:
    print(output.read())


#while True:
    #with pasimple.PaSimple(
            #pasimple.PA_STREAM_RECORD,
            #pasimple.PA_SAMPLE_S16LE,
            #1,
            #22050,
            #app_name='python',
            #stream_name=None,
            #server_name=None,
            #device_name='alsa_output.platform-bcm2835_audio.analog-stereo.monitor',
            #maxlength=-1,
            #tlength=-1,
            #prebuf=-1,
            #minreq=-1,
            #fragsize=-1
            #) as stream:
        #print(stream)
        #if stream:
            #data = stream.read(8)
            #print(sum(list(data)))
            #print(list(data)[4], list(data)[6]) # / 0-255
            #print(list(data)[6]) # / 0-255
            
