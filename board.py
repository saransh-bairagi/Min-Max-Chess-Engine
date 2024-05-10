import pygame as p
from piece import Pawn, Rook, Knight, Bishop, Queen, King
from chessAI import MoveFinder

p.mixer.init()
moveSound = p.mixer.Sound('sounds/move.wav')

class NoKingError(Exception):
    pass

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        
        # Alphabetic representation of chess baord
        self.rep = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        
        self.board = [[None for _ in range(cols)] for _ in range(rows)]
        self.playerColor = 'w'
        self.reset_board()
  
        
    def setPlayerColor(self, playerColor):
        if playerColor not in ['w', 'b']: return
        self.playerColor = playerColor
   
        
    def reset_board(self):
        '''
        Reset the chess board to starting position and clear the movelogs.
        '''
        change = {'p': Pawn, 'R': Rook, 'N': Knight, 'B': Bishop, 'Q': Queen, 'K': King}
        for i in range(self.rows):
            for j in range(self.cols):
                if self.rep[i][j] != '--':
                    self.board[i][j] = change[self.rep[i][j][1]](i, j, self.rep[i][j][0])
                else:
                    self.board[i][j] = None
                    
        self.movelog = []
        self.turn = 'w'
    
    
    def highlightLastMove(self, screen, startX, startY, SQ_SIZE):
        '''
        Highlight the squares of opponent's last move.
        '''
        if self.movelog:
            lastmove = self.movelog[-1]
            if lastmove != "castling":
                row, col = lastmove[0]
                x = startX + (col * SQ_SIZE)
                y = startY + (row * SQ_SIZE)
                
                sur = p.Surface((SQ_SIZE, SQ_SIZE))
                sur.set_alpha(128)
                sur.fill((219, 149, 229))
                screen.blit(sur, (x, y))
                           
                row, col = lastmove[1]
                x = startX + (col * SQ_SIZE)
                y = startY + (row * SQ_SIZE)
                
                sur = p.Surface((SQ_SIZE, SQ_SIZE))
                sur.set_alpha(128)
                sur.fill((219, 149, 229))
                screen.blit(sur, (x, y))
        
        
    def draw(self, screen):
        '''
        Draw all the chess pieces on board.
        '''
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] is not None:
                    self.board[i][j].draw(screen, self)
            
                    
    def select(self, row, col):
        '''
        Select the piece corresponding to (row, col) if any, otherwise unselect all pieces.
        '''
        self.unselectall()
        
        if self.board[row][col] is not None and self.board[row][col].color == self.turn:
            self.board[row][col].selected = True
            return (row, col)
        
        return (None, None)
    
                    
    def unselectall(self):
        '''
        Unselect all the pieces on board.
        '''
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j]: self.board[i][j].selected = False
          
    
    def rotate_board(self):
        '''
        Rotate the board 180 degrees.
        '''
        self.board = self.board[::-1]
        self.rep = self.rep[::-1]
        
        for i in range(self.rows):
            self.board[i] = self.board[i][::-1]
            self.rep[i] = self.rep[i][::-1]
            
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] is not None:
                    self.board[i][j].row = i
                    self.board[i][j].col = j
    
                    
    def chess_notation(self, row, col):
        '''
        Convert the (row, col) to chess notation.
        '''
        if self.playerColor == 'w':
            alp = chr(col + ord('a')) 
            num = self.rows - row
            return f'{alp}{num}'
        else:
            num = row + 1
            alp = chr(ord('h') - col)
            return f'{alp}{num}'
    
        
    def make_move(self, start, end, calc = False, castle = False):
        '''
        Call move function and unselect all pieces.
        '''
        self.move(start, end, calc, castle = castle)
        
        if not calc:
            self.unselectall()
        
        
    def make_move_computer(self):
        '''
        Call move function for computer.
        '''
        self.move_computer()
     
        
    def move_computer(self):
        '''
        Chooses a valid move for computer and execute it. If no valid moves are present computer is lost.
        '''
        move = MoveFinder.negaMax(self)
        
        if move is None: return
        start = move[0]
        end = move[1]
        if self.castling(start, end):
            return
        self.move(start, end, comp=True)
     
            
    def move(self, start, end, calc = False, comp = False, castle = False):
        '''
        Move the piece in start cell to end cell and see if there is check on any king.
        Returns the piece captured if any and add the move to log.
        '''
        removed = self.board[end[0]][end[1]]
        promoted = False
        
        self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = None
        self.board[end[0]][end[1]].row = end[0]
        self.board[end[0]][end[1]].col = end[1]
        color = self.board[end[0]][end[1]].color
        
        firstmove = False
        if self.board[end[0]][end[1]].img in ['p', 'K', 'R']:
            firstmove = self.board[end[0]][end[1]].firstMove
        
        if self.board[end[0]][end[1]].img == 'K' and not calc: 
            self.board[end[0]][end[1]].firstMove = False
        
        if self.board[end[0]][end[1]].img == 'R' and not calc: 
            self.board[end[0]][end[1]].firstMove = False
            
        if self.board[end[0]][end[1]].img == 'p' and not calc: 
            self.board[end[0]][end[1]].firstMove = False
            if end[0] == 0 or end[0] == self.rows - 1:
                promoteTo = {'R': Rook, 'N': Knight, 'B': Bishop, 'Q': Queen}
                if not comp:
                    prom = promoteTo.get(promote_menu(), 'Q')
                else:
                    prom = promoteTo['Q']
                self.board[end[0]][end[1]] = prom(end[0], end[1], color)
                promoted = True
        
        opp_color = 'w' if color == 'b' else 'b'
        
        in_check = self.is_check(color)
        x, y = self.find_king(color)
        self.board[x][y].inCheck = in_check
        
        in_check = self.is_check(opp_color)
        x, y = self.find_king(opp_color)
        self.board[x][y].inCheck = in_check
            
        if not castle:
            self.turn = 'b' if self.turn == 'w' else 'w'
            
        if not calc:
            moveSound.play()
            
        self.movelog.append([start, end, removed, promoted, firstmove])
        
        return removed
    
            
    def castling(self, start, end):
        '''
        Check if current move is castling. If it is do the castle else do normal move.
        '''
        sr, sc = start[0], start[1]
        er, ec = end[0], end[1]
        if self.board[sr][sc] is None or self.board[sr][sc].img != 'K':
            return False
        
        if sr == er and abs(sc-ec) == 2:
            mult = 1 if self.playerColor == 'w' else -1
            if (ec > sc and mult == 1) or (sc > ec and mult == -1):
                self.make_move((sr, sc), (er, ec))
                self.make_move((sr, ec+1*mult), (er, ec-1*mult), castle = True)
                self.movelog.append("castling")
            else:
                self.make_move((sr, sc), (er, ec))
                self.make_move((sr, ec-2*mult), (er, ec+1*mult), castle = True)
                self.movelog.append("castling")                
            return True
        else: return False  
    
                        
    def undomove(self, calc = False, comp = False):
        '''
        Undo the last move.
        '''
        
        if not calc:
            self.unselectall()
            
        if self.movelog:
            if comp:
                self.undomove()
                self.undomove()
                return 
            
            if self.movelog[-1] == "castling":
                self.movelog.pop()
                self.undomove()
                self.undomove()
                return
            
            start, end, removed, promoted, firstmove = self.movelog.pop()
            
            
            self.board[start[0]][start[1]] = self.board[end[0]][end[1]]
            self.board[end[0]][end[1]] = removed
            
            if firstmove:
                self.board[start[0]][start[1]].firstMove = True
            
            if removed is not None:
                self.board[end[0]][end[1]].row = end[0]
                self.board[end[0]][end[1]].col = end[1]
                
            self.board[start[0]][start[1]].row = start[0]
            self.board[start[0]][start[1]].col = start[1]
            
            if promoted:
                self.board[start[0]][start[1]] = Pawn(start[0], start[1], self.board[start[0]][start[1]].color)
            
            self.turn = 'b' if self.turn == 'w' else 'w'
            
            in_check = self.is_check('w')
            x, y = self.find_king('w')
            self.board[x][y].inCheck = in_check
            
            in_check = self.is_check('b')
            x, y = self.find_king('b')
            self.board[x][y].inCheck = in_check
       
        
    def generate_valid_moves(self, color):
        '''
        Generates all valid moves for all the pieces.
        '''
        validmoves = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] is None: continue
                if self.board[i][j].color == color:
                    vm = self.board[i][j].valid_moves(self)
                    for move in vm:
                        validmoves.append([(i, j), (move[1], move[0])])
                        
        return validmoves
    
    
    def generate_all_moves(self, color):
        '''
        Generates all valid moves for all the pieces.
        '''
        allmoves = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] is None: continue
                if self.board[i][j].color == color:
                    am = self.board[i][j].all_moves(self)
                    for move in am:
                        allmoves.append([(i, j), (move[1], move[0])])
                        
        return allmoves
    
    
    def calculate_control(self, color):
        '''
        Calculates the Attack and defense score of given color.
        Attack score is the value of opponent's pieces under attack.
        Defense score is the value of player's pieces under protection.
        '''
        all_moves = self.generate_all_moves(color)
        pieceScore = {"K": 0, "Q": 100, "R": 60, "N": 30, "B": 30, "p": 10}
        score = 0
        prot_coeff, att_coeff = 0.04, 0.06
        for move in all_moves:
            x, y = move[1][0], move[1][1]
            if self.board[x][y] is not None:
                if self.board[x][y].color == color: score += prot_coeff*pieceScore[self.board[x][y].img]
                else: score += att_coeff*pieceScore[self.board[x][y].img]
                
        return score                
    
            
    def find_king(self, color):
        '''
        Find the position of king on the board.
        '''
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] is None: continue
                if self.board[i][j].color == color and self.board[i][j].img == 'K':
                    return (i, j)
           
        # for i in range(8):
        #     for j in range(8):
        #         if self.board[i][j] is None: print("  ", end=' ')
        #         else: print(self.board[i][j].color + self.board[i][j].img, end=' ')
        #     print()
            
        raise NoKingError(f"{color} King is not present on the board")
                
                
    def is_checkmate(self, color):
        '''
        Return if the king is currently in checkmate.
        '''
        if self.turn != color: return False
        
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] is None: continue
                if self.board[i][j].color == color:
                    '''
                    # Generate all the valid moves for all the pieces.
                    # If any piece has a valid move then it is not checkmate.
                    # If there are no valid moves and king is in check, it is checkmate.
                    '''
                    validmoves = self.board[i][j].valid_moves(self)
                    if validmoves: return False
                    
        if self.is_check(color):
            return True
        
        return False
                
                
    def is_stalemate(self, color):
        '''
        Return if the king is currently in stalemate.
        '''
        if self.turn != color: return False
        
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] is None: continue
                if self.board[i][j].color == color:
                    validmoves = self.board[i][j].valid_moves(self)
                    if validmoves: return False
                    
        if not self.is_check(color):
            return True
        
        return False
            
            
    def is_check(self, color):
        '''
        Return if the king is currently in check.
        '''
        opp_color = 'w' if color == 'b' else 'b'
        check = False
        
        '''
        # Generate all the moves of opponent.
        # check if any of the move attack the cell of king.
        '''
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] is None: continue
                if self.board[i][j].color == opp_color:
                    validmoves = self.board[i][j].all_moves(self)
                    
                    for (y, x) in validmoves:
                        if self.board[x][y] is None: continue
                        if self.board[x][y].img == 'K' and self.board[x][y].color == color:
                            check = True
                            break
                
                if check: break
            if check: break
        
        return check
                 
from game import promote_menu
