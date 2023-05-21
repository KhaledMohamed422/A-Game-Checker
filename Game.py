import pygame
from Boards import Board
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
   
class Game:
 
	# The Game class contains methods for 
    #  - Checking if the game is over
    #  - Checking if there is a jump available
    #  - Displaying the winner of the game:

	def __init__(self):
		self.winner = None

	# checks if both colors still has a piece
	def check_piece(self, board):
		"""
		method iterates over each tile on the board and checks if it contains an occupying piece
		"""
		red_piece = 0
		black_piece = 0
		for y in range(board.board_size):
			for x in range(board.board_size):
				tile = board.get_tile_from_pos((x, y))
				if tile.occupying_piece != None:
					if tile.occupying_piece.color == "red":
						red_piece += 1
					else:
						black_piece += 1
		return red_piece, black_piece

	def is_game_over(self, board):
     
		""" 
		method calls the check_piece() method to get the current piece count for each color.
       If one color has no pieces left, the other color is declared the winner
       and the method returns True.
       Otherwise, the method returns False.
    	"""
		red_piece, black_piece = self.check_piece(board)
		if red_piece == 0 or black_piece == 0:
			self.winner = "Red" if red_piece > black_piece else "Black"
			return True
		else:
			return False

	def check_jump(self, board):
		piece = None
		for tile in board.tile_list:
			if tile.occupying_piece != None:
				piece = tile.occupying_piece
				if len(piece.valid_jumps()) != 0 and board.turn == piece.color:
					board.is_jump = True
					break
				else:
					board.is_jump = False
		if board.is_jump:
			board.selected_piece = piece
			board.handle_click(piece.pos)
		return board.is_jump

	def message(self):
		return f"{self.winner} Wins"