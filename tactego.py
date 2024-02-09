"""
File:    tactego.py
Author:  Tushar Passi
Date:    11/10/2023
Section: 56
E-mail:  mt40575@umbc.edu
Description:
  Simulates a simplified version of the Stratego game.

"""

X_VALUE = 1
Y_VALUE = 0
PIECE_STRENGTH_OR_FLAG = 0
NUM_PIECES = 1
STRENGTH_OF_PIECE = 1
FLAG = "F"
MINE = "M"
SAPPER = "S"
ASSASSIN = "A"

import random

def valid_piece(player, which_piece):
   """
   Checks if the piece selected is a valid piece
   :param player: the current player
   :param which_piece: the piece trying to be moved
   """
   if "F" in which_piece or "  " in which_piece or player not in which_piece:
      print("You must select a starting position with one of your pieces, not a flag.")
      return False
   else:
      return True


def who_won(player):
   """
   The function prints that the current player has won
   :param player: The current player
   """
   print(player + " has won the game")


def out_of_bounds(move_by, new_pos):
   """
   This function checks for "The position that you select 
   as the destination must be at most one place away up, 
   down, left, right, or diagonally from the original position."

   :param move_by: what we are moving
   :param new_pos: where we are trying to move to
   """
   x1 = int(move_by[X_VALUE])
   x2 = int(new_pos[X_VALUE])
   y1 = int(move_by[Y_VALUE])
   y2 = int(new_pos[Y_VALUE])

   # this code checks for if the player is moving more than 1 space in any direction
   # if it does, then there is an illegal move going on.

   if x1 == x2 or x1 - x2 == -1 or x1 - x2 == 1:
      if y1 - y2 == 1 or y1 - y2 == -1:
         return False
      
   if y1 == y2 or y1 - y2 == -1 or y1 - y2 == 1:
      if x1 - x2 == 1 or x1 - x2 == -1:
         return False

   if (x1 - x2 <= -1 and x1 - x2 >= 1) and (y1 - y2 >= -1 and y1 - y2 <= 1):
      return False
   
   print("That move was too far.")
   return True


def alternate_team(player):
   """
   This function alternates the player every turn
   :param player: the player who's going to be alternated
   """
   if player == "R":
      player = "B"
   else:
      player = "R"
   return player


def check_ending_pos(player, which_piece, board, new_pos_y, new_pos_x):
   """
   this function checks for the ending position is "okay." Meaning, if it is
   empty or has an enemy piece. If it doesn't, this function will prompt the user
   to select a new new_pos
   :param player: the current player
   :param which_piece: the piece trying to be moved
   :param board: the current board setup
   :param new_pos_y: the piece we want's y position
   :param new_pos_x: the piece we want's x position
   """
   the_new_pos = board[new_pos_y][new_pos_x]
   while player in the_new_pos and player in which_piece:
      print("You must selecting an ending position which is either empty or has an enemy piece.")
      new_pos = input("Select Position to move Piece >> ")
      new_pos = new_pos.split()
      the_new_pos = board[new_pos_y][new_pos_x]

   return the_new_pos


def turn(player, board, length, width):
   """
   Does the turn for the player and makes sure that turn is legal (in terms of what's being selected)
   :param player: the current player
   :param board: the current board setup
   :param length: length of the board
   :param width: width of the board
   
   """
   move_by = input("Select Piece to Move by Position >> ")
   move_by = move_by.split()

   move_by_x = int(move_by[X_VALUE])
   move_by_y = int(move_by[Y_VALUE])
 
   which_piece = board[move_by_y][move_by_x]
   is_valid = valid_piece(player, which_piece)
   if is_valid == False:
      return turn(player, board, length, width)

   new_pos = input("Select Position to move Piece >> ")
   new_pos = new_pos.split()

   new_pos_y = int(new_pos[Y_VALUE])
   new_pos_x = int(new_pos[X_VALUE])

   the_new_pos = check_ending_pos(player, which_piece, board, new_pos_y, new_pos_x)

   was_illegal = out_of_bounds(move_by, new_pos)
   if was_illegal == False:
      if len(board[move_by_y]) > 0:
         # if this is triggered, the current player wins
         # as long as the new position has a flag, the player's selection isn't a flag,
         # and that the flag being attacked is not the player's flag...
         if FLAG in the_new_pos and FLAG not in which_piece and player not in the_new_pos:
            return update_board(player, length, width, board, win=True)
         if MINE in which_piece:
            print("You can not select a mine.")
            return turn(player, board, length, width)
         # if neither piece is a flag
         if FLAG not in which_piece and FLAG not in the_new_pos:
            board[move_by_y][move_by_x] = "  "  # set the moved piece to an empty space
            # as long as the new piece is the enemy's piece
            if "  " not in the_new_pos and player not in the_new_pos:
               # if the piece we have is a sapper and the piece we're fighting is a sapper
               if the_new_pos[STRENGTH_OF_PIECE] == SAPPER or which_piece[STRENGTH_OF_PIECE] == SAPPER:
                  board[new_pos_y][new_pos_x] = "  "
                  board[new_pos_y][new_pos_x] = which_piece
               # otherwise if he piece is a Mine
               elif the_new_pos[STRENGTH_OF_PIECE] == MINE:
                  board[new_pos_y][new_pos_x] = "  "
                  board[move_by_y][move_by_x] = "  "
               # In order:
               # if the enemy is an assassin and we're not an assassin
               # if we're a sapper and the enemy is a mine
               # if we're a sapper and the enemy is a mine
               # if we're an assassin
               # if the strength of ours is greater than or equal to the enemy's strength
               elif (the_new_pos[STRENGTH_OF_PIECE] == ASSASSIN and which_piece[STRENGTH_OF_PIECE] != ASSASSIN) or \
                  (which_piece[STRENGTH_OF_PIECE] == SAPPER and the_new_pos[STRENGTH_OF_PIECE] == MINE) or \
                  which_piece[STRENGTH_OF_PIECE] == ASSASSIN or \
                  int(which_piece[STRENGTH_OF_PIECE:]) >= int(the_new_pos[STRENGTH_OF_PIECE:]):
                  board[new_pos_y][new_pos_x] = which_piece
            else:
               board[new_pos_y][new_pos_x] = which_piece
         else:
            print("You must selecting an ending position which is either empty or has an enemy piece.")
            return turn(player, board, length, width)
         player = alternate_team(player)
      else:
         print("Please select a correct coordinate")
         return turn(player, board, length, width)
   else:
      return turn(player, board, length, width)   
  
   return update_board(player, length, width, board, win=False)

def update_board(player, length, width, board, win):
   """
   A function which updates the board after a turn
   :param player: the current player
   :param length: length of board
   :param width: width of board
   :param win: if the player has won or not
   """

   # prints the top row of the board
   top_row(width)

   # prints the remaining rows
   initial_width = 0

   # works similar to board_initialise except
   # all we want to do is print each piece correctly
   for row in range(length):
      print("    ", end=str(row))
      print(" ", end="")
      if initial_width > width:
         initial_width = 0
      for piece in range(initial_width, width+initial_width):
         print(board[row][piece], end="   ")
      print("")


   if win == True:
      return who_won(player)
   else:
      return turn(player, board, length, width)

def top_row(width):
   """
   This function prints the top row of the board
   :param width: the width of the board
   """
   # prints the top row of board
   for i in range(width):
      # 0 is indented by 6 spaces in Prof Hamilton's version as well
      if i == 0:
         print(end="       ")
      print(str(i), end="    ")

   print("")
   

def board_initialise(length, width, red_pieces, blue_pieces):
   """
   Creates the initial board from user input
   :param length: length of the board
   :param width: width of the board
   :param red_pieces: a list of the shuffled pieces for red team
   :param blue_pieces: a list of the shuffled pieces for blue team
   """

   # for the TA checking this stuff, blame Sean if you find an error (jk jk, 
   # mans a G for helping me out)

   board = [] # board values are stored as 2D lists


   # for these for loops, a TA told me it was fine even when
   # I asked him about magic numbers

   # this for loop creates the initial empty board
   for i in range(length):
      row_list = []
      for j in range(width):
         row_list.append("  ")

      board.append(row_list)


   # this for loop creates the red team side
   width_counter = -1
   for i in range(int(length/2)):
      for j in range(width):
         width_counter += 1
         if width_counter < len(red_pieces):
               board[i][j] = "R" + str(red_pieces[width_counter])
         elif width_counter == width:
               board[i][j] = " "

   # this for loop creats the blue team side
   width_counter = -1
   for i in range(length - 1,int(length/2), -1):
      for j in range(width):
         width_counter += 1
         if width_counter < len(red_pieces):
               board[i][j] = "B" + str(blue_pieces[width_counter])           
         

   # prints the initial board
   top_row(width)
   for i in range(length):
      print("    " + str(i), end=" ")
      for j in range(width):
         print(board[i][j], end="   ")
      print()


   turn("R", board, length, width)


def tactego(pieces_file, length, width):
   red_pieces = []
   blue_pieces = []
   
   with open(pieces_file) as the_file:
      for line in the_file:
         pieces_split = line.split(" ") # e.g. ['5', '1\n']
         # gets rid of the unnecessary "\n" for the program
         if '\n' in pieces_split[NUM_PIECES]:
            pieces_split[NUM_PIECES] = pieces_split[1].replace('\n', '')
            
         # made into an integer because operations will be performed in other functions
         pieces_split[NUM_PIECES] = int(pieces_split[NUM_PIECES])

         # append the right amount of pieces to each list
         for i in range(pieces_split[NUM_PIECES]):
            red_pieces.append(pieces_split[PIECE_STRENGTH_OR_FLAG])
            blue_pieces.append(pieces_split[PIECE_STRENGTH_OR_FLAG])


   random.shuffle(red_pieces)
   random.shuffle(blue_pieces)
   
   board_initialise(length, width, red_pieces, blue_pieces)



if __name__ == '__main__':
  # changes layout of board
  random.seed(input('What is seed? '))
  file_name = input('What is the filename for the pieces? ')
  length = int(input('What is the length? '))
  width = int(input('What is the width? '))
  tactego(file_name, length, width)

