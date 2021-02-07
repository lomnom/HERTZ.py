Dependencies:
RPI.GPIO

Runs on python 2.7

USAGE:
python hertz.py hertz [pin] [length] [hertz] [debug]
eg. "python hertz.py hertz 18 10 30"
python hertz.py delay [pin] [length] [delay] [debug]
eg. "python hertz.py delay 18 10 1"
python hertz.py customDelay [pin] [length] [offDelay] [onDelay] [debug]
eg. "python hertz.py customDelay 18 10 0.2 1"
for debug, add "debug" at the end of the command
for infinite time, put "-1" as the time
