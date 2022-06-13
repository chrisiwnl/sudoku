import numpy as np
import pygame as py
import math
import time as timee
import threading

global black,red,green,white,grey

black = [0,0,0]
white = [255,255,255]
red = [255,0,0]
green = [0,255,0]
grey = [145, 145, 145]

class Button:
    def __init__(self,screen,x,y,width,height,name,color):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.color = color

    def DrawButton(self):
        #Drawing the button outline
        py.draw.rect(self.screen,self.color,[self.x,self.y,self.width,self.height],1)
        #Writing the text
        font = py.font.SysFont('arial', 25)
        text = font.render(str(self.name), True, black)
        py.draw.rect(self.screen,white,[self.x+10,self.y+20,85,25],0)
        py.display.flip()
        self.screen.blit(text, [self.x+10,self.y+15])
        py.display.update()

    def Collided(self):
        x,y = py.mouse.get_pos()
        if x > self.x and x < self.x+self.width and y > self.y and y < self.y + self.height:
            print("{} pressed".format(self.name))
            return self.name

    def SetName(self,name):
        self.name = name

class Tile:
    def __init__(self,screen,x,y,value):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.pos_x = self.x*self.width
        self.pos_y = self.y*self.height
        self.color = black
        self.value = value
        self.screen = screen
        self.highlighted = False

        #If the number is part of the default board than the user cant change it
        if value != 0:
            self.unmovable = True
        else:
            self.unmovable = False
    #Creating the font and writting it to the board
    def DrawValue(self,x,y,value,screen):
        font = py.font.SysFont('arial', 50)
        #If the value is in the default board we paint it grey, if its user inputed than its black.
        if self.unmovable == True:
            text = font.render(str(value), True, grey)
        else:
            text = font.render(str(value), True, black)
        py.draw.rect(self.screen,white,[x,y,50,50],0)
        py.display.flip()
        screen.blit(text, [x,y-10])
        py.display.update()
    #Drawing the tiles
    def Draw(self):
        #Drawing the borders for the tiles
        py.draw.rect(self.screen,self.color,[self.pos_y,self.pos_x,self.width,self.height],1)
        #Writting the value if its not 0
        if self.value != 0:
            self.DrawValue(self.pos_y+35,self.pos_x+35,self.value,self.screen)
        py.display.flip()
    #Changing the color of the border if the tile is highlighted
    def Highlight(self):
        self.color = green
        self.Draw()
        
        self.highlighted = True
    #Switching the border color back if we click on another tile
    def UnHighlight(self):
        self.highlighted = False
        self.color = black
        self.Draw()
    #Debug
    def PrintINF(self):
        print("Tile adat: {},{},{} ".format(self.x,self.y,self.value))
    #Changing the value of the tile
    def SetValue(self,new_value):
        if self.unmovable == True:
            pass
        else:
            self.value = new_value

class Game:

    def __init__(self):
        print("Jatek letrehozva")
        
        self.default  = [[5,3,0,0,7,0,0,0,0],
                      [6,0,0,1,9,5,0,0,0],
                      [0,9,8,0,0,0,0,6,0],
                      [8,0,0,0,6,0,0,0,3],
                      [4,0,0,8,0,3,0,0,1],
                      [7,0,0,0,2,0,0,0,6],
                      [0,6,0,0,0,0,2,8,0],
                      [0,0,0,4,1,9,0,0,5],
                      [0,0,0,0,8,0,0,7,9]]

        self.grid  = [[5,3,0,0,7,0,0,0,0],
                      [6,0,0,1,9,5,0,0,0],
                      [0,9,8,0,0,0,0,6,0],
                      [8,0,0,0,6,0,0,0,3],
                      [4,0,0,8,0,3,0,0,1],
                      [7,0,0,0,2,0,0,0,6],
                      [0,6,0,0,0,0,2,8,0],
                      [0,0,0,4,1,9,0,0,5],
                      [0,0,0,0,8,0,0,7,9]]

        #Could've done it with list comprehensions grid = [[0 for i in range(9)]for j in range(9)]
        self.solvedgrid  = [[0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0]]

        self.customgrid  = [[0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0]]

        self.og_grid  = [[0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0]]

    def possible(self,x,y,n):
        #Checking the row
        if n in self.grid[x]:
            #print("Sor Hiba")
            return False
        #Checking the column
        for i in range(9):
            if self.grid[i][y] == n:
                #print("Oszlop hiba")
                return False

        #Checking the square
        xx = (x//3)*3
        yy = (y//3)*3

        for i in range(3):
            for j in range(3):
                if self.grid[xx+i][yy+j] == n:
                    #print("Kocka hiba")
                    return False

        #print("Sikeres")
        return True

    def solver(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    for k in range(1,10):
                        if self.possible(i,j,k):
                            self.grid[i][j] = k
                            self.solver()
                            self.grid[i][j] = 0
                    return
        if np.count_nonzero(self.grid) == 81:
            self.solvedgrid = np.copy(self.grid)
        return

    def AddValue(self,i,j,value):
        self.grid[i][j] = value

    def RemoveValue(self,i,j):
        self.grid[i][j] = 0

    def PrintSolvedGrid(self):
        print(np.matrix(self.solvedgrid))

    def PrintGrid(self):
        print(np.matrix(self.grid))

class Program:
    #alsó 100 egészhez váltja a számot
    def roundup(self,x):
        return int(math.ceil(x / 100.0)) * 100
    #Creating the window
    def InitDisplay(self,width,height):
        screen = py.display.set_mode((width,height))
        py.display.set_caption("Sudoku")
        screen.fill(white)
        py.display.flip()
        return screen
    def DrawBoard(self,Tilok,screen,table):
        #Drawing the main lines
        py.draw.line(screen,black,[3,0],[3,900],5)
        py.draw.line(screen,black,[300,0],[300,900],5)
        py.draw.line(screen,black,[600,0],[600,900],5)
        py.draw.line(screen,black,[900,0],[900,900],5)
        py.draw.line(screen,black,[0,3],[900,3],5)
        py.draw.line(screen,black,[0,300],[900,300],5)
        py.draw.line(screen,black,[0,600],[900,600],5)
        py.draw.line(screen,black,[0,897],[900,897],5)

        #Creating the tile list and filling it up
        for i in range(9):
            tmp = []
            for j in range(9):
                tile = Tile(self.main_window,i,j,table[i][j])
                tile.Draw()
                tmp.append(tile)
            Tilok.append(tmp)
    
    def main(self):
        game = Game()
        py.init()
        clock = py.time.Clock()
        width,height = 1100,900
        game_width,game_height = 900,900
        self.main_window = self.InitDisplay(width,height)
        game.og_grid = np.copy(game.grid)
        game.solver()
        default_button = Button(self.main_window,950,100,100,50,"default",black)
        restart_button = Button(self.main_window,950,250,100,50,"restart",black)
        solve_button = Button(self.main_window,950,400,100,50,"solve",black)
        custom_button = Button(self.main_window,950,550,100,50,"custom",black)
        exit_button = Button(self.main_window,950,700,100,50,"exit",black)
        Tilok = []
        Buttons = [default_button,restart_button,solve_button,custom_button,exit_button]
        for button in Buttons:
            button.DrawButton()
        self.DrawBoard(Tilok,self.main_window,game.grid)
        ingame = True
        while ingame :
            for event in py.event.get():
                if event.type ==  py.QUIT:
                    ingame = False
                    py.quit()
                if event.type == py.MOUSEBUTTONDOWN:
                    x,y = py.mouse.get_pos()
                    xx,yy = int(self.roundup(y)/100)-1,int(self.roundup(x)/100)-1
                    print(x,y)
                    print(yy,xx)
                    for lista in Tilok:
                        for tile in lista:
                            if tile.highlighted == True:
                                tile.UnHighlight()
                    for lista in Tilok:
                        for tile in lista:
                            if tile.x == xx and tile.y == yy:
                                tile.Highlight()
                                tile.PrintINF()
                    #Handeling the buttons
                    for button in Buttons:
                        if button.Collided() == "default":
                            Tilok = []
                            game.og_grid = np.copy(game.default)
                            game.grid = np.copy(game.default)
                            py.draw.rect(self.main_window,white,[0,0,900,900],0)
                            self.DrawBoard(Tilok,self.main_window,game.og_grid)
                        if button.Collided() == "solve":
                            thread = threading.Thread(target=game.solver())
                            thread.start()
                            Tilok = []
                            thread.join()
                            py.draw.rect(self.main_window,white,[0,0,900,900],0)
                            self.DrawBoard(Tilok,self.main_window,game.solvedgrid)

                        elif button.Collided() == "restart":
                            Tilok = []
                            py.draw.rect(self.main_window,white,[0,0,900,900],0)
                            self.DrawBoard(Tilok,self.main_window,game.og_grid)

                        elif button.Collided() == "custom":
                            #Updateing the name of the button
                            button.SetName("save")
                            button.DrawButton()
                            #Drawing a clear grid
                            Tilok = []
                            py.draw.rect(self.main_window,white,[0,0,900,900],0)
                            self.DrawBoard(Tilok,self.main_window,game.customgrid)
                            game.grid = np.copy(game.customgrid)

                        elif button.Collided() == "save":
                            #Reseting the button to custom
                            button.SetName("custom")
                            button.DrawButton()
                            #Drawing custom board
                            py.draw.rect(self.main_window,white,[0,0,900,900],0)
                            self.DrawBoard(Tilok,self.main_window,game.grid)
                            #Making our custom grid the game grid
                            game.og_grid = np.copy(game.grid)

                        elif button.Collided() == "exit":
                            ingame = False
                            py.quit()

                if event.type == py.KEYDOWN:
                    for lista in Tilok:
                        for tile in lista:
                            if tile.highlighted == True:
                                 #Making BACKSPACE to clear the value of the highlighted tile
                                if event.key == py.K_BACKSPACE:
                                    tile.value = 0
                                    py.draw.rect(self.main_window,white,[tile.pos_y+35,tile.pos_x+35,50,50],0)
                                    py.display.flip()
                                    game.RemoveValue(tile.x,tile.y)
                                elif 0 < int(py.key.name(event.key)) < 10:
                                    tile.SetValue(int(py.key.name(event.key)))
                                    tile.DrawValue(tile.pos_y+35,tile.pos_x+35,tile.value,tile.screen)
                                    game.AddValue(tile.x,tile.y,int(py.key.name(event.key)))
                                    print(np.matrix(game.grid))

                comparison = game.grid == game.solvedgrid
                if comparison.all() == True:
                    print("Helyes megoldas")
                    ingame = False
                    py.quit()
        clock.tick(30)

program = Program()
program.main()
