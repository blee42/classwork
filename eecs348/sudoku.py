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

def create_solutions(size):
    possibleVals = []
    possibles = {}

    # possible number values
    for i in range(1,size+1):
        possibleVals.append(i)

    # dictionary of all rows, columns, and squares
    for i in range(0,size):
        row = "r" + str(i)
        col = "c" + str(i)
        sq = "sq" + str(i)
        possibles[row] = copy.deepcopy(possibleVals)
        possibles[col] = copy.deepcopy(possibleVals)
        possibles[sq] = copy.deepcopy(possibleVals)

    return possibles

def get_state(board, size, possibles):

    count = 0
    subsquare = int(math.sqrt(size))
    for row in range(0,size):
        for column in range(0,size):
            curVal = board[row][column]
            row_key = "r" + str(row)
            col_key = "c" + str(column)
            if row<subsquare & column<subsquare:
                sq_key = "sq0"
            elif row<subsquare:
                sq_key = "sq1"
            elif column<subsquare:
                sq_key = "sq2"
            else:
                sq_key = "sq3"
            if curVal != 0:
                print curVal
                col_possibles = possibles[col_key]
                row_possibles = possibles[row_key]
                sq_possibles = possibles[sq_key]
                print "old possibles"
                # print  col_key, col_possibles
                # print row_key, row_possibles
                print sq_key, sq_possibles
                col_possibles.remove(curVal)
                row_possibles.remove(curVal)
                sq_possibles.remove(curVal)

                possibles[col_key] = col_possibles
                possibles[row_key] = row_possibles
                possibles[sq_key] = sq_possibles
                print "new possibles"
                # print col_key, possibles[col_key]
                # print row_key, possibles[row_key]
                print sq_key, possibles[sq_key]
                # print

            # for subi in range(0,subsquare):
            #     for subj in range(0,subsquare):
            #         print "subsquare"
            #         print row, column
            #         row_index = row+(row-row%subsquare)
            #         col_index = column+(column-column%subsquare)
            #         print row_index, col_index
            #         print board[row_index][col_index]



    print possibles

def back_tracking(board, size, possibles):

    for row in range(0,size):
        for col in range(0,size):
            curVal = board[row][col]
            if curVal == 0:
                row_key = "r" + str(row)
                col_key = "c" + str(column)
                if row<subsquare & column<subsquare:
                    sq_key = "sq0"
                elif row<subsquare:
                    sq_key = "sq1"
                elif column<subsquare:
                    sq_key = "sq2"
                else:
                    sq_key = "sq3"

                rowp = possibles[row_key]
                colp = possibles[col_key]
                sqp = possibles[sq_key]

                for i in range(0,len(rowp))
                    val = possibles[row_key].pop(i)
                    if colp.index(val) & sqp.index(val):
                        


board = init_board('4x4.sudoku.txt')
print_board(board.CurrentGameboard)
sol = create_solutions(board.BoardSize)
get_state(board.CurrentGameboard, board.BoardSize, sol)

# def check_possible_solutions(board):
#     for row in range(0,4):
#         for column in range(0,4):
#             if board[row][column] == 0:
#                 print row
#                 print column
#                 print "possible solutio"

        

