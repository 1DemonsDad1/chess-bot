"""
Main driver.
Handling user input.
Displaying GameStatus objekt.
"""

import pygame as p
import ChessEngine, ChessAI
import itertools
import sys
from multiprocessing import Process, Queue

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
lightcolor= (233,237,204)
darkcolor=(119,153,84)
mapname="clasic"
format="png"
drawmore=False

def loadImages():
    """
    kreira globaln directory za image.
    izvede se samo enkrat v mainu in to je to.
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load(f"images/{mapname}/{piece}.{format}"), (SQUARE_SIZE, SQUARE_SIZE)
        )


def main():  # sourcery skip: avoid-builtin-shadow
    """
    main driver kode.
    handles user input in updatea grafike.
    """
    p.init()
    p.display.set_caption("ChessEngine")
    p.display.set_icon(p.image.load("images\icon\chessenginelogo.png"))
    font = p.font.Font('freesansbold.ttf', 20)
    big_font = p.font.Font('freesansbold.ttf', 50)
    small_font = p.font.Font('freesansbold.ttf', 12)
    
    def drawMenu():
        global drawmore
        
        p.draw.rect(screen,(81,80,76),(0,0,770,512))

        #playchess
        screen.blit(big_font.render('Play Chess',True,darkcolor),(70,80))

        #2players button
        p.draw.rect(screen,darkcolor,[100,200,100,50],40,7)
        screen.blit(font.render('2 players',True,lightcolor),(105,215))

        # vs ai as black
        p.draw.rect(screen,darkcolor,[100,300,100,50],40,7)
        screen.blit(font.render('Against',True,lightcolor),(110,305))
        screen.blit(font.render('bots',True,lightcolor),(125,325))
        screen.blit(font.render('*',True,lightcolor),(105,350))
        screen.blit(small_font.render('select options',True,lightcolor),(115,350))

        #themes
        screen.blit(big_font.render('Themes',True,darkcolor),(400,125))

        #themes buttons

        p.draw.rect(screen,(233,237,204),[350,200,25,25],0,0,7,0,0,0)
        p.draw.rect(screen,(119,153,84),[375,200,25,25],0,0,0,7,0,0)
        p.draw.rect(screen,(119,153,84),[350,225,25,25],0,0,0,0,7,0)    #theme1
        p.draw.rect(screen,(233,237,204),[375,225,25,25],0,0,0,0,0,7)

        p.draw.rect(screen,("#dee3e6"),[400,200,25,25],0,0,7,0,0,0)
        p.draw.rect(screen,("#8ca2ad"),[425,200,25,25],0,0,0,7,0,0)
        p.draw.rect(screen,("#8ca2ad"),[400,225,25,25],0,0,0,0,7,0)     #theme2
        p.draw.rect(screen,("#dee3e6"),[425,225,25,25],0,0,0,0,0,7)

        p.draw.rect(screen,("#f0d9b5"),[450,200,25,25],0,0,7,0,0,0)
        p.draw.rect(screen,("#b58863"),[475,200,25,25],0,0,0,7,0,0)
        p.draw.rect(screen,("#b58863"),[450,225,25,25],0,0,0,0,7,0)     #theme3
        p.draw.rect(screen,("#f0d9b5"),[475,225,25,25],0,0,0,0,0,7)

        p.draw.rect(screen,("#ececec"),[500,200,25,25],0,0,7,0,0,0)
        p.draw.rect(screen,("#c1c18e"),[525,200,25,25],0,0,0,7,0,0)     #theme4
        p.draw.rect(screen,("#c1c18e"),[500,225,25,25],0,0,0,0,7,0)
        p.draw.rect(screen,("#ececec"),[525,225,25,25],0,0,0,0,0,7)

        p.draw.rect(screen,("#dcdcdc"),[550,200,25,25],0,0,7,0,0,0)
        p.draw.rect(screen,("#c9c9c9"),[575,200,25,25],0,0,0,7,0,0)
        p.draw.rect(screen,("#c9c9c9"),[550,225,25,25],0,0,0,0,7,0)     #theme5
        p.draw.rect(screen,("#dcdcdc"),[575,225,25,25],0,0,0,0,0,7)

        p.draw.rect(screen,("#9f90b0"),[600,200,25,25],0,0,7,0,0,0)
        p.draw.rect(screen,("#7d4a8d"),[625,200,25,25],0,0,0,7,0,0)     #theme6
        p.draw.rect(screen,("#7d4a8d"),[600,225,25,25],0,0,0,0,7,0)
        p.draw.rect(screen,("#9f90b0"),[625,225,25,25],0,0,0,0,0,7)

        #----------------------Pieces-prewiev-----------------------#

        #squares for the piece preview
        for i in range(12):
            p.draw.rect(screen,(lightcolor if i%2==0 else darkcolor) if i<=5 else (darkcolor if i%2==0 else lightcolor),[(350+50*i) if i<=5 else (50+50*i),355 if i<=5 else 405,50,50])

        #Piece preview
        pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
        for ind,piece in enumerate(pieces):
            screen.blit(p.transform.scale(p.image.load(f"images/{mapname}/{piece}.{format}"), (50, 50)),((350+50*ind) if ind<=5 else (50+50*ind),355 if ind<=5 else 405))


        #------------------------------------------------Piece-skins--------------------------------------------------#

        #chess pieces
        for i in range(6):
            p.draw.rect(screen,darkcolor,[350+50*i,300,50,50],0,7)
            screen.blit(big_font.render(f'{i+1}',True,lightcolor),(362+50*i,303)) 

        
        # more pieces button
        p.draw.rect(screen,(0,0,0),[650,340,12,12],0,2)
        p.draw.rect(screen,(0,0,0),[654,341,4,10],0,1) if drawmore else p.draw.rect(screen,(255,255,255),[654,341,4,10],0,1)
        p.draw.rect(screen,(255,255,255),[651,344,10,4],0,1)

        if drawmore==True:
            p.draw.rect(screen,darkcolor,[700,250,50,50],0,7)
            screen.blit(big_font.render('7',True,lightcolor),(712,253))

            p.draw.rect(screen,darkcolor,[700,300,50,50],0,7)
            screen.blit(big_font.render('8',True,lightcolor),(712,303))

            p.draw.rect(screen,darkcolor,[700,350,50,50],0,7)
            screen.blit(big_font.render('9',True,lightcolor),(712,353))
        #------------------------------------------------End-of-draw-------------------------------------------------#
        return #da skrijem komentar end of draw 
    
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState()
    valid_moves = game_state.getValidMoves()
    move_made = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move
    running = True
    square_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    player_clicks = []  # this will keep track of player clicks (two tuples)
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = p.font.SysFont("Arial", 14, False, False)
    player_one = True  # if a human is playing white, then this will be True, else False
    player_two = False  # if a hyman is playing white, then this will be True, else False
    game=0
    while game==0:
        drawMenu()
        p.display.flip()
        for e in p.event.get():
                if e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    print(location)
                    global lightcolor
                    global darkcolor
                    global mapname
                    global format
                    global drawmore

                    if location[0]<=200 and location[0]>=100 and location[1]>=200 and location[1]<=250:#100-200x, 200-250y
                                                                                                        #100-200x, 300-350y
                        game=1
                    
                    if location[0]<=200 and location[0]>=100 and location[1]>=300 and location[1]<=350:
                        game=2

                    #---------------------------------------THEMES----------------------------------------------#
                    if location[0]<=400 and location[0]>=350 and location[1]>=200 and location[1]<=250:#theme 1
                        lightcolor= (233,237,204)
                        darkcolor=(119,153,84)
                    
                    if location[0]<=450 and location[0]>=400 and location[1]>=200 and location[1]<=250:#theme 2
                        lightcolor="#dee3e6"
                        darkcolor="#8ca2ad"
                    
                    if location[0]<=500 and location[0]>=450 and location[1]>=200 and location[1]<=250:#theme 3
                        lightcolor="#f0d9b5"
                        darkcolor="#b58863"

                    if location[0]<=550 and location[0]>=500 and location[1]>=200 and location[1]<=250:#theme 4
                        lightcolor="#ececec"
                        darkcolor="#c1c18e"

                    if location[0]<=600 and location[0]>=550 and location[1]>=200 and location[1]<=250:#theme 5
                        lightcolor="#dcdcdc"
                        darkcolor="#a9a9a9"

                    if location[0]<=650 and location[0]>=600 and location[1]>=200 and location[1]<=250:#theme 6
                        lightcolor="#9f90b0"
                        darkcolor="#7d4a8d"
                    

                    #---------------------------------------SKINS----------------------------------------------#

                    if location[0]<=400 and location[0]>=350 and location[1]>=300 and location[1]<=350:#skin 1
                        mapname="clasic"
                        format="png"
                    
                    if location[0]<=450 and location[0]>=400 and location[1]>=300 and location[1]<=350:#skin 2
                        mapname="polished"
                        format="png"
                    
                    if location[0]<=500 and location[0]>=450 and location[1]>=300 and location[1]<=350:#skin 3
                        mapname="KidsDrawing"
                        format="png"

                    if location[0]<=550 and location[0]>=500 and location[1]>=300 and location[1]<=350:#skin 4
                        mapname="7chess"
                        format="svg"

                    if location[0]<=600 and location[0]>=550 and location[1]>=300 and location[1]<=350:#skin 5
                        mapname="chessnut"
                        format="svg"

                    if location[0]<=650 and location[0]>=600 and location[1]>=300 and location[1]<=350:#skin 6
                        mapname="icpieces"
                        format="svg"

                    #---------------------------------------MORE-SKINS-------------------------------------------#
                    #button and functionality
                    if location[0]<=660 and location[0]>=651 and location[1]>=340 and location[1]<=350:#buton +
                        drawmore= not drawmore
                    
                    if drawmore and location[0]<=750 and location[0]>=700 and location[1]>=250 and location[1]<=300: #skin 7
                        mapname="letter"
                        format="svg"
                    
                    if drawmore and location[0]<=750 and location[0]>=700 and location[1]>=300 and location[1]<=350: #skin 8
                        mapname="KiwenSuwi"
                        format="svg"

                    if drawmore and location[0]<=750 and location[0]>=700 and location[1]>=350 and location[1]<=400: #skin 9
                        mapname="shapes"
                        format="svg"


                if e.type == p.QUIT:
                    p.quit()
                    sys.exit()
    loadImages()
    if game==1:
        while running:
            human_turn = True
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    sys.exit()
                # mouse handler
                elif e.type == p.MOUSEBUTTONDOWN:
                    if not game_over:
                        location = p.mouse.get_pos()  # (x, y) location of the mouse
                        col = location[0] // SQUARE_SIZE
                        row = location[1] // SQUARE_SIZE
                        if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
                            square_selected = ()  # deselect
                            player_clicks = []  # clear clicks
                        else:
                            square_selected = (row, col)
                            player_clicks.append(square_selected)  # append for both 1st and 2nd click

                        if len(player_clicks) == 2 and human_turn:  # after 2nd click
                            move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    game_state.makeMove(valid_moves[i])
                                    move_made = True
                                    animate = True
                                    square_selected = ()  # reset user clicks
                                    player_clicks = []
                            if not move_made:
                                player_clicks = [square_selected]
                

                

                # key handler
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z:  # undo when 'z' is pressed
                        game_state.undoMove()
                        move_made = True
                        animate = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True
                    if e.key == p.K_r:  # reset the game when 'r' is pressed
                        game_state = ChessEngine.GameState()
                        valid_moves = game_state.getValidMoves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True

                    if e.key == p.K_RETURN and game_over: # if enter is pressed when game is over
                        game_state = ChessEngine.GameState()
                        valid_moves = game_state.getValidMoves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True
                        running=False
                        game=0
                        main()
            

            if move_made:
                if animate:
                    animateMove(game_state.move_log[-1], screen, game_state.board, clock)
                valid_moves = game_state.getValidMoves()
                move_made = False
                animate = False
                move_undone = False

            drawGameState(screen, game_state, valid_moves, square_selected)

            if not game_over:
                drawMoveLog(screen, game_state, move_log_font)

            if game_state.checkmate:
                game_over = True
                if game_state.white_to_move:
                    p.draw.rect(screen,(81,80,76),(64,180,385,110),55,10)
                    drawEndGameText(screen, "Black wins by checkmate",0)
                    drawEndGameText(screen, "press ENTER to go to menu",1)
                    
                else:
                    p.draw.rect(screen,(81,80,76),(64,180,385,110),55,10)
                    drawEndGameText(screen, "White wins by checkmate",0)
                    drawEndGameText(screen, "press ENTER to go to menu",40,3)
                    

            elif game_state.stalemate:
                game_over = True
                p.draw.rect(screen,(81,80,76),(64,180,385,110),55,10)
                drawEndGameText(screen, "Stalemate",0)
                drawEndGameText(screen, "press ENTER to go to menu",1)
                

            clock.tick(MAX_FPS)
            p.display.flip()

    if game==2:
            
        while running:
            human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    sys.exit()
                # mouse handler
                elif e.type == p.MOUSEBUTTONDOWN:
                    if not game_over and human_turn:
                        location = p.mouse.get_pos()  # (x, y) location of the mouse
                        col = location[0] // SQUARE_SIZE
                        row = location[1] // SQUARE_SIZE
                        if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
                            square_selected = ()  # deselect
                            player_clicks = []  # clear clicks
                        else:
                            square_selected = (row, col)
                            player_clicks.append(square_selected)  # append for both 1st and 2nd click
                        if len(player_clicks) == 2 and human_turn:  # after 2nd click
                            move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    game_state.makeMove(valid_moves[i])
                                    move_made = True
                                    animate = True
                                    square_selected = ()  # reset user clicks
                                    player_clicks = []
                            if not move_made:
                                player_clicks = [square_selected]
                
                # key handler
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z:  # undo when 'z' is pressed
                        game_state.undoMove()
                        move_made = True
                        animate = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True
                    if e.key == p.K_r:  # reset the game when 'r' is pressed
                        game_state = ChessEngine.GameState()
                        valid_moves = game_state.getValidMoves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True

                    if e.key == p.K_RETURN and game_over: # if enter is pressed when game is over
                        game_state = ChessEngine.GameState()
                        valid_moves = game_state.getValidMoves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True
                        running=False
                        game=0
                        main()

            # AI move finder
            if not game_over and not human_turn and not move_undone:
                if not ai_thinking:
                    ai_thinking = True
                    return_queue = Queue()  # used to pass data between threads
                    move_finder_process = Process(target=ChessAI.findBestMove, args=(game_state, valid_moves, return_queue))
                    move_finder_process.start()

                if not move_finder_process.is_alive():
                    ai_move = return_queue.get()
                    if ai_move is None:
                        ai_move = ChessAI.findMove(game_state, valid_moves)
                    game_state.makeMove(ai_move)
                    move_made = True
                    animate = True
                    ai_thinking = False

            if move_made:
                if animate:
                    animateMove(game_state.move_log[-1], screen, game_state.board, clock)
                valid_moves = game_state.getValidMoves()
                move_made = False
                animate = False
                move_undone = False

            drawGameState(screen, game_state, valid_moves, square_selected)

            if not game_over:
                drawMoveLog(screen, game_state, move_log_font)

            if game_state.checkmate:
                game_over = True
                if game_state.white_to_move:
                    p.draw.rect(screen,(81,80,76),(64,180,385,110),55,10)
                    drawEndGameText(screen, "Black wins by checkmate",0)
                    drawEndGameText(screen, "press ENTER to go to menu",1)
                    
                else:
                    p.draw.rect(screen,(81,80,76),(64,180,385,110),55,10)
                    drawEndGameText(screen, "White wins by checkmate",0)
                    drawEndGameText(screen, "press ENTER to go to menu",40,3)
                    

            elif game_state.stalemate:
                game_over = True
                p.draw.rect(screen,(81,80,76),(64,180,385,110),55,10)
                drawEndGameText(screen, "Stalemate",0)
                drawEndGameText(screen, "press ENTER to go to menu",1)
                

            clock.tick(MAX_FPS)
            p.display.flip()


def drawGameState(screen, game_state, valid_moves, square_selected):
    """
    Vse grafike v trenutnem gamestateu
    """
    drawBoard(screen)  # draw squares on board
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)  # draw pieces on squares


def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    global colors
    colors = [lightcolor, darkcolor]
    for row, column in itertools.product(range(DIMENSION), range(DIMENSION)):
        color = colors[((row + column) % 2)]
        p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def highlightSquares(screen, game_state, valid_moves, square_selected):
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(game_state.move_log)) > 0:
        last_move = game_state.move_log[-1]
        s = square_highlight('green')
        screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE))
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == (
                'w' if game_state.white_to_move else 'b'):  # square_selected is a piece that can be moved
            s = square_highlight('blue')
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))

def square_highlight(arg0):
    result = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
    result.set_alpha(100)
    result.fill(p.Color(arg0))
    return result


def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for row, column in itertools.product(range(DIMENSION), range(DIMENSION)):
        piece = board[row][column]
        if piece != "--":
            screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawMoveLog(screen, game_state, font):
    """
    Nariše move log.
    """
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), move_log_rect)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = f'{str(i // 2 + 1)}. {str(move_log[i])} '
        if i + 1 < len(move_log):
            move_string += f"{str(move_log[i + 1])}  "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = "".join(
            move_texts[i + j]
            for j in range(moves_per_row)
            if i + j < len(move_texts)
        )
        text_object = font.render(text, True, p.Color('white'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def drawEndGameText(screen, text,num):
    
    if num==1:
        font = p.font.SysFont("Helvetica", 32, True, False)
        text_object = font.render(text, False, p.Color(81,80,76))
        text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                    BOARD_HEIGHT / 2 - text_object.get_height() / 2)
        screen.blit(text_object, text_location)
        text_object = font.render(text, False, p.Color('white'))
        screen.blit(text_object, text_location.move(2, 2))
        
    if num==0:
        font = p.font.SysFont("Helvetica", 32, True, False)
        text_object = font.render(text, False, p.Color(81,80,76))
        text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                    (BOARD_HEIGHT / 2 - text_object.get_height() / 2)-50)
        screen.blit(text_object, text_location)
        text_object = font.render(text, False, p.Color('white'))
        screen.blit(text_object, text_location.move(2, 2))

def animateMove(move, screen, board, clock):
    """
    Animating a move
    """
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 7  # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col * SQUARE_SIZE, enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
