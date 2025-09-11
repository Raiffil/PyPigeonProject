import pygame

# Load and scale bird images

BirdWidth =120
BirdHeight = 120

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

