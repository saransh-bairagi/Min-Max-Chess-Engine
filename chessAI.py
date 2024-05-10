from random import randint, choice, shuffle
import pygame as p

def rotated(board, mult=1):
    '''
    Rotate the piece tables and adjust scores for all colors and sides.
    '''
    n, m = len(board), len(board[0])
    new_board = [[0]*m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            new_board[i][j] = -board[i][j]*mult
    
    new_board = new_board[::-1]
    for i in range(n):
        new_board[i] = new_board[i][::-1]
        
    return new_board

pieceScore = {
    'K': 0,
    'Q': 10000,
    'R': 6000,
    'B': 3000,
    'N': 3000,
    'p': 1000 
}
CHECKMATE = 100000
STALEMATE = 0
CHECK = 1100

pawnTable = [
    [100, 100, 100, 100, 100, 100, 100, 100],
    [ 40,  30,  25,  40,  40,  25,  30,  40],
    [ 20,  5 ,  20,  5 ,  25,  10,  5 ,  20],
    [ 5 ,  5 ,  0 ,  5 ,  0 ,  0 ,  5 ,  5 ],
    [ 0 ,  0 ,  5 ,  15,  5 ,  5 ,  0 ,  0 ],
    [ 5 ,  0 ,  0 ,  10,  10,  0 ,  0 ,  5 ],
    [ 10,  10,  0 , -10, -10,  0 ,  10,  10],
    [ 0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ]
]
rookTable = [
    [ 20,  30,  40,  50,  50,  40,  30,  20],
    [ 0 ,  20,  30,  40,  40,  30,  20,  0 ],
    [ 0 ,  0 ,  0 ,  20,  20,  10,  0 ,  0 ],
    [ 0 ,  0 ,  10,  30,  30,  0 ,  20,  0 ],
    [ 0 ,  0 ,  0 ,  30,  30,  0 ,  0 ,  0 ],
    [ 0 ,  0 ,  0 ,  20,  20,  0 ,  0 ,  0 ],
    [ 0 ,  0 ,  20,  30,  30,  20,  0 ,  0 ],
    [ 0 ,  0 ,  10,  30,  30,  10,  10,  0 ]
]
bishopTable = [
    [ 20,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  20],
    [ 0 ,  10,  0 ,  0 ,  0 ,  0 ,  10,  0 ],
    [ 0 ,  0 ,  0 ,  8 ,  5 ,  0 ,  0 ,  0 ],
    [ 0 ,  30,  0 ,  10,  0 ,  10,  30,  0 ],
    [ 0 ,  0 ,  20,  10,  10,  20,  0 ,  0 ],
    [ 0 ,  0 ,  10,  5 ,  5 ,  10,  0 ,  0 ],
    [ 0 ,  5 ,  0 ,  5 ,  5 ,  0 ,  5 ,  0 ],
    [ 0 ,  0 , -10,  0 ,  0 , -10,  0 ,  0 ]
]
knightTable = [
    [ 5 ,  0 ,  0 ,  5 ,  5 ,  0 ,  0 ,  5 ],
    [ 0 ,  0 ,  10,  0 ,  0 ,  10,  0 ,  0 ],
    [ 0 ,  0 ,  0 ,  10,  10,  0 ,  0 ,  0 ],
    [ 0 ,  5 ,  0 ,  5 ,  5 ,  0 ,  5 ,  0 ],
    [ 0 ,  0 ,  0 ,  5 ,  5 ,  0 ,  0 ,  0 ],
    [ 0 ,  0 ,  5 ,  0 ,  0 ,  10,  0 ,  0 ],
    [ 0 ,  0 ,  0 ,  5 ,  5 ,  0 ,  0 ,  0 ],
    [ 0 , -5 ,  0 ,  0 ,  0 ,  0 , -10,  0 ]
]
queenTable = [
    [ 40,  25,  30,  40,  40,  30,  25,  40],
    [ 0 ,  20,  0 ,  0 ,  0 ,  0 ,  20,  0 ],
    [ 0 ,  0 ,  10,  0 ,  0 ,  10,  0 ,  0 ],
    [ 0 ,  0 ,  0 ,  30,  30,  0 ,  0 ,  0 ],
    [ 0 ,  0 ,  0 ,  30,  30,  0 ,  0 ,  0 ],
    [ 0 ,  0 ,  0 ,  10,  5 ,  10,  0 ,  0 ],
    [ 0 ,  0 ,  5 ,  5 ,  5 ,  0 ,  0 ,  0 ],
    [ 0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ]
]
kingTable = [
    [-40, -25, -30, -40, -40, -30, -25, -40],
    [-10, -20, -10, -10, -10, -10, -20, -10],
    [ -5,  -5, -10, -10, -10, -10,  -5,  -5],
    [ 0 ,  0 ,  0 , -30, -30,  0 ,  0 ,  0 ],
    [ 0 ,  0 ,  0 , -30, -30,  0 ,  0 ,  0 ],
    [ 0 ,  0 ,  0 , -10,  -5, -10,  0 ,  0 ],
    [-10,  -8,  -5,  -5,  -5,  -5,  -8, -10],
    [ 0 ,  0 ,  20,   0,  10,  0 ,  10,  0 ]
]

pieceTablePlayer = {
    'K': kingTable,
    'Q': queenTable,
    'R': rookTable,
    'B': bishopTable,
    'N': knightTable,
    'p': pawnTable
}

pieceTableComputer = {
    'K': rotated(kingTable),
    'Q': rotated(queenTable),
    'R': rotated(rookTable),
    'B': rotated(bishopTable),
    'N': rotated(knightTable),
    'p': rotated(pawnTable)
}

class MoveFinder:
    
    @staticmethod   
    def find_score(bo):
        '''
        Find the score of board based on piece value only.
        Positive score is good for white.
        '''
        score = 0
        board = bo.board
        for i in range(bo.rows):
            for j in range(bo.cols):
                if board[i][j] is None: continue
                if board[i][j].color == 'w': score += pieceScore[board[i][j].img]
                else: score -= pieceScore[board[i][j].img]
                    
        return score
    
    
    @staticmethod
    def randomMove(bo):
        '''
        Out of all valid moves, return a move at random.
        If no valid moves, return None.
        '''
        cutoff = 80
        anyvalidmove = False
        while True:
            for i in range(bo.rows):
                for j in range(bo.cols):
                    if bo.board[i][j] is None: continue
                    if bo.board[i][j].color == bo.turn:
                        validmoves = bo.board[i][j].valid_moves(bo)
                        # print(validmoves)
                        if validmoves:
                            anyvalidmove = True
                            if randint(10, 100) >= cutoff:
                                randomMove = choice(validmoves)
                                # print((i, j), randomMove)
                                return [(i, j), (randomMove[1], randomMove[0])]
                        else:
                            cutoff -= 10
                            
            if not anyvalidmove:
                return None
    
    
    @staticmethod
    def greedyMove(bo):
        '''
        Choose the current best move greedily. If all moves are equivalent choose a random move.
        '''
        turnMultiplier = 1 if bo.turn == 'w' else -1
        
        maxScore = MoveFinder.find_score(bo)*turnMultiplier
        bestMove = None
        effective = False
        for i in range(bo.rows):
            for j in range(bo.cols):
                if bo.board[i][j] is None: continue
                if bo.board[i][j].color == bo.turn:
                    validmoves = bo.board[i][j].valid_moves(bo)
                    for move in validmoves:
                        opp_color = 'w' if bo.board[i][j].color == 'b' else 'b'
                        bo.make_move((i, j), (move[1], move[0]), calc=True)
                        if bo.is_checkmate(opp_color):
                            score = CHECKMATE
                        elif bo.is_stalemate(opp_color):
                            score = STALEMATE
                        elif bo.is_check(opp_color):
                            score = CHECK
                        else:
                            score = MoveFinder.find_score(bo)*turnMultiplier
                            
                        
                        if score > maxScore:
                            maxScore = score
                            bestMove = [(i, j), (move[1], move[0])] 
                            effective = True
                        
                        bo.undomove()
        
        if bestMove is None:
            return MoveFinder.randomMove(bo)
        if not effective:
            return MoveFinder.randomMove(bo)
        
        return bestMove
    
    
    @staticmethod
    def miniMaxSmall(bo):
        '''
        Iterative minimax Algorithm that looks one move ahead.
        '''
        turnMultiplier = 1 if bo.turn == 'w' else -1
        
        # opponentMinMaxScore = MoveFinder.find_score(bo)*turnMultiplier
        opponentMinMaxScore = CHECKMATE
        bestMove = None
        opponent_color = 'w' if bo.turn == 'b' else 'b'
        
        playerMoves = bo.generate_valid_moves(bo.turn)
        shuffle(playerMoves)
        for playerMove in playerMoves:
            bo.make_move(playerMove[0], playerMove[1], calc = True)
            opponent_moves = bo.generate_valid_moves(opponent_color)
            shuffle(opponent_moves)
            
            # opponentMaxScore = MoveFinder.find_score(bo)*turnMultiplier
            opponentMaxScore = -CHECKMATE
            for oppMove in opponent_moves:
                bo.make_move(oppMove[0], oppMove[1], calc = True)
                score = 0
                if bo.is_checkmate(bo.turn):
                    score = -CHECKMATE*turnMultiplier
                elif bo.is_stalemate(bo.turn):
                    score = STALEMATE
                elif bo.is_check(bo.turn):
                    score = -CHECK*turnMultiplier
                
                score += -MoveFinder.find_score(bo)*turnMultiplier
                    
                if score > opponentMaxScore:
                    opponentMaxScore = score        
                bo.undomove()
            
            if  opponentMaxScore < opponentMinMaxScore:
                opponentMinMaxScore = opponentMaxScore
                bestMove = playerMove     
            
            bo.undomove()
                    
        if bestMove is None:
            return MoveFinder.randomMove(bo)
        
        return bestMove
    
    
    @staticmethod   
    def scoreBoard(bo):
        '''
        Improved method to find score.
        '''
        if bo.is_checkmate('w'): return -CHECKMATE
        if bo.is_checkmate('b'): return CHECKMATE
        if bo.is_stalemate('w') or bo.is_stalemate('b'): return STALEMATE
        
        score = 0
        
        if bo.is_check('w'): score -= CHECK
        elif bo.is_check('b'): score += CHECK
        
        board = bo.board
        for i in range(bo.rows):
            for j in range(bo.cols):
                if board[i][j] is None: continue
                
                if bo.playerColor == 'w':
                    if board[i][j].color == 'w': 
                        score += pieceTablePlayer[board[i][j].img][i][j]
                    else:
                        score += pieceTableComputer[board[i][j].img][i][j]
                else:
                    if board[i][j].color == 'w': 
                        score += rotated(pieceTablePlayer[board[i][j].img], mult=-1)[i][j]
                    else:
                        score += rotated(pieceTableComputer[board[i][j].img], mult=-1)[i][j]
                
                
                if board[i][j].color == 'w':
                    score += (20*pieceScore[board[i][j].img] + board[i][j].moveScore*8 + 12*bo.calculate_control('w'))
                else:
                    score -= (20*pieceScore[board[i][j].img] + board[i][j].moveScore*8 + 12*bo.calculate_control('b'))
                    
        return score
    
    
    @staticmethod
    def miniMax(bo):
        '''
        Recursive mini max algorithm without optimization.
        '''
        bestMove = None
        maxDepth = 3
        movescalc = 0

        def miniMaxHelper(bo, depth, whiteToMove):
            nonlocal bestMove, maxDepth, movescalc
            movescalc += 1
            if depth == 0:
                return MoveFinder.scoreBoard(bo)
            
            if whiteToMove:
                maxScore = -CHECKMATE
                validmoves = bo.generate_valid_moves('w')
                shuffle(validmoves)
                for move in validmoves:
                    bo.make_move(move[0], move[1], calc = True)
                    score = miniMaxHelper(bo, depth - 1, False)
                    if score > maxScore:
                        maxScore = score
                        if depth == maxDepth:
                            bestMove = move
                    bo.undomove(calc = True)
                return maxScore
            else:
                minScore = CHECKMATE
                validmoves = bo.generate_valid_moves('b')
                shuffle(validmoves)
                for move in validmoves:
                    bo.make_move(move[0], move[1], calc = True)
                    score = miniMaxHelper(bo, depth - 1, True)
                    if score < minScore:
                        minScore = score
                        if depth == maxDepth:
                            bestMove = move
                    bo.undomove(calc = True)
                return minScore         
            
        whiteToMove = (bo.turn == 'w')
        miniMaxHelper(bo, maxDepth, whiteToMove)
        if bestMove is None:
            return MoveFinder.randomMove(bo)
        # print("Moves Calculated:",movescalc)
        return bestMove
    
    
    @staticmethod
    def negaMax(bo):
        '''
        Efficient implementation of minimax(Negamax) with alpha beta pruning.
        '''
        bestMove = None
        maxDepth = 2 # + 1*(randint(0, 500) > 400)
        movescalc = 0

        def negaMaxHelper(bo, depth, turnMultiplier, alpha, beta):
            nonlocal bestMove, maxDepth, movescalc
            p.event.pump()
            movescalc += 1
            if depth == 0:
                return turnMultiplier*MoveFinder.scoreBoard(bo)
            
            # move_ordering
            maxScore = -CHECKMATE
            if turnMultiplier == 1: validmoves = bo.generate_valid_moves("w")
            else: validmoves = bo.generate_valid_moves("b")
                
            shuffle(validmoves)
            for move in validmoves:
                bo.make_move(move[0], move[1], calc = True)
                
                score = - negaMaxHelper(bo, depth - 1, - turnMultiplier, - beta, - alpha)
                if score > maxScore:
                    maxScore = score
                    if depth == maxDepth:
                        bestMove = move
                
                bo.undomove(calc = True)
                if maxScore > alpha:
                    alpha = maxScore
                if alpha >= beta:
                    break
                
            return maxScore
                
            
        turnMultiplier = 1 if (bo.turn == 'w') else -1
        negaMaxHelper(bo, maxDepth, turnMultiplier, -CHECKMATE, CHECKMATE)
        
        if bestMove is None:
            return MoveFinder.randomMove(bo)
        
        print("Moves Calculated:",movescalc,"... Depth:",maxDepth)
        return bestMove
    