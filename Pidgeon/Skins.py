import pygame

# Load and scale bird images

BirdWidth = 60
BirdHeight = 60

WinHeight = 900
WinWidth = 1500

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
        pygame.image.load("F4.png").convert_alpha(), (BirdWidth, BirdHeight)
    ),
    ]

def load_background():
    return pygame.transform.scale(
    pygame.image.load("Space.png").convert(),
    (WinWidth, WinHeight)
)