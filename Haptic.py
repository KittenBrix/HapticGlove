# import RPi.GPIO as G
import time, pygame, sys
import pygame.locals
#use broadcom board labellings
# G.setmode(G.BCM)

#set output pins for 10 3v 0.8mA rumble motors
#we can use the following pins
#4, 17, 27, 22, 9, 18, 23, 24, 25, 8, 7,  2 and 3 if l2C disabled, 14 and 15 if serial is disabled.

#on pi zeros, we have 20x2 pinouts, not 13x2 pinouts like on the b+, we have an additional set of pins:
# 5, 6, 13, 19, 26, 12, 16, 20, 21

pygame.init()
BLK = (0,0,0)
W = 640
H = 360
WS = pygame.display.set_mode((W,H), 0, 32)
WS.fill(BLK)

#define channels for recording presses
thmb = []
indx = []
midl = []
ring = []
pink = []

Lst = {pygame.K_SPACE:thmb, pygame.K_q:pink,pygame.K_w:ring,pygame.K_e:midl,pygame.K_r:indx}





recording = True
STARTTIME = time.time()
print("recording 'c' keypresses now...")
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
for k in Lst:
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("list for " + str(k) + ":")
    print(Lst[k])
pygame.quit()
sys.exit()
