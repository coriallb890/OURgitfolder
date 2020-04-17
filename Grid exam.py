import random   
import pygame

pygame.init()                                 #start up dat pygame
clock = pygame.time.Clock()                   #for framerate or something? still not very sure
screen = pygame.display.set_mode([704, 704])  #making the window
Done = False                                  #variable to keep track if window is open
MAPSIZE = 11                                #how many tiles in either direction of grid

TILEWIDTH = 63                                #pixel sizes for grid squares
TILEHEIGHT = 63
TILEMARGIN = 1

BLACK = (0, 0, 0)                             #some color definitions
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class MapTile(object):                       #The main class for stationary things that inhabit the grid ... grass, trees, rocks and stuff.
    def __init__(self, name, column, row):
        self.name = name
        self.column = column
        self.row = row


class Character(object):                    #Characters can move around and do cool stuff
    def __init__(self, name, column, row):
        self.name = name
        self.column = column
        self.row = row

    def move(self, direction):              #This function is how a character moves around in a certain direction
        
        if self.collision(direction):
            return
        if direction == "UP" and self.row > 0:       #If within boundaries of grid      
            self.row -= 1            #Go ahead and move

        elif direction == "LEFT" and self.column > 0:
            self.column -= 1

        elif direction == "RIGHT" and self.column < (MAPSIZE-1):
            self.column += 1

        elif direction == "DOWN" and self.row < (MAPSIZE-1):
            self.row += 1

        Map.update()       

    def collision(self, direction):       #Checks if anything is on top of the grass in the direction that the character wants to move. Used in the move function
        if direction == "UP":
            if len(Map.grid[self.column][(self.row)-1]) > 1:
                return True
        elif direction == "LEFT":
            if len(Map.grid[self.column-1][(self.row)]) > 1:
                return True
        elif direction == "RIGHT":
            if len(Map.grid[self.column+1][(self.row)]) > 1:
                return True
        elif direction == "DOWN":
            if len(Map.grid[self.column][(self.row)+1]) > 1:
                return True
        return False

    def location(self):
        print("Coordinates: " + str(self.column) + ", " + str(self.row))


class Map(object):              #The main class; where the action happens
    global MAPSIZE

    grid = []

    for row in range(MAPSIZE):     # Creating grid
        grid.append([])
        for column in range(MAPSIZE):
            grid[row].append([])

    for row in range(MAPSIZE):     #Filling grid with grass
        for column in range(MAPSIZE):
            tempTile = MapTile("Grass", column, row)
            grid[column][row].append(tempTile)

    for row in range(MAPSIZE):     #Adding walls
        for column in range(MAPSIZE):
            tempTile = MapTile("Wall", column, row)
            if row == 0 or row == (MAPSIZE - 1) or column == 0 or column == (MAPSIZE - 1):
                grid[column][row].append(tempTile)

    for i in range(5):          #Placing Random trees
        randRow = random.randint(1, MAPSIZE - 2)
        randColumn = random.randint(1, MAPSIZE - 2)
        tempTile = MapTile("Enemy", randColumn, randRow)
        grid[randColumn][randRow].append(tempTile)

    hero = Character("Hero", 5, MAPSIZE - 2)

    def update(self):        #Very important function
                             #This function goes through the entire grid
                             #And checks to see if any object's internal coordinates
                             #Disagree with its current position in the grid
                             #If they do, it removes the objects and places it 
                             #on the grid according to its internal coordinates 

        for column in range(MAPSIZE):      
            for row in range(MAPSIZE):
                for i in range(len(Map.grid[column][row])):
                    if Map.grid[column][row][i].column != column:
                        Map.grid[column][row].remove(Map.grid[column][row][i])
                    elif Map.grid[column][row][i].name == "Hero":
                        Map.grid[column][row].remove(Map.grid[column][row][i])
        Map.grid[int(Map.hero.column)][int(Map.hero.row)].append(Map.hero)

Map = Map()

while not Done:     #Main pygame loop

    for event in pygame.event.get():         #catching events
        if event.type == pygame.QUIT:
            Done = True       

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (TILEWIDTH + TILEMARGIN)  #Translating the position of the mouse into rows and columns
            row = pos[1] // (TILEHEIGHT + TILEMARGIN)
            print(str(row) + ", " + str(column))

            for i in range(len(Map.grid[column][row])):
                print(str(Map.grid[column][row][i].name))  #print stuff that inhabits that square

        elif event.type == pygame.KEYDOWN:
            KeyLookup = {
                pygame.K_LEFT: "LEFT",
                pygame.K_RIGHT: "RIGHT",
                pygame.K_DOWN: "DOWN",
                pygame.K_UP: "UP"
            }
            Map.hero.move(KeyLookup.get(event.key))
            
    screen.fill(BLACK)

    for row in range(MAPSIZE):           # Drawing grid
        for column in range(MAPSIZE):
            for i in range(0, len(Map.grid[column][row])):
                color = WHITE
                if Map.grid[column][row][i].name == "Enemy":
                    color = BLUE
                if Map.grid[column][row][i].name == "Wall":
                    color = RED
                if Map.grid[column][row][i].name == "Hero":
                    color = GREEN


            pygame.draw.rect(screen, color, [(TILEWIDTH + TILEMARGIN) * column + TILEMARGIN,
                                            (TILEHEIGHT + TILEMARGIN) * row + TILEMARGIN,
                                             TILEWIDTH,
                                             TILEHEIGHT])

    clock.tick(60)      #Limit to 60 fps or something

    pygame.display.flip()     #Honestly not sure what this does, but it breaks if I remove it
    Map.update()

pygame.quit()
