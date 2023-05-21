import pygame
from Board import Board
from Game import Game

# A International Checker Game

# to handle all internal modules (and components hardware)
pygame.init()

class Checkers:
    
	def __init__(self, screen): 
		self.screen = screen # game widow
		self.running = True # state of game is running 
		self.FPS = pygame.time.Clock() # Clock will be used to control the frame rate of the game.


	def draw(self, board):
     
		board.draw(self.screen)
		pygame.display.update()

	def main(self, window_width, window_height):
     
		board_size = 8
		# Line calculates the width and height of each tile on the board by dividing the window dimensions by the board size.
		tile_width, tile_height = window_width // board_size, window_height // board_size
  
	    # To draw a board of checker
		board = Board(tile_width, tile_height, board_size)
		game = Game()
		# Load the move sound effect
		move_sound = pygame.mixer.Sound("sounds/move_sound.wav")

		while self.running:
      
			# We want to handle all states in each frame 
			game.check_jump(board)
			# access on all events within queue 
            # handle with each frame , what is the even ?
            
			for self.event in pygame.event.get():
				if self.event.type == pygame.QUIT:
					self.running = False

				if not game.is_game_over(board):
					if self.event.type == pygame.MOUSEBUTTONDOWN:
					    # passing in the mouse position as a parameter.
         				# It handles the user's click on the board.
						if board.handle_click(self.event.pos):
							move_sound.play()
						
				else:
						message = game.message()
						font = pygame.font.Font(None, 36)
						text = font.render(message, True, (255, 255, 255))
						text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
						
						# Load and play the sound effect
						sound = pygame.mixer.Sound("sounds/win_sound.wav")
						sound.play()

						while True:
							for event in pygame.event.get():
								if event.type == pygame.QUIT:
									pygame.quit()
									return

							self.screen.fill((0, 0, 0))
							self.screen.blit(text, text_rect)
							pygame.display.flip()



			self.draw(board)
			self.FPS.tick(60)
			# controls the frame rate of the game by calling the tick method on the self.FPS clock object, specifying 60 frames per second.
   


if __name__ == "__main__":
    
	window_size = (750, 750)
	screen = pygame.display.set_mode(window_size)
	pygame.display.set_caption("Checkers")

	checkers = Checkers(screen)
	checkers.main(window_size[0], window_size[1])