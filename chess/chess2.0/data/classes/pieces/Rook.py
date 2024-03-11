import pygame

from data.classes.Piece import Piece

class Rook(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)

		img_path = f'data/imgs/{color[0]}_rook.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

		self.notation = 'R'


	def get_possible_moves(self, board):
		moves_north = [
			board.get_square_from_pos((self.x, y)) for y in range(self.y)[::-1]
		]
		output = [moves_north]
		moves_east = [
			board.get_square_from_pos((x, self.y)) for x in range(self.x + 1, 8)
		]
		output.append(moves_east)

		moves_south = [
			board.get_square_from_pos((self.x, y)) for y in range(self.y + 1, 8)
		]
		output.append(moves_south)

		moves_west = [
			board.get_square_from_pos((x, self.y)) for x in range(self.x)[::-1]
		]
		output.append(moves_west)

		return output
