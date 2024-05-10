import pygame as p

WIDTH = HEIGHT = 650
BOARD_WIDTH = 552
DIMENSION = 8
SQ_SIZE = BOARD_WIDTH // DIMENSION
IMAGES = {}


def loadImages():
    '''
    Load the images of all pieces.
    '''
    global IMAGES
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ',
              'bp', 'bR', 'bN', 'bB', 'bK', 'bQ' ]

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))

loadImages()
    

class Piece:
    img = ''
    startX = startY = (WIDTH - BOARD_WIDTH) // 2
    
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.moveScore = 0
        self.selected = False
    
        
    def all_moves(self, bo):
        '''
        Returns all the moves the piece can make.
        '''
    
    def valid_moves(self, bo):
        '''
        Returns the valid moves the piece can make.
        '''
    
    def draw(self, screen, bo):
        '''
        Draw the piece on board and it's valid moves if selected.
        '''
        board = bo.board
        image = IMAGES[self.color + self.img]
        
        x = self.startX + (self.col * SQ_SIZE)
        y = self.startY + (self.row * SQ_SIZE)
        
        if self.selected:
            p.draw.rect(screen, (0, 155, 155), p.Rect(x, y, SQ_SIZE, SQ_SIZE))
            vm = self.valid_moves(bo)
            for (xx, yy) in vm:
                xx = self.startX + (xx*SQ_SIZE)
                yy = self.startX + (yy*SQ_SIZE)
                
                sur = p.Surface((SQ_SIZE, SQ_SIZE))
                sur.set_alpha(128)
                sur.fill((0, 100, 200))
                screen.blit(sur, (xx, yy))
                
        if self.img == 'K':
            if self.inCheck:
                sur = p.Surface((SQ_SIZE, SQ_SIZE))
                sur.set_alpha(128)
                sur.fill((255, 0, 0))
                screen.blit(sur, (x, y))
                    
        screen.blit(image, (x, y))
           
        
class Pawn(Piece): 
    '''
    Pawn moves two squares on it's first move and one square in further moves.
    It can only move in front direction and take opponents pieces diagonally above it.
    Once a pawn reaches last row, it can be promoted to a Queen, Rook, Knight or Bishop.
    Capturing a pawn is worth 1 point.
    '''
    img = 'p'
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.firstMove = True
        self.promoted = False
        
    def valid_moves(self, bo):
        moves = self.all_moves(bo)
        
        l = len(moves)
        for i in range(l-1, -1, -1):
            move = moves[i]
            if bo.board[move[1]][move[0]] is not None and bo.board[move[1]][move[0]].img == 'K':
                del moves[i]
                continue
            
            bo.make_move((self.row, self.col), (move[1], move[0]), calc = True)
            
            if bo.is_check(self.color):
                del moves[i]
            bo.undomove(calc = True)
        
        self.moveScore = len(moves)
        return moves
    
    def all_moves(self, bo):
        board = bo.board
        i = self.row
        j = self.col
        
        moves = []
        self.moveScore = 0
        if self.color != bo.playerColor:
            if self.firstMove:    
                p = board[i+2][j]
                if p is None and board[i+1][j] is None:
                    moves.append((j, i+2))
            if i < DIMENSION - 1:
                p = board[i+1][j]
                if p is None:
                    moves.append((j, i+1))
                if j < DIMENSION - 1 and board[i+1][j+1] is not None and board[i+1][j+1].color != self.color:
                    moves.append((j+1, i+1))
                if j > 0 and board[i+1][j-1] is not None and board[i+1][j-1].color != self.color:
                    moves.append((j-1, i+1))
        else:
            if self.firstMove:    
                p = board[i-2][j]
                if p is None and board[i-1][j] is None:
                    moves.append((j, i-2))
            if i > 0:
                p = board[i-1][j]
                if p is None:
                    moves.append((j, i-1))
                if j < DIMENSION - 1 and board[i-1][j+1] is not None and board[i-1][j+1].color != self.color:
                    moves.append((j+1, i-1))
                if j > 0 and board[i-1][j-1] is not None and board[i-1][j-1].color != self.color:
                    moves.append((j-1, i-1))   
                
        return moves
                
    
        
class Rook(Piece): 
    '''
    Rook can move any number of steps in horizontal and vertical directions.
    Capturing a rook is worth 5 points.
    '''
    img = 'R'
    
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.firstMove = True
         
    def valid_moves(self, bo):
        moves = self.all_moves(bo)
        
        l = len(moves)
        for i in range(l-1, -1, -1):
            move = moves[i]
            if bo.board[move[1]][move[0]] is not None and bo.board[move[1]][move[0]].img == 'K':
                del moves[i]
                continue
            
            bo.make_move((self.row, self.col), (move[1], move[0]), calc = True)
            
            if bo.is_check(self.color):
                del moves[i]
            bo.undomove(calc = True)
        
        self.moveScore = len(moves)
        return moves
    
    def all_moves(self, bo):
        board = bo.board
        i = self.row
        j = self.col
        
        self.moveScore = 0
        moves = []
        for off in range(1, DIMENSION):
            x = i + off
            y = j
            
            if 0 <= x < DIMENSION:
                if board[x][y] is None: moves.append((y, x))
                elif board[x][y].color != self.color: 
                    moves.append((y, x))
                    break
                else:
                    break
        
        for off in range(1, DIMENSION):
            x = i - off
            y = j
            
            if 0 <= x < DIMENSION:
                if board[x][y] is None: moves.append((y, x))
                elif board[x][y].color != self.color: 
                    moves.append((y, x))
                    break
                else:
                    break
                
        for off in range(1, DIMENSION):
            x = i 
            y = j + off
            
            if 0 <= y < DIMENSION:
                if board[x][y] is None: moves.append((y, x))
                elif board[x][y].color != self.color: 
                    moves.append((y, x))
                    break
                else:
                    break
                
        for off in range(1, DIMENSION):
            x = i 
            y = j - off
            
            if 0 <= y < DIMENSION:
                if board[x][y] is None: moves.append((y, x))
                elif board[x][y].color != self.color: 
                    moves.append((y, x))
                    break
                else:
                    break
    
        return moves
    
class Knight(Piece): 
    '''
    A knight is the only piece that can jump over pieces and moves in a 'L' shape.
    Capturing a knight is worth 3 points.
    '''
    img = 'N'
    
    def valid_moves(self, bo):
        moves = self.all_moves(bo)
        
        l = len(moves)
        for i in range(l-1, -1, -1):
            move = moves[i]
            if bo.board[move[1]][move[0]] is not None and bo.board[move[1]][move[0]].img == 'K':
                del moves[i]
                continue
            
            bo.make_move((self.row, self.col), (move[1], move[0]), calc = True)
            
            if bo.is_check(self.color):
                del moves[i]
            bo.undomove(calc = True)
        
        self.moveScore = len(moves)
        return moves
    
    def all_moves(self, bo):
        board = bo.board
        i = self.row
        j = self.col
        
        moves = []
        vec = [(1, 2), (1, -2), (-1, 2), (-1, -2),
               (2, 1), (2, -1), (-2, 1), (-2, -1)]
        
        self.movescore = 0
        for x, y in vec:
            x = i + x
            y = j + y
            
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                
        return moves
    
    
class Bishop(Piece): 
    '''
    A bishop can move any number of steps in diagonal directions.
    Capturing a bishop is worth 3 points.
    '''
    img = 'B'
    
    def valid_moves(self, bo):
        moves = self.all_moves(bo)
        
        l = len(moves)
        for i in range(l-1, -1, -1):
            move = moves[i]
            if bo.board[move[1]][move[0]] is not None and bo.board[move[1]][move[0]].img == 'K':
                del moves[i]
                continue
            
            bo.make_move((self.row, self.col), (move[1], move[0]), calc = True)
            
            if bo.is_check(self.color):
                del moves[i]
            bo.undomove(calc = True)
            
        self.moveScore = len(moves)
        return moves
    
    def all_moves(self, bo):
        board = bo.board
        i = self.row
        j = self.col
        
        moves = []
        self.moveScore = 0
        for off in range(1, DIMENSION):
            x = i + off
            y = j + off
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                    if board[x][y] and board[x][y].color != self.color: 
                        break
                else:
                    break
            else: break
            
        for off in range(1, DIMENSION):
            x = i - off
            y = j - off
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                    if board[x][y] and board[x][y].color != self.color: 
                        break
                else:
                    break
            else: break
            
        for off in range(1, DIMENSION):
            x = i + off
            y = j - off
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                    if board[x][y] and board[x][y].color != self.color: 
                        break
                else:
                    break
            else: break
            
        for off in range(1, DIMENSION):
            x = i - off
            y = j + off
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                    if board[x][y] and board[x][y].color != self.color: 
                        break
                else:
                    break
            else: break
                
    
        return moves
    
    
class Queen(Piece): 
    '''
    A queen is a combination of bishop and rook and can move any number of steps in all directions.
    Capturing a queen is worth 9 points.
    '''
    img = 'Q'

    def valid_moves(self, bo):
        moves = self.all_moves(bo)
        
        l = len(moves)
        for i in range(l-1, -1, -1):
            move = moves[i]
            if bo.board[move[1]][move[0]] is not None and bo.board[move[1]][move[0]].img == 'K':
                del moves[i]
                continue
            
            bo.make_move((self.row, self.col), (move[1], move[0]), calc = True)
            
            if bo.is_check(self.color):
                del moves[i]
            bo.undomove(calc = True)
        
        self.moveScore = len(moves)
        return moves
    
    def all_moves(self, bo):
        board = bo.board
        i = self.row
        j = self.col
        
        moves = []
        self.moveScore = 0
        for off in range(1, DIMENSION):
            x = i + off
            y = j + off
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                    if board[x][y] and board[x][y].color != self.color: 
                        break
                else:
                    break
            else: break
            
        for off in range(1, DIMENSION):
            x = i - off
            y = j - off
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                    if board[x][y] and board[x][y].color != self.color: 
                        break
                else:
                    break
            else: break
            
        for off in range(1, DIMENSION):
            x = i + off
            y = j - off
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                    if board[x][y] and board[x][y].color != self.color: 
                        break
                else:
                    break
            else: break
            
        for off in range(1, DIMENSION):
            x = i - off
            y = j + off
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color:
                    moves.append((y, x))
                    if board[x][y] and board[x][y].color != self.color: 
                        break
                else:
                    break
            else: break
        
        for off in range(1, DIMENSION):
            x = i + off
            y = j
            
            if 0 <= x < DIMENSION:
                if board[x][y] is None: moves.append((y, x))
                elif board[x][y].color != self.color: 
                    moves.append((y, x))
                    break
                else:
                    break
        
        for off in range(1, DIMENSION):
            x = i - off
            y = j
            
            if 0 <= x < DIMENSION:
                if board[x][y] is None: moves.append((y, x))
                elif board[x][y].color != self.color: 
                    moves.append((y, x))
                    break
                else:
                    break
                
        for off in range(1, DIMENSION):
            x = i 
            y = j + off
            
            if 0 <= y < DIMENSION:
                if board[x][y] is None: moves.append((y, x))
                elif board[x][y].color != self.color: 
                    moves.append((y, x))
                    break
                else:
                    break
                
        for off in range(1, DIMENSION):
            x = i 
            y = j - off
            
            if 0 <= y < DIMENSION:
                if board[x][y] is None: moves.append((y, x))
                elif board[x][y].color != self.color: 
                    moves.append((y, x))
                    break
                else:
                    break
           
        return moves
    
    
class King(Piece): 
    '''
    A king can only move 1 step in all directions.
    '''
    img = 'K'
    
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.inCheck = False
        self.firstMove = True
    
    def valid_moves(self, bo):
        moves = self.all_moves(bo)
        
        l = len(moves)
        for i in range(l-1, -1, -1):
            move = moves[i]
            if bo.board[move[1]][move[0]] is not None and bo.board[move[1]][move[0]].img == 'K':
                del moves[i]
                continue
            
            bo.make_move((self.row, self.col), (move[1], move[0]), calc = True)
            
            if bo.is_check(self.color):
                del moves[i]
            bo.undomove(calc = True)
            
        if self.firstMove:
            try:
                board = bo.board
                x, y = self.row, self.col
                
                for mult in [-1, 1]:
                    if (bo.playerColor == 'w' and mult == 1) or (bo.playerColor == 'b' and mult == -1):
                        qc, bc, nc, rc = None, board[x][y+1*mult], board[x][y+2*mult], board[x][y+3*mult]
                    else:
                        qc, bc, nc, rc = board[x][y+1*mult], board[x][y+2*mult], board[x][y+3*mult], board[x][y+4*mult]
                    
                    if qc == bc == nc == None and rc is not None:
                        if rc.img == 'R' and not bo.is_check(self.color):
                            bo.make_move((x, y), (x, y+1*mult), calc=True)
                            if not bo.is_check(self.color):
                                bo.make_move((x, y+1*mult), (x, y+2*mult), calc=True)
                                if not bo.is_check(self.color):
                                    moves.append((y+2*mult, x))
                                bo.undomove(calc=True)
                            bo.undomove(calc=True)
                                
            except Exception as e:
                pass  
                
        return moves
    
    def all_moves(self, bo):
        board = bo.board
        i = self.row
        j = self.col
        
        moves = []
        vec = [(1, 0), (0, 1), (-1, 0), (0, -1),
               (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for x, y in vec:
            x = i + x
            y = j + y
            if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
                if board[x][y] is None or board[x][y].color != self.color: moves.append((y, x))
                
        return moves