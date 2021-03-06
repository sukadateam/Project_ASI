'''Version #: 0.1.4'''
while input("Hit Enter To Start: ") == None:
    pass
# Importing Essential Tools
from dbm import dumb #I'm Dumb
from ping3 import ping #Bing Bong.
import time #What time is it?
import threading #Not releated to sowing. Makes the program run faster by utilizing more cpu power.
import random #Just a bit of random to spice things up :)
from PIL import Image #Draws/Creates an image.
from psutil import cpu_count, cpu_stats #What does my hardware; that I spent way to much on, look like?
import os #Uses Operating System tools
import sys #Uses System Hardware tools.
import math #1 + 1 = 3 :)

# Create Essential Variables.
debug=True #Default = False
counter=0
threadCount=0 #Counts the amount of applicable threads created(exempting the orginal process).
ClosingInProgress=False #Lets other threads know an error has occured.
try:
    os.chdir('Desktop') #Sets the root directory. So I know where I am.
except:
    pass
#       0--1
counts=[0, 0] #Pixel Memory
pixel_drawcount=0
total_estPixels=254*255*255*255
SquareRoot=math.sqrt(total_estPixels)
SquareRootRound=round(SquareRoot) #Max X/Y Length
TotalFit=SquareRootRound*SquareRootRound
print(
    "\nEst Pixel Count: ", total_estPixels,
    "\nSquare Root: ", SquareRoot,
    "\nRounded Square Root: ", SquareRootRound, 
    "\nReverse Square Root: ", TotalFit, 
    '\nPlease wait...\n'
    )
print('Total Core Count: ' + str(cpu_count()))
print('Core Stats: '+str(cpu_stats()))
if debug==False:
    print('Launching in 5 seconds...')
    time.sleep(5) #Default = 5

# Partial Credit(StackOverflow) From, Unknown user.
class MyThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()
    def stop(self):
        # Kill code
        self._stop.set()
    def stopped(self):
        # Returns the stop status
        return self._stop.isSet()
    def run(self):
        # Edit this function to change each/all threads purpose.
        global threadCount
        collectPings(threadCount)

image = Image.new('RGB', (int(SquareRootRound), int(SquareRoot)))
DrawPixelCounterVert=0
DrawPixelCounterHorz=0 #Protects the system from drawing invisible pixels/Causing Errors
def DrawPixel(color):
    if color == "black":
        colorSet=(0, 0, 0)
    if color == "white":
        colorSet=(255, 255, 255)
    global pixel_drawcount, image, DrawPixelCounterVert, DrawPixelCounterHorz
    if DrawPixelCounterHorz == SquareRootRound: 
        DrawPixelCounterVert+=1
        if debug==True:
            print('DrawPixelCounterVert: ', DrawPixelCounterVert)
            time.sleep(.5)
        DrawPixelCounterHorz=0
    try:
        image.putpixel((DrawPixelCounterVert, DrawPixelCounterHorz), (colorSet))
    except Exception as Error:
        global CloseAllThreads, ClosingInProgress
        if ClosingInProgress==False:
            CloseThreads()
            ClosingInProgress=True
            sys.exit()
    DrawPixelCounterHorz+=1

# Counts the amount of black and white pixels.
def CountPixel(color):
    #"black"(0), "white"(1)
    global counter, counts
    counter+=1
    if counter > 299:
        os.system('clear')
        counter=0
        print(
            "Black: "+str(counts[0]),
            "White: "+str(counts[1]),
        )
    if color == "black":
        counts[0]+=1
    elif color == "white":
        counts[1]+=1
    DrawPixel(color)

# Pings All possible IP addresses
def collectPings(aIn, bIn=0, cIn=0, dIn=0):
    global ClosingInProgress
    if ClosingInProgress==False: #Destroys the process ability to continue.
        for a in range(254):
            if a>0:
                print('A Section Hit: '+str((a+1)+int(aIn)))
            for b in range(255):
                if b>0:
                    print('B section Hit: '+str((a+1)+int(aIn))+'.'+str(b+int(bIn)))
                for c in range(255):
                    for d in range(255):
                        #Returns False if Error and None if timed out.
                        try:
                            if ping(str((a+1)+int(aIn))+'.'+str(b+int(bIn))+'.'+str(c+int(cIn))+'.'+str(d+int(dIn)), timeout=0.50) in [False, None]:
                                CountPixel('black')
                            else:
                                CountPixel('white')
                        except:
                            print("Well shit.")
                            sys.exit()

# Input sets(VarName, Var Equals) Outputs var with given name. Can be used to create randomly generated vars.
def createVarNameFromString(var,other):
    globals()[var]=other

used=[] # Will be used later as a reference to terminate proccess after comepletion.
# Assigns random names for values.
for i in range(254):
    dumby=False
    while dumby==False:
        ab=''
        for i in range(6):
            ab+=random.choice('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefheijklmnopqrstuvwxyz')
        if ab not in used:
            used.append(ab)
            dumby=True # Ends section. Reloops until give range is complete.

# Creates Threads
for i in range(254):
    createVarNameFromString(used[i], MyThread())
    globals()[used[i]].start()

# Closes Existing Threads without closing the main proccess.
def CloseThreads(args=None):
    global used
    for i in range(254):
        print("Closing Thread:", i)
        globals()[used[i]].stop()

CloseAllThreads=threading.Thread(target=CloseThreads)

# Closes safely
def closeProgram():
    global image
    image.save('output-ip-addresses.png')

closeProgram()
