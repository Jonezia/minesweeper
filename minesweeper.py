import pygame
import time
import tkinter as tk
from tkinter import messagebox
import os
import sys
pygame.init()

mainfont = pygame.font.SysFont('Roboto',18)
timefont = pygame.font.SysFont('Roboto',20)

class Grid:    
    def __init__(self, rows, cols, win, edge):
        self.rows = rows
        self.cols = cols
        self.edge = edge
        self.squares = [[Square(i, j, edge) for j in range(cols)] for i in range(rows)]
        self.width = edge*cols
        self.height = edge*rows
        self.win = win
        self.remaining_mines = 0
        
    def draw(self):
        for i in range(self.rows+1):
            pygame.draw.line(self.win, (0,0,0), (0, i*self.edge), (self.width, i*self.edge))
        for i in range(self.cols+1):
            pygame.draw.line(self.win, (0,0,0), (i*self.edge, 0), (i*self.edge, self.height))
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].draw(self.win)
    
    def click(self,pos):
        if pos[0] < self.width and pos[1] < self.height:
            x = pos[0] // self.edge
            y = pos[1] // self.edge
            self.squares[int(y)][int(x)].lclick()
                
class Square:
    def __init__(self, row, col, edge):
        self.value = 5
        self.mine = False
        self.row = row
        self.col = col
        self.width = edge
        self.height = edge
        
    def lclick():
        pass
    
    def rclick():
        pass
        
    def draw(self,win):
        x = self.col*self.height
        y = self.row*self.height
        text = mainfont.render(str(self.value),1,(0,0,0))
        win.blit(text, (x + (self.height/2 - text.get_width()/2), y + (self.height/2 - text.get_height()/2)))
        
def redraw_window(win, board, time, remaining_mines, edge):
    win.fill((255,255,255))
    time = timefont.render("Time: " + time, 1, (0,0,0))
    win.blit(time, (edge*board.cols - 95, edge*board.rows+12))
    remaining_mines = timefont.render("Mines: " + str(remaining_mines), 1, (0,0,0))
    win.blit(remaining_mines, (25, edge*board.rows+12))
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
    
    win = pygame.display.set_mode((edge*cols,edge*rows+40))
    pygame.display.set_caption("Minesweeper")
    board = Grid(rows,cols,win,edge)
    running = True
    start = time.time()
    
    while running:
        play_time = round(time.time()-start)
        formatted_time = format_time(play_time)
        
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                running = False
            if event.type is pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                board.click(pos)
                
        redraw_window(win,board,formatted_time,board.remaining_mines, edge)
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