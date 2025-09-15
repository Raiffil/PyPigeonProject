import pygame
import numpy as np
from Skins import load_pigeon_frames
from Skins import load_background

#Initialize pygame
pygame.init()

WinHeight = 900
WinWidth = 1500

#Create a window
screen = pygame.display.set_mode((WinWidth, WinHeight))
pygame.display.set_caption('Space Pigeon')

#Starting position
y = 200
x = 500

#Variables
frame_index = 0
animation_speed = 100  #Milliseconds per frame
last_update = pygame.time.get_ticks()
animate = True

gravity = 0.003 #How fast it falls
jump = -1.1 #How strong the jump is (negative = upward)
velocity = 0

BirdWidth = 120
BirdHeight = 120

#Functions
pigeon_frames = load_pigeon_frames()
background = load_background()

#Main loop
running = True
while running:
    for event in pygame.event.get():  #Check for events
        if event.type == pygame.QUIT:  #End after pressing X
            running = False         #End Loop
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: #End after pressing Escape
                running = False

            if event.key == pygame.K_SPACE:
                velocity += jump #If Space is pressed → move up

    velocity += gravity  #Gravity works as long as game is running
    clipped_velocity = np.clip(velocity,-100, 0.8 ) #clip velocity so the gravity is more controlled
    y += clipped_velocity  #Speed of bird is stored in velocity to make jump smooth

    if y < 0: #Prevent falling off the screen
        y = 0
    elif y > WinHeight - BirdHeight:
        y = WinHeight - BirdHeight

    #Animate bird
    now = pygame.time.get_ticks()
    if animate:
        if now - last_update > animation_speed:
            last_update = now
            frame_index = (frame_index + 1) % len(pigeon_frames) #Back to 0 after reaching the last frame
    else:
        frame_index = 0  #Idle frame

    #Visuals
    screen.fill((35, 32, 43))
    screen.blit(background,(0,0))
    pigeon = pigeon_frames[frame_index]
    screen.blit(pigeon,(x,y))

    pygame.display.flip()         #Update the window