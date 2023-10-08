import pygame
import numpy as np
pygame.init()
WIDTH=900
HEIGHT=700
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('Chess engine')
font = pygame.font.Font('freesansbold.ttf', 20)
font1= pygame.font.Font('arial.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
small_font = pygame.font.Font('freesansbold.ttf', 12)
timer = pygame.time.Clock()
fps = 60
#game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
captured_pieces_white = []
captured_pieces_black = []
turn_step = 0
selection = 100
valid_moves = []
# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_queen = pygame.image.load('slike/black queen.png')
black_queen = pygame.transform.scale(black_queen, (50, 50))
black_queen_small = pygame.transform.scale(black_queen, (25, 25))
black_king = pygame.image.load('slike/black king.png')
black_king = pygame.transform.scale(black_king, (50, 50))
black_king_small = pygame.transform.scale(black_king, (25, 25))
black_rook = pygame.image.load('slike/black rook.png')
black_rook = pygame.transform.scale(black_rook, (50, 50))
black_rook_small = pygame.transform.scale(black_rook, (25, 25))
black_bishop = pygame.image.load('slike/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (50, 50))
black_bishop_small = pygame.transform.scale(black_bishop, (25, 25))
black_knight = pygame.image.load('slike/black knight.png')
black_knight = pygame.transform.scale(black_knight, (50, 50))
black_knight_small = pygame.transform.scale(black_knight, (25, 25))
black_pawn = pygame.image.load('slike/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (50, 50))
black_pawn_small = pygame.transform.scale(black_pawn, (25, 25))
white_queen = pygame.image.load('slike/white queen.png')
white_queen = pygame.transform.scale(white_queen, (50, 50))
white_queen_small = pygame.transform.scale(white_queen, (25, 25))
white_king = pygame.image.load('slike/white king.png')
white_king = pygame.transform.scale(white_king, (50, 50))
white_king_small = pygame.transform.scale(white_king, (25, 25))
white_rook = pygame.image.load('slike/white rook.png')
white_rook = pygame.transform.scale(white_rook, (50, 50))
white_rook_small = pygame.transform.scale(white_rook, (25, 25))
white_bishop = pygame.image.load('slike/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (50, 50))
white_bishop_small = pygame.transform.scale(white_bishop, (25, 25))
white_knight = pygame.image.load('slike/white knight.png')
white_knight = pygame.transform.scale(white_knight, (50, 50))
white_knight_small = pygame.transform.scale(white_knight, (25, 25))
white_pawn = pygame.image.load('slike/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (50, 50))
white_pawn_small = pygame.transform.scale(white_pawn, (25, 25))
surender = pygame.image.load('slike/white-flag.png')
surender = pygame.transform.scale(surender, (40, 40))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
white_promotions=['queen','knight', 'rook', 'bishop']
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
white_moved=[False,False,False,False,False,False,False,False,
            False,False,False,False,False,False,False,False]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
black_promotions=['queen','knight', 'rook', 'bishop']
black_moved=[False,False,False,False,False,False,False,False,
            False,False,False,False,False,False,False,False]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
# check variables/ flashing counter
counter = 0
winner = ''
game_over = False
white_ep=(100,100)
black_ep=(100,100)
white_promote=False
black_promote=False
promo_index=100
check=False
game_start=-1
castling_moves=[]
called=0
white=np.array(white_pieces)
black=np.array(black_pieces)
all_options_selected=False
alpha=float('-inf')
beta=float('inf')