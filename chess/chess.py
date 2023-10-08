import pygame
from konstante import *
import random
import numpy as np
import time
import timeit
pygame.init()

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
        screen.blit(surender,(760,355))
        screen.blit(font1.render('Surrender',True,'black'),(790, 375))
        if white_promote or black_promote:
            screen.blit(medium_font.render('Select piece to promote pawn', True,'black'),(20,420))

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
    global castling_moves
    moves_list=[]
    all_moves_list=[]
    castling_moves=[]
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
            moves_list, castling_moves=check_king(location,turn)
        all_moves_list.append(moves_list)
    return all_moves_list

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

#checking knight for antivirus
def checking_knight(color):
    moves_list=[]
    if color=='white':
        enemies_list=black_locations
        enemies_name=black_pieces
    else:
        enemies_name=white_pieces
        enemies_list=white_locations
    horse_locations=[]
    for i in enemies_list:
        if enemies_name[enemies_list.index(i)]=='knight':
            horse_locations.append(i)
    # 8x kockice
    targets=[(1,2),(1,-2),(2,1),(2,-1),(-1,2),(-1,-2),(-2,1),(-2,-1)]
    for j in range(len(horse_locations)):
        position=horse_locations[j]
        for i in range(8):
            target=(position[0]+targets[i][0],position[1]+targets[i][1])
            if 0<= target[0]<=7 and 0 <= target[1]<=7:
                moves_list.append(target)
    return moves_list

#piece protection (returns pieces around king that are protected)
def piece_antivirus(color,target): #friendly color and kings target
    move=[]
    ray2=[]
    rays=get_king_rays(target,color)
    black_locations1=[]
    white_locations1=[]
    for i in black_locations:
        if i != black_locations[black_pieces.index('king')]:
            black_locations1.append(i)
    for i in white_locations:
        if i != white_locations[white_pieces.index('king')]:
            white_locations1.append(i)
    for i in rays:
        ray2=line_options(i,target)
        if len(ray2)!=1:
            once=len(ray2)-1
        else:
            move.append(target)
            return move
        for j in ray2:   
            if j not in black_locations1 and j not in white_locations1:
                once-=1
            if j not in black_locations1 and j not in white_locations1 and once==0:
                move.append(target)
    return move

# check king
def check_king(position,color):
    moves=[]
    castle_moves=check_castling()
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
        if  target not in friends_list and 0<= target[0]<=7 and 0 <= target[1]<=7 and\
        target not in checking_knight(color) and target not in piece_antivirus(color,target) and\
        target not in one_list_all_moves(enemies_names,enemies_list,enemies_color) and\
        target not in checking_king(enemies_list[pieces.index('king')],color)and\
        target not in checking_pawn(color):
            moves.append(target)
    return moves,castle_moves

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

#gets rays in y for ep
def get_king_rays_pawn(king_location):
    position=king_location
    targets=[]
    for i in range(8):
        targets.append((i,position[1]))
    return targets

#check enpassant pawn bug
def ep_pawn(white_ep,black_ep):
    if turn_step<2:#whites move
        kingxposline=get_king_rays_pawn(white_locations[white_pieces.index('king')])
        enemies_list=black_locations
        enemies_names=black_pieces
        friends_list=white_locations
        friends_names=white_pieces
        ep=white_ep
        king=white_locations[white_pieces.index('king')]
    else:
        kingxposline=get_king_rays_pawn(black_locations[black_pieces.index('king')])
        enemies_list=white_locations
        enemies_names=white_pieces
        friends_list=black_locations
        friends_names=black_pieces
        ep=black_ep
        king=black_locations[black_pieces.index('king')]
    for i in kingxposline:
        if i in friends_list and friends_names[friends_list.index(i)]=='pawn' and ep!=(100,100):
            count=0
            for j in kingxposline:
                if j == enemies_list[enemies_names.index('rook')] or j==enemies_list[enemies_names.index('queen')]:#fix for index try not to do eval bc is gae  
                    if i in line_options(j,king):
                        #from king pos
                        x=king[0]-j[0]
                        if x>0:
                            x=1
                        elif x<0:
                            x=-1
                        for d in range(8):
                            target=((enemies_list[enemies_list.index(j)][0]+x*d),king[1])
                            if target in enemies_list:
                                if enemies_names[enemies_list.index(target)]=='queen' or enemies_names[enemies_list.index(target)]=='rook':
                                    count=0
                                elif enemies_names[enemies_list.index(target)]=='pawn' or enemies_names[enemies_list.index(target)]=='bishop' or enemies_names[enemies_list.index(target)]=='knight' or enemies_names[enemies_list.index(target)]=='king':
                                    count+=1
                            if target in friends_list:
                                if friends_names[friends_list.index(target)]=='pawn' or friends_names[friends_list.index(target)]=='bishop' or friends_names[friends_list.index(target)]=='knight':
                                    count+=1
                                if friends_names[friends_list.index(target)]=='king':
                                    break
                    if count<3:
                        return False
    return True

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
        #en passant check
        if ep_pawn(black_ep,white_ep):
            if (position[0]+1,position[1]+1)== black_ep:
                moves_list.append((position[0]+1,position[1]+1))
            if (position[0]-1,position[1]+1)== black_ep:
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
        #en passant check
        if ep_pawn(black_ep,white_ep):
            if (position[0]+1,position[1]-1)== white_ep:
                moves_list.append((position[0]+1,position[1]-1))
            if (position[0]-1,position[1]-1)== white_ep:
                moves_list.append((position[0]-1,position[1]-1))
    return moves_list

#en passant
def check_ep(old_coords, new_coords):
    if turn_step<=1:
        index=white_locations.index(old_coords)
        ep_coords=(new_coords[0], new_coords[1]-1)
        piece=white_pieces[index]
    else:
        index=black_locations.index(old_coords)
        ep_coords=(new_coords[0], new_coords[1]+1)
        piece=black_pieces[index]
    if piece=='pawn' and abs(old_coords[1]-new_coords[1])>1 :
        #if piece pawn and 2 moved for 2 return ep coords
        pass
    else:
        ep_coords=(100,100)
    return ep_coords

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
    if enemy_location in white_locations:
        if white_pieces[white_locations.index(enemy_location)]=='knight':
            return moves_list
            
        for i in range(4):
            path = True
            chain=1
            while path:
                if (position[0]+(chain* x), position[1]+ (chain *y))!=king_location:
                    moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                    chain += 1
                else:
                    path = False
        
    elif enemy_location in black_locations:
        if black_pieces[black_locations.index(enemy_location)]=='knight':
            return moves_list
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
    q=-1
    if color=='black':
        for i in white_opts:
            #king in check
            if black_locations[black_pieces.index('king')] in i:
                options=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
                for a in black_opts:
                    q+=1
                    for b in a:
                        #if b in coords between attacker and king
                        if b in line_options(white_locations[white_opts.index(i)],black_locations[black_pieces.index('king')]):
                            options[q].append(b)# this is the problem 100%
                        
                        #king moves
                        if b in check_king(black_locations[black_pieces.index('king')],'black')[0]:
                            options[black_opts.index(black_opts[black_pieces.index('king')])].append(b)

                return options      
        if not any(black_locations[black_pieces.index('king')]in sublist for sublist in white_opts):
            count=0
            king_rays=get_king_rays(black_locations[black_pieces.index('king')],'black')#pieces that could pin king
            options=black_opts
            betrayal=checking_betrayal(black_locations[black_pieces.index('king')],'black')#locaions of enemies that could be pined to king
            for d in betrayal: # pined to king
                for j in range(len(king_rays)):#could pin
                    if d in line_options(king_rays[j],black_locations[black_pieces.index('king')]):
                        count=0
                        for e in line_options(king_rays[j],black_locations[black_pieces.index('king')]):
                            if e in black_locations or e in white_locations:
                                count+=1
                        if count==5:
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
                    q+=1

                    for b in a:
                        #if b in coords between attacker and king
                        if b in line_options(black_locations[black_opts.index(i)],white_locations[white_pieces.index('king')]):
                            options[q].append(b)# this is the problem 100%

                        
                        #king moves
                        if b in check_king(white_locations[white_pieces.index('king')],'white')[0]:
                            options[white_opts.index(white_opts[white_pieces.index('king')])].append(b)

                return options
        if not any(white_locations[white_pieces.index('king')]in sublist for sublist in black_opts):
            count=0
            king_rays=get_king_rays(white_locations[white_pieces.index('king')],'white')
            options=white_opts
            betrayal=checking_betrayal(white_locations[white_pieces.index('king')],'white')
            for d in betrayal:
                for j in range(len(king_rays)):
                    if d in line_options(king_rays[j],white_locations[white_pieces.index('king')]):
                        count=0
                        for e in line_options(king_rays[j],white_locations[white_pieces.index('king')]):
                            if e in white_locations or e in black_locations:
                                count+=1
                        if count==5:
                            options[white_locations.index(d)]=[]
                            for k in line_options(king_rays[j],white_locations[white_pieces.index('king')]):
                                if k in check_options(white_pieces,white_locations,'white')[white_locations.index(d)]:
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
    screen.blit(font.render(f'press ENTER to Main menu',True,'White'),(200,240))

#draw king in check
def draw_check():
    global check 
    check=False
    if turn_step<2:
        king_index= white_pieces.index('king')
        king_location=white_locations[king_index]
        for i in range(len(black_options)):
            if king_location in black_options[i]:
                check=True
                if counter<15:
                    pygame.draw.rect(screen,'dark red',[white_locations[king_index][0]*50+1,white_locations[king_index][1]*50+1,50,50],5)
    else:
        king_index= black_pieces.index('king')
        king_location=black_locations[king_index]
        for i in range(len(white_options)):
            if king_location in white_options[i]:
                check=True
                if counter<15:
                    pygame.draw.rect(screen,'dark blue',[black_locations[king_index][0]*50+1,black_locations[king_index][1]*50+1,50,50],5)

#loose win
def win(color):
    king_location_black=black_locations[black_pieces.index('king')]
    king_location_white=white_locations[white_pieces.index('king')]
    list2=[]
    if color=='white':
        list=[]
        if check_king(king_location_black,'black')[0]==list and valid_check_moves('black')==[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] and any(king_location_black in sublist for sublist in white_options):
            return True
        else:
            return False
    if color=='black':
        list=[]
        
        if check_king(king_location_white,'white')[0]==list and valid_check_moves('white')==[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] and any(king_location_white in sublist for sublist in black_options):
            return True
        else:
            return False

#promotion
def check_promotion():
    pawn_indexes=[]
    white_promotion= False
    black_promotion=False
    promote_index=100
    for i in range(len(white_pieces)):
        if white_pieces[i]=='pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if white_locations[pawn_indexes[i]][1]==7:
            white_promotion=True
            promote_index=pawn_indexes[i]
    pawn_indexes=[]
    for i in range(len(black_pieces)):
        if black_pieces[i]=='pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if black_locations[pawn_indexes[i]][1]==0:
            black_promotion=True
            promote_index=pawn_indexes[i]
    return white_promotion,black_promotion,promote_index

#draw promotion
def draw_promotion():
    pygame.draw.rect(screen,'dark gray',[450,0,60,210])
    if white_promote:
        color='white'
        for i in range(len(white_promotions)):
            piece=white_promotions[i]
            index=piece_list.index(piece)
            screen.blit(white_images[index],(455,5+50*i))
    elif black_promote:
        color='black'
        for i in range(len(black_promotions)):
            piece=black_promotions[i]
            index=piece_list.index(piece)
            screen.blit(black_images[index],(455,5+50*i))
    pygame.draw.rect(screen,'white',[450,0,60,210],8)

#selection of promoted pieces
def check_promo_select():
    mouse_pos=pygame.mouse.get_pos()
    left_click=pygame.mouse.get_pressed()[0]
    x_pos=mouse_pos[0]//50
    y_pos=mouse_pos[1]//50
    if white_promote and left_click and x_pos>8 and y_pos<4 and x_pos<10:
        white_pieces[promo_index]=white_promotions[y_pos]
    elif black_promote and left_click and x_pos>8 and y_pos<4 and x_pos<10:
        black_pieces[promo_index]=black_promotions[y_pos]

#castling king
def check_castling():
    castle_moves=[]
    rook_indexes=[]
    rook_locations=[]
    king_index=0
    king_pos=(0,0)
    if turn_step >1:
        for i in range(len(black_pieces)):
            if black_pieces[i]=='rook':
                rook_indexes.append(black_moved[i])
                rook_locations.append(black_locations[i])
            if black_pieces[i]=='king':
                king_index=i
                king_pos=black_locations[i]
        if not black_moved[king_index]and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle=True
                if rook_locations[i][0]>king_pos[0]:
                    empty_squares=[(king_pos[0]+1,king_pos[1]),(king_pos[0]+2,king_pos[1]),(king_pos[0]+3,king_pos[1]),]
                else:
                    empty_squares=[(king_pos[0]-1,king_pos[1]),(king_pos[0]-2,king_pos[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j]in white_locations or empty_squares[j]in black_locations or  any(empty_squares[j] in nested_list for nested_list in white_options) or rook_indexes[i]:
                        castle=False
                if castle:
                    castle_moves.append((empty_squares[1],empty_squares[0]))
    else:
        for i in range(len(white_pieces)):
            if white_pieces[i]=='rook':
                rook_indexes.append(white_moved[i])
                rook_locations.append(white_locations[i])
            if white_pieces[i]=='king':
                king_index=i
                king_pos=white_locations[i]
        if not white_moved[king_index]and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle=True
                if rook_locations[i][0]>king_pos[0]:
                    empty_squares=[(king_pos[0]+1,king_pos[1]),(king_pos[0]+2,king_pos[1]),(king_pos[0]+3,king_pos[1]),]
                else:
                    empty_squares=[(king_pos[0]-1,king_pos[1]),(king_pos[0]-2,king_pos[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j]in white_locations or empty_squares[j]in black_locations or  any(empty_squares[j] in nested_list for nested_list in black_options) or rook_indexes[i]:
                        castle=False
                if castle:
                    castle_moves.append((empty_squares[1],empty_squares[0]))
    return castle_moves

#draw castling
def draw_castling(moves):
    for i in range(len(moves)):
        pygame.draw.circle(screen,'purple',(moves[i][0][0]*50+25,moves[i][0][1]*50+25),5)

#main menu
def draw_main_menu():
    #big play chess
    screen.blit(big_font.render('Play Chess',True,(119,153,84)),(100,125))

    #2players button
    pygame.draw.rect(screen,(119,153,84),[150,250,100,50],40,7)
    screen.blit(font.render('2 players',True,(233,237,204)),(155,265))

    # vs ai as black
    pygame.draw.rect(screen,(119,153,84),[150,350,100,50],40,7)
    screen.blit(font.render('Against',True,(233,237,204)),(160,355))
    screen.blit(font.render('bots',True,(233,237,204)),(175,375))
    screen.blit(font.render('*',True,(233,237,204)),(155,400))
    screen.blit(small_font.render('select options',True,(233,237,204)),(165,400))
    # add option buttons

#material advantage
def material(turn):
    white=np.array(white_pieces)
    black=np.array(black_pieces)
    material=0
    for i in black if turn else white:
        material+= 9 if i=='queen' else 5 if i=='rook' else 3 if i=='bishop' else 3 if i=='knight' else 1
    return material

#position evaluation
def evaluate():
    blackeval=material(True)
    whiteeval=material(False)
    evaluation=whiteeval-blackeval
    return evaluation

#algorithm for minmax 
def minmax(black_options,white_options,alpha,beta,depth,max_player):
    if depth==0 or win('black'if max_player==False else 'white'):
        return evaluate(),j
    
    if max_player:
        maxEval= float('-inf')
        for i in white_options:
            for j in i:#loop through all options of pieces
                prev_location=white_locations[white_options.index(i)]#get prev location for add back (simulation)
                white_locations[white_options.index(i)]=j #location of max players piece at index of piece = its posible location 
                wasin=False
                if j in black_locations:#remove pieces if piece location in enemies location
                    black_piece = black_locations.index(j)
                    prev_bindex=black_locations.index(j)
                    prev_blocation=black_locations[black_piece]
                    black_locations.pop(black_piece)
                    wasin=True

                if j in black_locations:#remove pieces if piece location in enemies location
                    black_piece = black_locations.index(j)
                    black_locations.pop(black_piece)
                
                black_options = valid_check_moves('black') 
                white_options = valid_check_moves('white')
                eval=minmax(black_options,white_options,alpha,beta,depth-1,False)[0] #recursion

                if wasin==True: #returns back the taken piece
                    black_locations.insert(prev_bindex,prev_blocation)

                white_locations[white_options.index(i)]=prev_location

                maxEval= max(maxEval,eval)
                alpha= max(alpha,eval)
                if beta<= alpha:
                    break
            if beta<=alpha:
                break
        return maxEval


    else:
        minEval= float('inf')
        for i in black_options:
            for j in i:#loop through all options of pieces
                prev_location=black_locations[black_options.index(i)]#get prev location for add back (simulation)
                black_locations[black_options.index(i)]=j#location of max players piece at index of piece = its posible location 
                wasin=False

                if j in white_locations:#remove pieces if piece location in enemies location
                    white_piece = white_locations.index(j)
                    prev_windex=white_locations.index(j)
                    prev_wlocation=white_locations[white_piece]
                    white_locations.pop(white_piece)
                    wasin=True

                black_options = valid_check_moves('black') 
                white_options = valid_check_moves('white')
                eval=minmax(black_options,white_options,alpha,beta,depth-1,True)[0] #recursion

                if wasin==True: #returns back the taken piece
                    white_locations.insert(prev_windex,prev_wlocation)

                black_locations[black_options.index(i)]=prev_location
                minEval= max(minEval,eval)
                beta= max(beta,eval)
                if beta<= alpha:
                    break
            if beta<=alpha:
                break
        return maxEval

    



    

#main loop
black_options = valid_check_moves('black') 
white_options = valid_check_moves('white')




run =True
while run:
    # start_time=time.time()
    timer.tick(fps)
    if counter <30:
        counter+=1
    else:
        counter=0
    screen.fill(color=(81,80,76))
    
    if game_start==-1:
        draw_main_menu()
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run=False
            if event.type== pygame.MOUSEBUTTONDOWN and event.button==1:
                x_coord=event.pos[0] //50
                y_coord=event.pos[1] //50
                click_coords = (x_coord,y_coord)
                print(click_coords)
                if click_coords==((3,5)) or click_coords==((4,5)):
                    game_start=0

    if game_start==0:
        screen.fill(color=(119,153,84))
        draw_board()
        draw_pieces()
        draw_captured()
        draw_check()
        print(minmax(black_options,white_options,alpha,beta,0,True))
        if not game_over:
            white_promote,black_promote, promo_index=check_promotion()
            if white_promote or black_promote:
                draw_promotion()
                check_promo_select()
                black_options = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
                white_options = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        if selection!=100:
            valid_moves=check_valid_moves()
            draw_valid(valid_moves)
            if selected_piece == 'king':
                draw_castling(castling_moves)
        
        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type== pygame.MOUSEBUTTONDOWN and event.button==1:
                x_coord=event.pos[0] //50
                y_coord=event.pos[1] //50
                click_coords = (x_coord,y_coord)
                black_options = valid_check_moves('black') 
                white_options = valid_check_moves('white')
                if turn_step <=1:#white turn
                    if click_coords==(15,7)or click_coords==(16,7) or click_coords==(17,7):
                        winner='black'
                    if click_coords in white_locations:
                        #dobi lokacijo kliknjenega piecea 
                        selection = white_locations.index(click_coords)
                        #check selected for castle
                        selected_piece=white_pieces[selection]
                        if turn_step==0:
                            turn_step=1
                    if click_coords in valid_moves and selection != 100:
                        white_ep=check_ep(white_locations[selection],click_coords)
                        white_locations[selection]=click_coords
                        white_moved[selection]=True
                        if click_coords in black_locations:
                            black_piece = black_locations.index(click_coords)
                            captured_pieces_white.append(black_pieces[black_piece])
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)
                            black_moved.pop(black_piece)
                        #en passant checking
                        if click_coords == black_ep:
                            black_piece = black_locations.index((black_ep[0], black_ep[1]-1))
                            captured_pieces_white.append(black_pieces[black_piece])
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)
                            black_moved.pop(black_piece)
                        black_options = valid_check_moves('black') 
                        white_options = valid_check_moves('white')
                        #win condition
                        if win('black'):
                            winner='black'
                        if win('white'):
                            winner='white'
                        turn_step=2
                        selection=100
                        valid_moves = []
                    # add castle
                    elif selection!=100 and selected_piece=='king':
                        black_options = valid_check_moves('black') 
                        white_options = valid_check_moves('white')
                        for q in range(len(castling_moves)):
                            if click_coords == castling_moves[q][0]:
                                white_locations[selection]=click_coords
                                white_moved[selection]=True
                                if click_coords == (1,0):
                                    rook_coords=(0,0)
                                else:
                                    rook_coords=(7,0)
                                rook_index=white_locations.index(rook_coords)
                                white_locations[rook_index]=castling_moves[q][1]
                                black_options = valid_check_moves('black')
                                white_options = valid_check_moves('white')
                                turn_step=2
                                selection=100
                                valid_moves = []
                if turn_step >1:#blacks turn
                    black_options = valid_check_moves('black') 
                    white_options = valid_check_moves('white')
                    if  click_coords==(15,7)or click_coords==(16,7) or click_coords==(17,7):
                        winner='white'
                    if click_coords in black_locations:
                        #dobi lokacijo kliknjenega piecea 
                        selection = black_locations.index(click_coords)
                        #check selected for castle
                        selected_piece=black_pieces[selection]
                        if turn_step==2:
                            turn_step=3
                    if click_coords in valid_moves and selection != 100:
                        black_ep=check_ep(black_locations[selection],click_coords)
                        black_locations[selection]=click_coords
                        black_moved[selection]=True
                        if click_coords in white_locations:
                            white_piece = white_locations.index(click_coords)
                            captured_pieces_black.append(white_pieces[white_piece])
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)
                            white_moved.pop(white_piece)
                        if click_coords == white_ep:
                            white_piece = white_locations.index((white_ep[0],white_ep[1]+1))
                            captured_pieces_black.append(white_pieces[white_piece])
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)
                            white_moved.pop(white_piece)
                        black_options = valid_check_moves('black') 
                        white_options = valid_check_moves('white')
                        #win condition
                        if win('white'):
                            winner='white'
                        if win('black'):
                            winner='black'
                        turn_step=0
                        selection=100
                        valid_moves = []
                    # add castle
                    elif selection!=100 and selected_piece=='king':
                        black_options = valid_check_moves('black') 
                        white_options = valid_check_moves('white')
                        for q in range(len(castling_moves)):
                            if click_coords == castling_moves[q][0]:
                                black_locations[selection]=click_coords
                                black_moved[selection]=True
                                if click_coords == (1,7):
                                    rook_coords=(0,7)
                                else:
                                    rook_coords=(7,7)
                                rook_index=black_locations.index(rook_coords)
                                black_locations[rook_index]=castling_moves[q][1]
                                black_options = valid_check_moves('black')
                                white_options = valid_check_moves('white')
                                turn_step=0
                                selection=100
                                valid_moves = []
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_RETURN:
                    game_over=False
                    winner=''
                    white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                    white_moved=[False,False,False,False,False,False,False,False,
                                False,False,False,False,False,False,False,False]
                    black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    black_moved=[False,False,False,False,False,False,False,False,
                                False,False,False,False,False,False,False,False]
                    black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                    captured_pieces_white = []
                    captured_pieces_black = []
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                    black_options = valid_check_moves('black') 
                    white_options = valid_check_moves('white')
                    game_start=-1
        if winner != '':
            game_over=True
            draw_game_over()
    
    if game_start==1 and all_options_selected:
        screen.fill(color=(119,153,84))
        draw_board()
        draw_pieces()
        draw_captured()
        draw_check()
        if not game_over:
            white_promote,black_promote, promo_index=check_promotion()
            if white_promote or black_promote:
                draw_promotion()
                check_promo_select()
                black_options = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
                white_options = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        if selection!=100:
            valid_moves=check_valid_moves()
            draw_valid(valid_moves)
            if selected_piece == 'king':
                draw_castling(castling_moves)
        
        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type== pygame.MOUSEBUTTONDOWN and event.button==1:
                x_coord=event.pos[0] //50
                y_coord=event.pos[1] //50
                click_coords = (x_coord,y_coord)
                black_options = valid_check_moves('black') 
                white_options = valid_check_moves('white')

                if turn_step <=1:#bots turn as white
                    
                    if click_coords in white_locations:
                        #dobi lokacijo kliknjenega piecea 
                        selection = white_locations.index(click_coords)
                        #check selected for castle
                        selected_piece=white_pieces[selection]
                        if turn_step==0:
                            turn_step=1
                    if click_coords in valid_moves and selection != 100:
                        white_ep=check_ep(white_locations[selection],click_coords)
                        white_locations[selection]=click_coords
                        white_moved[selection]=True
                        if click_coords in black_locations:
                            black_piece = black_locations.index(click_coords)
                            captured_pieces_white.append(black_pieces[black_piece])
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)
                            black_moved.pop(black_piece)
                        #en passant checking
                        if click_coords == black_ep:
                            black_piece = black_locations.index((black_ep[0], black_ep[1]-1))
                            captured_pieces_white.append(black_pieces[black_piece])
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)
                            black_moved.pop(black_piece)
                        black_options = valid_check_moves('black') 
                        white_options = valid_check_moves('white')
                        #win condition
                        if win('black'):
                            winner='black'
                        if win('white'):
                            winner='white'
                        turn_step=2
                        selection=100
                        valid_moves = []
                    # add castle
                    elif selection!=100 and selected_piece=='king':
                        black_options = valid_check_moves('black') 
                        white_options = valid_check_moves('white')
                        for q in range(len(castling_moves)):
                            if click_coords == castling_moves[q][0]:
                                white_locations[selection]=click_coords
                                white_moved[selection]=True
                                if click_coords == (1,0):
                                    rook_coords=(0,0)
                                else:
                                    rook_coords=(7,0)
                                rook_index=white_locations.index(rook_coords)
                                white_locations[rook_index]=castling_moves[q][1]
                                black_options = valid_check_moves('black')
                                white_options = valid_check_moves('white')
                                turn_step=2
                                selection=100
                                valid_moves = []
                if turn_step >1:#blacks turn
                    black_options = valid_check_moves('black') 
                    white_options = valid_check_moves('white')
                    if  click_coords==(15,7)or click_coords==(16,7) or click_coords==(17,7):
                        winner='white'
                    if click_coords in black_locations:
                        #dobi lokacijo kliknjenega piecea 
                        selection = black_locations.index(click_coords)
                        #check selected for castle
                        selected_piece=black_pieces[selection]
                        if turn_step==2:
                            turn_step=3
                    if click_coords in valid_moves and selection != 100:
                        black_ep=check_ep(black_locations[selection],click_coords)
                        black_locations[selection]=click_coords
                        black_moved[selection]=True
                        if click_coords in white_locations:
                            white_piece = white_locations.index(click_coords)
                            captured_pieces_black.append(white_pieces[white_piece])
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)
                            white_moved.pop(white_piece)
                        if click_coords == white_ep:
                            white_piece = white_locations.index((white_ep[0],white_ep[1]+1))
                            captured_pieces_black.append(white_pieces[white_piece])
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)
                            white_moved.pop(white_piece)
                        black_options = valid_check_moves('black') 
                        white_options = valid_check_moves('white')
                        #win condition
                        if win('white'):
                            winner='white'
                        if win('black'):
                            winner='black'
                        turn_step=0
                        selection=100
                        valid_moves = []
                    # add castle
                    elif selection!=100 and selected_piece=='king':
                        black_options = valid_check_moves('black') 
                        white_options = valid_check_moves('white')
                        for q in range(len(castling_moves)):
                            if click_coords == castling_moves[q][0]:
                                black_locations[selection]=click_coords
                                black_moved[selection]=True
                                if click_coords == (1,7):
                                    rook_coords=(0,7)
                                else:
                                    rook_coords=(7,7)
                                rook_index=black_locations.index(rook_coords)
                                black_locations[rook_index]=castling_moves[q][1]
                                black_options = valid_check_moves('black')
                                white_options = valid_check_moves('white')
                                turn_step=0
                                selection=100
                                valid_moves = []
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_RETURN:
                    game_over=False
                    winner=''
                    white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                    white_moved=[False,False,False,False,False,False,False,False,
                                False,False,False,False,False,False,False,False]
                    black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    black_moved=[False,False,False,False,False,False,False,False,
                                False,False,False,False,False,False,False,False]
                    black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                    captured_pieces_white = []
                    captured_pieces_black = []
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                    black_options = valid_check_moves('black') 
                    white_options = valid_check_moves('white')
                    game_start=-1
        if winner != '':
            game_over=True
            draw_game_over()
    
    
    # end_time=time.time()
    # result = timeit.timeit(stmt='valid_check_moves("black") ', globals=globals(), number=5)
    # result = timeit.timeit(stmt='valid_check_moves("white") ', globals=globals(), number=5)
    # print(f"Execution time is {result*1000/5} miliseconds")
    # print((end_time-start_time)*1000)
    pygame.display.flip()
pygame.quit()