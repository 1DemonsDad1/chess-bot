import pygame

from data.classes.Piece import Piece

class King(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)

		img_path = f'data/imgs/{color[0]}_king.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

		self.notation = 'K'


	def get_possible_moves(self, board):
		output = []
		moves = [
			(0,-1), # north
			(1, -1), # ne
			(1, 0), # east
			(1, 1), # se
			(0, 1), # south
			(-1, 1), # sw
			(-1, 0), # west
			(-1, -1), # nw
		]

		for move in moves:
			new_pos = (self.x + move[0], self.y + move[1])
			if (
				new_pos[0] < 8 and
				new_pos[0] >= 0 and 
				new_pos[1] < 8 and 
				new_pos[1] >= 0
			):
				output.append([
					board.get_square_from_pos(
						new_pos
					)
				])

		return output

	def can_castle(self, board):
		castle=["",""]
		if self.has_moved:
			return castle
		if board.is_in_check(self.color):
			return castle
		if self.color == 'white':

			kingside_rook = self.queenside(board, 7, castle)
			castle[0] = (
				"kingside"
				if (
					kingside_rook != None
					and not kingside_rook.has_moved
					and not (
						board.is_in_check(
							self.color, [(self.x, self.y), (self.x + 1, self.y)]
						)
					)
					and not (
						board.is_in_check(
							self.color, [(self.x, self.y), (self.x + 2, self.y)]
						)
					)
					and [board.get_piece_from_pos((i, 7)) for i in range(5, 7)]
					== [None, None]
				)
				else ""
			)
		elif self.color == 'black':

			kingside_rook = self.queenside(board, 0, castle)
			if (
				kingside_rook != None
				and not kingside_rook.has_moved 
				and not(board.is_in_check(self.color,[(self.x,self.y),(self.x+1,self.y)]))
				and	not(board.is_in_check(self.color,[(self.x,self.y),(self.x+2,self.y)])) 
				and [board.get_piece_from_pos((i, 0)) for i in range(5, 7)]
				== [None, None]
				):
				castle[0]="kingside"
			else:
				castle[0]=""
		return castle

	def queenside(self, board, arg1, castle):
		queenside_rook = board.get_piece_from_pos((0, arg1))
		result = board.get_piece_from_pos((7, arg1))
		if (
			queenside_rook != None
			and not queenside_rook.has_moved
			and not (
				board.is_in_check(
					self.color, [(self.x, self.y), (self.x - 1, self.y)]
				)
			)
			and not (
				board.is_in_check(
					self.color, [(self.x, self.y), (self.x - 2, self.y)]
				)
			)
			and [board.get_piece_from_pos((i, arg1)) for i in range(1, 4)]
			== [None, None, None]
		):	
			castle[1]="queenside"
		else:
			castle[1]=""

		return result

	def get_valid_moves(self, board):
		output = [
			square
			for square in self.get_moves(board)
			if not board.is_in_check(self.color, board_change=[self.pos, square.pos])
		]
		if self.can_castle(board)[1] == 'queenside':
			output.append(
				board.get_square_from_pos((self.x - 2, self.y))
			)
		if self.can_castle(board)[0] == 'kingside':
			output.append(
				board.get_square_from_pos((self.x + 2, self.y))
			)

		return output
