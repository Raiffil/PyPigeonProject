import pygame
import random
import numpy as np
import os

from Skins import load_menu_image
from Skins import load_pigeon_frames
from Skins import load_background
from Skins import load_restart_image
from Skins import load_star_image
from Skins import load_shop_image
from Skins import load_bird1_frames, load_bird2, load_bird3, load_bird4
from Skins import load_gate1, load_gate2, load_gate3, load_gate4

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

def load_stardust():
    #Load stardust from file, or return 0 if no file exists
    if os.path.exists("stardust.txt"):
        with open("stardust.txt", "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

def save_stardust(amount):
    #Save stardust to file
    with open("stardust.txt", "w") as f:
        f.write(str(amount))


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
star_size = 50
star_chance = 0.4   #Chance a star spawns in a gap
stars = []          #Active star list

#Lock gates in shop
unlocked_slots = [True, False, False, False, False]  #Slot 0 always unlocked
lock_costs = [0, 10, 20, 30, 40]  #Stardust cost per slot

#Objects (pipes)
obj_width = 100
min_gap = 200
max_gap = 350

base_obj_speed = 0.8          #Starting object speed
max_obj_speed = 3.0           #Maximum object speed

base_obj_spawn_interval = 1000 #Spawning time between objects (ms)
min_spawn_interval = 400      #Minimum time between objects

speed_increment = 0.05        #How much speed increases per point
interval_decrement = 20        #How much spawn interval decreases per point

#Font
font1 = pygame.font.SysFont(None, 40)
font2 = pygame.font.SysFont(None, 150)

#Game start
state = "menu"
running = True

#Menu button rects
start_btn = pygame.Rect(540, 350, 420, 140)
shop_btn  = pygame.Rect(540, 520, 420, 140)
quit_btn  = pygame.Rect(540, 685, 420, 140)

#Game over button rects
restart_btn = pygame.Rect(790, 565, 420, 140)
menu_btn    = pygame.Rect(290, 565, 420, 140)

#Shop button rects
shop_start_btn = pygame.Rect(885, 620, 420, 140)
shop_menu_btn = pygame.Rect(185, 620, 420, 140)

#Skin selection slots in shop
skin_slots = [
    pygame.Rect(195, 392, 200, 200),  # Slot 0: pigeon
    pygame.Rect(420, 392, 200, 200),  # Slot 1: bird1
    pygame.Rect(645, 392, 200, 200),  # Slot 2: bird2
    pygame.Rect(875, 392, 200, 200),  # Slot 3: bird3
    pygame.Rect(1100, 392, 200, 200)  # Slot 4: bird4
]

# Preview slot for currently selected skin
preview_slot = pygame.Rect(192, 160, 200, 200)

selected_skin = 0  # Default: animated pigeon


def reset_game():
    global x, y, velocity, objects, score, last_obj_spawn_time, frame_index
    global last_update, animate, game_waiting, stars

    y = 200 #Starting position
    x = 500
    velocity = 0 #How fast the bird is moving at the time
    objects = []  #Objects list
    score = 0 #Current score
    last_obj_spawn_time = pygame.time.get_ticks()
    frame_index = 0
    last_update = pygame.time.get_ticks()
    animate = True
    game_waiting = True #True when waiting for first jump
    stars = []

reset_game()

#Functions
pigeon_frames = load_pigeon_frames()
background = load_background()
menu_image = load_menu_image()
restart_image = load_restart_image()
high_score = load_high_score()
star_image = load_star_image()
stardust = load_stardust()
shop_image = load_shop_image()
bird1 = load_bird1_frames()
bird2 = load_bird2()
bird3 = load_bird3()
bird4 = load_bird4()
gate1 = load_gate1()
gate2 = load_gate2()
gate3 = load_gate3()
gate4 = load_gate4()

#Variables tied to functions
static_birds = [bird1[0], bird2, bird3, bird4] #Static images used in shop
lock_images = [None, gate1, gate2, gate3, gate4]  #Slot 0 has no lock

def create_obj(x_pos):
    gap_size = random.randint(min_gap, max_gap)  #Space the bird can fly through
    min_top = 80
    max_top = WinHeight - gap_size - 80
    gap_y = random.randint(min_top, max_top)
    if random.random() < star_chance:
        star_y = gap_y + gap_size // 2 - star_size // 2
        stars.append({'x': x_pos + obj_width // 2 - star_size // 2, 'y': star_y, 'collected': False})
    return {'x': x_pos,'gap_y': gap_y,'gap_size': gap_size,'passed': False}

#Main loop
while running:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():  #Check for events
        if event.type == pygame.QUIT:  #End after pressing X
            save_stardust(stardust)  #Save stardust before quitting
            running = False         #End Loop

        if state == 'menu':
            game_waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if start_btn.collidepoint(mx, my):
                    reset_game()
                    state = "game"
                elif shop_btn.collidepoint(mx, my):
                    state = "shop"
                elif quit_btn.collidepoint(mx, my):
                    running = False

        elif state == 'game':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "menu" #Go back to menu on ESC
                if event.key == pygame.K_SPACE:
                    if game_waiting:
                        game_waiting = False
                        velocity += jump  #If Space is pressed → move up
                    else:
                        velocity += jump

        elif state == 'restart':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if restart_btn.collidepoint(mx, my):
                    reset_game()
                    state = "game"
                elif menu_btn.collidepoint(mx, my):
                    state = "menu"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "menu"

        elif state == 'shop':
            game_waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if shop_start_btn.collidepoint(mx, my):
                    reset_game()
                    state = "game"
                elif shop_menu_btn.collidepoint(mx, my):
                    state = "menu"
                for i, rect in enumerate(skin_slots):
                    if rect.collidepoint(mx, my):
                        if unlocked_slots[i]:
                            selected_skin = i
                        elif stardust >= lock_costs[i]:
                            #Spend stardust and unlock slot
                            stardust -= lock_costs[i]
                            save_stardust(stardust)
                            unlocked_slots[i] = True
                            selected_skin = i
                        break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "menu"


    if state == "menu":
        screen.blit(menu_image, (0, 0))
        #Debug temp rects
        #pygame.draw.rect(screen, (255, 0, 0), start_btn, 2)
        #pygame.draw.rect(screen, (0,255,0), shop_btn, 2)
        #pygame.draw.rect(screen, (0,0,255), quit_btn, 2)

    elif state == "game":
        if not game_waiting:
            #Make the game harder over time
            obj_speed = min(base_obj_speed + score * speed_increment, max_obj_speed)
            obj_spawn_interval = max(base_obj_spawn_interval - score * interval_decrement, min_spawn_interval)

            #Bird physics
            velocity += gravity  #Gravity works as long as game is running
            clipped_velocity = np.clip(velocity, -1.2, 1)  #Clip velocity so the gravity is more controlled
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


        #Stars
        new_stars = []
        for star in stars:
            star['x'] -= obj_speed  #Move with objects
            star_rect = pygame.Rect(star['x'], star['y'], star_size, star_size)

            #Check collision with bird
            if not star['collected'] and bird_rect.colliderect(star_rect):
                star['collected'] = True
                stardust += 1
                save_stardust(stardust) #Saves to file

             #Keep star if still on screen and not collected
            if star['x'] > -star_size and not star['collected']:
                new_stars.append(star)

        stars = new_stars

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



        #Draw stars
        for star in stars:
            screen.blit(star_image, (star['x'], star['y']))

        #Show stardust
        stardust_text = font1.render(f"Stardust: {stardust}", True, (255, 255, 255))
        screen.blit(stardust_text, (40, 80))

        #Draw the selected bird
        if selected_skin == 0:
            #Animated pigeon
            pigeon_img = pigeon_frames[frame_index]
        elif selected_skin == 1:
            #Animated bird1
            pigeon_img = bird1[frame_index]
        else:
            #Static birds (bird2, bird3, bird4)
            pigeon_img = static_birds[selected_skin - 1]

        screen.blit(pygame.transform.scale(pigeon_img, (BirdWidth, BirdHeight)), (x, y))

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

    elif state == "shop":
        game_waiting = False
        screen.blit(shop_image, (0, 0))

        #Draw stardust counter
        stardust_text = font2.render(f"{stardust}", True, (255, 255, 255))
        screen.blit(stardust_text, (950, 220))

        #Draw skin selection slots
        for i, rect in enumerate(skin_slots):
            img = pigeon_frames[0] if i == 0 else static_birds[i - 1]
            screen.blit(pygame.transform.scale(img, (rect.width, rect.height)), rect.topleft)

            #Draw lock overlay if slot is still locked
            if not unlocked_slots[i] and i != 0:
                lock_img_scaled = pygame.transform.scale(lock_images[i], (rect.width, rect.height))
                screen.blit(lock_img_scaled, rect.topleft)

            #Debug temp frame
            #pygame.draw.rect(screen, (255, 255, 255), rect, 2)

        #Draw preview of currently selected skin
        preview_img = pigeon_frames[0] if selected_skin == 0 else static_birds[selected_skin - 1]
        screen.blit(pygame.transform.scale(preview_img, (preview_slot.width, preview_slot.height)),
                    preview_slot.topleft)
        #pygame.draw.rect(screen, (0, 255, 255), preview_slot, 4)  #Debug temp border

        #Debug temp buttons rects part3
        #pygame.draw.rect(screen, (255, 0, 0), shop_start_btn, 2)
        #pygame.draw.rect(screen, (0, 255, 0), shop_menu_btn, 2)

    #Press space to start
    if game_waiting:
        waiting_text = font2.render("Press SPACE to start", True, (255, 255, 255))
        screen.blit(waiting_text, (WinWidth // 2 - waiting_text.get_width() // 2, 400))

    pygame.display.flip()         #Update the window
