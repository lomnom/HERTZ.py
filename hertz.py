import sys #import sys to get arguments

mode=sys.argv[1]

#command parsing
if mode=="-help": #help screen
	print("USAGE:")
	print("python hertz.py hertz [pin] [length] [hertz] [debug]")
	print("eg. \"python hertz.py hertz 18 10 30\"")
	print("python hertz.py delay [pin] [length] [delay] [debug]")
	print("eg. \"python hertz.py delay 18 10 1\"")
	print("python hertz.py customDelay [pin] [length] [offDelay] [onDelay] [debug]")
	print("eg. \"python hertz.py customDelay 18 10 0.2 1\"")
	print("for debug, add \"debug\" at the end of the command")
	print("for infinite time, put \"-1\" as the time")
	print("to oscillate between multiple pins, put [pin1,pin2] as the pin")
	print("eg. python hertz.py hertz [18,23] -1 1")
	quit()
elif mode=="hertz": #python hertz.py hertz [pin] [length] [hertz] [debug]
	delay=None
	onPercent=100
	offPercent=100
	hertz=float(sys.argv[4])
	length=float(sys.argv[3])
	onWait=(1.0/float(hertz))*(float(onPercent)/100.0) #calculate time for led to be on
	offWait=(1.0/float(hertz))*(float(offPercent)/100.0) #calculate time for led to be off
	try: #check for debug
		if sys.argv[5]=="debug":
			debug=True
	except:
		debug=False
elif mode=="delay": #python hertz.py delay [pin] [length] [delay] [debug]
	hertz=None
	onPercent=100
	offPercent=100
	length=float(sys.argv[3])
	delay=float(sys.argv[4])
	onWait=delay #calculate time for led to be on
	offWait=delay #calculate time for led to be off
	try: #check for debug
		if sys.argv[5]=="debug":
			debug=True
	except:
		debug=False
elif mode=="customDelay": #python hertz.py customDelay [pin] [length] [offDelay] [onDelay] [debug]
	hertz=None
	onPercent=100
	offPercent=100
	length=float(sys.argv[3])
	delay=None
	offWait=float(sys.argv[4])
	onWait=float(sys.argv[5])
	try: #check for debug
		if sys.argv[6]=="debug":
			debug=True
	except:
		debug=False

#define debug funcions
if debug: #import datetime for debug logs
	from datetime import datetime
	def log(message): #define logging function to prevent repeated code
		currentTime = str(datetime.now().time())
		print("["+currentTime+"] "+message)
def done(): #log program exits if debug mode
	if debug:
		log("program exiting...")
	quit()

#import needed libraries
#check if gpio installed
try:
	import RPi.GPIO as GPIO #import pin comtrol
except:
	print("RPI.GPIO not installed!!!")
	done()
import time #import time for delay

#init GPIO
GPIO.setmode(GPIO.BCM) #use BCM pin numbering
GPIO.setwarnings(debug) #set warnings to on if debug mode, off otherwise

#parse pin to use
try:
	pin=int(sys.argv[2])
	doublePin=False
except:
	import ast
	pin=ast.literal_eval(sys.argv[2]) #parse input into list
	pin1=pin[0] #set pin
	pin2=pin[1]
	doublePin=True
	#log if doublepin
	if debug:
		log("doublePin: "+ str(doublePin))
		log("pin1: "+ str(pin1))
		log("pin2: "+ str(pin2))

#init pin to use
try: #check for valueError (invalidpin)
	if not doublePin: #init single pin if not doublePin
		GPIO.setup(int(pin),GPIO.OUT) #init used pin
	else:
		GPIO.setup(int(pin1),GPIO.OUT)
		GPIO.setup(int(pin2),GPIO.OUT)
except:
	if doublePin: #error
			print("either pin "+str(pin1)+" or pin "+str(pin2)+" is invalid!")
	else:
			print("pin \""+str(pin)+"\" is not valid") #log error
	done()

#print variables if debug
if debug:
	log("mode: "+str(mode)) #print all arguments
	log("pin: "+str(pin))

	log("hertz: "+str(hertz)) #hertz mode only

	log("delay: "+str(delay)) #delay mode only

	log("length: "+str(length))
	log("offPercent: "+str(offPercent))
	log("onPercent: "+str(onPercent))
	log("offWait: "+str(offWait))
	log("onWait: "+str(onWait))

#LED control functions
def on(GPIOused): #define on function to avoid repeated code
	GPIO.output(int(GPIOused),GPIO.HIGH) #on
	if debug:
		log("led on pin"+str(GPIOused)+" on")

def off(GPIOused): #define off function to avoid repeated code
	GPIO.output(int(GPIOused),GPIO.LOW) #off
	if debug:
		log("led on pin"+str(GPIOused)+" off")

#check for infinite time
if int(length)==-1: 
	infinite=True
	if debug:
		log("length is -1. making infinite true") #log in debug
else:
	infinite=False

#set needed vars
timeStrobing=0 

if debug:
	iteration=0 #track number of iterations if debug

#main program
try: #enclose loop to make keyboardinterrupt shut down led before closing
	#strobe loop
	while True:
		#track number of iterations if debug
		if debug: 
			iteration+=1 #increment iterations
			log("iteration: "+str(iteration)) #print iterations

		#toggle LED and wait
		if not doublePin:
			on(pin) #turn LED on\
		else:
			on(pin1)
			off(pin2)
		time.sleep(onWait) #delay before turning off

		#add time used for strobing in previous half-iteration to counter
		timeStrobing=timeStrobing+onWait

		#print timeStrobing if debug
		if debug:
			log("timeStrobing: "+str(timeStrobing))

		#if infinite, dont do timecheck
		if not infinite: 
			if timeStrobing>=float(length): #check if timeStrobing is more than needed strobe time
				if debug:
					log("timeStrobing >= length") #print that timeStrobing >= length if debug mode
				off() #turn off led
				done() #exit program

		#turn off led and wait
		if not doublePin:
			off(pin) #turn LED on\
		else:
			off(pin1)
			on(pin2)
		time.sleep(offWait) #delay before turning on

		#add time used for strobing in previous half-iteration to counter
		timeStrobing=timeStrobing+offWait #add delay before turning on to curent duration of strobing.

		#print timeStrobing if debug
		if debug: 
			log("timeStrobing: "+str(timeStrobing))

		#if infinite, dont do timecheck
		if not infinite: #if infinite, dont do timecheck
			if timeStrobing>=float(length): #check if timeStrobing is more than needed strobe time
				if debug:
					log("timeStrobing >= length") #print that timeStrobing >= length if debug mode
				done() #exit program
#error handling
except KeyboardInterrupt: #ctrl-c
	if debug:
		log("ctrl-c detected. turning led off and exiting.") #log that ctrl-c detected
	if doublePin: #turn off all leds
		off(pin1)
		off(pin2)
	else:
		off(pin)
	done()
