import pygame
from Game import Checkers

if __name__ == "__main__":
    
	window_size = (750, 750)
	screen = pygame.display.set_mode(window_size)
	pygame.display.set_caption("Checkers")

	checkers = Checkers(screen)
	checkers.main(window_size[0], window_size[1])