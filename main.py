from concurrent.futures import thread
from dbm import dumb
from ping3 import ping, verbose_ping
import time
import threading
import random
import PIL
from psutil import cpu_count, cpu_freq, cpu_stats, cpu_times
counter=0
#       0--1
counts=[0, 0]
pixel_drawcount=0
total_estPixels=254*255*255*255
print(
    "Est Pixel Count: ", total_estPixels,
    '\nPlease wait...'
    )
print('Total Core Count: ' + str(cpu_count()))
print('Core Stats: '+str(cpu_stats()))
time.sleep(5)

def DrawPixel(color):
    global pixel_drawcount

def CountPixel(color):
    #"black"(0), "white"(1)
    global counter, counts
    counter+=1
    if counter > 49:
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

#Pings All possible ip addresses
def collectPings(aIn, bIn=0, cIn=0, dIn=0):
    for a in range(254):
        if a>0:
            print('A Section Hit: '+str((a+1)+int(aIn)))
        for b in range(255):
            if b>0:
                print('B section Hit: '+str((a+1)+int(aIn))+'.'+str(b+int(bIn)))
            for c in range(255):
                for d in range(255):
                    #Returns False if Error and None if timed out.
                    if ping(str((a+1)+int(aIn))+'.'+str(b+int(bIn))+'.'+str(c+int(cIn))+'.'+str(d+int(dIn)), timeout=0.50) in [False, None]:
                        CountPixel('black')
                    else:
                        CountPixel('white')
                    time.sleep(2)

#Input sets(VarName, Var Equals) Outputs var with given name. Can be used to create randomly generated vars.
def createVarNameFromString(var,other):
        globals()[var]=other

used=[] #Will be used later as a reference to terminate proccess after comepletion.
for i in range(254):
    dumby=False
    print(i)
    while dumby==False:
        ab=''
        for i in range(6):
            ab+=random.choice('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefheijklmnopqrstuvwxyz')
        if ab not in used:
            used.append(ab)
            dumby=True #Ends section. Reloops until give range is complete.

#Creates Threads
for i in range(254):
    createVarNameFromString(used[i], threading.Thread(target=collectPings, args=(i,)))
    globals()[used[i]].start()
