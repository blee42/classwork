#!/usr/bin/env python
import struct, string, math, copy

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
        # print_board(board.CurrentGameboard)
        # print
        if check_assignment(board, row, col, i):
            gameBoard[row][col] = i
            
            if (solve_backtrack(board)):
                return True

            gameBoard[row][col] = 0

    return False

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

    return (not rowCheck) & (not colCheck) & (not boxCheck)

board4 = init_board('4x4.sudoku.txt')
sol = solve_backtrack(board4)
checkSol = iscomplete(board4.CurrentGameboard)
print "4x4 Board Solve: " + str(checkSol)

board9 = init_board('9x9.sudoku.txt')
sol = solve_backtrack(board9)
checkSol = iscomplete(board9.CurrentGameboard)
print "9x9 Board Solve: " + str(checkSol)

# board16 = init_board('16x16.sudoku.txt')
# sol = solve_backtrack(board16)
# checkSol = iscomplete(board16.CurrentGameboard)
# print "16x16 Board Solve: " + str(checkSol)

# board25 = init_board('25x25.sudoku.txt')
# sol = solve_backtrack(board25)
# checkSol = iscomplete(board25.CurrentGameboard)
# print "25x25 Board Solve: " + str(checkSol)



