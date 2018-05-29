#!/usr/bin/python
#recording aspect of HapticGlove
import sys, json, time
# import RPi.GPIO as G

#use broadcom board labellings
# G.setmode(G.BCM)


def PlayFile(filename, duration = -1):
    print("PlayFile called. => decompresses json in file and plays sound representation up to 'arg2' seconds (-1 to loop file).")

    def farg(finger, booll):
        # given a string finger name and an on/off bool.
        print("lol")
    PlaybackLoop(filename,duration,farg)
    print("PlayFile ending.")
    
def ExecuteFile(filename,duration = -1):
    print("ExecuteFile called. => power vibration motors on GPIO pins.")
    try:
        import RPi.GPIO as G
        print("succesfully imported RPi.GPIO")

    except Exception as err:
        print("This system can't import RPi.GPIO. Is this system a raspberry pi?")
        print(err)
        # return
    #set up the rpi outputs.

    # G.setmode(G.BCM)
    # G.setwarnings(False)
    # PINS = [4,17,27,22,9,18,23,24,25,8]
    # TEST = [4,17,27,22,9]
    CONFIG = {"thumb":0,"index":1,"middle":2,"ring":3,"pinky":4}
    #set output pins for 10 3v 0.8mA rumble motors. start them at 0V.
    #we can use the following pins
    #4, 17, 27, 22, 9, 18, 23, 24, 25, 8, 7,  2 and 3 if l2C disabled, 14 and 15 if serial is disabled.

    # for i in TEST:
    #     G.setup(i, G.OUT)
    #     G.output(i,G.LOW)

    #on pi zeros, we have 20x2 pinouts, not 13x2 pinouts like on the b+, we have an additional set of pins:
    # 5, 6, 13, 19, 26, 12, 16, 20, 21

    def farg(finger, booll):
        val = 'on' if booll else 'off'
        #val =G.HIGH if booll else G.LOW
        print(finger + ": " + val)
        #G.output(TEST[CONFIG[finger]] ,val)
        #TODO turn on and off the appropriate vibrator based on the finger and boolean


    PlaybackLoop(filename,duration, farg)
    # for finger in TEST:
    #     # turn off stray finger data
    #     G.output(finger,G.LOW)



def PlaybackLoop(filename,duration,func):
    F = None
    try:
        import json
        F = json.load(open(filename, 'r'))
        # print(F)
    except Exception as err:
        print("Error loading given filename. Is " + filename + " a real file?")
        print(err)
        return
    # iterator counter
    F2 = {}
    for element in F:
        F2[element] = 0
    #execute main loop
    now = time.time
    STARTTIME = now()
    TOTAL = 0
    while((now() < (STARTTIME + duration - TOTAL)) or (duration < 0)):
        cur = now()-STARTTIME
        # for each finger, evaluate if we have passed the last index value or hit the end
        # if we hit the end, we wait for the last one to end, and then we loop back, resetting STARTTIME
        for finger in F:
            if F2[finger] >= len(F[finger]) or F2[finger] == -1:
                # set to -1
                F2[finger] = -1
                continue
            # if current time greater than the recording index, flip vibrator power and increase index
            if cur >= F[finger][F2[finger]]:
                F2[finger] += 1
                val = True if (F2[finger] % 2 != 0) else False
                func(finger,val)
                # print(finger + ": " + val)

        repeat = True
        for n in F2:
            if F2[n] != -1:
                repeat = False
                break
        if repeat:
            TOTAL += cur
            STARTTIME = now()
            for n in F2:
                F2[n] = 0




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
    NM = {pygame.K_SPACE:"thumb", pygame.K_q:"pinky",pygame.K_w:"ring",pygame.K_e:"middle",pygame.K_r:"index"}
    thmb = []
    #define channels for recording presses
    indx = []
    midl = []
    ring = []
    pink = []
    Lst = {NM[pygame.K_SPACE]:thmb, NM[pygame.K_q]:pink,NM[pygame.K_w]:ring,NM[pygame.K_e]:midl,NM[pygame.K_r]:indx}
    recording = True
    STARTTIME = time.time()
    print("recording keypresses of q, w, e, r, and space now...")
    while recording:
        for e in pygame.event.get():
            try:
                if e.type == pygame.locals.QUIT:
                    recording = not recording
                elif e.type == pygame.KEYDOWN:
                    if (NM[e.key] in Lst) and (len(Lst[NM[e.key]])%2 == 0):
                        Lst[NM[e.key]].append(time.time()-STARTTIME)
                        print("Detected listener press.")
                elif e.type == pygame.KEYUP:
                    if (NM[e.key] in Lst)  and (len(Lst[NM[e.key]])%2 == 1):
                        Lst[NM[e.key]].append(time.time()-STARTTIME)
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
    elif sys.argv[1] == "-R":
        print("recording inputs to place on file: " +str(sys.argv[2])+".json.")
        RecordFile(sys.argv[2]+".json")
    elif sys.argv[1] == "-P":
        seconds = -1
        fnm = ""
        if len(sys.argv) == 4:
            fnm = sys.argv[2]
            seconds = float(sys.argv[3])
        if len(sys.argv) == 3:
            fnm = sys.argv[2]
        if fnm != "":
            PlayFile(fnm,seconds)
        else:
            print("Play called, but no fname was provided to play.")
    elif sys.argv[1] == "-E":
        seconds = -1
        fnm = ""
        if len(sys.argv) == 4:
            fnm = sys.argv[2]
            seconds = float(sys.argv[3])
        if len(sys.argv) == 3:
            fnm = sys.argv[2]
        if fnm != "":
            ExecuteFile(fnm,seconds)
        else:
            print("Execute called, but no fname was provided to play.")



if __name__ == '__main__':
    main()
