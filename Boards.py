import pygame
from Pieces import Pawn

class Tile:	
    
	"""
	The Tile class represents a single tile on the game board.
	"""
	def __init__(self, x, y, tile_width, tile_height):
     
		self.x = x
		self.y = y
		self.pos = (x, y)
		self.tile_width = tile_width
		self.tile_height = tile_height
		self.abs_x = x * tile_width
		self.abs_y = y * tile_height
		self.abs_pos = (self.abs_x, self.abs_y)

		self.color = 'light' if (x + y) % 2 == 0 else 'dark'
		self.draw_color = (255, 255, 255) if self.color == 'light' else (0, 0, 0)
		self.highlight_color = (255, 0, 0) if self.color == 'light' else (0, 0, 255)

		self.occupying_piece = None
		self.coord = self.get_coord()
  
		self.highlight = False
		self.rect = pygame.Rect(
      
			self.abs_x,
			self.abs_y,
			self.tile_width,
			self.tile_height
		)

	def get_coord(self):
		columns = 'abcdefgh'
		return columns[self.x] + str(self.y + 1)

	def draw(self, display):
     
		if self.highlight:
			pygame.draw.rect(display, self.highlight_color, self.rect)
		else:
			pygame.draw.rect(display, self.draw_color, self.rect)

		if self.occupying_piece != None:
			centering_rect = self.occupying_piece.img.get_rect()
			centering_rect.center = self.rect.center
			display.blit(self.occupying_piece.img, centering_rect.topleft)

class Board:
    
	"""
	- The Board class defines the behavior of a checkers game board and how it responds to user input.
    - It has an __init__() method that initializes the board with the specified tile_width, tile_height, and board_size.
    - It also initializes various variables such as selected_piece, turn, and is_jump:

	Board (Tiles - )
	Each State (Board will Change)
	"""
	def __init__(self,tile_width, tile_height, board_size):
     
		self.tile_width = tile_width
		self.tile_height = tile_height
		self.board_size = board_size
		self.selected_piece = None

		self.turn = "black"
		self.is_jump = False

		self.config = [
      
			['', 'bp', '', 'bp', '', 'bp', '', 'bp'],
			['bp', '', 'bp', '', 'bp', '', 'bp', ''],
			['', 'bp', '', 'bp', '', 'bp', '', 'bp'],
			['', '', '', '', '', '', '', ''],
			['', '', '', '', '', '', '', ''],
			['rp', '', 'rp', '', 'rp', '', 'rp', ''],
			['', 'rp', '', 'rp', '', 'rp', '', 'rp'],
			['rp', '', 'rp', '', 'rp', '', 'rp', '']
		]
  
		# Calls the generate_tiles method to create a list of Tile objects representing each tile on the board.
		self.tile_list = self.generate_tiles()
		self.setup()

	def generate_tiles(self):
		output = []
		for y in range(self.board_size):
			for x in range(self.board_size):
				output.append(
					Tile(x,  y, self.tile_width, self.tile_height)
				)
		return output

	def get_tile_from_pos(self, pos):
		for tile in self.tile_list:
			if (tile.x, tile.y) == (pos[0], pos[1]):
				return tile

	def setup(self):
		for y_ind, row in enumerate(self.config):
			for x_ind, x in enumerate(row):
				tile = self.get_tile_from_pos((x_ind, y_ind))
				if x != '':
					if x[-1] == 'p':
						color = 'red' if x[0] == 'r' else 'black'
						tile.occupying_piece = Pawn(x_ind, y_ind, color, self)

	def handle_click(self, pos):
     
		# First, the method extracts the x and y coordinates from the pos argument
		x, y = pos[0], pos[-1]
  
		if x >= self.board_size or y >= self.board_size:
			x = x // self.tile_width
			y = y // self.tile_height
   
		clicked_tile = self.get_tile_from_pos((x, y))

		if self.selected_piece is None:
			if clicked_tile.occupying_piece is not None:
				if clicked_tile.occupying_piece.color == self.turn:
					self.selected_piece = clicked_tile.occupying_piece
     
		elif self.selected_piece._move(clicked_tile):
			if not self.is_jump:
				self.turn = 'red' if self.turn == 'black' else 'black'
			else:
				if len(clicked_tile.occupying_piece.valid_jumps()) == 0:
					self.turn = 'red' if self.turn == 'black' else 'black'
     
			return True # Move 

		elif clicked_tile.occupying_piece is not None:
			if clicked_tile.occupying_piece.color == self.turn:
				self.selected_piece = clicked_tile.occupying_piece
    
		return False # Not Move 

	def draw(self, display):
		if self.selected_piece is not None:
			self.get_tile_from_pos(self.selected_piece.pos).highlight = True
			if not self.is_jump:
				for tile in self.selected_piece.valid_moves():
					tile.highlight = True
			else:
				for tile in self.selected_piece.valid_jumps():
					tile[0].highlight = True

		for tile in self.tile_list:
			tile.draw(display)