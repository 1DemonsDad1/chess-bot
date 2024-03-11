import pygame

from data.classes.Piece import Piece

class Pawn(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)
		self.ep_pawn=False
		img_path = f'data/imgs/{color[0]}_pawn.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

		self.notation = ' '


	def get_possible_moves(self, board):
		output = []
		moves = []
		# move forward
		if self.color == 'black':
			self.check_param(moves, 1, 2, 4)
		elif self.color == 'white':
			self.check_param(moves, -1, -2, 3)
		for move in moves:
			new_pos = (self.x, self.y + move[1])
			if new_pos[1] < 8 and new_pos[1] >= 0:
				output.append(
					board.get_square_from_pos(new_pos)
				)

		return output
		
	def check_param(self, moves, arg1, arg2, arg3):
		moves.append((0, arg1))
		if not self.has_moved:
			moves.append((0, arg2))
		self.ep_pawn = self.y == arg3

	def after_ep_checking(self,output,board): #after ep proces checking last ep parameters to be valid.
		if self.ep_pawn:
			for square in board.squares:
				if (
					square.y == self.y
					and square.occupying_piece != None
					and square.occupying_piece.notation == 'K'
				):
					king_pos=square.pos
					for square1 in board.squares:
						if (square1.y == self.y and 
							square1.occupying_piece != None
							and square1.occupying_piece.notation in ['Q', 'R']
						):
							attack_piece_pos=square1.pos
							for square2 in board.squares:
								if (
									square2.y==self.y and
									square2.occupying_piece!= None and
									square2.occupying_piece.notation not in ['K','N','B',]
								):
									output=[]


		return output

	def get_moves(self, board):
		output = []
		for square in self.get_possible_moves(board):
			if square.occupying_piece is None:
				output.append(square)
			else:
				break

		if self.color == 'white':
			if self.x < 7 and self.y >= 1:
				square = board.get_square_from_pos(
					(self.x + 1, self.y - 1)
				)
				self.square1_ep_desno(board, square, output)
			if self.x >= 1 and self.y >= 1:
				square = board.get_square_from_pos(
					(self.x - 1, self.y - 1)
				)
				self.square1_ep_levo(board, square, output)

		elif self.color == 'black':
			if self.x < 7 and self.y < 7:
				square = board.get_square_from_pos(
					(self.x + 1, self.y + 1)
				)
				self.square1_ep_desno(board, square, output)
			if self.x >= 1 and self.y < 7:
				square = board.get_square_from_pos(
					(self.x - 1, self.y + 1)
				)
				self.square1_ep_levo(board, square, output)
		
		output=self.after_ep_checking(output,board)# ep checking
		return output


	def square1_ep_levo(self, board, square, output):
		square1 = board.get_square_from_pos(
			(self.x-1,self.y)
		)
		if (
			square.occupying_piece != None
			and square.occupying_piece.color != self.color
		):
			output.append(square)
		if (
			self.ep_pawn
			and square.occupying_piece is None
			and square1.occupying_piece is not None
			and square1.occupying_piece.notation == ' '
			and board.last_move == square1.pos
		):
			output.append(square)

	def square1_ep_desno(self, board, square, output):
		square1 = board.get_square_from_pos(
			(self.x+1,self.y)
		)
		if (
			square.occupying_piece != None
			and square.occupying_piece.color != self.color
		):
			output.append(square)

		if (
			self.ep_pawn
			and square.occupying_piece is None
			and square1.occupying_piece is not None
			and square1.occupying_piece.notation == ' '
			and board.last_move == square1.pos
		):
			output.append(square)

	def attacking_squares(self, board):
		moves = self.get_moves(board)
		# return the diagonal moves 
		return [i for i in moves if i.x != self.x]