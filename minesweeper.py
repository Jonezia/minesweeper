import pygame
import time
import tkinter as tk
import random
from tkinter import messagebox
from itertools import product
import os
import sys
pygame.init()

mainfont = pygame.font.SysFont('Roboto',18)
timefont = pygame.font.SysFont('Roboto',20)

class Grid:    
    def __init__(self, rows, cols, win, edge, mines, mineMatrix, adjacencies):
        self.rows = rows
        self.cols = cols
        self.edge = edge
        self.squares = [[Square(i,j,edge,mineMatrix[i][j],adjacencies[i][j]) for j in range(cols)] for i in range(rows)]
        self.width = edge*cols
        self.height = edge*rows
        self.win = win
        self.flags = mines
        self.running = True
        
    def draw(self):
        for i in range(self.rows+1):
            pygame.draw.line(self.win, (0,0,0), (0, i*self.edge), (self.width, i*self.edge))
        for i in range(self.cols+1):
            pygame.draw.line(self.win, (0,0,0), (i*self.edge, 0), (i*self.edge, self.height))
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].draw(self.win)
    
    def click(self,pos,button):
        if pos[0] < self.width and pos[1] < self.height:
            x = int(pos[0] // self.edge)
            y = int(pos[1] // self.edge)
            if button == 1:
                self.squares[y][x].reveal()
            if button == 3:
                if self.squares[y][x].marked == False:
                    self.squares[y][x].marked = True
                    self.flags -= 1
                else:
                    self.squares[y][x].marked = False
                    self.flags += 1
                
class Square:
    def __init__(self, row, col, edge, mine, adjacents):
        self.adjacents = adjacents
        self.mine = mine
        self.marked = False
        self.revealed = False
        self.row = row
        self.col = col
        self.edge = edge
        
    def reveal(self):
        if not self.marked:
            if self.mine == 1:
                #Lose game
                pass
            self.revealed = True
        
    def draw(self,win):
        x = self.col*self.edge
        y = self.row*self.edge
        if self.revealed or self.marked:
            if self.revealed:
                if self.mine:
                    text = mainfont.render("B",1,(255,0,0))
                else:
                    text = mainfont.render(str(self.adjacents),1,(0,0,0))
            elif self.marked:
                text = mainfont.render("M",1,(0,0,0))
            win.blit(text, (x + (self.edge/2 - text.get_width()/2), y + (self.edge/2 - text.get_height()/2)))
            
class Generator:
    def __init__(self,rows,cols,mines):
        self.rows = rows
        self. cols = cols
        self.mineMatrix = [[0 for _ in range(cols)] for _ in range(rows)]
        for _ in range(mines):
            x = random.randint(0,self.rows-1)
            y = random.randint(0,self.cols-1)
            while self.mineMatrix[x][y] == 1:
                x = random.randint(0,self.rows-1)
                y = random.randint(0,self.cols-1)
            self.mineMatrix[x][y] = 1
        self.adjacencies()
        
    def adjacencies(self):
        self.adjacencies = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                adjacency = 0
                if self.mineMatrix[i][j] == 0:
                    for c in product(*(range(n-1, n+2) for n in (i,j))):
                        if c != (i,j) and 0 <= c[0] < self.rows and \
                        0 <= c[1] < self.cols and self.mineMatrix[c[0]][c[1]] == 1:
                            adjacency += 1
                self.adjacencies[i][j] = adjacency
        
def redraw_window(win, board, time, flags, edge):
    win.fill((255,255,255))
    time = timefont.render("Time: " + time, 1, (0,0,0))
    win.blit(time, (edge*board.cols - 95, edge*board.rows+12))
    flags = timefont.render("Flags: " + str(flags), 1, (0,0,0))
    win.blit(flags, (25, edge*board.rows+12))
    board.draw()

def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    if sec < 10:
        strsec = "0" + str(sec)
    else:
        strsec = str(sec)
    mat = " " + str(minute) + ":" + strsec
    return mat
        
def newGame(difficulty):
    edge = 30
    
    difficulties = {"easy":(9,9,10),"medium":(16,16,40),"hard":(30,16,99)}
    cols,rows,mines = difficulties[difficulty][0],difficulties[difficulty][1],difficulties[difficulty][2]
    
    generator = Generator(rows,cols,mines)
    
    win = pygame.display.set_mode((edge*cols,edge*rows+40))
    pygame.display.set_caption("Minesweeper")
    board = Grid(rows,cols,win,edge,mines,generator.mineMatrix,generator.adjacencies)
    start = time.time()
    
    while board.running:
        play_time = round(time.time()-start)
        formatted_time = format_time(play_time)
        
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                board.running = False
            if event.type is pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                board.click(pos,event.button)
                
        redraw_window(win,board,formatted_time,board.flags, edge)
        pygame.display.update()
        
mydifficulty = None

def setDifficulty(difficulty):
    global mydifficulty
    mydifficulty = difficulty
    window.quit()
    window.destroy()

window = tk.Tk()
window.title("Minesweeper Settings")
tk.Label(window, text="Choose Difficulty: ", pady = 10).pack()
    
tk.Button(window,text="easy",width=20,padx=20,command=lambda: setDifficulty("easy")).pack(fill="x")
tk.Button(window,text="medium",width=20,padx=20,command=lambda: setDifficulty("medium")).pack(fill="x")
tk.Button(window,text="hard",width=20,padx=20,command=lambda: setDifficulty("hard")).pack(fill="x")

window.mainloop()
newGame(mydifficulty)
pygame.quit()