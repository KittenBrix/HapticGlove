#!/usr/bin/python
#recording aspect of HapticGlove
import sys, json, time
# import RPi.GPIO as G

#use broadcom board labellings
# G.setmode(G.BCM)



def PlayFile(filename, duration = -1):
    print("PlayFile called. => decompresses json in file and plays sound representation up to 'arg2' seconds (-1 for full file).")

def ExecuteFile(filename,duration = -1):
    print("ExecuteFile called. => power vibration motors on GPIO pins.")
    try:
        import RPi.GPIO as G
        print("succesfully imported RPi.GPIO")

    except Exception as err:
        print("This system can't import RPi.GPIO. Is this system a raspberry pi?")
        print(err)

    #set output pins for 10 3v 0.8mA rumble motors
    #we can use the following pins
    #4, 17, 27, 22, 9, 18, 23, 24, 25, 8, 7,  2 and 3 if l2C disabled, 14 and 15 if serial is disabled.

    #on pi zeros, we have 20x2 pinouts, not 13x2 pinouts like on the b+, we have an additional set of pins:
    # 5, 6, 13, 19, 26, 12, 16, 20, 21

def RecordFile(filename = ""):
    print("RecordFile called.")
    import pygame
    import pygame.locals
    pygame.init()
    COL = (0,0,0)
    W = 128
    H = 90
    WS = pygame.display.set_mode((W,H), 0, 32)
    WS.fill(COL)

    #define channels for recording presses
    thmb = []
    indx = []
    midl = []
    ring = []
    pink = []
    Lst = {pygame.K_SPACE:thmb, pygame.K_q:pink,pygame.K_w:ring,pygame.K_e:midl,pygame.K_r:indx}
    recording = True
    STARTTIME = time.time()
    print("recording keypresses of q, w, e, r, and space now...")
    while recording:
        for e in pygame.event.get():
            try:
                if e.type == pygame.locals.QUIT:
                    recording = not recording
                elif e.type == pygame.KEYDOWN:
                    if (e.key in Lst) and (len(Lst[e.key])%2 == 0):
                        Lst[e.key].append(time.time()-STARTTIME)
                        print("Detected listener press.")
                elif e.type == pygame.KEYUP:
                    if (e.key in Lst)  and (len(Lst[e.key])%2 == 1):
                        Lst[e.key].append(time.time()-STARTTIME)
                        print("Detected listener release.")
            except Exception as ew:
                print(ew)
    #print the record
    for k in Lst:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("list for " + str(k) + ":")
        print(Lst[k])
    #save the record
    if filename == "":
        filename = "Record_" +str(time.time())+".json"
    f = open(filename,"w")
    f.write(json.dumps(Lst))
    f.close()
    #dispose of pygame resources
    pygame.quit()


def main():
    print(sys.argv)
    if (len(sys.argv) <= 1) or (sys.argv[1] not in ["-R","-P","-E"]):
        print("improper execution for " + str(sys.argv[0]) + ".")
        print("available options are:")
        print("-R 'fname'      :  opens record window and logs q, w, e, r, and space keypresses into optional 'fname' file.")
        print("                   Requires pygame.")
        print("-P 'fname' 's'  :  plays tone interpretation of 'fname' for 's' seconds. Requires pyAudio.")
        print("-E 'fname' 's'  :  plays vibration interpretation of 'fname' for 's' seconds. Requires execution on RPI.")
    elif len(sys.argv) == 2 and sys.argv[1] == "-R":
        print("no filename was specified, recording using time based name.")
        RecordFile()
    elif len(sys.argv) == 3 and sys.argv[1] == "-R":
        RecordFile(sys.argv[2])


if __name__ == '__main__':
    main()
