import random   
import pygame

pygame.init()                                 #start up dat pygame
clock = pygame.time.Clock()                   #for framerate or something? still not very sure
screen = pygame.display.set_mode([716, 716])  #making the window
Done = False                                  #variable to keep track if window is open
MAPSIZE = 11                                #how many tiles in either direction of grid

TILEWIDTH = 64                                #pixel sizes for grid squares
TILEHEIGHT = 64
TILEMARGIN = 1

BLACK = (0, 0, 0)           # fill
WHITE = (255, 255, 255)     # floor
GREEN = (0, 255, 0)         # player
RED = (255, 0, 0)           # wall
BLUE = (0, 0, 255)          # hill giants
GBLUE = (0, 255, 170)       # gnolls
RUST = (210, 150, 75)       # flind
MAGENTA = (225, 0, 230)     # mini boss 1
ORANGE = (155, 155, 0)      # mini boss 2
BROWN = (100, 40, 0)        # merchant
PINK = (225, 100, 180)      # healer
TAN = (230, 220, 170)       # mage
GRAY = (127, 127, 127)      # fighter
PURPLE = (240, 0, 255)      # rouge
LIME = (180, 255, 170)      # boss
WOOD = (20, 190, 140)       # door

class Floor(object):
    def __init__(self, name, enemyCount):
        self.name = name
        self.enemyCount = enemyCount

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def enemyCount(self):
        return self._enemyCount
    @enemyCount.setter
    def enemyCount(self, value):
        self._enemyCount = value


class FightFloor(Floor):
    def __init__(self, name, enemyCount, hillCount, gnollCount, flindCount):
        Floor.__init__(self, name, enemyCount)
        self.hillCount = hillCount
        self.gnollCount = gnollCount
        self.flindCount = flindCount
    
    @property
    def hillCount(self):
        return self._hillCount
    @hillCount.setter
    def hillCount(self, value):
        self._hillCount = value

    @property
    def gnollCount(self):
        return self._gnollCount
    @gnollCount.setter
    def gnollCount(self, value):
        self._gnollCount = value

    @property
    def flindCount(self):
        return self._flindCount
    @flindCount.setter
    def flindCount(self, value):
        self._flindCount = value
    
class MiniFloor(Floor):
    def __init__(self, name, enemyCount, mini, partyMem):
        Floor.__init__(self, name, enemyCount)
        self.mini = mini
        self.party = partyMem
        
class SpecialFloor(Floor):
    def __init__(self, name, enemyCount, boss, merchant):
        Floor.__init__(self, name, enemyCount)
        self.boss = boss
        self.merchant = merchant

    @property
    def boss(self):
        return self._boss
    @boss.setter
    def boss(self, value):
        self._boss = value

    @property
    def merchant(self):
        return self._merchant
    merchant.setter
    def merchant(self, value):
        self._merchant = value
                
class Special(object):                       #The main class for stationary things that inhabit the grid ... grass, trees, rocks and stuff.
    def __init__(self, name, column, row):
        self.name = name
        self.column = column
        self.row = row


class Player(Special):                      #The player 
    def __init__(self, name, column, row, party):
        Special.__init__(self, name, column, row)
        self.party = party

    @property
    def party(self):
        return self._party
    
    @party.setter
    def party(self, value):
        if (value == 1 or value == 2):
            party = value
        

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

    f1 = SpecialFloor("Floor 1", 0, 0, 1)
    f2 = FightFloor("Floor 2", 3, 3, 0, 0)
    f3 = FightFloor("Floor 3", 5, 5, 0, 0)
    f4 = FightFloor("Floor 3", 5, 3, 2, 0)
    f5 = MiniFloor("Mini Boss Floor 1", 1, 1, 2)
    f6 = FightFloor("Floor 3", 5, 2, 3, 0)
    f7 = FightFloor("Floor 3", 5, 0, 5, 0)
    f8 = FightFloor("Floor 3", 5, 0, 3, 2)
    f9 = MiniFloor("Mini Boss Floor 2", 1, 1, 2)
    f10 = FightFloor("Floor 3", 5, 0, 2, 3)
    f11 = FightFloor("Floor 3", 5, 0, 0, 5)
    f12 = FightFloor("Floor 3", 5, 0, 0, 7)
    f13 = SpecialFloor("Floor 1", 0, 0, 1)

    currentRoom = f5
    
    global MAPSIZE
    grid = []

    hero = Player("Hero", 5, MAPSIZE - 2, 0)
            
    for row in range(MAPSIZE):                  # Creating grid
        grid.append([])
        for column in range(MAPSIZE):
            grid[row].append([])

    for row in range(MAPSIZE):                  #Filling grid with the ground
        for column in range(MAPSIZE):
             tempTile = Special("Ground", column, row)
             grid[column][row].append(tempTile)

    for row in range(MAPSIZE):                  #Adding walls
        for column in range(MAPSIZE):
             tempTile = Special("Wall", column, row)
             if row == 0 or row == (MAPSIZE - 1) or column == 0 or column == (MAPSIZE - 1):
                 grid[column][row].append(tempTile)
                 
    if currentRoom == f2 or currentRoom == f3 or currentRoom == f4 or currentRoom == f6:
        i = 1
        while i <= (currentRoom.hillCount):                               
            randRow = random.randint(1, MAPSIZE - 2)
            randColumn = random.randint(1, MAPSIZE - 2)
            tempTile = Special("Hill Giant", randColumn, randRow)
            grid[randColumn][randRow].append(tempTile)
            if ((randRow in (8, 9)) and (randColumn in (4, 5, 6))) or (grid.count(randRow) > 0 and grid.count(randColumn) > 0):
                grid[randColumn][randRow].remove(tempTile)
            else:
                i += 1
    if currentRoom == f4 or currentRoom == f6 or currentRoom == f7 or currentRoom == f8 or currentRoom == f10:
        i = 1
        while i <= (currentRoom.gnollCount):                               
            randRow = random.randint(1, MAPSIZE - 2)
            randColumn = random.randint(1, MAPSIZE - 2)
            tempTile = Special("Gnoll", randColumn, randRow)
            grid[randColumn][randRow].append(tempTile)
            if ((randRow in (8, 9)) and (randColumn in (4, 5, 6))) or grid.count(randRow) > 0 or grid.count(randColumn) > 0:
                grid[randColumn][randRow].remove(tempTile)
            else:
                i += 1
    if currentRoom == f8 or currentRoom == f11 or currentRoom == f10 or currentRoom == f12:
        i = 1
        while i <= (currentRoom.flindCount):                               
            randRow = random.randint(1, MAPSIZE - 2)
            randColumn = random.randint(1, MAPSIZE - 2)
            tempTile = Special("Flind", randColumn, randRow)
            grid[randColumn][randRow].append(tempTile)
            if ((randRow in (8, 9)) and (randColumn in (4, 5, 6))) or grid.count(randRow) > 0 or grid.count(randColumn) > 0:
                grid[randColumn][randRow].remove(tempTile)
            else:
                i += 1
    if currentRoom == f5:
        tempTile = Special("Healer", 3, 6)
        grid[3][6].append(tempTile)
        tempTile = Special("Mage", 7, 6)
        grid[7][6].append(tempTile)
        tempTile = Special("Mini1", 5, 3)
        grid[5][3].append(tempTile)

    if currentRoom == f9:
        tempTile = Special("Fighter", 3, 6)
        grid[3][6].append(tempTile)
        tempTile = Special("Rouge", 7, 6)
        grid[7][6].append(tempTile)
        tempTile = Special("Mini2", 5, 3)
        grid[5][3].append(tempTile)

    if currentRoom == f1:
        tempTile = Special("Merchant", 5, 5)
        grid[5][5].append(tempTile)
        door = Special("Door", 5, 0)
        grid[5][0].append(door)

    if currentRoom == f13:
        tempTile = Special("Boss", 5, 5)
        grid[5][5].append(tempTile)

    def draw(self):
        screen.fill(BLACK)
        for row in range(MAPSIZE):           # Drawing grid
            for column in range(MAPSIZE):
                for i in range(0, len(Map.grid[column][row])):
                    color = WHITE
                    if Map.grid[column][row][i].name == "Hill Giant":
                        color = BLUE
                    if Map.grid[column][row][i].name == "Gnoll":
                        color = GBLUE
                    if Map.grid[column][row][i].name == "Flind":
                        color = RUST
                    if Map.grid[column][row][i].name == "Healer":
                        color = PINK
                    if Map.grid[column][row][i].name == "Mage":
                        color = TAN
                    if Map.grid[column][row][i].name == "Mini1":
                        color = MAGENTA
                    if Map.grid[column][row][i].name == "Fighter":
                        color = GRAY
                    if Map.grid[column][row][i].name == "Rouge":
                        color = PURPLE
                    if Map.grid[column][row][i].name == "Mini2":
                        color = ORANGE
                    if Map.grid[column][row][i].name == "Wall":
                        color = RED
                    if Map.grid[column][row][i].name == "Hero":
                        color = GREEN
                    if Map.grid[column][row][i].name == "Merchant":
                        color = BROWN
                    if Map.grid[column][row][i].name == "Boss":
                        color = LIME
                    if Map.grid[column][row][i].name == "Door":
                        color = WOOD
    

                pygame.draw.rect(screen, color, [(TILEWIDTH + TILEMARGIN) * column + TILEMARGIN,
                                                 (TILEHEIGHT + TILEMARGIN) * row + TILEMARGIN,
                                                 TILEWIDTH,
                                                 TILEHEIGHT])

    def update(self):        #Very important function
                             #This function goes through the entire grid
                             #And checks to see if any object's internal coordinates
                             #Disagree with its current position in the grid
                             #If they do, it removes the objects and places it 
                             #on the grid according to its internal coordinates 

        for column in range(MAPSIZE):      
            for row in range(MAPSIZE):
                for i in range(len(self.grid[column][row])):
                    if Map.grid[column][row][i].column != column:
                        Map.grid[column][row].remove(Map.grid[column][row][i])
                    elif Map.grid[column][row][i].name == "Hero":
                        Map.grid[column][row].remove(Map.grid[column][row][i])
        Map.grid[int(Map.hero.column)][int(Map.hero.row)].append(Map.hero)

Map = Map()

while not Done:     #Main pygame loop
    Map.draw()
    for event in pygame.event.get():        #catching events
        if event.type == pygame.QUIT:
            Done = True       

        elif event.type == pygame.KEYDOWN:
            KeyLookup = {
                pygame.K_LEFT: "LEFT",
                pygame.K_RIGHT: "RIGHT",
                pygame.K_DOWN: "DOWN",
                pygame.K_UP: "UP"
            }
            Map.hero.move(KeyLookup.get(event.key))


    clock.tick(60)      #Limit to 60 fps or something
    pygame.display.flip()     #Honestly not sure what this does, but it breaks if I remove it
    Map.update()


pygame.quit()
