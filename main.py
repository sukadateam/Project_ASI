from concurrent.futures import thread
from dbm import dumb
from ping3 import ping, verbose_ping
import time
import threading
import random
counter=0

def DrawPixel(color):
    #"black"(0), "white"(1)
    pass

#Pings All possible ip addresses
def collectPings(aIn, bIn=0, cIn=0, dIn=0):
    for a in range(254):
        print('A Section Hit: '+str((a+1)+int(aIn)))
        for b in range(255):
            print('B section Hit: '+str((a+1)+int(aIn))+'.'+str(b+int(bIn)))
            for c in range(255):
                for d in range(255):
                    #Returns False if Error and None if timed out.
                    if ping(str((a+1)+int(aIn))+'.'+str(b+int(bIn))+'.'+str(c+int(cIn))+'.'+str(d+int(dIn)), timeout=0.50) in [False, None]:
                        DrawPixel('black')
                    else:
                        DrawPixel('white')

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
            dumby=True #Ends section. Reloops until give range in complete.

#Creates Threads
for i in range(254):
    createVarNameFromString(used[i], threading.Thread(target=collectPings, args=(i,)))
    globals()[used[i]].start()
