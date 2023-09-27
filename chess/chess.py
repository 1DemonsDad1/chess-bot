import pygame


pygame.init()

WIDTH=900
HEIGHT=700
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('Chess engine')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
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

# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
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

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]

small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]

black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]

small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

# check variables/ flashing counter
counter = 0
winner = ''
game_over = False

# draw main game board
def draw_board():
    for i in range(32):
        column = i % 4
        row = i//4
        if row % 2 == 0:
            pygame.draw.rect(screen, (233,237,204),[300 -(column*100), row * 50,50,50])
        else:
            pygame.draw.rect(screen, (233,237,204),[350 -(column*100), row * 50,50,50])
        pygame.draw.rect(screen, (81,80,76), [0,400,WIDTH, 300])
        pygame.draw.rect(screen, (81,80,76), [400,0, 500,401])
        pygame.draw.rect(screen, 'white', [0,400,WIDTH, 300],1)
        pygame.draw.rect(screen, 'white', [400,0, 500,401],1)
        status_text = ['White: select a Piece to Move!', 'White: Select a Destination!',
                        'Black: select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(font.render(status_text[turn_step], True, 'black'), (20, 420))

#pieces on board
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 50 +1, white_locations[i][1] * 50 + 1))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 50 + 1, white_locations[i][1] * 50 + 1))
        if turn_step <2:
            if selection==i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0]*50+1, white_locations[i][1]*50+1,50,50],2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 50 + 1, black_locations[i][1] * 50 + 1))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 50 + 1, black_locations[i][1] * 50 + 1))
        if turn_step >=2:
            if selection==i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0]*50+1, black_locations[i][1]*50+1,50,50],2)

# checking all possible moves on board
def check_options(pieces,locations,turn):

    moves_list=[]
    all_moves_list=[]
    for i in range((len(pieces))):
        location = locations[i]
        piece=pieces[i]
        if piece=='pawn':
            moves_list=check_pawn(location,turn)
        elif piece=='rook':
            moves_list=check_rook(location,turn)
        elif piece=='knight':
            moves_list=check_knight(location,turn)
        elif piece=='bishop':
            moves_list=check_bishop(location,turn)
        elif piece=='queen':
            moves_list=check_queen(location,turn)
        elif piece=='king':
            moves_list=check_king(location,turn)
        all_moves_list.append(moves_list)




    return all_moves_list

#piece protection
def piece_antivirus(pieces,names,color):
    moves_list=[]
    if color=='white':
        enemies_list=black_locations
        friends_list=white_locations
    else:
        friends_list=black_locations
        enemies_list=white_locations
    position = names[pieces.index('king')]

    # 8x kockice king
    targets=[(1,0),(1,1),(1,-1),(-1,0),(-1,1),(-1,-1),(0,1),(0,-1)]

    for i in range(8):
        target=(position[0]+targets[i][0],position[1]+targets[i][1])

        if  target not in friends_list and 0<= target[0]<=7 and 0 <= target[1]<=7 and target not in #check king rays in es work:
            moves_list.append(target)

    return moves_list

#check options without king options
def one_list_all_moves(pieces,locations,turn):
    moves_list=[]
    all_moves_list1=[]
    all_moves_list=[]
    
    
    for i in range((len(pieces))):
        location = locations[i]
        piece=pieces[i]
        
        if piece=='rook':
        
            moves_list=check_rook(location,turn)
        elif piece=='knight':
        
            moves_list=check_knight(location,turn)
        elif piece=='bishop':
        
            moves_list=check_bishop(location,turn)
        elif piece=='queen':
            
            moves_list=check_queen(location,turn)
        
        all_moves_list1.append(moves_list)

    for j in all_moves_list1:
        for d in j:
            all_moves_list.append(d)


    
    return all_moves_list


#check king again for check king 
def checking_king(position,color):
    moves_list=[]
    if color=='white':
        enemies_list=black_locations
        friends_list=white_locations
    else:
        friends_list=black_locations
        enemies_list=white_locations
    

    # 8x kockice king
    targets=[(1,0),(1,1),(1,-1),(-1,0),(-1,1),(-1,-1),(0,1),(0,-1)]

    for i in range(8):
        target=(position[0]+targets[i][0],position[1]+targets[i][1])

        if  target not in friends_list and 0<= target[0]<=7 and 0 <= target[1]<=7 :
            moves_list.append(target)

    return moves_list

# check king
def check_king(position,color):
    moves=[]
    if color=='white':
        enemies_list=black_locations
        friends_list=white_locations
        enemies_names=black_pieces
        enemies_color='black'
    else:
        friends_list=black_locations
        enemies_list=white_locations
        enemies_names=white_pieces
        enemies_color='white'

    pieces=white_pieces if color=='white' else black_pieces

    # 8x kockice king
    targets=[(1,0),(1,1),(1,-1),(-1,0),(-1,1),(-1,-1),(0,1),(0,-1)]
    for i in range(8):
        target=(position[0]+targets[i][0],position[1]+targets[i][1])
        if  target not in friends_list and 0<= target[0]<=7 and 0 <= target[1]<=7 and target not in piece_antivirus(enemies_names,enemies_list,enemies_color) and target not in one_list_all_moves(enemies_names,enemies_list,enemies_color) and\
        target not in checking_king(enemies_list[pieces.index('king')],color)and\
        target not in checking_pawn(color):
            moves.append(target)
    
    return moves

#check queen valid moves
def check_queen(position,color):

    moves_list = check_bishop(position,color)
    second_list=check_rook(position,color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list

#check bishop 
def check_bishop(position,color):
    moves_list = []
    if color=='white':
        enemies_list=black_locations
        friends_list=white_locations
    else:
        friends_list=black_locations
        enemies_list=white_locations

    for i in range(4): # gordesno gorlevo doldesno dollevo
        path = True
        chain=1
        if i ==0:
            x=1
            y=-1
        elif i==1:
            x=-1
            y=-1
        elif i==2:
            x= 1
            y=1
        else:
            x=-1
            y=1
        while path:
            if (position[0]+(chain* x), position[1]+ (chain *y))not in friends_list and 0<= position[0] + (chain *x)<=7 and 0<= position[1]+ (chain*y)<=7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
            
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False



    return moves_list

#check knight
def check_knight(position,color):
    moves_list=[]
    if color=='white':
        enemies_list=black_locations
        friends_list=white_locations
    else:
        friends_list=black_locations
        enemies_list=white_locations
    # 8x kockice
    targets=[(1,2),(1,-2),(2,1),(2,-1),(-1,2),(-1,-2),(-2,1),(-2,-1)]
    for i in range(8):
        target=(position[0]+targets[i][0],position[1]+targets[i][1])
        if target not in friends_list and 0<= target[0]<=7 and 0 <= target[1]<=7:
            moves_list.append(target)



    return moves_list

#rook checking
def check_rook(position,color):
    moves_list=[]
    if color=='white':
        enemies_list=black_locations
        friends_list=white_locations
    else:
        friends_list=black_locations
        enemies_list=white_locations

    for i in range(4): # dol gor levo desno
        path = True
        chain=1
        if i ==0:
            x=0
            y=1
        elif i==1:
            x=0
            y=-1
        elif i==2:
            x= 1
            y=0
        else:
            x=-1
            y=0
        while path:
            if (position[0]+(chain* x), position[1]+ (chain *y))not in friends_list and 0<= position[0] + (chain *x)<=7 and 0<= position[1]+ (chain*y)<=7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
            
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False

    return moves_list

#pawn checking again for king check
def checking_pawn(color):
    pawn_list=[]

    j=0
    

    if color=='white':
        pawn_list=[]
        black=black_pieces
        for i in black:
            if i=='pawn':
                x=((black_locations[[i for i, n in enumerate(black) if n == 'pawn'][j]]))# 1 -1
                y=((black_locations[[i for i, n in enumerate(black) if n == 'pawn'][j]]))# -1,-1
                pawn_list.append((x[0]+1,x[1]-1))
                pawn_list.append((y[0]-1,y[1]-1))
                j+=1
    
    if color=='black':
        pawn_list=[]
        white=white_pieces
        for i in white:
            if i=='pawn':
                x=((white_locations[[i for i, n in enumerate(white) if n == 'pawn'][j]]))# 1,1
                y=((white_locations[[i for i, n in enumerate(white) if n == 'pawn'][j]]))# -1,1
                pawn_list.append((x[0]+1,x[1]+1))
                pawn_list.append((y[0]-1,y[1]+1))

                j+=1
    
    return pawn_list 

# pawn checking
def check_pawn(position,color):
    moves_list=[]

    if color=='white':
        if (position[0], position[1]+1) not in white_locations and  (position[0],position[1]+1) not in black_locations and position[1]<7:
            moves_list.append((position[0],position[1]+1))
        if (position[0], position[1]+2) not in white_locations and  (position[0],position[1]+2) not in black_locations and (position[0],position[1]+1)not in white_locations and (position[0],position[1]+1)not in black_locations and position[1]==1:
            moves_list.append((position[0],position[1]+2))
        if (position[0]+1,position[1]+1)in black_locations:
            moves_list.append((position[0]+1,position[1]+1))
        if (position[0]-1,position[1]+1)in black_locations:
            moves_list.append((position[0]-1,position[1]+1))

    else:
        if (position[0], position[1]-1) not in white_locations and  (position[0],position[1]-1) not in black_locations and position[1]>0:
            moves_list.append((position[0],position[1]-1))
        if (position[0], position[1]-2) not in white_locations and  (position[0],position[1]-2) not in black_locations and  (position[0],position[1]-1) not in black_locations and  (position[0],position[1]-1) not in white_locations and position[1]==6:
            moves_list.append((position[0],position[1]-2))
        if (position[0]+1,position[1]-1)in white_locations:
            moves_list.append((position[0]+1,position[1]-1))
        if (position[0]-1,position[1]-1)in white_locations:
            moves_list.append((position[0]-1,position[1]-1))

    return moves_list

#vector line(returns locations in between)
def line_options(enemy_location,king_location):
    moves_list=[enemy_location]
    x=king_location[0]-enemy_location[0]
    y=king_location[1]-enemy_location[1]
    if x>0:
        x=1
    elif x<0:
        x=-1
    if y>0:
        y=1
    elif y<0:
        y=-1
    position=enemy_location
    for i in range(4):
        path = True
        chain=1
        while path:
            if (position[0]+(chain* x), position[1]+ (chain *y))!=king_location:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                chain += 1
            else:
                path = False
    

    return moves_list

#check if pieces that are blocking king from check cant move
def checking_betrayal(position1,color):
    moves_list = []
    if color=='black':
        friends_name=white_pieces
        friends_list=black_locations
    else:
        friends_list=white_locations
        friends_name=black_pieces
    position=position1
    
    for i in range(4): # gordesno gorlevo doldesno dollevo
        path = True
        chain=0
        if i ==0:
            x=1
            y=-1
        elif i==1:
            x=-1
            y=-1
        elif i==2:
            x= 1
            y=1
        else:
            x=-1
            y=1
        while path:
            chain += 1
            if (position[0] + (chain * x), position[1] + (chain * y))in friends_list:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
            
                
                
            if position[0] + (chain * x)>7 and position[1] + (chain * y)>7 or position[0] + (chain * x)<0 and position[1] + (chain * y)<0 or position[0] + (chain * x)<0 and position[1] + (chain * y)>7 or position[0] + (chain * x)>7 and position[1] + (chain * y)<0:
                path= False
                
            
            
            
    
    for i in range(4): #gor dol levo desno
        path1=True
        chain1=0
        if i ==0:
            x=0
            y=1
        elif i==1:
            x=0
            y=-1
        elif i==2:
            x= 1
            y=0
        else:
            x=-1
            y=0
        while path1:
            chain1 += 1
            if (position[0] + (chain1 * x), position[1] + (chain1 * y))in friends_list:
                moves_list.append((position[0] + (chain1 * x), position[1] + (chain1 * y)))
                
            
            if (position[1] + (chain1 * y))>7 or (position[1] + (chain1 * y))<0 or (position[1] + (chain1 * x))>7 or (position[1] + (chain1 * x))<0:
                path1= False
                
            

    return moves_list

#geting all lines from king where pieces could be attacking (pins)
def get_king_rays(king_location,color):
    moves_list = []
    if color=='black':
        enemies_list=white_locations
        enemies_name=white_pieces
    else:
        enemies_name=black_pieces
        enemies_list=black_locations
    position=king_location
    
    for i in range(4): # gordesno gorlevo doldesno dollevo
        path = True
        chain=0
        if i ==0:
            x=1
            y=-1
        elif i==1:
            x=-1
            y=-1
        elif i==2:
            x= 1
            y=1
        else:
            x=-1
            y=1
        while path:
            chain += 1
            if (enemies_name[enemies_list.index((position[0] + (chain * x), position[1] + (chain * y)))]=="queen" or enemies_name[enemies_list.index((position[0] + (chain * x), position[1] + (chain * y)))]=="bishop") if (position[0] + (chain * x), position[1] + (chain * y))in enemies_list else False:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                path = False
                
                
            if position[0] + (chain * x)>7 and position[1] + (chain * y)>7 or position[0] + (chain * x)<0 and position[1] + (chain * y)<0 or position[0] + (chain * x)<0 and position[1] + (chain * y)>7 or position[0] + (chain * x)>7 and position[1] + (chain * y)<0:
                path= False
                
            
            
            
    
    for i in range(4): #gor dol levo desno
        path1=True
        chain1=0
        if i ==0:
            x=0
            y=1
        elif i==1:
            x=0
            y=-1
        elif i==2:
            x= 1
            y=0
        else:
            x=-1
            y=0
        while path1:
            chain1 += 1
            if (enemies_name[enemies_list.index((position[0] + (chain1 * x), position[1] + (chain1 * y)))]=="queen" or enemies_name[enemies_list.index((position[0] + (chain1 * x), position[1] + (chain1 * y)))]=="rook")if (position[0] + (chain1 * x), position[1] + (chain1 * y))in enemies_list else False:
                moves_list.append((position[0] + (chain1 * x), position[1] + (chain1 * y)))
                path1 = False
                
                
            
            if (position[1] + (chain1 * y))>7 or (position[1] + (chain1 * y))<0 or (position[1] + (chain1 * x))>7 or (position[1] + (chain1 * x))<0:
                path1= False
                
            

    return moves_list


#king defense from check and all moves
def valid_check_moves(color):
    options=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    white_opts=check_options(white_pieces,white_locations,'white')
    black_opts=check_options(black_pieces,black_locations,'black')
    
    if color=='black':
        for i in white_opts:
            #king in check
            if black_locations[black_pieces.index('king')] in i:
                options=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
                for a in black_opts:
                    for b in a:
                        #if b in coords between attacker and king
                        if b in line_options(white_locations[white_opts.index(i)],black_locations[black_pieces.index('king')]):
                            options[black_opts.index(a)].append(b)
                        #king moves
                        if b in check_king(black_locations[black_pieces.index('king')],'black'):
                            options[black_opts.index(black_opts[black_pieces.index('king')])].append(b)
                return options
        if not any(black_locations[black_pieces.index('king')]in sublist for sublist in white_opts):
            count=0
            king_rays=get_king_rays(black_locations[black_pieces.index('king')],'black')
            
            options=black_opts
            betrayal=checking_betrayal(black_locations[black_pieces.index('king')],'black')
            
            for d in betrayal:
                for j in range(len(king_rays)):
                    if d in line_options(king_rays[j],black_locations[black_pieces.index('king')]):
                        count=0
                        for e in line_options(king_rays[j],black_locations[black_pieces.index('king')]):
                            if e in black_locations:
                                count+=1
                        
                        if count==4:
                            options[black_locations.index(d)]=[]
                            for k in line_options(king_rays[j],black_locations[black_pieces.index('king')]):
                                if k in check_options(black_pieces,black_locations,'black')[black_locations.index(d)]:
                                    options[black_locations.index(d)].append(k)
            return options

    if color=='white':
        for i in black_opts:
            #king in check
            if white_locations[white_pieces.index('king')] in i:
                options=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
                for a in white_opts:
                    for b in a:
                        #if b in coords between attacker and king
                        if b in line_options(black_locations[black_opts.index(i)],white_locations[white_pieces.index('king')]):
                            options[white_opts.index(a)].append(b)
                        #king moves
                        if b in check_king(white_locations[white_pieces.index('king')],'white'):
                            options[white_opts.index(white_opts[white_pieces.index('king')])].append(b)
                return options
        if not any(white_locations[white_pieces.index('king')]in sublist for sublist in black_opts):
            king_rays=get_king_rays(white_locations[white_pieces.index('king')],'white')
            options=white_opts
            betrayal=checking_betrayal(white_locations[white_pieces.index('king')],'white')
            for d in betrayal:
                for j in range(len(king_rays)):
                    if d in line_options(king_rays[j],white_locations[white_pieces.index('king')]):
                        count=0
                        for e in line_options(king_rays[j],white_locations[white_pieces.index('king')]):
                            if e in white_locations:
                                count+=1
                        
                        if count==4:
                            options[white_locations.index(d)]=[]
                            for k in line_options(king_rays[j],white_locations[white_pieces.index('king')]):
                                if k in check_options(white_pieces,white_locations,'black')[white_locations.index(d)]:
                                    options[white_locations.index(d)].append(k)
            return options

#valid moves for selected piece
def check_valid_moves():

    if turn_step<2:
        options_list=white_options
    else:
        options_list=black_options

    valid_options=options_list[selection]
    return valid_options

#check valid moves
def draw_valid(moves):
    if turn_step<2:
        color='red'
    else:
        color='blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen,color,(moves[i][0]*50+25,moves[i][1]*50+25),5)

#captured pieces draw
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece=captured_pieces_white[i]
        index=piece_list.index(captured_piece)
        screen.blit(small_black_images[index],(425,5+20*i))
    for i in range(len(captured_pieces_black)):
        captured_piece=captured_pieces_black[i]
        index=piece_list.index(captured_piece)
        screen.blit(small_white_images[index],(400,5+20*i))

#game over
def draw_game_over():
    pygame.draw.rect(screen,'black', [200,200,400,70])
    screen.blit(font.render(f'{winner} won',True,'White'),(200,200))
    screen.blit(font.render(f'press ENTER to restart',True,'White'),(200,240))

#draw king in check
def draw_check():

    if turn_step<2:

        king_index= white_pieces.index('king')
        king_location=white_locations[king_index]
        for i in range(len(black_options)):
            if king_location in black_options[i]:
                if counter<15:
                    pygame.draw.rect(screen,'dark red',[white_locations[king_index][0]*50+1,white_locations[king_index][1]*50+1,50,50],5)
    else:

        king_index= black_pieces.index('king')
        king_location=black_locations[king_index]
        for i in range(len(white_options)):
            if king_location in white_options[i]:
                if counter<15:
                    pygame.draw.rect(screen,'dark blue',[black_locations[king_index][0]*50+1,black_locations[king_index][1]*50+1,50,50],5)

#loose win
def win(color):
    king_location_black=black_locations[black_pieces.index('king')]
    king_location_white=white_locations[white_pieces.index('king')]
    list2=[]
    if color=='white':
        list=[]
        if check_king(king_location_black,'black')==list and valid_check_moves('black')==[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] and any(king_location_black in sublist for sublist in white_options):
            return True
        else:
            return False
    if color=='black':
        list=[]
        if check_king(king_location_white,'white')==list and valid_check_moves('white')==[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] and any(king_location_white in sublist for sublist in black_options):
            return True
        else:
            return False
        


#main loop
black_options = valid_check_moves('black') 

white_options = valid_check_moves('white')

run =True
while run:

    timer.tick(fps)
    if counter <30:
        counter+=1
    else:
        counter=0
    
    screen.fill(color=(119,153,84))
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    
    #king opt.


    if selection!=100:
        valid_moves=check_valid_moves()
        draw_valid(valid_moves)


    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type== pygame.MOUSEBUTTONDOWN and event.button==1:
            x_coord=event.pos[0] //50
            y_coord=event.pos[1] //50
            click_coords = (x_coord,y_coord)
            if turn_step <=1:
                
                if click_coords in white_locations:
                    #dobi lokacijo kliknjenega piecea 
                    selection = white_locations.index(click_coords)
                    if turn_step==0:
                        turn_step=1
                if click_coords in valid_moves and selection != 100:
                    white_locations[selection]=click_coords
                    
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)


                    black_options = valid_check_moves('black') 

                    white_options = valid_check_moves('white')
                    #win condition
                    if win('black'):
                        winner='black'
                    elif win('white'):
                        winner='white'

                    turn_step=2
                    selection=100
                    valid_moves = []

            if turn_step >1:

                if click_coords in black_locations:
                    #dobi lokacijo kliknjenega piecea 
                    selection = black_locations.index(click_coords)
                    if turn_step==2:
                        turn_step=3
                if click_coords in valid_moves and selection != 100:
                    black_locations[selection]=click_coords
                    
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    
                    black_options = valid_check_moves('black') 

                    white_options = valid_check_moves('white')
                    #win condition
                    if win('white'):
                        winner='black'
                    elif win('black'):
                        winner='white'
                    turn_step=0
                    selection=100
                    valid_moves = []
    if winner != '':
        game_over=True
        draw_game_over()



    pygame.display.flip()
pygame.quit()
