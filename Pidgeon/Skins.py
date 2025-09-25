import pygame

# Load and scale bird images

BirdWidth = 60
BirdHeight = 60

WinHeight = 900
WinWidth = 1500

star_size = 50

def load_pigeon_frames():
    return [
        pygame.transform.scale(
        pygame.image.load("F1.png").convert_alpha(), (BirdWidth, BirdHeight)
    ),
    pygame.transform.scale(
        pygame.image.load("F2.png").convert_alpha(), (BirdWidth, BirdHeight)
    ),
    pygame.transform.scale(
        pygame.image.load("F3.png").convert_alpha(), (BirdWidth, BirdHeight)
    ),
    pygame.transform.scale(
        pygame.image.load("F4.png").convert_alpha(), (BirdWidth, BirdHeight)),]

def load_background():
    return pygame.transform.scale(
    pygame.image.load("Space.png").convert(),
    (WinWidth, WinHeight))

def load_menu_image():
    return pygame.transform.scale(
        pygame.image.load("SpaceMenu.png").convert(),
        (WinWidth, WinHeight))

def load_restart_image():
    return pygame.transform.scale(
        pygame.image.load("SpaceGameOver.png").convert(),
        (WinWidth, WinHeight))

def load_star_image():
    return pygame.transform.scale(
        pygame.image.load("Star.png").convert_alpha(),
        (star_size, star_size))

def load_shop_image():
    return pygame.transform.scale(
        pygame.image.load("SpaceShop.png").convert(),
        (WinWidth, WinHeight))

def load_bird1_frames():
    frames = []
    for i in range(1, 5):
        frame = pygame.image.load(f"Bird1_F{i}.png").convert_alpha()
        frames.append(frame)
    return frames

def load_bird2():
    return pygame.image.load("bird2.png").convert_alpha()

def load_bird3_frames():
    frames = []
    for i in range(1, 5):
        frame = pygame.image.load(f"Bird3_F{i}.png").convert_alpha()
        frames.append(frame)
    return frames

def load_bird4():
    return pygame.image.load("bird4.png").convert_alpha()


def load_gate1():
    return pygame.image.load("gate1.png").convert_alpha()

def load_gate2():
    return pygame.image.load("gate2.png").convert_alpha()

def load_gate3():
    return pygame.image.load("gate3.png").convert_alpha()

def load_gate4():
    return pygame.image.load("gate4.png").convert_alpha()
