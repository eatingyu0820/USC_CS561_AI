from random import choice
import random
import sys
import time
import math
from copy import deepcopy
import operator
import timeit
import argparse
from collections import Counter

class OPGO:
    def __init__(self, n):
        self.size = n
        self.X_move = True
        self.died_pieces = [] 
        self.n_move = 0 
        self.max_move = n * n - 1 
        self.komi = n/2 
        self.verbose = False 


    def set_board(self, piece_type, previous_board, board):

        for i in range(self.size):
            for j in range(self.size):
                if previous_board[i][j] == piece_type and board[i][j] != piece_type:
                    self.died_pieces.append((i, j))

        self.previous_board = previous_board
        self.board = board

    def compare_board(self, b1, b2):

        for i in range(self.size):
            for j in range(self.size):
                if b1[i][j] != b2[i][j]:
                    return False
        return True

    def copy_board(self):
        return deepcopy(self)

    def detect_neighbor(self, i, j):

        board = self.board
        neighbors = []
        if i > 0: neighbors.append((i-1, j))
        if i < len(board) - 1: neighbors.append((i+1, j))
        if j > 0: neighbors.append((i, j-1))
        if j < len(board) - 1: neighbors.append((i, j+1))
        return neighbors

    def detect_neighbor_ally(self, i, j):
        board = self.board
        neighbors = self.detect_neighbor(i, j)
        group_allies = []
        for piece in neighbors:
            if board[piece[0]][piece[1]] == board[i][j]:
                group_allies.append(piece)
        return group_allies

    def ally_dfs(self, i, j):
        stack = [(i, j)] 
        ally_members = [] 
        while stack:
            piece = stack.pop()
            ally_members.append(piece)
            neighbor_allies = self.detect_neighbor_ally(piece[0], piece[1])
            for ally in neighbor_allies:
                if ally not in stack and ally not in ally_members:
                    stack.append(ally)
        return ally_members

    def find_liberty(self, i, j):
        board = self.board
        ally_members = self.ally_dfs(i, j)
        for member in ally_members:
            neighbors = self.detect_neighbor(member[0], member[1])
            for piece in neighbors:
                if board[piece[0]][piece[1]] == 0:
                    return True
        return False

    def find_died_pieces(self, piece_type):
        board = self.board
        died_pieces = []

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == piece_type:
                    if not self.find_liberty(i, j):
                        died_pieces.append((i,j))
        return died_pieces


    def remove_died_pieces(self, piece_type):
        died_pieces = self.find_died_pieces(piece_type)
        if not died_pieces: return []
        self.remove_certain_pieces(died_pieces)
        return died_pieces


    def remove_certain_pieces(self, positions):
        board = self.board
        for piece in positions:
            board[piece[0]][piece[1]] = 0
        self.update_board(board)


    def opp_valid_place_check(self, i, j, piece_type, test_check=False):
        board = self.board
        verbose = self.verbose
        if test_check:
            verbose = False


        if not (i >= 0 and i < len(board)):
            return False
        if not (j >= 0 and j < len(board)):
            return False
        

        if board[i][j] != 0:
            return False
        

        test_go = self.copy_board()
        test_board = test_go.board


        test_board[i][j] = piece_type
        test_go.update_board(test_board)
        if test_go.find_liberty(i, j):
            return True


        test_go.remove_died_pieces(3 - piece_type)
        if not test_go.find_liberty(i, j):
            return False


        else:
            if self.died_pieces and self.compare_board(self.previous_board, test_go.board):
                return False
        return True
        

    def update_board(self, new_board):
        self.board = new_board


    def score(self, piece_type):

        board = self.board
        cnt = 0
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == piece_type:
                    cnt += 1
        return cnt          



class GO:
    def __init__(self, n):
        self.size = n
        self.X_move = True
        self.died_pieces = []
        self.n_move = 0
        self.max_move = n * n - 1
        self.komi = n/2
        self.verbose = False

    def set_board(self, piece_type, previous_board, board):

        for i in range(self.size):
            for j in range(self.size):
                if previous_board[i][j] == piece_type and board[i][j] != piece_type:
                    self.died_pieces.append((i, j))

        self.previous_board = previous_board
        self.board = board

    def compare_board(self, b1, b2):

        for i in range(self.size):
            for j in range(self.size):
                if b1[i][j] != b2[i][j]:
                    return False
        return True

    def copy_board(self):
        return deepcopy(self)

    def detect_neighbor(self, i, j):
        board = self.board
        neighbors = []

        if i > 0: neighbors.append((i-1, j))
        if i < len(board) - 1: neighbors.append((i+1, j))
        if j > 0: neighbors.append((i, j-1))
        if j < len(board) - 1: neighbors.append((i, j+1))
        return neighbors

    def detect_neighbor_moves(self, board, i, j):
        neighbors = []

        if i > 0: neighbors.append((i-1, j))
        if i < len(board) - 1: neighbors.append((i+1, j))
        if j > 0: neighbors.append((i, j-1))
        if j < len(board) - 1: neighbors.append((i, j+1))
        return neighbors

    def detect_neighbor_ally(self, i, j):

        board = self.board
        neighbors = self.detect_neighbor(i, j)
        allies = []

        for x in neighbors:

            if board[x[0]][x[1]] == board[i][j]:
                allies.append(x)
        return allies

    def detect_neighbor_ally_moves(self, board, i, j):

        neighbors = self.detect_neighbor_moves(board, i, j)
        allies = []

        for piece in neighbors:

            if board[piece[0]][piece[1]] == board[i][j]:
                allies.append(piece)
        return allies

    def ally_dfs(self, i, j):

        stack = [(i, j)] 
        allies = []
        while stack:
            piece = stack.pop()
            allies.append(piece)
            neighbor_allies = self.detect_neighbor_ally(piece[0], piece[1])
            for ally in neighbor_allies:
                if ally not in stack and ally not in allies:
                    stack.append(ally)
        return allies

    def ally_dfs_moves(self, board, i, j):

        stack = [(i, j)]
        allies = []
        while stack:
            piece = stack.pop()
            allies.append(piece)
            neighbor_allies = self.detect_neighbor_ally_moves(board, piece[0], piece[1])
            for ally in neighbor_allies:
                if ally not in stack and ally not in allies:
                    stack.append(ally)
        return allies

    def find_liberty(self, i, j):

        board = self.board
        allies = self.ally_dfs(i, j)
        for x in allies:
            neighbors = self.detect_neighbor(x[0], x[1])
            for y in neighbors:
                if board[y[0]][y[1]] == 0:
                    return True
        return False

    def find_liberty_moves(self, board, i, j):

        allies = self.ally_dfs_moves(board, i, j)
        for x in allies:
            neighbors = self.detect_neighbor_moves(board, x[0], x[1])
            for y in neighbors:
                if board[y[0]][y[1]] == 0:
                    return True
        return False

    def find_died_pieces(self, piece_type):

        board = self.board
        died_pieces = []
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == piece_type:
                    if not self.find_liberty(i, j):
                        died_pieces.append((i,j))
        return died_pieces

    def find_died_pieces_moves(self, board, piece_type):

        died_pieces = []
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == piece_type:
                    if not self.find_liberty_moves(board, i, j):
                        died_pieces.append((i,j))
        return died_pieces


    def remove_died_pieces(self, piece_type):
        died_pieces = self.find_died_pieces(piece_type)
        if not died_pieces: return []
        self.remove_certain_pieces(died_pieces)
        return died_pieces


    def remove_certain_pieces(self, positions):
        board = self.board
        for piece in positions:
            board[piece[0]][piece[1]] = 0
        self.update_board(board)


    def valid_place_check(self, i, j, piece_type, test_check=False): 
        board = self.board
        verbose = self.verbose
        if test_check:
            verbose = False
        if not (i >= 0 and i < len(board)):
            return False
        if not (j >= 0 and j < len(board)):
            return False
        if board[i][j] != 0:
            return False
        test_go = self.copy_board()
        test_board = test_go.board
        test_board[i][j] = piece_type
        test_go.update_board(test_board)
        if test_go.find_liberty(i, j):
            return True
        test_go.remove_died_pieces(3 - piece_type)
        if not test_go.find_liberty(i, j):
            return False
        else:
            if self.died_pieces and self.compare_board(self.previous_board, test_go.board):
                return False
        return True

    def valid_place_check_moves(self, board, i, j, piece_type, test_check=False):
        verbose = self.verbose
        if test_check:
            verbose = False
        if not (i >= 0 and i < len(board)):
            return False
        if not (j >= 0 and j < len(board)):
            return False
        if board[i][j] != 0:
            return False
        test_go = self.copy_board()
        test_board = test_go.board
        test_board[i][j] = piece_type
        test_go.update_board(test_board)
        if test_go.find_liberty(i, j):
            return True
        test_go.remove_died_pieces(3 - piece_type)
        if not test_go.find_liberty(i, j):
            return False
        else:
            if self.died_pieces and self.compare_board(self.previous_board, test_go.board):
                return False
        return True
        

    def update_board(self, new_board):  
        self.board = new_board


    def score(self, piece_type):
        board = self.board
        cnt = 0
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == piece_type:
                    cnt += 1
        return cnt

def readInput(n, path="input.txt"):

    with open(path, 'r') as f:
        lines = f.readlines()

        piece_type = int(lines[0])

        previous_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:n+1]]
        board = [[int(x) for x in line.rstrip('\n')] for line in lines[n+1: 2*n+1]]

        return piece_type, previous_board, board



def writeOutput(result, path="output.txt"):
    res = ""
    if result == "PASS":
        res = "PASS"
    else:
        res += str(result[0]) + ',' + str(result[1])

    with open(path, 'w') as f:
        f.write(res)



def find_our_location(board, piece_type):
    placement = []
    for i in range(go.size):
        for j in range(go.size):
            if board[i][j] == piece_type:
                placement.append((i,j))
    return placement



def evaluate(board, color):
    scoreo, scorex = wins()

    if color == 1:
        score = scorex - scoreo
    if color == 2:
        score = scoreo - scorex
    return score

def wins():
    cnt_2 = go.score(2)
    cnt_1 = go.score(1)
    return cnt_2 + go.komi, cnt_1


def empty_cells(board,player):
    possible_placements = []
    for i in range(go.size):
        for j in range(go.size):
            if go.valid_place_check(i, j, player, test_check = True):
                possible_placements.append((i,j))
    random.shuffle(possible_placements)
    return possible_placements

def empty_cells_moves(board,player):
    possible_placements = []
    for i in range(go.size):
        for j in range(go.size):
            if go.valid_place_check_moves(board, i, j, player, test_check = True):
                possible_placements.append((i,j))
    random.shuffle(possible_placements)
    return possible_placements

def opp_empty_cells(opgo,board,player):
    possible_placements = []
    for i in range(opgo.size):
        for j in range(opgo.size):
            if opgo.opp_valid_place_check(i, j, player, test_check = True):
                possible_placements.append((i,j))
    random.shuffle(possible_placements)
    return possible_placements


def valid_move(x,y,player):
    if (x,y) in empty_cells(board,player):
        return True
    else:
        return False

def set_move(board, x, y, player):
    if valid_move(x,y, player):
        go.previous_board = deepcopy(board)
        board[x][y] = player
        go.board = board
        return board
    else:
        return board

def opp_valid_move(opgo, x,y,player):
    if (x,y) in opp_empty_cells(opgo,board,player):
        return True
    else:
        return False

def opp_set_move(opgo, board, x, y, player):
    if opp_valid_move(opgo, x,y, player):
        opgo.previous_board = deepcopy(board)
        board[x][y] = player
        opgo.board = board
        return board
    else:
        return board

def minimax_min_node(board, color, depth, alpha, beta, start_time):
    new_board = deepcopy(board)
    cur_min = math.inf
    moves = empty_cells(new_board,color)

    end = time.time()
    if len(moves) == 0 or depth == 0 or end - start_time> 8.5:
        return (-1,-1), evaluate(new_board, color)
    else: 
        for i in moves:
            board_to_pass_each_time = deepcopy(board)
            new_board = set_move(board_to_pass_each_time, i[0], i[1], color)
            go.remove_died_pieces(3 - color)
            if color == 1:
                next_player = 2
            else:
                next_player = 1
            new_move, new_score = minimax_max_node(new_board, next_player, depth - 1, alpha, beta, start_time)
            if new_score < cur_min:
                cur_min = new_score
                best_move = i
            beta = min(new_score, beta) 
            if beta <= alpha:
                break
        return best_move, cur_min 

def minimax_max_node(board, color, depth, alpha, beta, start_time):
    end = time.time()
    new_board = deepcopy(board)
    cur_max = -math.inf
    moves = empty_cells(new_board,color)
    stonestoremove = []
    for i in moves:
        go.board[i[0]][i[1]] = color
        opmoves = empty_cells(go.board, 3 - color)
        for j in opmoves:
            go.board[j[0]][j[1]] = 3 - color
            deadstones = go.find_died_pieces(color)
            go.board[j[0]][j[1]] = 0
            if i in deadstones:
                if i not in stonestoremove:
                    stonestoremove.append(i)
        go.board[i[0]][i[1]] = 0

    for x in stonestoremove:
        if x in moves:
            moves.remove(x)


    if len(moves) == 0 or depth == 0 or end - start_time> 8.5:
        return (-1,-1), evaluate(new_board, color)
    else: 
        for i in moves:
            board_to_pass_each_time = deepcopy(board)
            new_board = set_move(board_to_pass_each_time, i[0], i[1], color)
            go.remove_died_pieces(3 - color)
            if color == 1:
                next_player = 2
            else:
                next_player = 1
            new_move, new_score = minimax_min_node(new_board, next_player, depth - 1, alpha, beta, start_time)
            if new_score > cur_max:
                cur_max = new_score
                best_move = i
            alpha = max(new_score, alpha) 
            if beta <= alpha:
                break
        return best_move, cur_max

def select_move_minimax(board, color):
    start = time.time()
    best_move, score = minimax_max_node(board, color, max_depth, -math.inf, math.inf, start )
    i, j = best_move[0], best_move[1]

    return i,j, score

def opp_minimax_min_node(opgo,board, color, depth, alpha, beta, start_time):
    new_board = deepcopy(board)

    cur_min = math.inf
    moves = opp_empty_cells(opgo, new_board,color)

    end = time.time()
    if len(moves) == 0 or depth == 0 or end - start_time> 8.5:
        return (-1,-1), evaluate(new_board, color)
    else: 
        for i in moves:

            board_to_pass_each_time = deepcopy(board)
            new_board = opp_set_move(opgo,board_to_pass_each_time, i[0], i[1], color)
            opgo.remove_died_pieces(3 - color)
            if color == 1:
                next_player = 2
            else:
                next_player = 1
            new_move, new_score = opp_minimax_max_node(opgo,new_board, next_player, depth - 1, alpha, beta, start_time)
            if new_score < cur_min:
                cur_min = new_score
                best_move = i
            beta = min(new_score, beta) 
            if beta <= alpha:
                break
        return best_move, cur_min 

def opp_minimax_max_node(opgo, board, color, depth, alpha, beta, start_time):
    end = time.time()
    new_board = deepcopy(board)
    cur_max = -math.inf
    moves = opp_empty_cells(opgo, new_board,color)

    if len(moves) == 0 or depth == 0 or end - start_time> 8.5:
        return (-1,-1), evaluate(new_board, color)
    else: 
        for i in moves:

            board_to_pass_each_time = deepcopy(board)
            new_board = opp_set_move(opgo,board_to_pass_each_time, i[0], i[1], color)
            opgo.remove_died_pieces(3 - color)
            if color == 1:
                next_player = 2
            else:
                next_player = 1
            new_move, new_score = opp_minimax_min_node(opgo,new_board, next_player, depth - 1, alpha, beta, start_time)
            if new_score > cur_max:
                cur_max = new_score
                best_move = i
            alpha = max(new_score, alpha) 
            if beta <= alpha:
                break
        return best_move, cur_max


def opp_select_move_minimax(opgo, board, color):
    start = time.time()
    best_move, score = opp_minimax_max_node(opgo, board, color, max_depth_opponent, -math.inf, math.inf, start )
    i, j = best_move[0], best_move[1]

    return i,j, score




def get_input(go, piece_type):

    empty_spaces = []
    for i in range(go.size):
        for j in range(go.size):
            if go.board[i][j] == 0:
                empty_spaces.append((i,j))



    killcount = dict()
    for i in empty_spaces:
        go.board[i[0]][i[1]] = piece_type
        died_pieces = go.find_died_pieces(3-piece_type)
        go.board[i[0]][i[1]] = 0
        if len(died_pieces) >= 1:
            killcount[i] = len(died_pieces)

    sorted_killcount = sorted(killcount, key = killcount.get, reverse = True)

    for i in sorted_killcount:
        testboard = deepcopy(go.board)
        testboard[i[0]][i[1]] = piece_type
        died_stone = go.find_died_pieces_moves(testboard, 3 - piece_type)
        for x in died_stone:
            testboard[x[0]][x[1]] = 0
        if i !=None and go.previous_board != testboard:
            return i
    moves = empty_cells(go.board,piece_type)

    moves_to_remove = []
    for i in moves:
        go.board[i[0]][i[1]] = piece_type
        oppmove = empty_cells_moves(go.board, 3-piece_type)
        for j in oppmove:
            go.board[j[0]][j[1]] = 3 - piece_type
            died_pieces = go.find_died_pieces(piece_type)
            go.board[j[0]][j[1]] = 0
            if i in died_pieces:
                moves_to_remove.append(i)
        go.board[i[0]][i[1]] = 0
    for x in moves_to_remove:
        if x in moves:
            moves.remove(x)
    print('these are the final moves')
    print(moves)

    if len(moves) == 0:
        return "PASS"

    save_moves = dict()
    opponent_moves = []
    for i in range(go.size):
        for j in range(go.size):
            if go.board[i][j] == 0:
                opponent_moves.append((i,j))

    for i in opponent_moves:
        go.board[i[0]][i[1]] = 3-piece_type
        our_dead_stones = go.find_died_pieces(piece_type)
        go.board[i[0]][i[1]] = 0
        if len(our_dead_stones) >=1:
            save_moves[i] = len(our_dead_stones)

    sorted_save_moves = sorted(save_moves, key = save_moves.get, reverse = True)


    for i in sorted_save_moves:
        if i != None and i in moves:
            return i

    position_of_opponent = find_our_location(go.board, 3-piece_type)
    empty_x = []
    neighbours = []

    for i in position_of_opponent:
        neighbors = [(i[0]+board[0], i[1]+board[1]) for board in 
                    [(-1,0), (1,0), (0,-1), (0,1)] 
                    if ( (0 <= i[0]+board[0] < go.size) and (0 <= i[1]+board[1] < go.size))]
        for x in neighbors:
            neighbours.append(x)

    for i in neighbours:
        if board[i[0]][i[1]]==0:
            empty_x.append(i)
    for x in moves:
        testboard = deepcopy(go.board)
        testboard[x[0]][x[1]] = piece_type
        died_stone = go.find_died_pieces_moves(testboard, 3 - piece_type)
        for m in died_stone:
            testboard[m[0]][m[1]] = 0
        position_of_opponent = find_our_location(testboard, 3 - piece_type)
        empty_y = []
        neighbours = []

        for i in position_of_opponent:
            neighbors = [(i[0]+board[0], i[1]+board[1]) for board in 
                        [(-1,0), (1,0), (0,-1), (0,1)] 
                        if ( (0 <= i[0]+board[0] < go.size) and (0 <= i[1]+board[1] < go.size))]
            for n in neighbors:
                neighbours.append(n)

        for z in neighbours:
            if board[z[0]][z[1]] == 0:
                empty_y.append(z)

        if len(empty_x) - len(empty_y) >=1:
            return x


    if len(moves) >= 15:
        if (2,2) in moves:
            x = 2
            y = 2
            return (x,y)
        if (1,1) in moves:
            x = 1
            y = 1
            return (x,y)
        if (1,3) in moves:
            x = 1
            y = 3
            return (x,y)
        if (3,1) in moves:
            x = 3
            y = 1
            return (x,y)
        if (3,3) in moves:
            x = 3
            y = 3
            return (x,y)
        if (2,0) in moves:
            x = 2
            y = 0
            return (x,y)
        if (2,4) in moves:
            x = 2
            y = 4
            return (x,y)
        if (0,2) in moves:
            x = 0
            y = 2
            return (x,y)
        if (4,2) in moves:
            x = 4
            y = 2
            return (x,y)

    opp_board = deepcopy(go.board)
    opp_previous_board = deepcopy(go.previous_board)

    opgo = OPGO(5)
    opgo.set_board(3-piece_type, opp_previous_board, opp_board)

    movei, movej, score = opp_select_move_minimax(opgo, opp_board, 3-piece_type)
    x, y = movei, movej
    go.board[x][y] = 3 - piece_type
    empty_spaces = []
    for i in range(go.size):
        for j in range(go.size):
            if go.board[i][j] == 0:
                empty_spaces.append((i,j))


    killcount = dict()
    for i in empty_spaces:
        go.board[i[0]][i[1]] = piece_type
        died_pieces = go.find_died_pieces(3-piece_type)
        go.board[i[0]][i[1]] = 0
        if len(died_pieces) >= 1:
            print('taking out more than 1 opponents')
            killcount[i] = len(died_pieces)

    killcount_remove = []
    sorted_killcount = sorted(killcount, key = killcount.get, reverse = True)
    go.board[x][y] = 0

    if len(sorted_killcount) != 0:
        for i in sorted_killcount:
            go.board[i[0]][i[1]] == piece_type
            opmoves = empty_cells_moves(go.board, 3- piece_type)
            for j in opmoves:
                go.board[j[0]][j[1]] = 3 - piece_type
                died_pieces = go.find_died_pieces_moves(go.board, piece_type)
                go.board[j[0]][j[1]] = 0
                if i in died_pieces:
                    killcount_remove.append(i)
            go.board[i[0]][i[1]] = 0

        for x in killcount_remove:
            if x in sorted_killcount:
                sorted_killcount.remove(x)


        for i in sorted_killcount:
            if i in moves:
                return i
    movei, movej, score = select_move_minimax(go.board, piece_type)
    x, y = movei, movej
    return(x,y)



N = 5
max_depth = 4
max_depth_opponent = 1
piece_type, previous_board, board = readInput(N)
go = GO(N)
go.set_board(piece_type, previous_board, board)
action = get_input(go, piece_type)
if action == None:
    action = "PASS"
writeOutput(action)