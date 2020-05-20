from time import sleep
from random import randint
import random
from math import ceil
from StatsAndItems import *
from Combat import *
import pygame
import pickle

pygame.init()  # start up dat pygame
pygame.font.init()
clock = pygame.time.Clock()  # for framerate or something? still not very sure
pygame.display.set_caption("The Tower")
WIDTH = 716
HEIGHT = 716
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # making the window
Done = False  # variable to keep+ track if window is open
MAPSIZE = 11  # how many tiles in either direction of grid
VOLUME = .1

TILEWIDTH = 64  # pixel sizes for grid squares
TILEHEIGHT = 64
TILEMARGIN = 1

BLACK = (0, 0, 0)  # fill
WHITE = (255, 255, 255)  # floor
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 97, 3)
RED = (255, 0, 0)


inventory = []
goldCoins = 0
playerMoves = []
partyMember = []
block = 10
experience = 0

party = []

def checkList(inventory):
    original = screen.copy()
    font = pygame.font.SysFont('Arial', 25)
    scroll = pygame.image.load("GameArt\Extra\scroll.png")
    scroll = pygame.transform.scale(scroll, (scroll.get_size()[0] * 9 / 4, scroll.get_size()[1] * 2))
    screen.blit(scroll, (125, 100))
    justScroll = screen.copy()

    if len(inventory) == 0:
        screen.blit(font.render("Inventory is empty.", True, BLACK), (180, 175))
        screen.blit(font.render("Back", True, WHITE), (315, 505))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return None

    maxi = len(inventory)
    place = 0
    cursor = 0
    for i in range(11):
        if i >= len(inventory):
            break
        screen.blit(font.render(inventory[i].name, True, BLACK), (180, 175+(i*30)))
    screen.blit(font.render("Back", True, BLACK), (315, 505))
    screenshot = screen.copy()
    screen.blit(font.render(inventory[0].name, True, WHITE), (180, 175))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_UP) and place > 0:
                        place -= 1
                        if cursor > 0:
                            screen.blit(screenshot, (0, 0))
                            cursor -= 1
                            screen.blit(font.render(inventory[place].name, True, WHITE), (180, 175+(cursor*30)))#
                        else:
                            screen.blit(justScroll, (0, 0))
                            count = 0
                            for i in range(place, place+11):
                                if i >= len(inventory):
                                    break
                                screen.blit(font.render(inventory[i].name, True, BLACK), (180, 175+(count*30)))
                                count += 1
                            screen.blit(font.render("Back", True, BLACK), (315, 505))
                            screenshot = screen.copy()
                            screen.blit(font.render(inventory[place].name, True, WHITE), (180, 175)) #

                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN) and place < maxi:
                        place += 1
                        if cursor < 10 and cursor < maxi-1:
                            screen.blit(screenshot, (0, 0))
                            cursor += 1
                            screen.blit(font.render(inventory[place].name, True, WHITE), (180, 175+(cursor*30))) #
                        elif place == maxi:
                            screen.blit(screenshot, (0, 0))
                            cursor += 1
                            screen.blit(font.render("Back", True, WHITE), (315, 505)) #
                        else:
                            screen.blit(justScroll, (0, 0))
                            count = 0
                            for i in range(place-10, place+1):
                                if i >= len(inventory):
                                    break
                                screen.blit(font.render(inventory[i].name, True, BLACK), (180, 175+(count*30)))
                                count+=1
                            screen.blit(font.render("Back", True, BLACK), (315, 505))
                            screenshot = screen.copy()
                            screen.blit(font.render(inventory[place].name, True, WHITE), (180, 175+(10*30))) #
                    if event.key == pygame.K_RETURN:
                        try:
                            screen.blit(original, (0, 0))
                            return inventory[place]
                        except:
                            screen.blit(original, (0, 0))
                            pygame.display.update()
                            return None
        pygame.display.update()


def useItem(item, who):
    original = screen.copy()
    font = pygame.font.SysFont('Arial', 22)
    scroll = pygame.image.load("GameArt\Extra\scroll.png")
    scroll = pygame.transform.scale(scroll, (int(scroll.get_size()[0] * 1.5), int(scroll.get_size()[1] * .75)))
    screen.blit(scroll, ((WIDTH/2) - (scroll.get_size()[0]/2), 260))

    verb = "Equip"
    if isinstance(item, Consumable):
        verb = "Use"
    size = font.size("{} the".format(verb))[0]
    screen.blit(font.render("{} the".format(verb), True, BLACK), ((WIDTH/2)-(size/2), 290))
    size = font.size(item.name + "?")[0]
    screen.blit(font.render(item.name + "?", True, BLACK), ((WIDTH/2)-(size/2), 320))
    screen.blit(font.render("Yes", True, BLACK), (275, 370))
    screen.blit(font.render("No", True, BLACK), (405, 370))
    screenshot = screen.copy()
    screen.blit(font.render("No", True, BLACK, WHITE), (405, 370))
    pygame.display.update()
    which = 1

    while which != -99:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if which == 1:
                            which = 0
                            screen.blit(screenshot, (0, 0))
                            screen.blit(font.render("Yes", True, BLACK, WHITE), (275, 370))
                    elif event.key == pygame.K_RIGHT:
                        if which == 0:
                            which = 1
                            screen.blit(screenshot, (0, 0))
                            screen.blit(font.render("No", True, BLACK, WHITE), (405, 370))
                    elif event.key == pygame.K_RETURN:
                        if which == 1:
                            return False
                        which = -99
        pygame.display.update()
    screen.blit(original, (0, 0))
    if isinstance(item, Consumable):
        Fightable.flavorText(who.name + " " + item.statusEffect.verb + " the " + item.name + "!")
        sleep(1.25)
        who.getEffect(item.statusEffect)
        screen.blit(original, (0, 0))
    elif isinstance(item, Weapon):
        inventory.append(who.weapon)
        who.weapon = item
        inventory.remove(item)
    elif isinstance(item, Armor):
        inventory.append(who.armor)
        who.armor = item
        inventory.remove(item)
    return True


def userWarning(string):
    nope = pygame.mixer.Sound("SoundFX\Error.wav")
    nope.set_volume(VOLUME)
    nope.play()
    original = screen.copy()
    font = pygame.font.SysFont('Arial', 20)
    scroll = pygame.image.load("GameArt\Extra\scroll.png")
    scroll = pygame.transform.scale(scroll, (int(scroll.get_size()[0] * 2), int(scroll.get_size()[1] * 0.75)))
    screen.blit(scroll, ((WIDTH/2) - (scroll.get_size()[0]/2), 260))
    size = font.size(string)[0]
    screen.blit(font.render(string, True, BLACK), ((WIDTH/2)-(size/2), 290))
    size = font.size("Press Enter To Continue")[0]
    screen.blit(font.render("Press Enter To Continue", True, BLACK), ((WIDTH/2)-(size/2), 370))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        nope = pygame.mixer.Sound("SoundFX\Click.wav")
                        nope.set_volume(VOLUME)
                        nope.play()
                        screen.blit(original, (0, 0))
                        pygame.display.update()
                        return


def fadeToBlack(time=.01):
    original = screen.copy()
    screen.fill(BLACK)
    black = screen.copy()
    screen.blit(original, (0, 0))
    for i in range(50):
        black.set_alpha(i)
        screen.blit(black, (0, 0))
        pygame.display.update()
        sleep(time)


class Floor(object):
    def __init__(self, name, enemyCount, nextFloor):
        self.name = name
        self.enemyCount = enemyCount
        self.nextFloor = nextFloor

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

    @property
    def nextFloor(self):
        return self._nextFloor

    @nextFloor.setter
    def nextFloor(self, value):
        self._nextFloor = value


class FightFloor(Floor):
    def __init__(self, name, enemyCount, nextFloor, hillCount, gnollCount, flindCount):
        Floor.__init__(self, name, enemyCount, nextFloor)
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

    def clone(self):
        return FightFloor(self.name, self.enemyCount, self.nextFloor, self.hillCount, self.gnollCount, self.flindCount)


class MiniFloor(Floor):
    def __init__(self, name, enemyCount, nextFloor, mini, partyMem):
        Floor.__init__(self, name, enemyCount, nextFloor)
        self.mini = mini
        self.partyMem = partyMem

    def clone(self):
        return MiniFloor(self.name, self.enemyCount, self.nextFloor, self.mini, self.partyMem)


class SpecialFloor(Floor):
    def __init__(self, name, enemyCount, nextFloor, boss, merchant):
        Floor.__init__(self, name, enemyCount, nextFloor)
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

    @merchant.setter
    def merchant(self, value):
        self._merchant = value

    def clone(self):
        return SpecialFloor(self.name, self.enemyCount, self.nextFloor, self.boss, self.merchant)


class Special(object):  # The main class for stationary things that inhabit the grid ... grass, trees, rocks and stuff.
    def __init__(self, name, image, column, row):
        self.name = name
        self.image = image
        self.column = column
        self.row = row

f13 = SpecialFloor("Floor 1", 1, None, 1, 0)
f12 = FightFloor("Floor 3", 7, f13, 0, 0, 7)
f11 = FightFloor("Floor 3", 5, f12, 0, 0, 5)
f10 = FightFloor("Floor 3", 5, f11, 0, 2, 3)
f9 = MiniFloor("Mini Boss Floor 2", 1, f10, 1, 2)
f8 = FightFloor("Floor 3", 5, f9, 0, 3, 2)
f7 = FightFloor("Floor 3", 5, f8, 0, 5, 0)
f6 = FightFloor("Floor 3", 5, f7, 2, 3, 0)
f5 = MiniFloor("Mini Boss Floor 1", 1, f6, 1, 2)
f4 = FightFloor("Floor 3", 5, f5, 3, 2, 0)
f3 = FightFloor("Floor 3", 5, f4, 5, 0, 0)
f2 = FightFloor("Floor 2", 3, f3, 3, 0, 0)
f1 = SpecialFloor("Floor 1", 1, f2, 0, 1)

currentFloor = f1

enemyName = ["","Giant", "Gnoll", "Flind", "Mini1", "Mini2"]
ignoreName = ["Wall", "Fighter", "Rouge", "Mage", "Healer"]

class Player(Special):  # The player
    def __init__(self, name, image, column, row, party):
        Special.__init__(self, name, image, column, row)
        self.party = party

    @property
    def party(self):
        return self._party

    @party.setter
    def party(self, value):
        if value == 1 or value == 2:
            party = value

    def move(self, direction):  # This function is how a character moves around in a certain direction
        if self.collision(direction) == False:
            if direction == "UP" and self.row > 0:  # If within boundaries of grid
                self.row -= 1  # Go ahead and move

            elif direction == "LEFT" and self.column > 0:
                self.column -= 1

            elif direction == "RIGHT" and self.column < (MAPSIZE - 1):
                self.column += 1

            elif direction == "DOWN" and self.row < (MAPSIZE - 1):
                self.row += 1
        Map.update()

    def collision(self, direction):  # Checks if anything is on top of the grass in the direction that the character wants to move. Used in the move function
        if direction == "UP":
            if len(Map.grid[self.column][self.row - 1]) > 1:
                for i in range(0, len(Map.grid)):
                    name = Map.grid[self.column][self.row - 1][i].name
                    if name in enemyName:
                        global block
                        block = enemyName.index(name)
                        return block
                    elif name == "Merchant":
                        return 8
                    elif name == "Boss":
                        return 15
                    elif name in ignoreName:
                        return 20
            else:
                return False

        elif direction == "LEFT":
            if len(Map.grid[self.column - 1][self.row]) > 1:
                for i in range(0, len(Map.grid)):
                    name = Map.grid[self.column - 1][self.row][i].name
                    if name in enemyName:
                        block = enemyName.index(name)
                        return block
                    elif name == "Merchant":
                        return 8
                    elif name == "Boss":
                        return 15
                    elif name in ignoreName:
                        return 20
            else:
                return False
        elif direction == "RIGHT":
            if len(Map.grid[self.column + 1][self.row]) > 1:
                for i in range(0, len(Map.grid)):
                    name = Map.grid[self.column + 1][self.row][i].name
                    if name in enemyName:
                        block = enemyName.index(name)
                        return block
                    elif name == "Merchant":
                        return 8
                    elif name == "Boss":
                        return 15
                    elif name in ignoreName:
                        return 20
            else:
                return False
        elif direction == "DOWN":
            if len(Map.grid[self.column][self.row + 1]) > 1:
                for i in range(0, len(Map.grid)):
                    name = Map.grid[self.column][self.row + 1][i].name
                    if name in enemyName:
                        block = enemyName.index(name)
                        return block
                    elif name == "Merchant":
                        return 8
                    elif name == "Boss":
                        return 15
                    elif name in ignoreName:
                        return 20
            else:
                return False

    def location(self):
        print("Coordinates: " + str(self.column) + ", " + str(self.row))

class Map(object):  # The main class; where the action happens

    grid = []
    hero = Player("Hero", "GameArt\OverworldSprites\PlayerSpriteTemp.gif", 5, 9, 0)
    rowRange = range(1,7) + range(10)

    def build(self):
        if len(Map.grid) != 0:
            del Map.grid[:]

        for row in range(MAPSIZE):  # Creating grid
            Map.grid.append([])
            for column in range(MAPSIZE):
                Map.grid[row].append([])

        for row in range(MAPSIZE):  # Filling grid with the ground
            for column in range(MAPSIZE):
                tempTile = Special("Ground", "GameArt\Extra\Ground.png", column, row)
                Map.grid[column][row].append(tempTile)

        for row in range(MAPSIZE):  # Adding walls
            for column in range(MAPSIZE):
                tempTile = Special("Wall", "GameArt\Extra\Wall.png", column, row)
                if row == 0 or row == (MAPSIZE - 1) or column == 0 or column == (MAPSIZE - 1):
                    Map.grid[column][row].append(tempTile)

        row = [1, 2, 3, 4, 5, 6, 7]
        column = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        if currentFloor == f2 or currentFloor == f3 or currentFloor == f4 or currentFloor == f6:
            i = 1
            while i <= (currentFloor.hillCount):
                randRow = random.choice(row)
                row.remove(randRow)
                randColumn = random.choice(column)
                column.remove(randColumn)
                tempTile = Special("Giant", "GameArt\OverworldSprites\GiantSpriteTemp.gif", randColumn, randRow)
                Map.grid[randColumn][randRow].append(tempTile)
                i += 1
        if currentFloor == f4 or currentFloor == f6 or currentFloor == f7 or currentFloor == f8 or currentFloor == f10:
            i = 1
            while i <= (currentFloor.gnollCount):
                randRow = random.choice(row)
                row.remove(randRow)
                randColumn = random.choice(column)
                column.remove(randColumn)
                tempTile = Special("Gnoll", "GameArt\OverworldSprites\GnollSprite.gif", randColumn, randRow)
                Map.grid[randColumn][randRow].append(tempTile)
                i += 1
        if currentFloor == f8 or currentFloor == f11 or currentFloor == f10 or currentFloor == f12:
            i = 1
            while i <= (currentFloor.flindCount):
                randRow = random.choice(row)
                row.remove(randRow)
                randColumn = random.choice(column)
                column.remove(randColumn)
                tempTile = Special("Flind", "GameArt\OverworldSprites\FlindTemp.png", randColumn, randRow)
                Map.grid[randColumn][randRow].append(tempTile)
                i += 1

        if currentFloor == f5:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("GameMusic\BossRoom.wav")
            pygame.mixer.music.play(-1)
            tempTile = Special("Healer", "GameArt\OverworldSprites\HealerTemp.png", 3, 6)
            Map.grid[3][6].append(tempTile)
            tempTile = Special("Mage", "GameArt\OverworldSprites\MageTemp.png", 7, 6)
            Map.grid[7][6].append(tempTile)
            tempTile = Special("Mini1", "GameArt\OverworldSprites\MiniTemp.png", 5, 3)
            Map.grid[5][3].append(tempTile)

        if currentFloor == f9:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("GameMusic\BossRoom.wav")
            pygame.mixer.music.play(-1)
            tempTile = Special("Fighter", "GameArt\OverworldSprites\FighterTemp.png", 3, 6)
            Map.grid[3][6].append(tempTile)
            tempTile = Special("Rouge", "GameArt\OverworldSprites\RougeTemp.png", 7, 6)
            Map.grid[7][6].append(tempTile)
            tempTile = Special("Mini2", "GameArt\OverworldSprites\MiniTempT.png", 5, 3)
            Map.grid[5][3].append(tempTile)

        if currentFloor == f1:
            tempTile = Special("Merchant", "GameArt\OverworldSprites\MerchSprite.gif", 5, 5)
            Map.grid[5][5].append(tempTile)

            pygame.mixer.music.stop()
            pygame.mixer.music.set_volume(.8*VOLUME)
            song = pygame.mixer.music.load("GameMusic\MerchIntro.wav")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pass
            pygame.mixer.music.stop()
            song = pygame.mixer.music.load("GameMusic\MerchTheme.wav")
            pygame.mixer.music.play(-1)

        if currentFloor == f13:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("GameMusic\FinalBossRoom.wav")
            pygame.mixer.music.play(-1)
            tempTile = Special("Boss", "GameArt\OverworldSprites\BossTemp.png", 5, 5)
            Map.grid[5][5].append(tempTile)


    def draw(self):
        screen.fill(BLACK)
        for row in range(MAPSIZE):  # Drawing grid
            for column in range(MAPSIZE):
                who = None
                for i in range(0, len(Map.grid[column][row])):
                    color = WHITE
                    if not isinstance(Map.grid[column][row][i].image, str):
                        color = Map.grid[column][row][i].image
                    else:
                        who = Map.grid[column][row][i]

                if who is not None:
                    img = pygame.image.load("GameArt\Extra\ground.png")
                    img.blit(pygame.image.load(who.image), (0, 0))
                    screen.blit(img, ((TILEWIDTH + TILEMARGIN) * column + TILEMARGIN,
                                      (TILEHEIGHT + TILEMARGIN) * row + TILEMARGIN))
                else:
                    recta = pygame.draw.rect(screen, color, [(TILEWIDTH + TILEMARGIN) * column + TILEMARGIN,
                                                             (TILEHEIGHT + TILEMARGIN) * row + TILEMARGIN,
                                                             TILEWIDTH,
                                                             TILEHEIGHT])

    def update(self):  # Very important function
        # This function goes through the entire grid
        # And checks to see if any object's internal coordinates
        # Disagree with its current position in the grid
        # If they do, it removes the objects and places it
        # on the grid according to its internal coordinates

        for column in range(MAPSIZE):
            for row in range(MAPSIZE):
                for i in range(len(self.grid[column][row])):
                    if Map.grid[column][row][i].column != column:
                        Map.grid[column][row].remove(Map.grid[column][row][i])
                    elif Map.grid[column][row][i].name == "Hero":
                        Map.grid[column][row].remove(Map.grid[column][row][i])
        Map.grid[int(Map.hero.column)][int(Map.hero.row)].append(Map.hero)

Map = Map()


def menu():
    font1 = pygame.font.SysFont('Arial', 90)
    font2 = pygame.font.SysFont('Arial', 60)
    selected = "start"
    bg_img = pygame.image.load("GameArt\Extra\menu.gif")
    men = True
    pygame.mixer.music.set_volume(VOLUME)
    song = pygame.mixer.music.load("GameMusic\MainMenu.wav")
    pygame.mixer.music.play(-1)

    select = pygame.mixer.Sound("SoundFX\Select.wav")
    select.set_volume(.25*VOLUME)
    while men:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(select)
                    if selected == "quit":
                        selected = "load"
                    else:
                        selected = "start"
                elif event.key == pygame.K_DOWN:
                    pygame.mixer.Sound.play(select)
                    if selected == "start":
                        selected = "load"
                    else:
                        selected = "quit"
                if event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(select)
                    if selected == "start":
                        pygame.mixer.music.fadeout(1000)
                        fadeToBlack()
                        gameMap()
                        return
                    if selected == "load":
                        loadGame()
                    if selected == "quit":
                        pygame.quit()
                        quit()


        # Main Menu UI
        screen.blit(bg_img, bg_img.get_rect())
        title = font1.render("The Tower", False, BLACK)
        if selected == "start":
            text_start = font2.render("NEW GAME", False, WHITE)
        else:
            text_start = font2.render("NEW GAME", False, BLACK)
        if selected == "load":
            text_load = font2.render("LOAD SAVE", False, WHITE)
        else:
            text_load = font2.render("LOAD SAVE", False, BLACK)
        if selected == "quit":
            text_quit = font2.render("QUIT", False, WHITE)
        else:
            text_quit = font2.render("QUIT", False, BLACK)

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        load_rect = text_load.get_rect()
        quit_rect = text_quit.get_rect()

        screen.blit(title, (WIDTH / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (WIDTH / 2 - (start_rect[2] / 2), 300))
        screen.blit(text_load, (WIDTH / 2 - (load_rect[2] / 2), 360))
        screen.blit(text_quit, (WIDTH / 2 - (quit_rect[2] / 2), 420))
        pygame.display.update()
        clock.tick(60)

############################
# Save File Format:
# [floor, level, party members, inventory, gold, moves]
# e.g. [1, 3, ["Healer"], [dagger, health1], 69, [fight, die]]
############################

def saveGame():
    try:
        save = open("savefile.txt", "wb")
        inven = []
        pMoves = []
        pMember = []
        for i in range(len(inventory)):
            inven.append(inventory[i].clone())
        for i in range(len(party)):
            pMember.append(party[i].clone())
        for i in range(len(playerMoves)):
            pMoves.append(playerMoves[i].clone())
        saveStuff = [currentFloor.clone(), experience, pMember, inven, goldCoins, pMoves]
        pickle.dump(saveStuff, save)
        save.close()
    except IOError:
        userWarning("Failed to save game!")

def loadGame():
    try:
        save = open("savefile.txt", "r").read()
        print "Found a save file!"
        if (len(save) != 0):
            try:
                saveFile = open("savefile.txt", "rb")
                save = pickle.load(saveFile)
                currentFloor = save[0]
                experience = save[1]
                party = save[2]
                inventory = []
                for i in range(len(save[3])):
                    inventory.append(eval(str(p[i])))
                goldCoins = save[4]
                playerMoves = save[5]
                pygame.mixer.music.fadeout(1000)
                fadeToBlack()
                gameMap()
            except:
                userWarning("Save file is corrupted!")
        else:
            userWarning("Save file is empty!")
    except:
        userWarning("Unable to find or load save file!")

def popup():
    font1 = pygame.font.SysFont('Arial', 75)
    font2 = pygame.font.SysFont('Arial', 60)
    selected = 1
    bg_img = pygame.image.load("GameArt\Extra\menu.gif")
    pop = True

    select = pygame.mixer.Sound("SoundFX\Select.wav")
    select.set_volume(.25*VOLUME)
    while pop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(select)
                    selected = 1
                elif event.key == pygame.K_DOWN:
                    pygame.mixer.Sound.play(select)
                    selected = 2
                if event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(select)
                    if selected == 1:
                        return
                    if selected == 2:
                        return

        # Pop Up UI
        if currentFloor == f1:
            screen.blit(bg_img, bg_img.get_rect())
            title1 = font1.render("What move do you", False, BLACK)
            title2 = font1.render("want to learn?", False, BLACK)
            if selected == 1:
                opt1 = font2.render("Healing Move", False, WHITE)
            else:
                opt1 = font2.render("Healing Move", False, BLACK)
            if selected == 2:
                opt2 = font2.render("Spell Move", False, WHITE)
            else:
                opt2 = font2.render("Spell Move", False, BLACK)


        elif currentFloor == f5 or currentFloor == f9:
            screen.blit(bg_img, bg_img.get_rect())
            title1 = font1.render("Who do you want", False, BLACK)
            title2 = font1.render("to join your party?", False, BLACK)
            if currentFloor == f5:
                if selected == 1:
                    opt1 = font2.render("Healer", False, WHITE)
                else:
                    opt1 = font2.render("Healer", False, BLACK)
                if selected == 2:
                    opt2 = font2.render("Mage", False, WHITE)
                else:
                    opt1 = font2.render("Mage", False, BLACK)
            if currentFloor == f9:
                if selected == 1:
                    opt1 = font2.render("Fighter", False, WHITE)
                else:
                    opt1 = font2.render("Fighter", False, BLACK)
                if selected == 2:
                    opt2 = font2.render("Rouge", False, WHITE)
                else:
                    opt2 = font2.render("Rouge", False, BLACK)

        title1_rect = title1.get_rect()
        title2_rect = title2.get_rect()
        start_rect = opt1.get_rect()
        quit_rect = opt1.get_rect()

        screen.blit(title1, (WIDTH / 2 - (title1_rect[2] / 2), 80))
        screen.blit(title2, (WIDTH / 2 - (title2_rect[2] / 2), 160))
        screen.blit(opt1, (WIDTH / 2 - (start_rect[2] / 2), 300))
        screen.blit(opt2, (WIDTH / 2 - (quit_rect[2] / 2), 360))
        pygame.display.update()
        clock.tick(60)


def merchText():
    talk = True
    background = pygame.image.load("GameArt\Extra\Background.png")
    merchant = pygame.image.load("GameArt\Merchant\Happy.png")
    merchant = pygame.transform.scale(merchant, (int(merchant.get_size()[0]*.255), int(merchant.get_size()[1]*.255)))
    noMerch = screen.copy()
    box = pygame.image.load("GameArt\Extra\Text.png")
    merch_rect = merchant.get_rect()
    font = pygame.font.SysFont('Arial', 30)
    text1 = font.render("Why, hello there stranger! Let me guess, you're here", False, BLACK)
    text2 = font.render("about the missing villager, right? I can tell. You", False, BLACK)
    text4 = font.render("wannabe heros had.", False, BLACK)
    text3 = font.render("have that same look in your eyes all the other", False, BLACK)
    i = 0
    click = pygame.mixer.Sound("SoundFX\Click.wav")
    click.set_volume(VOLUME)
    global currentFloor
    while talk:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                pygame.mixer.Sound.play(click)
                if i == 0:
                    screen.blit(noMerch, (0, 0))
                    merchant = pygame.transform.scale(pygame.image.load("GameArt\Merchant\Stand.png"), (int(merchant.get_size()[0]), int(merchant.get_size()[1])))
                    text1 = font.render("Well, the villagers are here, but they're not the ", False, BLACK)
                    text2 = font.render("same as they were before. Yeenoghu, the beast", False, BLACK)
                    text3 = font.render("responsible for this tower, has already turned them", False, BLACK)
                    text4 = font.render("into the monsters that now live in this tower.", False, BLACK)
                    i += 1
                elif i == 1:
                    screen.blit(noMerch, (0, 0))
                    merchant = pygame.transform.scale(pygame.image.load("GameArt\Merchant\Sad.png"), (int(merchant.get_size()[0]), int(merchant.get_size()[1])))
                    text1 = font.render("He's been doing this for centuries now. He uses", False, BLACK)
                    text2 = font.render("magic to move the tower around so he never runs", False, BLACK)
                    text3 = font.render("out of victims to put under his curse.", False, BLACK)
                    text4 = font.render("", False, BLACK)
                    i += 1
                elif i == 2:
                    text1 = font.render("Looks like the curse has started to affect you", False, BLACK)
                    text2 = font.render("as well. There's flind fur starting to grow on", False, BLACK)
                    text3 = font.render("your arms. Don't worry, there's still a chance", False, BLACK)
                    text4 = font.render("you can go back to normal. Won't be easy though.", False, BLACK)
                    i += 1
                elif i == 3:
                    screen.blit(noMerch, (0, 0))
                    merchant = pygame.transform.scale(pygame.image.load("GameArt\Merchant\Stand.png"), (int(merchant.get_size()[0]), int(merchant.get_size()[1])))
                    i += 1
                    text1 = font.render("Only way to break the curse is to kill Yennughu,", False, BLACK)
                    text2 = font.render("the creator the curse. But you have to fight your", False, BLACK)
                    text3 = font.render("way up for even the chance to fight him. If you want", False, BLACK)
                    text4 = font.render("some help though I may be of some assistance.", False, BLACK)
                    i += 1
                elif i == 4:
                    screen.blit(noMerch, (0, 0))
                    merchant = pygame.transform.scale(pygame.image.load("GameArt\Merchant\Happy.png"), (int(merchant.get_size()[0]), int(merchant.get_size()[1])))
                    text1 = font.render("I may be rusty, but I still know some powerful", False, BLACK)
                    text2 = font.render("fighting techniques. I only have time to teach", False, BLACK)
                    text3 = font.render("you one though.", False, BLACK)
                    text4 = font.render("", False, BLACK)
                    i += 1
                elif i == 5:
                    screen.blit(noMerch, (0, 0))
                    merchant = pygame.transform.scale(pygame.image.load("GameArt\Merchant\Stand.png"), (int(merchant.get_size()[0]), int(merchant.get_size()[1])))
                    text1 = font.render("I'll also open up my shop for you. You'll ", False, BLACK)
                    text2 = font.render("probably find some valueables after your fights", False, BLACK)
                    text3 = font.render("and I'll gladly take them off your hands.", False, BLACK)
                    text4 = font.render("", False, BLACK)
                    i += 1
                elif i == 6:
                    text1 = font.render("I'll only open it after you finish clearing out", False, BLACK)
                    text2 = font.render("all the enemies on a floor. Those monsters", False, BLACK)
                    text3 = font.render("are dangerous and I'm not gonna risk my life.", False, BLACK)
                    text4 = font.render("", False, BLACK)
                    i += 1
                elif i == 7:
                    screen.blit(noMerch, (0, 0))
                    merchant = pygame.transform.scale(pygame.image.load("GameArt\Merchant\Congrats.png"), (int(merchant.get_size()[0]), int(merchant.get_size()[1])))
                    text1 = font.render("That's all the help I can offer though. Don't", False, BLACK)
                    text2 = font.render("worry though, I'm sure you'll be able to pull", False, BLACK)
                    text3 = font.render("it off.", False, BLACK)
                    text4 = font.render("", False, BLACK)
                    i += 1
                elif i == 8:
                    screen.blit(noMerch, (0, 0))
                    merchant = pygame.transform.scale(pygame.image.load("GameArt\Merchant\Stand.png"), (int(merchant.get_size()[0]), int(merchant.get_size()[1])))
                    text1 = font.render("Hopefully.", False, BLACK)
                    text2 = font.render("", False, BLACK)
                    text3 = font.render("", False, BLACK)
                    text4 = font.render("", False, BLACK)
                    i += 1
                elif i == 9:
                    popup()
                    changeFloor()
                    return

        screen.fill(WHITE)
        screen.blit(background, background.get_rect())
        screen.blit(merchant, (WIDTH / 2 - (merch_rect[2] / 2), 50))
        screen.blit(box, (0, 475))
        screen.blit(text1, (10, 505))
        screen.blit(text2, (10, 540))
        screen.blit(text3, (10, 575))
        screen.blit(text4, (10, 610))
        pygame.display.update()

def bossText():
    talk = True
    background = pygame.image.load("GameArt\Extra\Background.png")
    merchant = pygame.image.load("GameArt\Merchant\Stand.png")
    box = pygame.image.load("GameArt\Extra\Text.png")
    merch_rect = merchant.get_rect()
    font = pygame.font.SysFont('Arial', 30)
    text1 = font.render("What do you want you lowly flinds? I didn't ask for", False, BLACK)
    text2 = font.render("you to come up! ", False, BLACK)
    text4 = font.render("", False, BLACK)
    text3 = font.render("", False, BLACK)
    i = 0
    global currentFloor
    while talk:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if i == 0:
                    text1 = font.render("Wait a minute... That look in your eyes... You", False, BLACK)
                    text2 = font.render("aren't fully changed yet. But judging by the look of", False, BLACK)
                    text3 = font.render("you, it won't be much longer.", False, BLACK)
                    text4 = font.render("", False, BLACK)
                    i += 1
                elif i == 1:
                    text1 = font.render("Oh, so you're still gonna try and fight? It's", False, BLACK)
                    text2 = font.render("futile, there's no way you'll be able to defeat", False, BLACK)
                    text3 = font.render("me.", False, BLACK)
                    text4 = font.render("", False, BLACK)
                    i += 1
                elif i == 2:
                    text1 = font.render("Still gonna try? Well bring it on! I could use", False, BLACK)
                    text2 = font.render("the practice.", False, BLACK)
                    text3 = font.render("", False, BLACK)
                    text4 = font.render("", False, BLACK)
                    i += 1
                elif i == 3:
                    # boss fight
                    return

        screen.fill(WHITE)
        screen.blit(background, background.get_rect())
        screen.blit(merchant, (WIDTH / 2 - (merch_rect[2] / 2), 50))
        screen.blit(box, (0, 475))
        screen.blit(text1, (10, 505))
        screen.blit(text2, (10, 540))
        screen.blit(text3, (10, 575))
        pygame.display.update()

def shop():
    shopping = True
    global currentFloor
    global items
    global goldCoins

    font1 = pygame.font.SysFont('Arial', 50)
    font2 = pygame.font.SysFont('Arial', 13)
    background = pygame.image.load("GameArt\Extra\Background.png")
    merchant = pygame.image.load("GameArt\Merchant\Stand.png")
    sign = pygame.image.load("GameArt\Extra\Sign.png")
    button = pygame.image.load("GameArt\Extra\Buttonfull.png")
    rest = pygame.image.load("GameArt\Extra\Rest.png")
    gold = pygame.image.load("GameArt\Extra\Gold.png")
    rest_rect = rest.get_rect(center=(125, 655))
    buy_rect = pygame.Rect(290, 215, 400, 87)
    sell_rect = pygame.Rect(290, 390, 400, 300)

    if currentFloor == f2 or currentFloor == f3 or currentFloor == f4:
        shop = random.sample(grade0Items, 6)
    elif currentFloor == f5 or currentFloor == f6 or currentFloor == f7 or currentFloor == f8:
        shop = random.sample(grade1Items, 6)
    elif currentFloor == f9 or currentFloor == f10 or currentFloor == f11 or currentFloor == f12:
        shop = random.sample(grade2Items, 6)
    else:
        shop = []

    while shopping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if buy_rect.collidepoint(pos):
                    j = 0
                    for i in shop:
                        item_rect = pygame.Rect(290, 215 + (j * 14.5), 400, 14.5)
                        if item_rect.collidepoint(pos):
                            if len(inventory) < 20 and (goldCoins - i.cost) >= 0:
                                goldCoins -= i.cost
                                shop.remove(i)
                                inventory.append(i)
                        j += 1
                        
                if sell_rect.collidepoint(pos):
                    print pos
                    j = 0
                    for i in inventory:
                        item_rect = pygame.Rect(290, 390 + (j * 14.5), 400, 14.5)
                        if item_rect.collidepoint(pos):
                            goldCoins += (i.cost/2)
                            inventory.remove(i)
                        j += 1
                        
                if rest_rect.collidepoint(pos):
                    changeFloor()
                    return

        title = font1.render("Merchant's Shop", False, BLACK)
        done = font1.render("DONE", False, BLACK)
        buy = font1.render("Click Item to Buy", False, BLACK)
        sell = font1.render("Sell for 1/2 Cost", False, BLACK)
        goldNum = font2.render("Gold: {}".format(goldCoins), False, BLACK)

        screen.fill(WHITE)
        screen.blit(background, background.get_rect())
        screen.blit(merchant, (0, 130))
        screen.blit(sign, (0, 0))
        screen.blit(button, (283, 130))
        screen.blit(gold, (283, 110))
        screen.blit(rest, rest_rect)
        screen.blit(title, (150, 45))
        screen.blit(done, (55, 625))
        screen.blit(buy, (310, 140))
        screen.blit(sell, (310, 320))
        screen.blit(goldNum, (290, 113))

        j = 0
        for i in shop:
            item = font2.render(i.flavor, False, BLACK)
            screen.blit(item, (290, 215 + (j * 15)))
            j += 1

        j = 0
        for i in inventory:
            item = font2.render(i.flavor, False, BLACK)
            screen.blit(item, (290, 390 + (j * 15)))
            j += 1

        pygame.display.update()


def changeFloor():
    global currentFloor
    currentFloor = currentFloor.nextFloor
    Map.hero.column = 5
    Map.hero.row = 9
    Map.build()
    return


def gameMap():
    global block
    bg_img = pygame.image.load("GameArt\Extra\menu.gif")
    gameMap = True
    Map.build()
    pygame.display.update()

    while gameMap:
        Map.draw()

        if currentFloor == None:
            screen.blit(bg_img, bg_img.get_rect())

        for event in pygame.event.get():  # catching events
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                Pos = pygame.mouse.get_pos()
                print Pos

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Map.hero.move("LEFT")
                    if Map.hero.collision("LEFT") == 8:
                        merchText()
                    elif Map.hero.collision("UP") == 15:
                        bossText()
                    elif Map.hero.collision("LEFT") == block:
                        print block
                    elif Map.hero.collision("LEFT") == 20:
                        print ""

                if event.key == pygame.K_RIGHT:
                    Map.hero.move("RIGHT")
                    if Map.hero.collision("RIGHT") == 8:
                        merchText()
                    elif Map.hero.collision("UP") == 15:
                        bossText()
                    elif Map.hero.collision("RIGHT") == block:
                        print block
                    elif Map.hero.collision("RIGHT") == 20:
                        print ""

                if event.key == pygame.K_UP:
                    Map.hero.move("UP")
                    if Map.hero.collision("UP") == 8:
                        merchText()
                    elif Map.hero.collision("UP") == 15:
                        bossText()
                    elif Map.hero.collision("UP") == block:
                        print block
                    elif Map.hero.collision("UP") == 20:
                        print ""

                if event.key == pygame.K_DOWN:
                    Map.hero.move("DOWN")
                    if Map.hero.collision("DOWN") == 8:
                        merchText()
                    elif Map.hero.collision("UP") == 15:
                        bossText()
                    elif Map.hero.collision("DOWN") == block:
                        print block
                    elif Map.hero.collision("DOWN") == 20:
                        print ""

                if event.key == pygame.K_RETURN:
                    changeFloor()
                if event.key == pygame.K_a:
                    bossText()
                if event.key == pygame.K_i:
                    checkList(inventory)
                if event.key == pygame.K_b:
                    shop()

        clock.tick(60)  # Limit to 60 fps or something
        pygame.display.update()  # Honestly not sure what this does, but it breaks if I remove it
        Map.update()
        saveGame()


def combatTest():
    Fightable.combat([gallant, throureum], [enemyTest.clone(), enemyTest.clone(), enemyTest.clone(), enemyTest.clone()], screen, inventory)

combatTest()
menu()

pygame.quit()