import pygame

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


	def check_moves_available(self, board):

		for tile in board.tile_list:
			if tile.occupying_piece is not None and tile.occupying_piece.color == board.turn:
				if len(tile.occupying_piece.valid_moves()) > 0 or len(tile.occupying_piece.valid_jumps()) > 0:
					return True
		return False


	def is_game_over(self, board):
        
		red_piece, black_piece = self.check_piece(board)

		if red_piece == 0 or black_piece == 0:
			self.winner = "Red" if red_piece > black_piece else "Black"
			return True
		elif not self.check_moves_available(board):
			self.winner = "Red" if board.turn == "black" else "Black"
			return True
		else:
			return False

		

	def message(self):
		return f"{self.winner} Wins"