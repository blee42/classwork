#!/usr/bin/env python
import struct, string, math, copy, time, timeit

#this will be the game object your player will manipulate
class SudokuBoard:

    #the constructor for the SudokuBoard
    def __init__(self, size, board):
      self.BoardSize = size #the size of the board
      self.CurrentGameboard= board #the current state of the game board

    #This function will create a new sudoku board object with
    #with the input value placed on the GameBoard row and col are
    #both zero-indexed
    def set_value(self, row, col, value):
        self.CurrentGameboard[row][col]=value #add the value to the appropriate position on the board
        return SudokuBoard(self.BoardSize, self.CurrentGameboard) #return a new board of the same size with the value added
    


# parse_file
#this function will parse a sudoku text file (like those posted on the website)
#into a BoardSize, and a 2d array [row,col] which holds the value of each cell.
# array elements witha value of 0 are considered to be empty

def parse_file(filename):
    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board
    



#takes in an array representing a sudoku board and tests to
#see if it has been filled in correctly
def iscomplete( BoardArray ):
        size = len(BoardArray)
        subsquare = int(math.sqrt(size))

        #check each cell on the board for a 0, or if the value of the cell
        #is present elsewhere within the same row, column, or square
        for row in range(size):
            for col in range(size):

                if BoardArray[row][col]==0:
                    return False
                for i in range(size):
                    if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                        return False
                    if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                        return False
                #determine which square the cell is in
                SquareRow = row // subsquare
                SquareCol = col // subsquare
                for i in range(subsquare):
                    for j in range(subsquare):
                        if((BoardArray[SquareRow*subsquare + i][SquareCol*subsquare + j] == BoardArray[row][col])
                           and (SquareRow*subsquare + i != row) and (SquareCol*subsquare + j != col)):
                            return False
        return True

# creates a SudokuBoard object initialized with values from a text file like those found on the course website
def init_board( file_name ):
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def print_board(board):
    for row in board:
        print row

def solve_backtrack(board):
    size = board.BoardSize
    gameBoard = board.CurrentGameboard
    blanks = find_blanks(board)
    if(not blanks):
        return True

    row, col = blanks
    for i in range(1,size+1):
        if check_assignment(board, row, col, i):
            gameBoard[row][col] = i
            
            if (solve_backtrack(board)):
                return True

            gameBoard[row][col] = 0

    return False

def solve_forwardcheck(board):
    size = board.BoardSize
    gameBoard = board.CurrentGameboard
    blanks = find_blanks(board)
    
    # if assignment returns no blanks, puzzle solved
    if(not blanks):
        return True

    # assign first blank
    row, col = blanks

    # find domain
    d = find_single_solution(board, row, col)
    dOld = copy.deepcopy(d)
    for value in dOld:
        # check assignment 
        if check_assignment(board, row, col, value):
            gameBoard[row][col] = value

            if(solve_forwardcheck(board)):
                return True

            gameBoard[row][col] = 0
            d = dOld
        else:
            d = dOld

    return False

def find_single_solution(board, row, col):
    size = board.BoardSize
    gameBoard = board.CurrentGameboard
    sol = []

    for i in range(1,size+1):
        if(check_assignment(board, row, col, i)):
            sol.append(i)

    return sol


def solve_backtrackMRV(board):
    size = board.BoardSize
    gameBoard = board.CurrentGameboard
    blanks = find_blanks(board)
    if(not blanks):
        return True

    mrv = find_MRV(board)

    if (not mrv):
        return True

    row, col = mrv
    d = [1,2,3,4]
    dOld = copy.deepcopy(d)
    for value in dOld:
        if check_assignment(board, row, col, value):
            gameBoard[row][col] = value
            
            if (solve_backtrack(board)):
                return True

            gameBoard[row][col] = 0
            d = dOld

    print "did we get here?"
    return False

def solve_backtrackLCV(board):
    size = board.BoardSize
    gameBoard = board.CurrentGameboard
    blanks = find_blanks(board)
    if(not blanks):
        return True

    mrv = find_MRV(board)

    if (not mrv):
        return True

    row, col = mrv
    value = find_LCV(board, row, col)

    if (value == 0):
        print "error: could not find a LCV"

    if check_assignment(board, row, col, value):
        gameBoard[row][col] = value
        
        if (solve_backtrack(board)):
            return True

        gameBoard[row][col] = 0

    return False

def find_LCV(board, row, col):
    size = board.BoardSize
    boardClone = copy.deepcopy(board)
    gameBoardClone = boardClone.CurrentGameboard
    maxVal = 0

    domain = find_single_solution(board, row, col)

    for value in domain:
        # add value to board
        gameBoardClone[row][col] = value
        solutions = find_all_solutions(boardClone)
        solBoard = solutions.CurrentGameboard

        solCount = 0
        maxSolCount = 0

        # count number of constraints
        for i in range(0,size):
            for j in range(0, size):
                solCount = solCount + len(solBoard[i][j])

        # find max solCount
        if (solCount > maxSolCount):
            maxSolCount = solCount
            maxVal = value

    return maxVal

def find_MRV(board):
    size = board.BoardSize
    
    solutions = find_all_solutions(board)

    solBoard = solutions.CurrentGameboard
    mrv = [0,0,size]

    for row in range(0,size):
        for col in range(0,size):
            curLen = len(solBoard[row][col])

            if (curLen < mrv[2]) and (curLen != 0) :
                mrv[0] = row
                mrv[1] = col
                mrv[2] = curLen

    if (mrv[2] == size):
        return False

    return mrv[0], mrv[1]

def find_all_solutions(board):
    size = board.BoardSize
    gameBoard = board.CurrentGameboard

    # initialize solutions grid
    solutions = copy.deepcopy(board)
    solBoard = solutions.CurrentGameboard
    for row in range(0,size):
        for col in range(0,size):
            solBoard[row][col] = []

    for row in range(0,size):
        for col in range(0,size):
            if (gameBoard[row][col] == 0):
                for i in range(1,size+1):
                    if (check_assignment(board, row, col, i)):
                        solBoard[row][col].append(i)

    return solutions

def find_empty(board):
    size = board.BoardSize
    solBoard = board.CurrentGameboard
    for row in range(0,size):
        for col in range(0,size):
            if solBoard[row][col] != []:
                return False
    return True


def find_blanks(board):
    size = board.BoardSize
    gameBoard = board.CurrentGameboard
    for row in range(0,size):
        for col in range(0,size):
            if gameBoard[row][col] == 0:
                return row, col
    return False

def check_row(board, row, num):
    size = board.BoardSize
    gameBoard = board.CurrentGameboard
    for col in range(0,size):
        if gameBoard[row][col] == num:
            return True
    return False

def check_col(board, col, num):
    size = board.BoardSize
    gameBoard = board.CurrentGameboard
    for row in range(0,size):
        if gameBoard[row][col] == num:
            return True
    return False

def check_box(board, startRow, startCol, num):
    subsize = int(math.sqrt(board.BoardSize))
    gameBoard = board.CurrentGameboard
    for subrow in range(0,subsize):
        for subcol in range(0,subsize):
            if gameBoard[subrow+startRow][subcol+startCol] == num:
                return True
    return False

def check_assignment(board, row, col, num):
    subsize = int(math.sqrt(board.BoardSize))
    rowCheck = check_row(board, row, num)
    colCheck = check_col(board, col, num)
    boxCheck = check_box(board, row-row%subsize, col-col%subsize, num)

    return (not rowCheck) and (not colCheck) and (not boxCheck)
    # return (not rowCheck) and (not boxCheck)

# Simple Backtracking
board4 = init_board('4x4.sudoku.txt')
sol = solve_backtrack(board4)
timer = timeit.Timer(lambda: solve_backtrack(board4))
checkSol = iscomplete(board4.CurrentGameboard)
print "4x4 Board Solve Simple Backtrack: " + str(checkSol)
print "Time: " + str(timer.timeit(number=1))

# MRV Backtracking
board4 = init_board('4x4.sudoku.txt')
sol = solve_backtrackMRV(board4)
timer = timeit.Timer(lambda: solve_backtrackMRV(board4))
checkSol = iscomplete(board4.CurrentGameboard)
print "4x4 Board Solve MRV Backtrack: " + str(checkSol)
print "Time: " + str(timer.timeit(number=1))

# MRV+LCV Backtracking
board4 = init_board('4x4.sudoku.txt')
sol = solve_backtrackLCV(board4)
timer = timeit.Timer(lambda: solve_backtrackLCV(board4))
checkSol = iscomplete(board4.CurrentGameboard)
print "4x4 Board Solve MRV+LCV Backtrack: " + str(checkSol)
print "Time: " + str(timer.timeit(number=1))

# Forward Checking
board4 = init_board('4x4.sudoku.txt')
sol = solve_forwardcheck(board4)
timer = timeit.Timer(lambda: solve_forwardcheck(board4))
checkSol = iscomplete(board4.CurrentGameboard)
print "4x4 Board Solve Forward Checking: " + str(checkSol)
print "Time: " + str(timer.timeit(number=1))

print

# Simple Backtracking
board9 = init_board('9x9.sudoku.txt')
sol = solve_backtrack(board9)
timer = timeit.Timer(lambda: solve_backtrack(board9))
checkSol = iscomplete(board9.CurrentGameboard)
print "9x9 Board Solve Simple Backtrack: " + str(checkSol)
print "Time: " + str(timer.timeit(number=1))

# MRV Backtracking
board9 = init_board('9x9.sudoku.txt')
size = board9.BoardSize
sol = solve_backtrackMRV(board9)
timer = timeit.Timer(lambda: solve_backtrackMRV(board9))
checkSol = iscomplete(board9.CurrentGameboard)
print "9x9 Board Solve MRV Backtrack: " + str(checkSol)
print "Time: " + str(timer.timeit(number=1))

# MRV+LCV Backtracking
board9 = init_board('9x9.sudoku.txt')
sol = solve_backtrackLCV(board9)
timer = timeit.Timer(lambda: solve_backtrackLCV(board9))
checkSol = iscomplete(board9.CurrentGameboard)
print "9x9 Board Solve MRV+LCV Backtrack: " + str(checkSol)
print "Time: " + str(timer.timeit(number=1))

# Forward Checking
board9 = init_board('9x9.sudoku.txt')
sol = solve_forwardcheck(board9)
timer = timeit.Timer(lambda: solve_forwardcheck(board9))
checkSol = iscomplete(board9.CurrentGameboard)
print "9x9 Board Solve Forward Checking: " + str(checkSol)
print "Time: " + str(timer.timeit(number=1))

print

# # Simple Backtracking
# board16 = init_board('16x16.sudoku.txt')
# sol = solve_backtrack(board16)
# checkSol = iscomplete(board16.CurrentGameboard)
# print "16x16 Board Solve Simple Backtrack: " + str(checkSol)

# MRV Backtracking
board16 = init_board('16x16.sudoku.txt')
size = board16.BoardSize
sol = solve_backtrackMRV(board16)
checkSol = iscomplete(board16.CurrentGameboard)
print "16x16 Board Solve MRV Backtrack: " + str(checkSol)

# # MRV+LCV Backtracking
# board16 = init_board('16x16.sudoku.txt')
# sol = solve_backtrackLCV(board16)
# checkSol = iscomplete(board16.CurrentGameboard)
# print "16x16 Board Solve MRV+LCV Backtrack: " + str(checkSol)

# # Forward Checking
# board16 = init_board('16x16.sudoku.txt')
# sol = solve_forwardcheck(board16)
# checkSol = iscomplete(board16.CurrentGameboard)
# print "16x16 Board Solve Forward Checking: " + str(checkSol)

print

# # Simple Backtracking
# board25 = init_board('25x25.sudoku.txt')
# sol = solve_backtrack(board25)
# checkSol = iscomplete(board25.CurrentGameboard)
# print "25x25 Board Solve Simple Backtrack: " + str(checkSol)

# # MRV Backtracking
# board25 = init_board('25x25.sudoku.txt')
# size = board25.BoardSize
# sol = solve_backtrackMRV(board25)
# checkSol = iscomplete(board25.CurrentGameboard)
# print "25x25 Board Solve MRV Backtrack: " + str(checkSol)

# # MRV+LCV Backtracking
# board25 = init_board('25x25.sudoku.txt')
# sol = solve_backtrackLCV(board25)
# checkSol = iscomplete(board25.CurrentGameboard)
# print "25x25 Board Solve MRV+LCV Backtrack: " + str(checkSol)

# # Forward Checking
# board25 = init_board('25x25.sudoku.txt')
# sol = solve_forwardcheck(board25)
# checkSol = iscomplete(board25.CurrentGameboard)
# print "25x25 Board Solve Forward Checking: " + str(checkSol)



