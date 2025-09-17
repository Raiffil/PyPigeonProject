import pygame
import random
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

gravity = 0.005 #How fast it falls
jump = -1.2  #How strong the jump is (negative = upward)
velocity = 0

BirdWidth = 60
BirdHeight = 60

#Objects (pipes)
obj_width = 100
obj_speed = 1.2     #How fast they move left
obj_gap = 250

#min_gap = 200
#max_gap = 400
#obj_gap = random.randint(min_gap, max_gap) #Space the bird can fly through

#Object spawn timing (ms)
obj_spawn_interval = 800   #Time between obj spawns
last_obj_spawn_time = pygame.time.get_ticks()
objects = [] #Objects list

#Score
score = 0
font = pygame.font.SysFont(None, 48)

#Functions
pigeon_frames = load_pigeon_frames()
background = load_background()

def create_obj(x_pos):
    min_top = 80  #Makes the gap in random y
    max_top = WinHeight - obj_gap - 80
    gap_y = random.randint(min_top, max_top)
    return {'x': x_pos, 'gap_y': gap_y, 'passed': False}

#Main loop
running = True
while running:
    now = pygame.time.get_ticks()
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
    clipped_velocity = np.clip(velocity,-100, 1 ) #Clip velocity so the gravity is more controlled
    y += clipped_velocity  #Speed of bird is stored in velocity to make jump smoother

    if y < 0: #Prevent falling off the screen
        y = 0
    elif y > WinHeight - BirdHeight:
        y = WinHeight - BirdHeight

    if now - last_obj_spawn_time > obj_spawn_interval:
        last_obj_spawn_time = now  #Spawns objects
        spawn_x = WinWidth + 20
        objects.append(create_obj(spawn_x))

    bird_rect = pygame.Rect(x, int(y), BirdWidth, BirdHeight) #Bird hitbox
    new_obj = []
    for obj in objects:
        obj['x'] -= obj_speed  #Make objects move left

        #Draw the objects
        top_obj = pygame.Rect(int(obj['x']), 0, obj_width, int(obj['gap_y']))
        bottom_obj = pygame.Rect(int(obj['x']), int(obj['gap_y'] + obj_gap), obj_width, WinHeight - int(obj['gap_y'] + obj_gap))

        #Collision check per pipe
        if bird_rect.colliderect(top_obj) or bird_rect.colliderect(bottom_obj):
            print("Collision! Game over. Score:", score)
            running = False
            break

        #When object passes the bird's x coordinate get a point
        if not obj['passed'] and (obj['x'] + obj_width) < x:
            obj['passed'] = True
            score += 1

        #Keep the object if it's still on screen (or a bit past left edge)
        if obj['x'] + obj_width > -50:
            new_obj.append(obj)

        #Save rects inside the object so they can be drawn after the background
        obj['top_rect'] = top_obj
        obj['bottom_rect'] = bottom_obj

    #Replace objects list with surviving objects
    objects = new_obj

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

    obj_color = (255, 255, 255)
    for obj in objects:
        pygame.draw.rect(screen, obj_color, obj['top_rect'])
        pygame.draw.rect(screen, obj_color, obj['bottom_rect'])

    pigeon = pigeon_frames[frame_index]
    screen.blit(pigeon,(x,y))

    #Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    pygame.display.flip()         #Update the window