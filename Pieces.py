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
							tile.occupying_piece = King(
								self.x, self.y, self.color, self.board
							)
							move_sound.play()

					return True
		else:
			self.board.selected_piece = None
			return False

class Pawn(Piece):
    
	def __init__(self, x, y, color, board):
     
		super().__init__(x, y, color, board)
		img_path = f'images/{color}-pawn.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width, board.tile_height))
		self.notation = 'p'

	def _possible_moves(self):
		# (x, y) move for left and right
		if self.color == "red":
			possible_moves = ((-1, -1), (+1, -1)) 
		else:
			possible_moves = ((-1, +1), (+1, +1))
		return possible_moves

	def valid_moves(self):
		tile_moves = []
		moves = self._possible_moves()
		for move in moves:
			tile_pos = (self.x + move[0], self.y + move[-1])
			if tile_pos[0] < 0 or tile_pos[0] > 7 or tile_pos[-1] < 0 or tile_pos[-1] > 7:
				pass
			else:
				tile = self.board.get_tile_from_pos(tile_pos)
				if tile.occupying_piece == None:
					tile_moves.append(tile)
		return tile_moves

	def valid_jumps(self):
		tile_jumps = []
		moves = self._possible_moves()
		for move in moves:
			tile_pos = (self.x + move[0], self.y + move[-1])
			if tile_pos[0] < 0 or tile_pos[0] > 7 or tile_pos[-1] < 0 or tile_pos[-1] > 7:
				pass
			else:
				tile = self.board.get_tile_from_pos(tile_pos)
				if self.board.turn == self.color:
					if tile.occupying_piece != None and tile.occupying_piece.color != self.color:
						next_pos = (tile_pos[0] + move[0], tile_pos[-1] + move[-1])
						next_tile = self.board.get_tile_from_pos(next_pos)		
						if next_pos[0] < 0 or next_pos[0] > 7 or next_pos[-1] < 0 or next_pos[-1] > 7:
							pass
						else:
							if next_tile.occupying_piece == None:
								tile_jumps.append((next_tile, tile))
		return tile_jumps

class King(Piece):
    
	def __init__(self, x, y, color, board):
		super().__init__(x, y, color, board)
		img_path = f'images/{color}-king.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width, board.tile_height))
		self.notation = 'k'

	def _possible_moves(self):
		possible_moves = ((-1, -1), (+1, -1), (-1, +1), (+1, +1))
		return possible_moves

	def valid_moves(self):
		tile_moves = []
		moves = self._possible_moves()
		for move in moves:
			tile_pos = (self.x + move[0], self.y + move[-1])
			if tile_pos[0] < 0 or tile_pos[0] > 7 or tile_pos[-1] < 0 or tile_pos[-1] > 7:
				pass
			else:
				tile = self.board.get_tile_from_pos(tile_pos)
				if tile.occupying_piece == None:
					tile_moves.append(tile)
		return tile_moves

	def valid_jumps(self):
		tile_jumps = []
		moves = self._possible_moves()
		for move in moves:
			tile_pos = (self.x + move[0], self.y + move[-1])
			if tile_pos[0] < 0 or tile_pos[0] > 7 or tile_pos[-1] < 0 or tile_pos[-1] > 7:
				pass
			else:
				tile = self.board.get_tile_from_pos(tile_pos)
				if self.board.turn == self.color:
					if tile.occupying_piece != None and tile.occupying_piece.color != self.color:
						next_pos = (tile_pos[0] + move[0], tile_pos[-1] + move[-1])
						next_tile = self.board.get_tile_from_pos(next_pos)		
						if next_pos[0] < 0 or next_pos[0] > 7 or next_pos[-1] < 0 or next_pos[-1] > 7:
							pass
						else:
							if next_tile.occupying_piece == None:
								tile_jumps.append((next_tile, tile))
		return tile_jumps