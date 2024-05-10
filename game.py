import pygame as p
import os
from board import Board


WIDTH = HEIGHT = 650
BOARD_WIDTH = 552
DIMENSION = 8
SQ_SIZE = BOARD_WIDTH // DIMENSION
startX = startY = (WIDTH - BOARD_WIDTH) // 2
FPS = 15
bo = Board(DIMENSION, DIMENSION)
p.init()
screen = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption('Chess Game')


def drawboard(screen):
    '''
    Draw the checkered pattern chess board.
    '''
    colors = [p.Color(232, 235, 239), p.Color(125, 135, 150)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)&1]
            p.draw.rect(screen, color, p.Rect(startX + c*SQ_SIZE, startY + r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def end_screen(bo, screen):
    '''
    Check if the game has ended and display the text on screen.
    '''
    font = p.font.SysFont('Arial', 20)
    
    whitecm = font.render('White Checkmated. (R to restart)', True, (0, 0, 0))
    blackcm = font.render('Black Checkmated. (R to restart)', True, (0, 0, 0))
    whitesm = font.render('White Stalemated. (R to restart)', True, (0, 0, 0))
    blacksm = font.render('Black Stalemated. (R to restart)', True, (0, 0, 0))
    tm = font.render(f"{'white' if bo.turn == 'w' else 'Black'} to move", True, (255, 255, 255))
    
    p.draw.rect(screen, (59, 1, 60), p.Rect(startX, 10, 125, 20))
    screen.blit(tm, (startX, 10))
    
    if bo.is_checkmate('w'): screen.blit(whitecm, (150, 285))
    elif bo.is_checkmate('b'): screen.blit(blackcm, (150, 285))
    elif bo.is_stalemate('w'): screen.blit(whitesm, (150, 285))
    elif bo.is_stalemate('b'): screen.blit(blacksm, (150, 285))
    

def redraw_gamewindow(screen):
    '''
    Draw board, add pieces and update screen.
    '''
    global bo
    drawboard(screen)
    bo.highlightLastMove(screen, startX, startY, SQ_SIZE)
    bo.draw(screen)
    end_screen(bo, screen)
    
    p.display.update()
    
    
def click(pos):
    '''
    return index of cell on board given mouse click.
    '''
    x, y = pos
    row, col = -1, -1
    if startX < x < startX + BOARD_WIDTH:
        if startY < y < startY + BOARD_WIDTH:
            x -= startX
            y -= startY
            row = y // SQ_SIZE
            col = x // SQ_SIZE
            
    # print(row, col)
    return (row, col)


def main_menu(screen):
    screen.fill(p.Color(180, 180, 200))
    
    running = True
    p1x, p1y, p1w, p1h = 20, 30, 200, 50
    p2x, p2y, p2w, p2h = 20, 120, 200, 50
    gamemode, playerColor = 1, 'w'
    clock = p.time.Clock()
    
    
    p.draw.rect(screen, (30, 30, 30), p.Rect(p1x, p1y, p1w, p1h))
    p.draw.rect(screen, (30, 30, 30), p.Rect(p2x, p2y, p2w, p2h))
    
    font = p.font.SysFont('Arial', 20)
    
    p1txt = font.render('Against Computer', True, (120, 120, 120))
    screen.blit(p1txt, (p1x + 20, p1y + 15))
    
    p2txt = font.render('Against Player', True, (120, 120, 120))
    screen.blit(p2txt, (p2x + 20, p2y + 15))
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                exit(0)
                
            if e.type == p.MOUSEBUTTONDOWN:
                x, y = p.mouse.get_pos()
                if p1x <= x <= p1x + p1w and p1y <= y <= p1y + p1h:
                    gamemode = 1
                    running = False
                    break
                
                if p2x <= x <= p2x + p2w and p2y <= y <= p2y + p2h:
                    gamemode = 2
                    running = False
                    break
                
        clock.tick(FPS)
        p.display.flip()
    
    if gamemode == 1:
        running = True
        p.draw.rect(screen, (30, 30, 30), p.Rect(p1x, p1y, p1w, p1h))
        p.draw.rect(screen, (30, 30, 30), p.Rect(p2x, p2y, p2w, p2h))
        
        p1txt = font.render('Play as White', True, (120, 120, 120))
        screen.blit(p1txt, (p1x + 20, p1y + 15))
        
        p2txt = font.render('Play as black', True, (120, 120, 120))
        screen.blit(p2txt, (p2x + 20, p2y + 15))
        
        while running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    exit(0)
                    
                if e.type == p.MOUSEBUTTONDOWN:
                    x, y = p.mouse.get_pos()
                    if p1x <= x <= p1x + p1w and p1y <= y <= p1y + p1h:
                        playerColor = 'w'
                        running = False
                        break
                    
                    if p2x <= x <= p2x + p2w and p2y <= y <= p2y + p2h:
                        playerColor = 'b'
                        running = False
                        break
                
            clock.tick(FPS)
            p.display.flip()
    
    return (gamemode, playerColor)


def promote_menu():
    global screen
    
    screen.fill(p.Color(180, 180, 200))
    
    running = True
    clock = p.time.Clock()
    
    font = p.font.SysFont('Arial', 20)
    heading = font.render('Promote pawn to?', True, (0, 0, 0))
    screen.blit(heading, (40, 20))
    
    promotes = [(40, 60, 100, 40, 'Q', 'Queen'), (40, 120, 100, 40, 'R', 'Rook'), (40, 180, 100, 40, 'N', 'Knight'), (40, 240, 100, 40, 'B', 'Bishop')]
    
    for sx, sy, w, h, pc, pn in promotes:
        p.draw.rect(screen, (30, 30, 30), p.Rect(sx, sy, w, h))
        name = font.render(pn, True, (180, 180, 200))
        screen.blit(name, (sx + 10, sy + 10))
    
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                exit(0)
                
            if e.type == p.MOUSEBUTTONDOWN:
                x, y = p.mouse.get_pos()
                
                for sx, sy, w, h, pc, pn in promotes:
                    if sx <= x <= sx + w and sy <= y <= sy + h:
                        screen.fill(p.Color(59, 1, 60))
                        return pc
                
                
        clock.tick(FPS)
        p.display.flip()
    
    

def main():
    global screen
    clock = p.time.Clock()
    
    gamemode, playerColor = main_menu(screen)
    bo.setPlayerColor(playerColor)
    if bo.playerColor == 'b': bo.rotate_board()
    
    screen.fill(p.Color(59, 1, 60))
    running = True
    start = (None, None)
    while running:
        redraw_gamewindow(screen)
        
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                break
            if e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    if gamemode == 2:
                        bo.undomove()
                    elif bo.turn == bo.playerColor:
                        bo.undomove(comp = True)
                    start = (None, None)
                if e.key == p.K_r:
                    bo.reset_board()
                    start = (None, None)
                    
            if e.type == p.MOUSEBUTTONDOWN:
                '''
                # If the click is outside board unselect all pieces
                # If there is no piece already selected, then select this one.
                # Otherwise if the cell is in valid moves, move the piece.
                # Otherwise unselect the piece or select other piece.
                '''
                pos = p.mouse.get_pos()
                row, col = click(pos)
                if gamemode == 2 or bo.turn == bo.playerColor:
                    if (row, col) != (-1, -1):
                        if start != (None, None):
                            if (col, row) in bo.board[start[0]][start[1]].valid_moves(bo):
                                if bo.castling(start, (row, col)): pass
                                else: bo.make_move(start, (row, col))
                                start = (None, None)    
                            else: start = bo.select(row, col)
                        else: start = bo.select(row, col)
                    else: bo.unselectall()
                
        if gamemode == 1 and bo.turn != bo.playerColor:
            redraw_gamewindow(screen)
            bo.make_move_computer()
            
        clock.tick(FPS)
        p.display.flip()
        
    p.quit()
    
    
if __name__ == "__main__":
    main()