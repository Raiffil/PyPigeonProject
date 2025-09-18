import pygame
import random
import numpy as np
import os

from Skins import load_menu_image
from Skins import load_pigeon_frames
from Skins import load_background
from Skins import load_restart_image

#Initialize pygame
pygame.init()

#Saving highscore
def load_high_score():
    #Load high score from file, or return 0 if no file exists
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

def save_high_score(score):
    #Save high score to file.
    with open("highscore.txt", "w") as f:
        f.write(str(score))

#Create a window
WinHeight = 900
WinWidth = 1500
screen = pygame.display.set_mode((WinWidth, WinHeight))
pygame.display.set_caption('Space Pigeon')

#Variables
animation_speed = 100  #Milliseconds per frame
gravity = 0.005 #How fast the bird falls
jump = -1.2  #How strong the jump is (negative = upward)
BirdWidth = 60
BirdHeight = 60

#Objects (pipes)
obj_width = 100
obj_speed = 1.2       #1.2 or 0.8 #how fast they move left
min_gap = 200
max_gap = 350
obj_spawn_interval = 800         #800 or 1000  #Time between obj spawns

#Font
font1 = pygame.font.SysFont(None, 40)
font2 = pygame.font.SysFont(None, 150)

#Menu
state = "menu"
running = True

#Menu button rects
start_btn = pygame.Rect(540, 350, 420, 140)
shop_btn  = pygame.Rect(540, 520, 420, 140)
quit_btn  = pygame.Rect(540, 685, 420, 140)

#Game over button rects
restart_btn = pygame.Rect(790, 565, 420, 140)
menu_btn    = pygame.Rect(290, 565, 420, 140)

def reset_game():
    global x, y, velocity, objects, score, last_obj_spawn_time, frame_index
    global last_update, animate, game_ready

    y = 200 #Starting position
    x = 500
    velocity = 0 #How fast the bird is moving at the time
    objects = []  #Objects list
    score = 0 #Current score
    last_obj_spawn_time = pygame.time.get_ticks()
    frame_index = 0
    last_update = pygame.time.get_ticks()
    animate = True
    game_ready = True #True when waiting for first jump

reset_game()

#Functions
pigeon_frames = load_pigeon_frames()
background = load_background()
menu_image = load_menu_image()
restart_image = load_restart_image()
high_score = load_high_score()

def create_obj(x_pos):
    gap_size = random.randint(min_gap, max_gap)  #Space the bird can fly through
    min_top = 80
    max_top = WinHeight - gap_size - 80
    gap_y = random.randint(min_top, max_top)
    return {'x': x_pos,'gap_y': gap_y,'gap_size': gap_size,'passed': False}

#Main loop
while running:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():  #Check for events
        if event.type == pygame.QUIT:  #End after pressing X
            running = False         #End Loop

        if state == 'menu':
            game_ready = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if start_btn.collidepoint(mx, my):
                    reset_game()
                    state = "game"
                elif shop_btn.collidepoint(mx, my):
                    print("Shop not implemented yet")
                elif quit_btn.collidepoint(mx, my):
                    running = False

        elif state == 'game':
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = "menu" #Go back to menu on ESC
                    if event.key == pygame.K_SPACE:
                        if game_ready:
                            game_ready = False
                            velocity += jump  #If Space is pressed → move up
                        else:
                            velocity += jump

        elif state == "restart":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if restart_btn.collidepoint(mx, my):
                    reset_game()
                    state = "game"
                elif menu_btn.collidepoint(mx, my):
                    state = "menu"

    if state == 'menu':
        screen.blit(menu_image, (0, 0))
        #Debug temp rects
        #pygame.draw.rect(screen, (255, 0, 0), start_btn, 2)
        #pygame.draw.rect(screen, (0,255,0), shop_btn, 2)
        #pygame.draw.rect(screen, (0,0,255), quit_btn, 2)

    elif state == "game":
        if not game_ready:
            velocity += gravity  #Gravity works as long as game is running
            clipped_velocity = np.clip(velocity, -100, 1)  #Clip velocity so the gravity is more controlled
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

                top_obj = pygame.Rect(int(obj['x']), 0, obj_width, int(obj['gap_y']))
                bottom_obj = pygame.Rect(int(obj['x']), int(obj['gap_y'] + obj['gap_size']), obj_width, WinHeight - int(obj['gap_y'] + obj['gap_size']))

                #Collision check per pipe
                if bird_rect.colliderect(top_obj) or bird_rect.colliderect(bottom_obj):
                    print("Collision! Game over. Score:", score)
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)  #Write new high score to file
                    state = "restart"
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
        score_text = font1.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (40, 40))


    elif state == "restart":
        screen.blit(restart_image,(0, 0))
        #Debug temp buttons rects part2
        #pygame.draw.rect(screen, (255, 0, 0), restart_btn, 2)
        #pygame.draw.rect(screen, (0, 255, 0), menu_btn, 2)

        #Show scores
        score_text = font2.render(f" {score}", True, (71, 37, 114))
        high_text  = font2.render(f" {high_score}", True, (71, 37, 114))
        screen.blit(score_text, (960, 410))
        screen.blit(high_text, (530, 410))

    #Press space to start
    if game_ready:
        ready_text = font2.render("Press SPACE to start", True, (255, 255, 255))
        screen.blit(ready_text, (WinWidth // 2 - ready_text.get_width() // 2, 400))

    pygame.display.flip()         #Update the window
