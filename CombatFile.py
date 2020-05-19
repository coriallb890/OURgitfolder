from time import sleep
from random import randint
from math import ceil
from StatsAndItems import *
import random
import pygame

pygame.init()  # start up dat pygame
pygame.font.init()
clock = pygame.time.Clock()  # for framerate or something? still not very sure
pygame.display.set_caption("The Tower")
WIDTH = 716
HEIGHT = 716
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # making the window
Done = False  # variable to keep+ track if window is open
MAPSIZE = 11  # how many tiles in either direction of grid

TILEWIDTH = 64  # pixel sizes for grid squares
TILEHEIGHT = 64
TILEMARGIN = 1

BLACK = (0, 0, 0)  # fill
WHITE = (255, 255, 255)  # floor
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 97, 3)
RED = (255, 0, 0)


inventory = random.sample(items, 5)
goldCoins = 0
playerMoves = []
partyMember = []
block = 10

def checkList(inventory):
    original = screen.copy()
    font = pygame.font.SysFont('Arial', 25)
    scroll = pygame.image.load("GameArt\Extra\scroll.png")
    scroll = pygame.transform.scale(scroll, (scroll.get_size()[0] * 9 / 4, scroll.get_size()[1] * 2))
    screen.blit(scroll, (125, 100))
    justScroll = screen.copy()
    maxi = len(inventory)
    place = 0
    cursor = 0
    for i in range(11):
        if i >= len(inventory):
            break
        screen.blit(font.render(inventory[i].name, True, BLACK), (180, 175+(i*30)))
    screen.blit(font.render("Back", True, BLACK), (315, 505))
    screenshot = screen.copy()
    screen.blit(font.render(inventory[0].name, True, WHITE), (180, 175)) #
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
                        if cursor < 10:
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
        pass
    elif isinstance(item, Armor):
        pass
    return True


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


class MiniFloor(Floor):
    def __init__(self, name, enemyCount, nextFloor, mini, partyMem):
        Floor.__init__(self, name, enemyCount, nextFloor)
        self.mini = mini
        self.party = partyMem


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
            tempTile = Special("Healer", "GameArt\OverworldSprites\HealerTemp.png", 3, 6)
            Map.grid[3][6].append(tempTile)
            tempTile = Special("Mage", "GameArt\OverworldSprites\MageTemp.png", 7, 6)
            Map.grid[7][6].append(tempTile)
            tempTile = Special("Mini1", "GameArt\OverworldSprites\MiniTemp.png", 5, 3)
            Map.grid[5][3].append(tempTile)

        if currentFloor == f9:
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
            pygame.mixer.music.set_volume(.8)
            song = pygame.mixer.music.load("GameMusic\MerchIntro.wav")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pass
            pygame.mixer.music.stop()
            song = pygame.mixer.music.load("GameMusic\MerchTheme.wav")
            pygame.mixer.music.play(-1)

        if currentFloor == f13:
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


class Fightable(object):
    def __init__(self, name, fight, defense, agility, health, moves,
                 gender=Gender("it", "it", "it", "its", "its", "itself")):
        self._name = name
        self._fight = fight
        self._maxFight = fight
        self._health = health
        self._maxHealth = health
        self._defense = defense
        self._maxDefense = defense
        self._agility = agility
        self._maxAgility = agility
        self._gender = gender
        self._learnableMoves = moves
        self._moves = []
        self._statusEffects = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def fight(self):
        return self._fight

    @fight.setter
    def fight(self, value):
        if (value > 0):
            self._fight = value

    @property
    def maxFight(self):
        return self._maxFight

    @maxFight.setter
    def maxFight(self, value):
        if (value > 0):
            self._maxFight = value

    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self, value):
        if (value > 0):
            self._defense = value
        else:
            self._defense = 0

    @property
    def maxDefense(self):
        return self._maxDefense

    @maxDefense.setter
    def maxDefense(self, value):
        if (value > 0):
            self._maxDefense = value

    @property
    def agility(self):
        return self._agility

    @agility.setter
    def agility(self, value):
        if (value > 0):
            self._agility = value

    @property
    def maxAgility(self):
        return self._maxAgility

    @maxAgility.setter
    def maxAgility(self, value):
        if (value > 0):
            self._maxAgility = value

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value < self.maxHealth:
            if value > 0:
                self._health = value
            else:
                self._health = 0
        else:
            self._health = self.maxHealth

    @property
    def maxHealth(self):
        return self._maxHealth

    @maxHealth.setter
    def maxHealth(self, value):
        if (value > 0):
            self._maxHealth = value

    @property
    def gender(self):
        return self.gender

    @gender.setter
    def gender(self, value):
        self._gender = value

    @property
    def moves(self):
        return self._moves

    @property
    def learnableMoves(self):
        return self._learnableMoves

    @property
    def statusEffects(self):
        return self._statusEffects

    def healthColor(self):
        if self.health >= self.maxHealth * .75:
            return GREEN
        if self.health >= self.maxHealth * .5:
            return YELLOW
        if self.health >= self.maxHealth * .25:
            return ORANGE
        return RED

    def getEffect(self, m):
        if isinstance(m, Move):
            x = 0
            while x < len(m.statusEffects()):
                x += 1
                if m.statusEffects()[x].turns > 0:
                    self.statusEffects.append(m.statusEffects[x].clone())
                    Fightable.flavorText("{} has been {}".format(self.name, m.statusEffects[x].verb))
                else:
                    self.oneAndDone(m.statusEffects[x])
        else:
            if m.turns > 0:
                self.statusEffects.append(m.clone())
            else:
                self.oneAndDone(m)

    def oneAndDone(self, st):
        suffered = ""
        x = 0
        while x < len(st.stats):
            if x != 0:
                suffered += "\n"

            if st.stats[x] == "health":
                self.health += (st.amounts[x])
                verb = " loses "
                if st.amounts[x] >= 0:
                    verb = " gains "
                plural = "s"
                if abs(st.amounts[x]) == 1:
                    plural = ""
                suffered += self.name + verb + str(abs(st.amounts[x])) + " hitpoint" + plural + "!"

            elif st.stats[x] == ("fight"):
                self.fight += (st.amounts[x])
                verb = ""
                if abs(st.amounts[x]) > 4:
                    verb = "greatly"
                elif abs(st.amounts[x]) <= 2:
                    verb = "slightly"
                if st.amounts[x] >= 0:
                    verb = " is " + verb + " strengthened"
                else:
                    verb = " is " + verb + " weakened"
                suffered += self.name + verb + "!"

            elif st.stats[x] == ("defense"):
                self.defense += (st.amounts[x])
                verb = ""
                if abs(st.amounts[x]) > 4:
                    verb = "greatly"
                elif abs(st.amounts[x]) <= 2:
                    verb = "slightly"
                if st.amounts[x] >= 0:
                    verb = "'s defenses are " + verb + " reinforced"
                else:
                    verb = "'s defenses are " + verb + " diminished"
                suffered += self.name + verb + "!"

            elif st.stats[x] == "agility":
                self.agility += (st.amounts[x])
                verb = ""
                if abs(st.amounts[x]) > 4:
                    verb = "greatly"
                elif abs(st.amounts[x]) <= 2:
                    verb = "slightly"
                if st.amounts[x] >= 0:
                    verb = "'s speed is " + verb + " increased"
                else:
                    verb = "'s speed is " + verb + " decreased"
                suffered += self.name + verb + "!"
            x += 1

        Fightable.flavorText(suffered)
        sleep(1)

    def sufferEffects(self):
        x = 0
        things = []
        while x < len(self.statusEffects):
            things.append(self.statusEffects[x].doIt(self))
            x += 1
        return things

    def hasMovesLeft(self):
        x = 0
        while x < len(self.moves):
            if self.moves[x].left() > 0:
                return True
            x += 1
        return False

    def revert(self):
        self.fight = self.maxFight
        self.defense = self.maxDefense
        self.agility = self.maxAgility

    @staticmethod
    def area(t):
        a = 0
        for x in range(0, len(t)):
            a += t[x].size
        return a

    @staticmethod
    def totalHealth(team):
        health = 0
        x = 0
        while x < len(team):
            health += team[x].health
            x += 1
        print health
        return health

    @staticmethod
    def firstOf(coords):
        for x in range(len(coords)-1, -1, -1):
            if coords[x] != -1:
                return coords[x]
        return -1

    @staticmethod
    def selectFromCoords(coords, enemies, target):
        screenshot = screen.copy()
        locations = []
        img = None


        l = 0
        while Fightable.firstOf(coords[l]) == -1:
            l += 1

        if target == "Single" or target == "Vert Line":
            locations = [(185, 300 + 100 * len(coords[0])), (285, 300 + 100 * len(coords[0])),
                         (390, 300 + 100 * len(coords[0])), (490, 300 + 100 * len(coords[0]))]
            img = pygame.image.load("GameArt\Buttons\This.png")
        elif target == "Hori Line":
            for x in range(0, len(coords[0])):
                locations.append((300, (x * 100 + 200)))
            img = pygame.image.load("GameArt\Buttons\This.png")
        else:
            locations = [(0, 0)]
            img = pygame.image.load("GameArt\Buttons\Empty.png")


        l = 0
        screens = []
        while l < len(locations)+1:
            screen.blit(screenshot, (0, 0))
            while l < len(coords) and Fightable.firstOf(coords[l]) == -1:
                l += 1
            if l < len(locations):
                Fightable.printCoords(coords, enemies, Fightable.firstOf(coords[l]))
                screen.blit(img, locations[l])
            else:
                screen.blit(pygame.image.load("GameArt\Buttons\Back.png"), (650, 650))
            screens.append(screen.copy())
            l += 1
        l = 0
        screen.blit(screens[l], (0, 0))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        l -= 1
                        if l < 0:
                            l = len(screens)-1
                        screen.blit(screens[l], (0, 0))
                    if event.key == pygame.K_RIGHT:
                        l += 1
                        if l >= len(screens):
                            l = 0
                        screen.blit(screens[l], (0, 0))
                    if event.key == pygame.K_RETURN:
                        if l == len(locations):
                            return [-1]
                        x = 0
                        t = -1
                        for x in range(4):
                            if Fightable.firstOf(coords[x]) != -1:
                                t+=1
                            if t == l:
                                return [Fightable.firstOf(coords[x])]
                        return [-1]
            pygame.display.update()

    @staticmethod
    def printHeroes(heroes, highlight=-1, yellow=-1):
        font = pygame.font.SysFont('Arial', 25)
        colors = [WHITE, WHITE, WHITE]
        if yellow != -1:
            colors[yellow] = RED
        if highlight == 0:
            pygame.draw.rect(screen, colors[0], [35, 0, 216, 120])
            heroes[0].blurtStats(font, (40, 25))
        else:
            pygame.draw.rect(screen, colors[0], [35, 0, 216, 100])
            heroes[0].blurtStats(font, (40, 5))
        if highlight == 1:
            pygame.draw.rect(screen, colors[1], [252, 0, 216, 120])
            if len(heroes) > 1:
                heroes[1].blurtStats(font, (257, 25))
        else:
            pygame.draw.rect(screen, colors[1], [252, 0, 216, 100])
            if len(heroes) > 1:
                heroes[1].blurtStats(font, (257, 5))
        if highlight == 2:
            pygame.draw.rect(screen, colors[2], [469, 0, 216, 120])
            if len(heroes) > 2:
                heroes[2].blurtStats(font, (474, 25))
        else:
            pygame.draw.rect(screen, colors[2], [469, 0, 216, 100])
            if len(heroes) > 2:
                heroes[2].blurtStats(font, (474, 5))

    @staticmethod
    def printCoords(coordinates, enemies, highlight=-1, attacking=-1):
        rects = []
        for y in range(len(coordinates[0])):
            rec = []
            for x in range(4):
                if coordinates[x][y] == -1:
                    rec.append(None)
                else:
                    color = enemies[coordinates[x][y]].healthColor()
                    if highlight == coordinates[x][y]:
                        color = WHITE
                    rec.append(pygame.draw.rect(screen, color, [160 + (x * 100), 250 + (y * 100), 100, 100]))
            rects.append(rec)

        for y in range(len(coordinates[0])):
            for x in range(4):
                if coordinates[x][y] != -1:
                    if enemies[coordinates[x][y]].size == 1:
                        try:
                            im = pygame.transform.flip(enemies[coordinates[x][y]].generateImage(), attacking==coordinates[x][y], False)
                            screen.blit(im, (
                                rects[y][x].x - (im.get_size()[0] / 4), rects[y][x].y - (im.get_size()[1] * 3 / 5)))
                        except:
                            screen.blit(pygame.image.load("GameArt\Placeholders\PlaceholderSize1.png"),
                                        (rects[y][x].x, rects[y][x].y))
                    elif enemies[coordinates[x][y]].size == 2:
                        if x == len(coordinates) - 1 or coordinates[x + 1][y] != coordinates[x][y]:
                            try:
                                im = pygame.transform.flip(enemies[coordinates[x][y]].generateImage(), attacking==coordinates[x][y], False)
                                screen.blit(im, (rects[y][x].x - im.get_size()[1], rects[y][x].y - im.get_size()[0]))
                            except:
                                screen.blit(pygame.image.load("GameArt\Placeholders\PlaceholderSize2.png"),
                                            (rects[y][x].x - 100, rects[y][x].y))
                    elif enemies[coordinates[x][y]].size == 3:
                        if y == len(coordinates[0]) - 1 or coordinates[x][y + 1] != coordinates[x][y]:
                            try:
                                im = pygame.transform.flip(enemies[coordinates[x][y]].generateImage(), attacking==coordinates[x][y], False)
                                screen.blit(im, (rects[y][x].x - im.get_size()[1], rects[y][x].y - im.get_size()[0]))
                            except:
                                screen.blit(pygame.image.load("GameArt\Placeholders\PlaceholderSize3.png"),
                                            (rects[y][x].x, rects[y][x].y - 100))
                    else:
                        if y == len(coordinates[0]) - 1 or coordinates[x][y + 1] != coordinates[x][y]:
                            if x == len(coordinates) - 1 or coordinates[x + 1][y] != coordinates[x][y]:
                                try:
                                    im = pygame.transform.flip(enemies[coordinates[x][y]].generateImage(), attacking==coordinates[x][y], False)
                                    screen.blit(im,
                                                (rects[y][x].x - im.get_size()[1], rects[y][x].y - im.get_size()[0]))
                                except:
                                    screen.blit(pygame.image.load("GameArt\Placeholders\PlaceholderSize4.png"),
                                                (rects[y][x].x - 100, rects[y][x].y - 100))

    @staticmethod
    def flavorText(string):
        pygame.draw.rect(screen, WHITE, [5, 536, 706, 150])
        font = pygame.font.SysFont('Arial', 25)
        x = 0
        while len(string) > 0:
            if len(string) >= 60:
                screen.blit(font.render(string[0:60], True, (255, 0, 0)), (12, 550+(x*30)))
                string = string[60:]
            else:
                screen.blit(font.render(string, True, (255, 0, 0)), (12, 550+(x*30)))
                string = ""
            x += 1
        pygame.display.update()

    @staticmethod
    def printScreen(coordinates, enemies, heroes, attacking=-1):
        screen.fill(BLACK)  # 4 sets of 165

        Fightable.printCoords(coordinates, enemies, attacking, attacking)
        Fightable.printHeroes(heroes)

        pygame.display.update()

    @staticmethod
    def ask():
        screenshot = screen.copy()
        rects = [pygame.image.load("GameArt\Buttons\Fight.png"), pygame.image.load("GameArt\Buttons\Defend.png"),
                 pygame.image.load("GameArt\Buttons\Special.png"), pygame.image.load("GameArt\Buttons\Item.png")]
        screen.blit(pygame.transform.scale(rects[0], (rects[0].get_size()[0] * 3 / 2, rects[0].get_size()[1] * 3 / 2)),
                    (312, 565))
        screen.blit(rects[2], (257, 618.75))
        screen.blit(rects[1], (332, 637))
        screen.blit(rects[3], (410, 618.75))
        highlighted = rects[0]
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        highlighted = rects[0]
                        screen.blit(screenshot, (0, 0))
                        screen.blit(pygame.transform.scale(rects[0], (
                            rects[0].get_size()[0] * 3 / 2, rects[0].get_size()[1] * 3 / 2)), (312, 565))
                        screen.blit(rects[1], (332, 637))
                        screen.blit(rects[2], (257, 618.75))
                        screen.blit(rects[3], (410, 618.75))
                    elif event.key == pygame.K_DOWN:
                        highlighted = rects[1]
                        screen.blit(screenshot, (0, 0))
                        screen.blit(rects[0], (332, 587))
                        screen.blit(pygame.transform.scale(rects[1], (
                            rects[1].get_size()[0] * 3 / 2, rects[1].get_size()[1] * 3 / 2)), (312, 650))
                        screen.blit(rects[2], (257, 618.75))
                        screen.blit(rects[3], (410, 618.75))
                    elif event.key == pygame.K_LEFT:
                        highlighted = rects[2]
                        screen.blit(screenshot, (0, 0))
                        screen.blit(rects[0], (332, 587))
                        screen.blit(rects[1], (332, 637))
                        screen.blit(pygame.transform.scale(rects[2], (
                            rects[2].get_size()[0] * 3 / 2, rects[2].get_size()[1] * 3 / 2)), (220, 605))
                        screen.blit(rects[3], (410, 618.75))
                    elif event.key == pygame.K_RIGHT:
                        highlighted = rects[3]
                        screen.blit(screenshot, (0, 0))
                        screen.blit(rects[0], (332, 587))
                        screen.blit(rects[1], (332, 637))
                        screen.blit(rects[2], (257, 618.75))
                        screen.blit(pygame.transform.scale(rects[3], (
                            rects[3].get_size()[0] * 3 / 2, rects[3].get_size()[1] * 3 / 2)), (410, 605))
                    if event.key == pygame.K_RETURN:
                        screen.blit(screenshot, (0, 0))
                        pygame.display.update()
                        if highlighted == rects[0]:
                            return "fight"
                        if highlighted == rects[1]:
                            return "defend"
                        if highlighted == rects[2]:
                            return "special"
                        return "item"
            pygame.display.update()

    @staticmethod
    def combat(heroes, enemies):
        global inventory
        trySize = 0
        while (trySize + 1) * 4 < Fightable.area(enemies):
            trySize += 1
        coordinates = None
        while coordinates is None:
            trySize += 1
            coordinates = [[], [], [], []]
            for o in range(0, trySize):
                for t in range(0, 4):
                    coordinates[t].append(-1)
            tries = 0
            j = 0
            while j < len(enemies) and tries < 5000:
                e = enemies[j]
                if e.size == 1:
                    x = -1
                    y = -1
                    attempts = 0
                    while x == -1 and attempts < 50:
                        x = randint(0, len(coordinates) - 1)
                        y = randint(0, len(coordinates[0]) - 1)
                        if coordinates[x][y] == -1:
                            coordinates[x][y] = j
                        else:
                            x = -1
                            y = -1
                        attempts += 1
                    if (x == -1):
                        coordinates = [[], [], [], []]
                        for o in range(0, trySize):
                            for t in range(0, 4):
                                coordinates[t].append(-1)
                        tries += 1
                        j = -1
                elif (e.size == 2):
                    x = -1
                    y = -1
                    attempts = 0
                    while (x == -1 and attempts < 50):
                        attempts += 1
                        x = randint(0, len(coordinates) - 1)
                        y = randint(0, len(coordinates[0]) - 1)
                        if (coordinates[x][y] == -1):
                            if (x - 1 > 0):
                                if (x + 1 < len(coordinates)):
                                    first = -1
                                    if (randint(0, 1) == 1):
                                        first = 1
                                    if (coordinates[x + first][y] == -1):
                                        coordinates[x][y] = j
                                        coordinates[x + first][y] = j
                                    elif (coordinates[x + (first * -1)][y] == -1):
                                        coordinates[x][y] = j
                                        coordinates[x + (first * -1)][y] = j
                                    else:
                                        x = -1
                                else:
                                    if (coordinates[x - 1][y] == -1):
                                        coordinates[x][y] = j
                                        coordinates[x - 1][y] = j
                                    else:
                                        x = -1
                            else:
                                if (coordinates[x + 1][y] == -1):
                                    coordinates[x][y] = j
                                    coordinates[x + 1][y] = j
                                else:
                                    x = -1
                        else:
                            x = -1
                            y = -1
                    if (x == -1):
                        coordinates = [[], [], [], []]
                        for o in range(0, trySize):
                            for t in range(0, 4):
                                coordinates[t].append(-1)
                        tries += 1
                        j = -1
                elif (e.size == 3):
                    x = -1
                    y = -1
                    potentials = []
                    for d in range(0, len(coordinates)):
                        for f in range(0, len(coordinates[0]) - 1):
                            potentials.append([d, f])
                    while x == -1 and y == -1 and len(potentials) > 0:
                        attempt = potentials.pop(randint(0, len(potentials) - 1))
                        if coordinates[attempt[0]][attempt[1]] == -1 and coordinates[attempt[0]][attempt[1] + 1] == -1:
                            x = attempt[0]
                            y = attempt[1]
                    if x != -1:
                        coordinates[x][y] = j
                        coordinates[x][y + 1] = j
                    else:
                        coordinates = [[], [], [], []]
                        for o in range(0, trySize):
                            for t in range(0, 4):
                                coordinates[t].append(-1)
                        tries += 1
                        j = -1
                elif e.size == 4:
                    x = -1
                    y = -1
                    potentials = []
                    for d in range(0, len(coordinates) - 1):
                        for f in range(0, len(coordinates[0]) - 1):
                            potentials.append([f, f + 1, d, d + 1])
                    while (x == -1 and y == -1 and len(potentials) > 0):
                        attempt = potentials.pop(randint(0, len(potentials) - 1))
                        if (coordinates[attempt[2]][attempt[0]] == -1 and coordinates[attempt[3]][attempt[0]] == -1 and
                                coordinates[attempt[2]][attempt[1]] == -1 and coordinates[attempt[3]][
                                    attempt[1]] == -1):
                            x = attempt[2]
                            y = attempt[0]
                    if (x != -1):
                        coordinates[x][y] = j
                        coordinates[x][y + 1] = j
                        coordinates[x + 1][y] = j
                        coordinates[x + 1][y + 1] = j
                    else:
                        coordinates = [[], [], [], []]
                        for o in range(0, trySize):
                            for t in range(0, 4):
                                coordinates[t].append(-1)
                        tries += 1
                        j = -1
                j += 1
            if tries == 5000:
                coordinates = None

        while Fightable.totalHealth(heroes) > 0 and Fightable.totalHealth(enemies) > 0:
            Fightable.printScreen(coordinates, enemies, heroes)
            screenshot = screen.copy()
            gamePlanH = []
            gamePlanE = []
            for x in range(len(heroes)):
                Fightable.printHeroes(heroes, x)
                zoop = screen.copy()
                pygame.display.update()
                who = heroes[x]
                if who.health > 0:
                    for y in range(0, (who.agility / 10) + 1):
                        deciding = True
                        while deciding:
                            screen.blit(zoop, (0, 0))
                            Fightable.printHeroes(heroes, x)
                            what = Fightable.ask()
                            if what == "fight":
                                w = Fightable.selectFromCoords(coordinates, enemies, "Single")
                                if w[0] != -1:
                                    gamePlanH.append("H {} Attack {}".format(x, w[0]))
                                    deciding = False
                            elif what == "defend":
                                Fightable.flavorText(who.name + " takes a defensive stance!")
                                sleep(1)
                                screen.blit(screenshot, (0, 0))
                                who.oneAndDone(StatusEffect("", "", ["defense"], [int(ceil(who.maxDefense*(2.0/3.0)))], 1))
                                deciding = False
                                gamePlanH.append("H {} Defend".format(x))
                            elif what == "special":
                                if (len(who.moves) > 0):
                                    choosing = True
                                    while (choosing):
                                        moves = []
                                        moves.append(Fightable.printHeroes(
                                            heroes, x) + "\n\nWhich technique?")
                                        for m in range(0, len(who.moves)):
                                            moves.append(who.moves[m].name)
                                        moves.append("Nevermind")
                                        move = ask(moves) - 1
                                        clear()
                                        if (move != len(moves) - 1):
                                            hi = Fightable.selectFromCoords(coordinates, enemies,
                                                                            heroes[x].moves[move].target)
                                            clear()
                                            if (hi[0] != -1):
                                                gamePlanH.append("H " + str(x) + " Move " + str(move) + "-" + str(hi))
                                                deciding = False
                                                choosing = False
                                        else:
                                            choosing = False
                                else:
                                    print("No known techniques.")
                                    clearI()
                            elif what == "item":
                                if (len(inventory) > 0):
                                    item = checkList(inventory)
                                    screen.blit(screenshot, (0, 0))
                                    if item != None:
                                        deciding = not(useItem(item, who))
                                        if not deciding:
                                            inventory.remove(item)
                                else:
                                    Fightable.flavorText("Inventory is empty.")
                                    sleep(1)
                else:
                    Fightable.flavorText(who.name + " is unconscious!")
                    sleep(1)
                    screen.blit(screenshot, (0, 0))
                screen.blit(screenshot, (0, 0))
                pygame.display.update()
                strings = who.sufferEffects()
                print strings
                for s in strings:
                    for t in s:
                        Fightable.flavorText(t)
                        sleep(1.5)
                screen.blit(screenshot, (0, 0))
            for x in range(len(enemies)):
                en = enemies[x]
                if en.health > 0:
                    who = None
                    while who is None:
                        who = random.choice(heroes)
                        if (who.health <= 0):
                            who = None
                    if en.hasMovesLeft() and randint(0, 2) == 1:
                        move = -1
                        while (move == -1):
                            move = randint(0, len(en.moves - 1))
                            if (en.moves[move].left() == 0):
                                move = -1
                        gamePlanE.append("E " + str(x) + " Move " + move + "-" + heroes.index(who))
                    else:
                        gamePlanE.append("E " + str(x) + " Attack " + str(heroes.index(who)))

            combinedGamePlan = []

            speeds = []
            for c in range(0, len(gamePlanH)):
                index = int(gamePlanH[c][2:3])
                speeds.append(heroes[index].agility)
                if (speeds[c] > 10):
                    if (c > 0):
                        divisions = 0
                        while (c - divisions > 0 and int(gamePlanH[c - divisions][2:3]) == int(gamePlanH[c][2:3])):
                            divisions += 1
                        divisions -= 1
                        if (divisions > 0):
                            speeds[c] = speeds[c] - (divisions * 10)
                    else:
                        speeds[c] = 10
                if (speeds[c] == 0):
                    speeds[c] = 1
                speeds[c] *= 1000
                speeds[c] += c
            for c in range(0, len(speeds) - 1):
                if (speeds[c] < speeds[c + 1]):
                    hold = speeds[c]
                    speeds[c] = speeds[c + 1]
                    speeds[c + 1] = hold
                    c -= 2
                    if (c < -1):
                        c = -1
            newGamePlanH = []
            for c in range(0, len(speeds)):
                newGamePlanH.append(gamePlanH[(speeds[c] % 1000)])
            gamePlanH = newGamePlanH

            while len(gamePlanH) > 0 or len(gamePlanE) > 0:
                if len(gamePlanH) > 0:
                    if len(gamePlanE) > 0:
                        s1 = heroes[int(gamePlanH[0][2:3])].agility
                        s2 = enemies[int(gamePlanE[0][2:3])].agility
                        if s1 > s2:
                            combinedGamePlan.append(gamePlanH.pop(0))
                        elif s1 < s2:
                            combinedGamePlan.append(gamePlanE.pop(0))
                        else:
                            if randint(0, 1) == 1:
                                combinedGamePlan.append(gamePlanH.pop(0))
                            else:
                                combinedGamePlan.append(gamePlanE.pop(0))
                    else:
                        combinedGamePlan.append(gamePlanH.pop(0))
                else:
                    combinedGamePlan.append(gamePlanE.pop(0))

            undefend = []
            for x in range(0, len(combinedGamePlan)):
                Fightable.printScreen(coordinates, enemies, heroes)
                pygame.display.update()
                screenshot = screen.copy()
                action = combinedGamePlan[x]
                print action
                if action[0:1] == "H":
                    who = heroes[int(action[2:3])]
                    Fightable.printHeroes(heroes, int(action[2:3]))
                    pygame.display.update()
                    if who.health > 0:
                        if("Attack" in action):
                            eWho = enemies[int(action[(action.index("Attack") + 7):])]
                            if (eWho.health > 0):
                                Fightable.printHeroes(heroes, heroes.index(who))
                                Fightable.flavorText(who.name + " " + who.weapon.verb + " " + who.gender.posAdj + " "
                                                     + who.weapon.name + " at " + eWho.title + eWho.name)
                                pygame.display.update()
                                if (randint(0, 99) < eWho.agility):
                                    sleep(1.25)
                                    Fightable.flavorText(eWho.title.capitalize() + eWho.name + " dodges the attack!")
                                    pygame.display.update()
                                    sleep(1.5)
                                    screen.blit(screenshot, (0, 0))
                                    pygame.display.update()
                                else:
                                    amount = who.fightT() - eWho.defense
                                    if (amount <= 0):
                                        amount = 1
                                    eWho.health += (amount * -1)
                                    Fightable.printCoords(coordinates, enemies)
                                    screenshot = screen.copy()
                                    Fightable.printCoords(coordinates, enemies, enemies.index(eWho))
                                    other = screen.copy()
                                    screen.blit(screenshot, (0, 0))
                                    pygame.display.update()
                                    for b in range(0, 5):
                                        if (3 % (b + 1) == 0):
                                            screen.blit(other, (0, 0))
                                        else:
                                            screen.blit(screenshot, (0, 0))
                                        pygame.display.update()
                                        sleep(.1)

                                    dead = ""
                                    print eWho.health
                                    if (eWho.health <= 0):
                                        dead = (eWho.title.capitalize() + eWho.name + " has been defeated!")
                                        for e in range(0, len(coordinates)):
                                            for w in range(0, len(coordinates[0])):
                                                if (coordinates[e][w] == int(action[(action.index("Attack") + 7):])):
                                                    coordinates[e][w] = -1
                                    Fightable.flavorText(eWho.title.capitalize() + eWho.name + " takes {} damage! ".format(amount) + dead)
                                    pygame.display.update()
                                    sleep(1.5)
                                    if dead != "":
                                        sleep(.25)
                                        for x in coordinates:
                                            for y in x:
                                                if y == enemies.index(eWho):
                                                    y = -1
                                        Fightable.printCoords(coordinates, enemies)
                                    Fightable.printScreen(coordinates, enemies, heroes)
                                    pygame.display.update()
                            else:
                                Fightable.flavorText(who.name + "'s target is already dead...")
                                pygame.display.update()
                                sleep(1.5)
                                screen.blit(screenshot, (0, 0))
                                pygame.display.update()
                        elif("Move" in action):
                            move = who.moves[int(action[9:10])]
                            Fightable.flavorText(who.name + " uses " + move.name + "!")
                            targets = action[action.index("[") + 1:len(action) - 1]
                            targs = []
                            happenstances = ""
                            while (len(targets) > 0):
                                targ = None
                                if move.statusEffects[0].stats[0] < 0:
                                    if (targets.index(",") != -1):
                                        targ = enemies[int(targets[0:targets.index(",")])]
                                        targets = targets[targets.index(" ") + 1:]
                                    else:
                                        targ = enemies[int(targets)]
                                        targets = ""
                                    if (targ.health > 0):
                                        for s in range(0, len(move.statusEffects())):
                                            st = move.statusEffects()[s]
                                            happenstances += "\n" + targ.getEffect(move) + "\n"
                                        if (targ.health <= 0):
                                            happenstances += (targ.name + " has been defeated!\n\n")
                                            for e in range(0, len(coordinates)):
                                                for w in range(0, len(coordinates[0])):
                                                    if (coordinates[e][w] == enemies.index(targ)):
                                                        coordinates[e][w] = -1
                                        targs.append(enemies.index(targ))
                                        clear()
                                        print(Fightable.printHeroes(
                                            heroes) + "\n\n" + who.name + " uses " + move.name + "!\n" + happenstances)
                                        sleep(200)
                                        clear()
                                        print(Fightable.printHeroes(
                                            heroes) + "\n" + who.name + " uses " + move.name + "!\n\n" + happenstances)
                                        sleep(200)
                                else:
                                    pass
                        elif("Defend" in action):
                            Fightable.flavorText(who.name + " has " + who.gender.posAdj + " guard up!")
                            undefend.append(who)
                            sleep(.6)
                            screen.blit(screenshot, (0, 0))
                    else:
                        Fightable.flavorText(who.name + " is unconscious!")
                        sleep(1)
                        screen.blit(screenshot, (0, 0))
                else:
                    who = enemies[(int(action[2:3]))]
                    screen.blit(screenshot, (0, 0))
                    who.sufferEffects()
                    if who.health > 0:
                        if "Attack" in action:
                            hWho = heroes[int(action[(action.index("Attack") + 7):])]
                            if hWho.health > 0:
                                Fightable.printCoords(coordinates, enemies, [enemies.index(who)])
                                Fightable.flavorText(who.title.capitalize() + who.name + " " + who.verb + " at " + hWho.name)
                                pygame.display.update()
                                sleep(1.5)
                                screen.blit(screenshot, (0, 0))
                                pygame.display.update()
                                sleep(.005)
                                Fightable.printScreen(coordinates, enemies, heroes, enemies.index(who))
                                pygame.display.update()
                                sleep(.1)
                                screen.blit(screenshot, (0, 0))
                                pygame.display.update()
                                if (randint(0, 99) < hWho.agility):
                                    Fightable.flavorText(hWho.name + " dodges the attack!")
                                    pygame.display.update()
                                else:
                                    amount = who.fight - hWho.defenseT()
                                    if (amount <= 0):
                                        amount = 1
                                    hWho.health += (amount * -1)
                                    Fightable.printScreen(coordinates, enemies, heroes)
                                    screenshot = screen.copy()
                                    for b in range(5):
                                        if (3 % (b + 1) == 1):
                                            Fightable.printHeroes(heroes, yellow=heroes.index(hWho))
                                        else:
                                            Fightable.printHeroes(heroes)
                                        pygame.display.update()
                                        sleep(.1)
                                    Fightable.flavorText(hWho.name + " takes {} damage!".format(amount))
                                    pygame.display.update()
                                    sleep(1.5)
                                    if (hWho.health <= 0):
                                        Fightable.flavorText(hWho.name + " has fainted!")
                                        pygame.display.update()
                                        sleep(1.5)
                                    screen.blit(screenshot, (0, 0))
                                    pygame.display.update()
                            else:
                                Fightable.flavorText(who.title.capitalize() + who.name + "'s target is already down...")
                                sleep(2)
                        elif "Move" in action:
                            pass
                        else:
                            pass

            for h in undefend:
                h.defense -= int(ceil(h.maxDefense *(2.0/3.0)))

        if Fightable.totalHealth(heroes) <= 0:
            fadeToBlack()
            pygame.mixer.music.fadeout(800)
            pygame.mixer.music.stop()
            pygame.mixer.music.load("GameMusic\GameOver.wav")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pass
            pygame.mixer.music.stop()
            pygame.mixer.music.load("GameMusic\GameOverIdle.wav")
            pygame.mixer.music.play(-1)
            return False



class Hero(Fightable):
    def __init__(self, name, moves, leveling, caste, gender, weapon, armor):
        super(Hero, self).__init__(name, 0, 0, 0, 0, moves)
        self._leveling = leveling
        self._caste = caste
        self._inventory = []
        self._level = 0
        self.levelUp()
        self.health = self.maxHealth
        self.setGender(gender)
        self._weapon = weapon
        self._armor = armor

    def setGender(self, g):
        if g == 1:
            self.gender = Gender("male", "he", "him", "his", "his", "himself")
        elif g == 2:
            self.gender = Gender("female", "she", "her", "her", "hers", "herself")
        else:
            self.gender = Gender("you", "you", "you", "your", "yours", "yourself")

    @property
    def caste(self):
        return self._caste

    @caste.setter
    def caste(self, value):
        self._caste = value

    @property
    def inventory(self):
        return self._inventory

    @inventory.setter
    def inventory(self, value):
        self._inventory = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def leveling(self):
        return self._leveling

    @leveling.setter
    def leveling(self, value):
        self._leveling = value

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        self._gender = value

    @property
    def weapon(self):
        return self._weapon

    @weapon.setter
    def weapon(self, value):
        self._weapon = value

    @property
    def armor(self):
        return self._armor

    @armor.setter
    def armor(self, value):
        self._armor = value

    def fightT(self):
        return self.fight + self.weapon.fight

    def defenseT(self):
        return self.defense + self.armor.defense

    def levelUp(self):
        self.level += 1
        self.maxHealth += (self.leveling[0][self.level - 1])
        self.maxFight += (self.leveling[1][self.level - 1])
        self.maxDefense += (self.leveling[2][self.level - 1])
        self.maxAgility += (self.leveling[3][self.level - 1])
        if len(self.learnableMoves) > 0 and self.level % (10 / len(self.learnableMoves)) == 0:
            m = self.learnableMoves[self.level / (10 / len(self.learnableMoves)) - 1]
            print(self.name + " has learned the new skill: " + m.name + ".")
            self.moves.append(m)

    def revert(self):
        self.fight = self.maxFight
        self.defense = self.maxDefense
        self.agility = self.maxAgility

    def blurtStats(self, font, coords):
        screen.blit(font.render(self.name + " | " + self.caste, True, (255, 0, 0)), coords)
        screen.blit(font.render("{}/{} HP".format(self.health, self.maxHealth), True, (255, 0, 0)),
                    (coords[0], coords[1] + 30))
        string = ""
        for x in self.statusEffects:
            string += x.name[0]
        screen.blit(font.render(string, True, (255, 0, 0)), (coords[0], coords[1] + 60))

    def __str__(self):
        string = self.name + ", " + self.caste + "\n"
        string += "Level " + str(self.level) + "\n"
        string += "Health: " + str(self.health) + "/" + str(self.maxHealth) + "\n"
        string += "Fight: " + str(self.fight)
        if self.fight != self.maxFight:
            string += "/" + str(self.maxFight)
            string += "\n"
        string += "Defense: " + str(self.defense)
        if self.defense != self.maxDefense:
            string += "/" + str(self.maxDefense)
        string += "\n"
        string += "Agility: " + str(self.agility)
        if self.agility != self.maxAgility:
            string += "/" + str(self.maxAgility)
        string += "\n"
        return string


class Enemy(Fightable):
    def __init__(self, name, desc, verb, title, health, fight, defense, agility, moves, drops, size, imageFolder,
                 appearance=[], gender=Gender("none", "it", "it", "its", "its", "itself")):
        super(Enemy, self).__init__(name, fight, defense, agility, health, moves)
        self._verb = verb
        self._title = title
        self._drops = drops
        self._desc = desc
        self._size = size
        self._imageFolder = imageFolder
        self.gender = gender
        self.appearance = appearance

    @property
    def verb(self):
        return self._verb

    @verb.setter
    def verb(self, value):
        self._verb = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def drops(self):
        return self._drops

    @drops.setter
    def drops(self, value):
        self._drops = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value

    def clone(self):
        return Enemy(self.name, self.desc, self.verb, self.title, self.health, self.fight, self.defense, self.agility,
                     self.moves, self.drops, self.size, self._imageFolder);

    def generateImage(self):
        # This code is gonna be horrible
        if self.name == "gnoll":
            color = randint(1, 3)
            goTo = []
            if self.appearance == []:
                goTo.append(color)
            else:
                color = self.appearance[0]
            image = pygame.image.load("GameArt\Gnoll\Color{} Gnoll\Body.png".format(color))
            image.blit(pygame.image.load("GameArt\Gnoll\Color{} Gnoll\Head1.png".format(color)), (0, 0))
            mane = randint(1, 2)
            if self.appearance == []:
                goTo.append(mane)
            else:
                mane = self.appearance[1]
            image.blit(pygame.image.load("GameArt\Gnoll\Color{} Gnoll\Mane{}.png".format(color, mane)), (0, 0))
            chin = randint(1, 2)
            chest = randint(1, 2)
            if self.appearance == []:
                goTo.append(chin)
            else:
                chin = self.appearance[2]
            if self.appearance == []:
                goTo.append(chest)
            else:
                chest = self.appearance[3]
            if chin == 1:
                image.blit(pygame.image.load("GameArt\Gnoll\Markings\Head1Chin.png"), (0, 0))
            if chest == 1:
                image.blit(pygame.image.load("GameArt\Gnoll\Markings\Chest.png"), (0, 0))
            if chin == 1 and chest == 1:
                image.blit(pygame.image.load("GameArt\Gnoll\Markings\ChinChestMid.png"), (0, 0))
            spots = randint(1, 2)
            if self.appearance == []:
                goTo.append(spots)
            else:
                spots = self.appearance[4]
            if spots == 1:
                image.blit(pygame.image.load("GameArt\Gnoll\Markings\Head1HeadSpots.png"), (0, 0))
            spots = randint(1, 2)
            if self.appearance == []:
                goTo.append(spots)
            else:
                spots = self.appearance[5]
            if spots == 1:
                image.blit(pygame.image.load("GameArt\Gnoll\Markings\Spots1.png"), (0, 0))
            else:
                image.blit(pygame.image.load("GameArt\Gnoll\Markings\Spots2.png"), (0, 0))

            image = pygame.transform.scale(image, (175, 280))
            if self.appearance == []:
                self.appearance = goTo
            return image
        else:
            # return pygame.image.load(self._imageFolder)
            return None

    def __str__(self):
        string = self.name + "\n" + self.desc + "\n"
        string += "Health: " + str(self.health) + "/" + str(self.maxHealth) + "\n"
        string += "Fight: " + str(self.fight)
        if self.fight != self.maxFight:
            string += "/" + str(self.maxFight)
            string += "\n"
        string += "Defense: " + str(self.defense)
        if self.defense != self.maxDefense:
            string += "/" + str(self.maxDefense)
            string += "\n"
        string += "Agility: " + str(self.agility)
        if self.agility != self.maxAgility:
            string += "/" + str(self.maxAgility)
            string += "\n"
        return string


Map = Map()


def menu():
    font1 = pygame.font.SysFont('Arial', 90)
    font2 = pygame.font.SysFont('Arial', 60)
    selected = "start"
    bg_img = pygame.image.load("GameArt\Extra\menu.gif")
    men = True

    song = pygame.mixer.music.load("GameMusic\MainMenu.wav")
    pygame.mixer.music.play(-1)

    select = pygame.mixer.Sound("SoundFX\Select.wav")
    select.set_volume(.25)
    while men:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(select)
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    pygame.mixer.Sound.play(select)
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(select)
                    if selected == "start":
                        pygame.mixer.music.fadeout(1000)
                        fadeToBlack()
                        gameMap()
                        return
                    if selected == "quit":
                        pygame.quit()
                        quit()


        # Main Menu UI
        screen.blit(bg_img, bg_img.get_rect())
        title = font1.render("The Tower", False, BLACK)
        if selected == "start":
            text_start = font2.render("START", False, WHITE)
        else:
            text_start = font2.render("START", False, BLACK)
        if selected == "quit":
            text_quit = font2.render("QUIT", False, WHITE)
        else:
            text_quit = font2.render("QUIT", False, BLACK)

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        screen.blit(title, (WIDTH / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (WIDTH / 2 - (start_rect[2] / 2), 300))
        screen.blit(text_quit, (WIDTH / 2 - (quit_rect[2] / 2), 360))
        pygame.display.update()
        clock.tick(60)


def popup():
    font1 = pygame.font.SysFont('Arial', 75)
    font2 = pygame.font.SysFont('Arial', 60)
    selected = 1
    bg_img = pygame.image.load("GameArt\Extra\menu.gif")
    pop = True

    while pop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = 1
                elif event.key == pygame.K_DOWN:
                    selected = 2
                if event.key == pygame.K_RETURN:
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
    merchant = pygame.image.load("GameArt\Extra\Merch.gif")
    box = pygame.image.load("GameArt\Extra\Text.png")
    merch_rect = merchant.get_rect()
    font = pygame.font.SysFont('Arial', 30)
    text1 = font.render("Why, hello there stranger! Let me guess, you're here", False, BLACK)
    text2 = font.render("about the missing villager, right? I can tell. You", False, BLACK)
    text4 = font.render("wannabe heros had.", False, BLACK)
    text3 = font.render("have that same look in your eyes all the other", False, BLACK)
    i = 0
    global currentFloor
    while talk:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if i == 0:
                    text1 = font.render("Well, the villagers are here, but they're not the ", False, BLACK)
                    text2 = font.render("same as they were before. Yeenoghu, the beast", False, BLACK)
                    text3 = font.render("responsible for this tower, has already turned them", False, BLACK)
                    text4 = font.render("into the monsters that now live in this tower.", False, BLACK)
                    i += 1
                elif i == 1:
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
                    i += 1
                    text1 = font.render("Only way to break the curse is to kill Yennughu,", False, BLACK)
                    text2 = font.render("the creator the curse. But you have to fight your", False, BLACK)
                    text3 = font.render("way up for even the chance to fight him. If you want", False, BLACK)
                    text4 = font.render("some help though I may be of some assistance.", False, BLACK)
                    i += 1
                elif i == 4:
                    text1 = font.render("I may be rusty, but I still know some powerful", False, BLACK)
                    text2 = font.render("fighting techniques. I only have time to teach", False, BLACK)
                    text3 = font.render("you one though.", False, BLACK)
                    text4 = font.render("", False, BLACK)
                    i += 1
                elif i == 5:
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
                    text1 = font.render("That's all the help I can offer though. Don't", False, BLACK)
                    text2 = font.render("worry though, I'm sure you'll be able to pull", False, BLACK)
                    text3 = font.render("it off.", False, BLACK)
                    text4 = font.render("", False, BLACK)
                    i += 1
                elif i == 8:
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
    merchant = pygame.image.load("GameArt\Extra\Merch.gif")
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
    merchant = pygame.image.load("GameArt\Extra\Merch.gif")
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



def combatTest():
    enemyTest = Enemy("gnoll", "This is a test.", "lashes out", "the", 15, 4, 2, 2, [], [], 1, "Gnoll")
    enemyTest1 = Enemy("Placeholder Slime", "This is a test.", "burbles", "", 15, 4, 2, 2, [], [], 1, "Slime")
    enemyTest2 = Enemy("Placeholder Slime", "This is a test.", "burbles", "", 15, 4, 2, 2, [], [], 2, "Slime")
    enemyTest3 = Enemy("Placeholder Slime", "This is a test.", "burbles", "", 15, 4, 2, 2, [], [], 3, "Slime")
    enemyTest4 = Enemy("Placeholder Slime", "This is a test.", "burbles", "", 15, 4, 2, 2, [], [], 4, "Slime")
    test = Hero("Valor", [], [
        [10, 2, 2, 2, 2, 1, 3, 1, 3, 2, 4],
        [2, 0, 2, 0, 0, 1, 0, 2, 2, 3, 3],
        [1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 3],
        [1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 2]], "Knight", 1, battle_axe, leather)
    test1 = Hero("Gallant", [], [
        [10, 2, 2, 2, 2, 1, 3, 1, 3, 2, 4],
        [2, 0, 2, 0, 0, 1, 0, 2, 2, 3, 3],
        [1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 3],
        [1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 2]], "Knight", 1, bigger_sword, leather)

    for i in range(7):
        test.levelUp()
    test.revert()
    test.health = test.maxHealth

    Fightable.combat([test, test1], [enemyTest.clone(), enemyTest.clone()])


menu()


pygame.quit()
