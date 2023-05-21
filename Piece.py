import pygame

pygame.init()

class Piece:
    
	"""
	The Piece class is a parent class for all checker pieces in the game.
    It contains common attributes and methods that are shared among all pieces such as the position of the piece on the board,
    its color and the ability to move to certain tiles on the board based on the game rules.
	"""
 
	def __init__(self, x, y, color, board):
     
		self.x = x
		self.y = y
		self.pos = (x, y)
		self.board = board
		self.color = color

	def _move(self, tile):
     
		move_sound = pygame.mixer.Sound("sounds/Be-King.wav")
  
		for i in self.board.tile_list:
			i.highlight = False

		if tile in self.valid_moves() and not self.board.is_jump:
      
			prev_tile = self.board.get_tile_from_pos(self.pos)
			self.pos, self.x, self.y = tile.pos, tile.x, tile.y

			prev_tile.occupying_piece = None
			tile.occupying_piece = self
			self.board.selected_piece = None
			self.has_moved = True

			# Pawn promotion
			if self.notation == 'p':
				if self.y == 0 or self.y == 7:
					from King import King
					tile.occupying_piece = King(
						self.x, self.y, self.color, self.board
					)
					move_sound.play()
			return True

		elif self.board.is_jump:
			for move in self.valid_jumps():
				if tile in move:
					prev_tile = self.board.get_tile_from_pos(self.pos)
					jumped_piece = move[-1]
					self.pos, self.x, self.y = tile.pos, tile.x, tile.y

					prev_tile.occupying_piece = None
					jumped_piece.occupying_piece = None
					tile.occupying_piece = self
					self.board.selected_piece = None
					self.has_moved = True

					# Pawn promotion
					if self.notation == 'p':
						if self.y == 0 or self.y == 7:
							from King import King
							tile.occupying_piece = King(
								self.x, self.y, self.color, self.board
							)
							move_sound.play()

					return True
		else:
			self.board.selected_piece = None
			return False