from cmath import inf
import pygame
import pygamepopup
import random
import numpy as np

mainClock = pygame.time.Clock()
from pygame.locals import *
import tkinter as tk
from tkinter import messagebox
  
pygame.init()
pygamepopup.init()

#define game mode
MODE_3X3 = "_m33_"
MODE_5X5 = "_m55_"
MODE_7X7 = "_m77_"
  
# Define window properties
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
pygame.display.set_caption('Caro')

# Game code
WIN = '_wn_'
LOSE = '_ls_'
DRAW = '_drw_'
NORESULT = '_nr_'
PLAYER = 1
BOT = 2
 
class BUTTON:
    def __init__(self, image, position):
        self.prcImg = image
        self.prcRect = image.get_rect(topleft=position)
    def draw(self):
        display_surface.blit(self.prcImg, self.prcRect)

class MAIN_MENU:
    def __init__(self):
        # put image to display surface at (0, 0)
        display_surface.blit(mainFrame_img, (0, 0))

        # Create button
        self.playgameButton = BUTTON(playgameButton_img, (180, 340))
        # Display button
        self.playgameButton.draw()
        pygame.display.update()
        
    def running(self):
        while True:
            click = False
            mx, my = pygame.mouse.get_pos()

            # event checking loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    # deactivates the pygame library
                    pygame.quit()
                    # End program
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
    
            if self.playgameButton.prcRect.collidepoint((mx, my)):
                if click:
                    nextPage = MODE()
                    nextPage.running()

            pygame.display.update()
            mainClock.tick(60)
 
class MODE:
    def __init__(self):
        # put image to display surface at (0, 0)
        display_surface.blit(modeFrame_img, (0, 0))

        # Create button
        self.modeButton33 = BUTTON(modeButton33_img, (180, 200))
        self.modeButton55 = BUTTON(modeButton55_img, (180, 300))
        self.modeButton77 = BUTTON(modeButton77_img, (180, 400))
        # Display button
        self.modeButton33.draw()
        self.modeButton55.draw()
        self.modeButton77.draw()
        pygame.display.update()

    def running(self):
        modeRunning = True
        while modeRunning:
            click = False
            mx, my = pygame.mouse.get_pos()
            # event checking loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    # deactivates the pygame library
                    pygame.quit()
                    # End program
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            if self.modeButton33.prcRect.collidepoint((mx, my)):
                if click:
                    modeRunning = False
                    selectPiece = SELECT_MODE().running()
                    nextPage = GAME(MODE_3X3, selectPiece)
                    nextPage.running()
            elif self.modeButton55.prcRect.collidepoint((mx, my)):
                if click:
                    modeRunning = False
                    selectPiece = SELECT_MODE().running()
                    nextPage = GAME(MODE_5X5, selectPiece)
                    nextPage.running()
            elif self.modeButton77.prcRect.collidepoint((mx, my)):
                if click:
                    modeRunning = False
                    selectPiece = SELECT_MODE().running()
                    nextPage = GAME(MODE_7X7, selectPiece)
                    nextPage.running()
            
            pygame.display.update()
            mainClock.tick(60)

class SELECT_MODE:
    def __init__(self):
        # put image to display surface at (0, 0)
        display_surface.blit(selectFrame_img, (0, 0))

        # Create button
        self.xSlcBtn = BUTTON(xPiece_img, (50, 300))
        self.oSlcBtn = BUTTON(oPiece_img, (350, 300))
        # Display button
        self.xSlcBtn.draw()
        self.oSlcBtn.draw()
        pygame.display.update()

    def running(self):
        while True:
            click = False
            mx, my = pygame.mouse.get_pos()
            # event checking loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    # deactivates the pygame library
                    pygame.quit()
                    # End program
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            if self.xSlcBtn.prcRect.collidepoint((mx, my)):
                if click:
                    return 'x'
            elif self.oSlcBtn.prcRect.collidepoint((mx, my)):
                if click:
                    return 'o'
            
            pygame.display.update()
            mainClock.tick(60)

class GAME: #option: 33 or 55 or 77
    def __init__(self, option, piece):
        #Game properties
        self.chessPieceCount_g = 0
        self.squarePerRow_g = 0
        self.squareList_g = []
        self.clientPiece = piece
        self.botPiece = 'o' if piece == 'x' else 'x'
        self.isEnd = False

        if option == MODE_3X3:
            self.squarePerRow_g = 3
            self.criWin = 4
            self.depth = float(inf)
            display_surface.blit(gameBackground33_img, (0, 0))
        elif option == MODE_5X5:
            self.squarePerRow_g = 5
            self.criWin = 5
            self.depth = 5
            display_surface.blit(gameBackground55_img, (0, 0))
        elif option == MODE_7X7:
            self.squarePerRow_g = 7
            self.criWin = 6
            self.depth = 5
            display_surface.blit(gameBackground77_img, (0, 0))
        pygame.display.update()

        self.squareSize = WINDOW_WIDTH / self.squarePerRow_g
        self.xPiece_img_resized = pygame.transform.scale(xPiece_img, (self.squareSize, self.squareSize))
        self.oPiece_img_resized = pygame.transform.scale(oPiece_img, (self.squareSize, self.squareSize))

        self.board = np.zeros((self.squarePerRow_g, self.squarePerRow_g))

        for rows in range(self.squarePerRow_g):
            for cols in range(self.squarePerRow_g):
                #[left - top - width - height]
                s = pygame.Rect(self.squareSize * cols, self.squareSize * rows, self.squareSize, self.squareSize)
                self.squareList_g.append((rows, cols, s))

        #END of setting game properties
        #---------------------------------------------
        #Game running
        self.running()

    def running(self):
        click = False
        gameRunning = True
        if self.botPiece == 'x':
            self.botTurn()
        while gameRunning:
            mx, my = pygame.mouse.get_pos()
            # event checking loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    # deactivates the pygame library
                    pygame.quit()
                    # End program
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            if click:
                for square in self.squareList_g:
                    if square[2].collidepoint((mx, my)):
                        if self.board[square[0]][square[1]] == 0:
                            self.add_a_chess(self.clientPiece, square, PLAYER)
                            if self.isEnd == False:
                                self.botTurn()
                click = False

            mainClock.tick(60)
    def add_a_chess(self, type, square, who):
        #Mask the square has been tick on the board
        self.board[square[0]][square[1]] = 1 if type == self.clientPiece else 2
        #Display piece on the board
        if type == 'x':
            display_surface.blit(self.xPiece_img_resized, (square[2][0], square[2][1]))
        elif type == 'o':
            display_surface.blit(self.oPiece_img_resized, (square[2][0], square[2][1]))
            
        pygame.display.update()
        result = self.checkWin(self.board, square[0], square[1], who)

        if result != NORESULT:
            self.isEnd = True
            if result == DRAW:
                tk.messagebox.showinfo(title='RESULT', message='DRAW')
            elif result == WIN:
                tk.messagebox.showinfo(title='RESULT', 
                message="YOU WIN") if who == PLAYER else tk.messagebox.showinfo(title='RESULT', 
                                                                message="BOT WIN")
            choose = tk.messagebox.askyesno(title="Info", message="Do you want to play a new game?")
            if choose:
                self.isEnd = False
                newGame = MAIN_MENU()
                newGame.running()
            else:
                # deactivates the pygame library
                pygame.quit()
                # End program
                quit()
    #MAIN ALGORITHM
    def botTurn(self):
        x, y = self.AlphaBetaSearch()
        square = [x, y, pygame.Rect(
                        self.squareSize * y, 
                        self.squareSize * x,
                        self.squareSize, 
                        self.squareSize 
                    )]
        self.add_a_chess(self.botPiece, square, BOT)

    def AlphaBetaSearch(self):
        a = float(-inf) # Alpha
        b = float(inf) # Beta
        curDepth = 0

        maxVar, x, y = self.maxValue(self.board, None, None, a, b, curDepth)
        if x == None or y == None:
            print("Error: x = None or y = None")

        return (x, y)

    def maxValue(self, curState, x, y, a, b, curDepth):
        if x != None:
            result = self.checkWin(curState, x, y, PLAYER)
            if result == WIN:
                return (-10, x, y)
            elif result == DRAW:
                return (0, x, y)
            elif curDepth == self.depth:
                return (0, x, y)
        var = float(-inf)
        rx, ry = None, None

        for ir, row in enumerate(curState):
            for ic, col in enumerate(row):
                if(curState[ir][ic] == 0):
                    curState[ir][ic] = 2
                    curDepth += 1
                    maxVar, maxx, maxy = self.minValue(curState, ir, ic, a, b, curDepth)
                    curState[ir][ic] = 0
                    curDepth -= 1

                    if maxVar > var:
                        var = maxVar
                        rx, ry = ir, ic
                    if var >= b:
                        return (var, rx, ry)
                    a = max(var, a)
          
        return (var, rx, ry)

    def minValue(self, curState, x, y, a, b, curDepth):
        result = self.checkWin(curState, x, y, BOT)
        if result == WIN:
            self.foundedPath = True
            return (10, x, y)
        elif result == DRAW:
            return (0, x, y)
        elif curDepth == self.depth:
            return (0, x, y)

        var = float(inf)
        rx, ry = None, None

        for ir, row in enumerate(curState):
            for ic, col in enumerate(row):
                if(curState[ir][ic] == 0):
                    curState[ir][ic] = 1
                    curDepth += 1
                    minVar, maxx, maxy = self.maxValue(curState, ir, ic, a, b, curDepth)
                    curState[ir][ic] = 0
                    curDepth -= 1

                    if minVar < var:
                        var = minVar
                        rx, ry = ir, ic
                    if var <= a:
                        return (var, rx, ry)
                    b = min(var, b)

        return (var, rx, ry)


    #Check win - draw - lose
    def checkWin(self, checkBoard, x, y, who):
        # Check collumn
        count = 0
        i, j = x, y
        while(i < self.squarePerRow_g and checkBoard[i][j] == who):
            count += 1
            i += 1
        i = x
        while(i >= 0 and checkBoard[i][j] == who):
            count += 1
            i -= 1
        if count >= self.criWin:
            return WIN

        # Check row
        count = 0
        i, j = x, y
        while(j < self.squarePerRow_g and checkBoard[i][j] == who):
            count += 1
            j += 1
        j = y
        while(j >= 0 and checkBoard[i][j] == who):
            count += 1
            j -= 1
        if count >= self.criWin:
            return WIN
        # check cheo phai
        count = 0
        i, j = x, y
        while(i >= 0 and j < self.squarePerRow_g and checkBoard[i][j] == who):
            count += 1
            i -= 1
            j += 1

        i, j = x, y
        while(i < self.squarePerRow_g and j >= 0 and checkBoard[i][j] == who):
            count += 1
            i += 1
            j -= 1
        if count >= self.criWin:
            return WIN
        # check cheo trai
        count = 0
        i, j = x, y
        while(i < self.squarePerRow_g and j < self.squarePerRow_g and checkBoard[i][j] == who):
            count += 1
            i += 1
            j += 1
        i, j = x, y
        while(i >= 0 and j >= 0 and checkBoard[i][j] == who):
            count += 1
            i -= 1
            j -= 1
        if count >= self.criWin:
            return WIN

        #check draw
        if np.count_nonzero(checkBoard) == self.squarePerRow_g * self.squarePerRow_g:
            return DRAW
        
        return NORESULT
 
if __name__ == '__main__':
    # create the display surface object
    # of specific dimension..e(X, Y).
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # Load image.
    mainFrame_img = pygame.image.load('mainFrame.png')
    modeFrame_img = pygame.image.load('modeFrame.png')
    selectFrame_img = pygame.image.load('selectFrame.png')
    playgameButton_img = pygame.image.load('playgameButton.png')
    modeButton33_img = pygame.image.load('3x3button.png')
    modeButton55_img = pygame.image.load('5x5button.png')
    modeButton77_img = pygame.image.load('7x7button.png')
    gameBackground33_img = pygame.image.load('3x3caro.png')
    gameBackground55_img = pygame.image.load('5x5caro.png')
    gameBackground77_img = pygame.image.load('7x7caro.png')
    xPiece_img = pygame.image.load('x.png')
    oPiece_img = pygame.image.load('o.png')

    #Run
    game = MAIN_MENU()
    game.running()
