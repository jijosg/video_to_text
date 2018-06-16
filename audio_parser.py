from converter import Converter
import speech_recognition as sr
import os
import sys

input = sys.argv[1]

c = Converter()
conv = c.convert( input, '/tmp/output.mp3', {
    'format': 'mp3',
    'audio': {
        'codec': 'mp3',
        'samplerate': 11025,
        'channels': 2
    }})
for timecode in conv:
    print "Converting (%f) ...\r" % timecode

os.system("ffmpeg -i /tmp/output.mp3 /tmp/output.wav")
os.system("rm /tmp/output.mp3")

duration = os.popen("ffmpeg -i /tmp/output.wav 2>&1 | grep \"Duration\"| cut -d ' ' -f 4 | sed s/,// | sed 's@\..*@@g' | awk '{ split($1, A, \":\"); split(A[3], B, \".\"); print 3600*A[1] + 60*A[2] + B[1] }'").read()
print "duration : "+duration
r = sr.Recognizer()
audioFile = sr.AudioFile("/tmp/output.wav")
splitDuration = 15
finalText = ""
for i in range(0,int(duration),15):
    with audioFile as source:
        audio = r.record(source,offset=i,duration=splitDuration)
        try:
            s = r.recognize_google(audio)
            finalText += s
        except Exception as e:
            print("Exception: "+str(e))

print finalText
os.system("rm /tmp/output.wav")