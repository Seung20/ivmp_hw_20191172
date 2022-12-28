import pygame
import numpy as np 
import os
import sys
from pygame.locals import *

# 게임 윈도우 크기
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 1000




# 색 정의
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)


# Pygame 초기화
pygame.init()

# 윈도우 제목
pygame.display.set_caption("TicTacToe")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

#Box sizes and gap
gap = 15
size = 280

pos_x = [(gap), (gap*2 + size), (gap*3 + size*2), (gap), (gap*2 + size), (gap*3 + size*2), (gap), (gap*2 + size), (gap*3 + size*2)]
pos_y = [(gap*3 + size*2), (gap*3 + size*2), (gap*3 + size*2), (gap*2 + size),(gap*2 + size),(gap*2 + size),(gap) ,(gap), (gap)]


# 9개의 버튼을 만들고, board[1]~board[9]까지 저장
# board[7] board[8] board[9]
# board[4] board[5] board[6]
# board[1] board[2] board[3]

losboard = "YOULOSE^^!".split()

def drawBoard(board):
    for i in range(0, 9):
        pygame.draw.rect(screen,GREY,[pos_x[i], pos_y[i], size, size])
    for t in range(1, 10):
        ttext = c_font.render(board[t], True, BLACK)
        screen.blit(ttext,(pos_x[t-1]+20, pos_y[t-1]-10))


# player는 o로 고정, player는 x로 고정
def inputPlayerLetter():
    return ['O', 'X']


# 선공 정하기
def whoGoesFirst():
    # Randomly choose the player who goes first.
    if np.random.randint(0, 2) == 0:
        return 'computer'
    else:
        return 'player'



def makeMove(board, letter, move):
    board[move] = letter

def isWinner(bo, le):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don't have to type as much.
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
    (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
    (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
    (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
    (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
    (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
    (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
    (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal



def getBoardCopy(board):
    # Make a copy of the board list and return it.
    boardCopy = []
    for i in board:
        boardCopy.append(i)
    return boardCopy


def isSpaceFree(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] == ' '

def chooseRandomMoveFromList(board, movesList):
    # Returns a valid move from the passed list on the passed board.
    # Returns None if there is no valid move.

    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return np.random.choice(possibleMoves)
    else:
        return None


def getComputerMove(board, computerLetter):
    # Given a board and the computer's letter, determine where to move and return that move.

    playerLetter = 'O'
    computerLetter = 'X'
   
    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for i in range(1, 10):
        boardCopy = getBoardCopy(board)
        if isSpaceFree(boardCopy, i):
            makeMove(boardCopy, computerLetter, i)
            if isWinner(boardCopy, computerLetter):
                return i

    # Check if the player could win on his next move, and block them.
    for i in range(1, 10):
        boardCopy = getBoardCopy(board)
        if isSpaceFree(boardCopy, i):
            makeMove(boardCopy, playerLetter, i)
            if isWinner(boardCopy, playerLetter):
                return i

    # Try to take one of the corners, if they are free.
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    # Try to take the center, if it is free.
    if isSpaceFree(board, 5):
        return 5

    # Move on one of the sides.
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True
    
#폰트
a_font = pygame.font.SysFont('onyx', 50)
b_font = pygame.font.SysFont('onyx', 40)
c_font = pygame.font.SysFont('onyx', 400)
starting_text = a_font.render("Tic Tac Toe", True, BLACK)


# # 게임 종료 전까지 반복
done = False
theBoard = [' '] * 10
playerLetter, computerLetter = inputPlayerLetter()
turn = whoGoesFirst()

showingturntext = b_font.render("The " + turn +" will go first", True, BLACK)

# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == MOUSEBUTTONUP: #마우스 버튼이 눌러지고 떠질 때
            mpos = pygame.mouse.get_pos()
            if turn == 'player':
                # Player's turn.
                drawBoard(theBoard)
                # move = getPlayerMove(theBoard)
                move = ' '
   
                for i in range(9):
                    if (pos_x[i] <= mpos[0] <= pos_x[i] + size) and (pos_y[i] <=mpos[1] <= pos_y[i] + size):       
                        move = i+1 
                
                
                makeMove(theBoard, playerLetter, move)

                if isWinner(theBoard, playerLetter):
                    drawBoard(theBoard)
                    done = True
                    pygame.time.delay(2000)

                    
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        done = True
                        pygame.time.delay(2000)
                        break
                    else:
                        turn = 'computer'


            else:
                # Computer's turn.
                move = getComputerMove(theBoard, computerLetter)
                makeMove(theBoard, computerLetter, move)

                if isWinner(theBoard, computerLetter):
                    done = True
                    pygame.time.delay(2000)
                    
                        
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        done = True
                        pygame.time.delay(2000)
                        break
                    else:
                        turn = 'player'
            
    screen.fill(WHITE)
    drawBoard(theBoard)
    screen.blit(starting_text, (WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 + 400))
    screen.blit(showingturntext, (WINDOW_WIDTH/2 - 200, WINDOW_HEIGHT/2 + 450))
    
    # 화면 업데이트
    pygame.display.flip()
    
    clock.tick(60) 

# 게임 종료
pygame.quit()