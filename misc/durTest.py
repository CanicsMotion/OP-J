import wave
import contextlib
fname = '/home/pi/Documents/Janeks Projects/Python/OP-J/rec/newRec.wav'
with contextlib.closing(wave.open(fname,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    print(duration)