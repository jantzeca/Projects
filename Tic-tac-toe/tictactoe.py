from tkinter import *
from tkinter.colorchooser import *
from collections import defaultdict
import functools
import numpy as np

board = np.zeros((3, 3), dtype='int')
color1 = 'red'
color2 = 'gray'
player = 1
gameover = False
tiegame = False

def tie():
    global board
    for row in range(3):
        for col in range(3):
            if board[row, col] == 0:
                return False
    return True

def checkWin(player):
    global board
    win = False
    if(board[0, 0] != 0 and (board[0, 0] == board[0, 1] and board[0, 0] == board[0, 2])):
        win = True
    elif(board[1, 0] != 0 and (board[1, 0] == board[1, 1] and board[1, 0] == board[1, 2])):
        win = True
    elif(board[2, 0] != 0 and (board[2, 0] == board[2, 1] and board[2, 0] == board[2, 2])):
        win = True
    elif(board[0, 0] != 0 and (board[0, 0] == board[1, 0] and board[0, 0] == board[2, 0])):
        win = True
    elif(board[0, 1] != 0 and (board[0, 1] == board[1, 1] and board[0, 1] == board[2, 1])):
        win = True
    elif(board[0, 2] != 0 and (board[0, 2] == board[1, 2] and board[0, 2] == board[2, 2])):
        win = True
    elif(board[0, 0] != 0 and (board[0, 0] == board[1, 1] and board[0, 0] == board[2, 2])):
        win = True
    elif(board[0, 2] != 0 and (board[0, 2] == board[1, 1] and board[0, 2] == board[2, 0])):
        win = True
    return win

def resetboard():
    global board, gameover, tiegame, player
    gameover = False
    tiegame = False
    player = 1
    for row in range(3):
        for col in range(3):
            square[row][col].create_rectangle(0, 0, 200, 200, fill='black')
    board = np.zeros((3, 3), dtype='int')
    chatter.config(text='Player ' + str(1) + '\'s turn')

def redraw_board():
    global board
    for row in range(3):
        for col in range(3):
            if board[row, col] in (1, 2):
                piece(row, col, board[row, col])

def key(event):
    global board, player, root, color1, color2, gameover, tiegame
    if event.char == 'l':
        resetboard()
        print('loading game ...')
        board = np.fromfile('/google/tinker/Tic-tac-toe/tictactoe_board.txt', \
                                sep=',', dtype='int').reshape(3, 3)
        redraw_board()
        with open('/google/tinker/Tic-tac-toe/tictactoe_player.txt', 'r') as f:
            player = int(f.readline())
            print('Player is ', player)
            '''pick1 = eval(f.readline())
            print('pick1 is ', str(pick1))'''
    elif event.char == 's':
        print('saving game ....')
        with open('/google/tinker/Tic-tac-toe/tictactoe_player.txt', 'w') as f:
            f.write(str(player) + '\n')
            #f.write(str(pick1) + '\n')
        board.tofile('/google/tinker/Tic-tac-toe/tictactoe_board.txt', sep=',')
        with open('/google/tinker/Tic-tac-toe/tictactoe_map.txt', 'w') as f:
            f.write(np.array_str(board))
    elif event.char == 'x':
        root.quit()
    elif event.char == '1':
        color1 = askcolor()[1]
        redraw_board()
    elif event.char == '2':
        color2 = askcolor()[1]
        redraw_board()
    elif event.char == 'r':
        resetboard()
        # print('reset')


def piece(row, col, player, reset=False):
    global color1, color2
    if player == 1:
        color = color1
    elif player == 2:
        color = color2
    else:
        color = 'black'
    if player == 1 and reset:
        square[row][col].create_line(10, 10, 190, 190, fill=color, width=20)
        square[row][col].create_line(10, 190, 190, 10, fill=color, width=20)
    elif player == 2 and reset:
        square[row][col].create_oval(10, 10, 190, 190, fill=color)
        square[row][col].create_oval(40, 40, 160, 160, fill='black')
    elif player == 1:
        square[row][col].create_line(10, 10, 190, 190, fill=color, width=20)
        square[row][col].create_line(10, 190, 190, 10, fill=color, width=20)
    elif player == 2:
        square[row][col].create_oval(10, 10, 190, 190, fill=color)
        square[row][col].create_oval(40, 40, 160, 160, fill='black')


#player 1 is x, player 2 is o
def picksquare(row, col, event):
    global board, player, pick, gameover, tiegame
    if gameover or tiegame:
        return
    if board[row, col] == 0:
        board[row, col] = player
        piece(row, col, player)
        if checkWin(player):
            gameover = True
            chatter.config(text='Player ' + str(player) + ' Wins!')
        if not gameover and tie():
            tiegame = True
            chatter.config(text='It\'s a tie.')
            return
        if player == 1 and not gameover:
            player = 2
            chatter.config(text='Player '+ str(player) + '\'s turn.')
        elif player == 2 and not gameover:
            player = 1
            chatter.config(text='Player ' + str(player) + '\'s turn.')
    else:
        return

root = Tk()
root.geometry('620x650')
root.bind("<Key>", key)

square = defaultdict(list)
frame = Frame(root)
frame2 = Frame(frame)
frame2.grid()

for row in range(3):
    for col in range(3):
        square[row].append(Canvas(frame2, height=200, width=200, bg='black'))
        square[row][col].grid(row=row, column=col)
        square[row][col].bind('<Button-1>', functools.partial(picksquare, row, col))
frame2.pack(fill=X)

chatter = Label(frame, text='Chatter ...')
chatter.pack(fill=X)
frame.pack(fill=X)

chatter.config(text='Player ' + str(player) + '\'s turn.')
mainloop()
