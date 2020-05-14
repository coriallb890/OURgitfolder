from random import randint
import random
import pygame

pygame.init()  # start up dat pygame
pygame.font.init()
clock = pygame.time.Clock()  # for framerate or something? still not very sure
pygame.display.set_caption("The Tower")
WIDTH = 716
HEIGHT = 716
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # making the window
Done = False  # variable to keep track if window is open
MAPSIZE = 11  # how many tiles in either direction of grid

TILEWIDTH = 64  # pixel sizes for grid squares
TILEHEIGHT = 64
TILEMARGIN = 1

BLACK = (0, 0, 0)  # fill
WHITE = (255, 255, 255)  # floor

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


class Player(Special):  # The player
    def __init__(self, name, image, column, row, party):
        Special.__init__(self, name, image, column, row)
        self.party = party

    @property
    def party(self):
        return self._party

    @party.setter
    def party(self, value):
        if (value == 1 or value == 2):
            party = value

    def move(self, direction):  # This function is how a character moves around in a certain direction

        if self.collision(direction):
            return
        if direction == "UP" and self.row > 0:  # If within boundaries of grid
            self.row -= 1  # Go ahead and move

        elif direction == "LEFT" and self.column > 0:
            self.column -= 1

        elif direction == "RIGHT" and self.column < (MAPSIZE - 1):
            self.column += 1

        elif direction == "DOWN" and self.row < (MAPSIZE - 1):
            self.row += 1

        else:
            return -9

        Map.update()

    def collision(self, direction):  # Checks if anything is on top of the grass in the direction that the character wants to move. Used in the move function
        if direction == "UP":
            if len(Map.grid[self.column][(self.row) - 1]) > 1:
                return True
        elif direction == "LEFT":
            if len(Map.grid[self.column - 1][(self.row)]) > 1:
                return True
        elif direction == "RIGHT":
            if len(Map.grid[self.column + 1][(self.row)]) > 1:
                return True
        elif direction == "DOWN":
            if len(Map.grid[self.column][(self.row) + 1]) > 1:
                return True
        return False

    def location(self):
        print("Coordinates: " + str(self.column) + ", " + str(self.row))

currentFloor = f1

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
                tempTile = Special("Hill Giant", "GameArt\OverworldSprites\GiantSpriteTemp.gif", randColumn, randRow)
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


class StatusEffect:
    def __init__(self, name, verb, stats, amounts, turns):
        self._turns = turns
        self._name = name
        self._verb = verb
        self._stats = stats
        self._amounts = amounts

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def verb(self):
        return self.verb

    @verb.setter
    def verb(self, value):
        self._verb = value

    @property
    def stats(self):
        return self._stats

    @stats.setter
    def stats(self, value):
        self._stats = value

    @property
    def amounts(self):
        return self._amounts

    @amounts.setter
    def amounts(self, value):
        self._amounts = value

    @property
    def turns(self):
        return self._turns

    @turns.setter
    def turns(self, value):
        self._turns = value

    def doIt(self, who):
        if (self.turns > 0):
            for x in range(0, len(self.stats)):
                if (self.stats[x] == "health"):
                    who.health += (self.amounts[x])
                    verb = " loses "
                    if (self.amounts[x] >= 0):
                        verb = " gains "
                    plural = "s"
                    if (abs(self.amounts[x]) == 1):
                        plural = ""
                    print(who.name + verb + str(
                        abs(self.amounts[x])) + " hitpoint" + plural + " from the " + self.name + "!")
                elif (self.stats[x].equals("fight")):
                    who.fight += (self.amounts[x])
                    verb = ""
                    if (abs(self.amounts[x]) > 4):
                        verb = "greatly"
                    elif (abs(self.amounts[x]) <= 2):
                        verb = "slightly"
                    if (self.amounts[x] >= 0):
                        verb = " is " + verb + " strengthened "
                    else:
                        verb = " is " + verb + " weakened "
                    print(who.name + verb + "by the " + self.name + "!")
                elif (self.stats[x].equals("defense")):
                    who.changedefense += (self.amounts[x])
                    verb = ""
                    if (abs(self.amounts[x]) > 4):
                        verb = "greatly"
                    elif (abs(self.amounts[x]) <= 2):
                        verb = "slightly"
                    if (self.amounts[x] >= 0):
                        verb = "'s defenses are " + verb + " reinforced "
                    else:
                        verb = "'s defenses are " + verb + " diminished "
                    print(who.name + verb + "by the " + self.name + "!")
                elif (self.stats[x] == "agility"):
                    who.agility += (self.amounts[x])
                    verb = ""
                    if (abs(self.amounts[x]) > 4):
                        verb = "greatly"
                    elif (abs(self.amounts[x]) <= 2):
                        verb = "slightly"
                    if (self.amounts[x] >= 0):
                        verb = "'s speed is " + verb + " increased "
                    else:
                        verb = "'s speed is " + verb + " decreased "
                    print(who.name + verb + "by the " + self.name + "!")
            self.turns -= 1
        else:
            who.statusEffects().pop(self)

    def clone(self):
        return StatusEffect(self.name, self.verb, self.stat, self.amount, self.turns)


class Move:
    def __init__(self, name, target, uses, statusEffects):
        self._name = name
        self._target = target
        self._uses = uses
        self._left = uses
        self._statusEffects = statusEffects

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def uses(self):
        return self._uses

    @uses.setter
    def uses(self, value):
        self._uses = value

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    @property
    def statusEffects(self):
        return self._statusEffects

    @statusEffects.setter
    def statusEffects(self, value):
        self._statusEffects = value


class Gender:
    def __init__(self, name, subj, obj, posAdj, posPro, refl):
        self._name = name
        self._subj = subj
        self._obj = obj
        self._posAdj = posAdj
        self._posPro = posPro
        self._refl = refl

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def subj(self):
        return self._subj

    @subj.setter
    def subj(self, value):
        self._subj = value

    @property
    def obj(self):
        return self._obj

    @obj.setter
    def obj(self, value):
        self._obj = value

    @property
    def posAdj(self):
        return self._posAdj

    @posAdj.setter
    def posAdj(self, value):
        self._posAdj = value

    @property
    def posPos(self):
        return self._posPos

    @posPos.setter
    def posPos(self, value):
        self._posPos = value

    @property
    def refl(self):
        return self._refl

    @refl.setter
    def refl(self, value):
        self._refl = value


class Item(object):
    def __init__(self, name, cost, grade):
        self._name = name
        self._cost = cost
        self._grade = grade

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        self._cost = value

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        self._grade = value


class Weapon(Item):
    def __init__(self, name, cost, grade, fight, rang, accuracy, consistency, critRate):
        super(Weapon, self).__init__(name, cost, grade)
        self._fight = fight
        self._range = rang
        self._accuracy = accuracy
        self._consistency = consistency
        self._critRate = critRate

    @property
    def fight(self):
        return self._fight

    @fight.setter
    def fight(self, value):
        self._fight = value

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, value):
        self._range = value

    @property
    def accuracy(self):
        return self._accuracy

    @accuracy.setter
    def accuracy(self, value):
        self._accuracy = value

    @property
    def consistency(self):
        return self._consistency

    @consistency.setter
    def consistency(self, value):
        self._consistency = value

    @property
    def critRate(self):
        return self._critRate

    @critRate.setter
    def critRate(self, value):
        self._critRate = value


class Armor(Item):
    def __init__(self, name, cost, grade, defense, durabillity):
        super(Armor, self).__init__(name, cost, grade)
        self._defense = defense
        self._durabillity = durabillity

    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self, value):
        self._defense = value

    @property
    def durabillity(self):
        return self._durability

    @durabillity.setter
    def durability(self, value):
        self._durability = value


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
        if (value > -1):
            self._health = value

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
        blurb = ""
        x = 0
        while x < len(m.statusEffects()):
            x += 1
            if m.statusEffects()[x].turns() > 0:
                self.statusEffects.append(m.statusEffects()[x].clone())
                blurb += "{} has been {}".format(self.name, m.statusEffects()[x].verb)
            else:
                blurb += (self.oneAndDone(m.statusEffects()[x]))
        return blurb

    def oneAndDone(self, st):
        suffered = ""
        x = 0
        while x < len(st.stat()):
            if x != 0:
                suffered += "\n"

            if st.stat()[x] == "health":
                self.health += (st.amount()[x])
                verb = " loses "
                if st.amount()[x] >= 0:
                    verb = " gains "
                plural = "s"
                if abs(st.amount()[x]) == 1:
                    plural = ""
                suffered += self.name + verb + str(abs(st.amount()[x])) + " hitpoint" + plural + "!"

            elif st.stat()[x] == ("fight"):
                self.fight += (st.amount()[x])
                verb = ""
                if abs(st.amount()[x]) > 4:
                    verb = "greatly"
                elif abs(st.amount()[x]) <= 2:
                    verb = "slightly"
                if st.amount()[x] >= 0:
                    verb = " is " + verb + " strengthened"
                else:
                    verb = " is " + verb + " weakened"
                suffered += self.name + verb + "!"

            elif st.stat()[x] == ("defense"):
                self.defense += (st.amount()[x])
                verb = ""
                if abs(st.amount()[x]) > 4:
                    verb = "greatly"
                elif abs(st.amount()[x]) <= 2:
                    verb = "slightly"
                if st.amount()[x] >= 0:
                    verb = "'s defenses are " + verb + " reinforced"
                else:
                    verb = "'s defenses are " + verb + " diminished"
                suffered += self.name + self.verb + "!"

            elif st.stat()[x] == "agility":
                self.agility += (st.amount()[x])
                verb = ""
                if abs(st.amount()[x]) > 4:
                    verb = "greatly"
                elif abs(st.amount()[x]) <= 2:
                    verb = "slightly"
                if st.amount()[x] >= 0:
                    verb = "'s speed is " + verb + " increased"
                else:
                    verb = "'s speed is " + verb + " decreased"
                suffered += self.name + self.verb + "!"
            x += 1

        return suffered

    def sufferEffects(self):
        x = 0
        while x < len(self.statusEffects):
            self.statusEffects[x].doIt(self)
            x += 1

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
        return health

    @staticmethod
    def selectFromCoords(coords, enemies, target):
        highlight = [-1]
        highlighted = []
        while True:
            if target.find("Single") != -1:
                if len(highlighted) <= len(enemies):
                    y = 0
                    x = 0
                    while y < len(coords[0]) and highlight[0] == -1:
                        while x < len(coords) and highlight[0] == -1:
                            if coords[x][y] != -1 and coords[x][y] in highlighted:
                                highlighted.append(coords[x][y])
                                highlight = [coords[x][y]]
                            x += 1
                        y += 1
                else:
                    highlight = [-1]
            elif target.find("Vert Line") != -1:
                if len(highlighted) <= len(enemies):
                    highlight = []
                    unused = False
                    x = 0
                    while x < 4 and not (unused):
                        y = 0
                        while y < len(coords[0]) and not (unused):
                            if coords[x][y] != -1 and not (coords[x][y] in highlighted):
                                highlighted.append(coords[x][y])
                                unused = True
                            y += 1
                        x += 1
                    x -= 1
                    if (unused):
                        y = 0
                        while (y < len(coords[0])):
                            if (coords[x][y] != -1):
                                if (not ((coords[x][y]) in highlighted)):
                                    highlighted.append(coords[x][y])
                                highlight.append(coords[x][y])
                            y += 1
                    else:
                        highlight = [-1]
                else:
                    highlight = [-1]
            elif target.find("Hori Line") != -1:
                if len(highlighted) <= len(enemies):
                    highlight = []
                    unused = False
                    y = 0
                    while y < len(coords[0]) and not (unused):
                        x = 0
                        while x < len(coords) and not (unused):
                            if (coords[x][y] != -1 and not (coords[x][y] in highlighted)):
                                highlighted.append(coords[x][y])
                                unused = True
                            x += 1
                        y += 1
                    y -= 1
                    if (unused):
                        x = 0
                        while (x < len(coords)):
                            if (coords[x][y] != -1):
                                if (not (coords[x][y] in highlighted)):
                                    highlighted.append(coords[x][y])
                                highlight.append(coords[x][y])
                            x += 1
                    else:
                        highlight = [-1]
                else:
                    highlight = [-1]
            else:
                highlight = [-1]
            nev = "Back"
            if (highlight[0] == -1):
                nev = "\033[0;93mBack\033[0m"
            print(
                "Which enemy? (Press enter to scroll through options, type a key and press enter to select)\n{}\n\n{}".format(
                    Fightable.printCoords(coords, enemies, highlight), nev))
            if (not (raw_input() == "")):
                return highlight
            if (highlight[0] == -1):
                highlighted = []
            highlight = [-1]
            clear()

    @staticmethod
    def printHeroes(heroes):
        return Fightable.printHeroes(heroes, -1)

    @staticmethod
    def printHeroes(heroes, highlighted):
        string = " ------------------------------------------------ \n|"
        for x in range(0, 4):
            try:
                string += heroes[x].healthColorT()
                if (highlighted == x):
                    string += "\033[1;37m"
                string += heroes[x].name + "\033[0m"
                d = 0
                while (d < 11 - len(heroes[x].name)):
                    string += " "
                    d += 1
                if (x == 2):
                    string += " "
                string += "|"
            except:
                string += "\033[0m           "
                if (x == 2):
                    string += " "
                string += "|"
        string += "\n|"
        for x in range(0, 4):
            try:
                stats = str(heroes[x].health) + "/" + str(heroes[x].maxHealth) + " HP"
                string += heroes[x].healthColorT()
                if (highlighted == x):
                    string += "\033[1;37m"
                string += stats + "\033[0m"
                d = 0
                while (d < 11 - len(stats)):
                    string += " "
                    d += 1
                if (x == 2):
                    string += " "
                string += "|"
            except:
                string += "           "
                if (x == 2):
                    string += " "
                string += "|"
        string += "\n|           |           |           |            |\n"
        string += " ------------------------------------------------"
        return string

    @staticmethod
    def printCoordsS(coordinates, enemies):
        return Fightable.printCoords(coordinates, enemies, [-1])

    @staticmethod
    def printCoords(coordinates, enemies, highlight):
        printMe = " ------------------------------------------------"
        for z in range(0, len(coordinates[0])):
            printMe += "\033[00m"
            printMe += "\n|"
            for x in range(0, len(coordinates)):
                if (coordinates[x][z] != -1):
                    if (coordinates[x][z] in highlight):
                        printMe += "\033[0;93m"
                    else:
                        printMe += enemies[coordinates[x][z]].healthColor()
                    printedAName = False
                    if (x > 0):
                        if (coordinates[x - 1][z] != coordinates[x][z]):
                            printMe += "\033[0m"
                            printMe += "\b|"
                            if (coordinates[x][z] in highlight):
                                printMe += "\033[0;93m"
                            else:
                                printMe += enemies[coordinates[x][z]].healthColor()
                        else:
                            printMe += " "
                    if ((enemies[coordinates[x][z]]).size == 2):
                        if (x > 0):
                            if (coordinates[x - 1][z] != coordinates[x][z]):
                                printMe += enemies[coordinates[x][z]].name
                                printedAName = True
                            else:
                                printMe += "            "
                        else:
                            printMe += enemies[coordinates[x][z]].name
                            printedAName = True
                    elif (enemies[coordinates[x][z]].size == 3):
                        if (z > 0):
                            if (coordinates[x][z - 1] != coordinates[x][z]):
                                printMe += enemies[coordinates[x][z]].name
                                printedAName = True
                            else:
                                printMe += "            "
                        else:
                            printMe += enemies[coordinates[x][z]].name
                            printedAName = True
                    elif (enemies[coordinates[x][z]].size == 4):
                        if (x > 0 or z > 0):
                            if ((x < len(coordinates) - 1 and coordinates[x + 1][z] == coordinates[x][z]) and z < len(
                                    coordinates[0]) - 1 and coordinates[x][z + 1] == coordinates[x][z]):
                                printMe += enemies[coordinates[x][z]].name
                                printedAName = True
                            else:
                                if (z > 0 and coordinates[x][z] == coordinates[x][z - 1]):
                                    printMe += "            "
                                    if (x < len(coordinates) - 2 and coordinates[x][z] == coordinates[x + 1][z]):
                                        printMe += "\b"
                                else:
                                    printMe += "            "
                                    if (x > 0 and coordinates[x][z] == coordinates[x - 1][z] and x != len(
                                            coordinates) - 1):
                                        printMe += "\b"
                        else:
                            printMe += enemies[coordinates[x][z]].name
                            printedAName = True
                    else:
                        printMe += enemies[coordinates[x][z]].name
                        printedAName = True
                    if (printedAName):
                        y = 0
                        while (y < 11 - len(enemies[coordinates[x][z]].name)):
                            printMe += " "
                            y += 1

                    if (enemies[coordinates[x][z]].size == 2 or enemies[coordinates[x][z]].size == 4):
                        if (x == len(coordinates) - 1 or coordinates[x + 1][z] != coordinates[x][z]):
                            if (enemies[coordinates[x][z]].size == 4 and x > 0 and z > 0 and coordinates[x - 1][z] ==
                                    coordinates[x][z] and coordinates[x][z - 1] == coordinates[x][z]):
                                printMe += "\b"
                            elif (enemies[coordinates[x][z]].size == 2 and x != len(coordinates) - 1):
                                printMe += "\b"
                            printMe += "\033[0m"
                            printMe += "|"
                            if (coordinates[x][z] in highlight):
                                printMe += "\033[0;93m"
                            else:
                                printMe += enemies[coordinates[x][z]].healthColor()
                    if (enemies[coordinates[x][z]].size == 3):
                        if (x == len(coordinates) - 1 or coordinates[x + 1][z] != coordinates[x][z]):
                            if (x < len(coordinates) - 1 and z > 0 and coordinates[x][z - 1] == coordinates[x][z]):
                                printMe += "\b"
                            elif (x == len(coordinates) - 1 and (z == 0 or coordinates[x][z - 1] != coordinates[x][z])):
                                printMe += " "
                            printMe += "\033[0m"
                            printMe += "|"
                            if (coordinates[x][z] in highlight):
                                printMe += "\033[0;93m"
                            else:
                                printMe += enemies[coordinates[x][z]].healthColor()
                    elif (enemies[coordinates[x][z]].size == 1):
                        if (x == len(coordinates) - 1):
                            printMe += " "
                        printMe += "\033[0m"
                        printMe += "|"
                        if (coordinates[x][z] in highlight):
                            printMe += "\033[0;93m"
                        else:
                            printMe += enemies[coordinates[x][z]].healthColor()
                    printMe += "\033[0m"
                else:
                    printMe += "            "
            if (coordinates[len(coordinates) - 1][z] == -1):
                printMe += "|"
            printMe += "\n|"
            for x in range(0, len(coordinates)):
                if (x > 0):
                    if (coordinates[x - 1][z] != coordinates[x][z]):
                        printMe += "\033[0m"
                        printMe += "\b|"
                if (coordinates[x][z] != -1):
                    if (coordinates[x][z] in highlight):
                        printMe += "\033[0;93m"
                    else:
                        printMe += enemies[coordinates[x][z]].healthColor()
                printMe += "            "
                printMe += "\033[0m"
                if (x == len(coordinates) - 1 and coordinates[x][z] != -1):
                    printMe += " "
                if (coordinates[x][z] != -1 and (
                        enemies[coordinates[x][z]].size % 2 != 0 or x == len(coordinates) - 1)):
                    printMe += "\033[0m"
                    printMe += "\b|"
            if (coordinates[len(coordinates) - 1][z] == -1):
                printMe += "|"
            printMe += "\n"
            if (z == len(coordinates[0]) - 1):
                printMe += " ------------------------------------------------"
            else:
                printMe += "|"
                for x in range(0, len(coordinates)):
                    printMe += "\033[0m"
                    if (coordinates[x][z] != -1 and not (
                            (enemies[coordinates[x][z]].size == 3 or enemies[coordinates[x][z]].size == 4))):
                        printMe += "------------"
                    elif (z < len(coordinates[0]) - 1 and coordinates[x][z + 1] != -1 and coordinates[x][z] !=
                          coordinates[x][z + 1]):
                        printMe += "------------"
                    elif (coordinates[x][z] != -1 and (
                            enemies[coordinates[x][z]].size == 3 or enemies[coordinates[x][z]].size == 4) and
                          coordinates[x][z + 1] == -1):
                        printMe += "------------"
                    elif (coordinates[x][z] != -1 and enemies[coordinates[x][z]].size == 3 and coordinates[x][
                        z + 1] != -1):
                        printMe += "\033[0m"
                        printMe += "\b|"
                        if (coordinates[x][z] in highlight):
                            printMe += "\033[0;93m"
                        else:
                            printMe += enemies[coordinates[x][z]].healthColor()
                        printMe += "           "
                        if (x != len(coordinates) - 1):
                            printMe += "\033[0m"
                            printMe += "|"
                            if (coordinates[x][z] in highlight):
                                printMe += "\033[0;93m"
                            else:
                                printMe += enemies[coordinates[x][z]].healthColor()
                        else:
                            printMe += " "
                    elif (coordinates[x][z] != -1 and enemies[coordinates[x][z]].size == 4 and z < len(
                            coordinates[0]) - 1 and coordinates[x][z + 1] != -1):
                        if (x > 0 and coordinates[x - 1][z] != coordinates[x][z]):
                            printMe += "\033[0m"
                            printMe += "\b|"
                        if (coordinates[x][z] in highlight):
                            printMe += "\033[0;93m"
                        else:
                            printMe += enemies[coordinates[x][z]].healthColor()
                        printMe += "           "
                        if (x != len(coordinates) - 1 and coordinates[x + 1][z] != coordinates[x][z]):
                            printMe += "\033[0m"
                            printMe += "|"
                            if (coordinates[x][z] in highlight):
                                printMe += "\033[0;93m"
                            else:
                                printMe += enemies[coordinates[x][z]].healthColor()
                        else:
                            printMe += " "
                    else:
                        printMe += "            "
                printMe += "\033[0m"
                printMe += "|"
        return printMe

    @staticmethod
    def combat(heroes, enemies):
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
                        for f in range(0, len(coordinates[0])):
                            potentials.append([d, f])
                    while (x == -1 and y == -1 and len(potentials) > 0):
                        attempt = potentials.pop(randint(0, len(potentials) - 1))
                        if (coordinates[attempt[0]][attempt[1]] == -1 and coordinates[attempt[0]][
                            attempt[1] + 1] == -1):
                            x = attempt[0]
                            y = attempt[1]
                    if (x != -1):
                        coordinates[x][y] = j
                        coordinates[x][y + 1] = j
                    else:
                        coordinates = [[], [], [], []]
                        for o in range(0, trySize):
                            for t in range(0, 4):
                                coordinates[t].append(-1)
                        tries += 1
                        j = -1
                elif (e.size == 4):
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
            if (tries == 5000):
                coordinates = None

        while Fightable.totalHealth(heroes) > 0 and Fightable.totalHealth(enemies) > 0:
            while True:
                screen.fill(BLACK)  # 4 sets of 165
                starty = 150 - (len(coordinates[0]) - 1) * 35
                for x in range(0, len(coordinates[0])):
                    pygame.draw.rect(screen, WHITE,
                                     [157 + ((x % 2) * 50), ((len(coordinates[0]) - x) * 125) + starty, 400,
                                      100])
                font = pygame.font.SysFont('Arial', 25)
                pygame.draw.rect(screen, WHITE, [35, 0, 216, 100])
                heroes[0].blurtStats(font, (40, 5))
                pygame.draw.rect(screen, WHITE, [252, 0, 216, 100])
                if len(heroes) > 1:
                    heroes[1].blurtStats(font, (257, 5))
                pygame.draw.rect(screen, WHITE, [469, 0, 216, 100])
                if len(heroes) > 2:
                    heroes[2].blurtStats(font, (474, 5))

                screen.blit(enemies[0].generateImage(), (0, 0))

                pygame.display.update()

            gamePlanH = []
            gamePlanE = []
            for x in range(0, len(heroes)):
                who = heroes[x]
                who.sufferEffects()
                if who.health > 0:
                    for y in range(0, (who.agility / 10) + 1):
                        deciding = True
                        while (deciding):
                            times = ""
                            if (y == 1):
                                times = " second"
                            elif (y == 2):
                                times = " third"
                            elif (y == 3):
                                times = " fourth"
                            elif (y > 0):
                                times = " next"
                            what = -1
                            if (who.gender.subj == "you"):
                                what = ask([Fightable.printCoordsS(coordinates,
                                                                   enemies) + "\n\n" + Fightable.printHeroes(heroes,
                                                                                                             x) + "\n\nWhat should you do on your" + times + " turn?\n",
                                            "Check stats", "Attack", "Use Technique", "Use Item", "Defend", "Flee"])
                            else:
                                what = ask([Fightable.printCoordsS(coordinates,
                                                                   enemies) + "\n\n" + Fightable.printHeroes(heroes,
                                                                                                             x) + "\n\nWhat should " + who.name + " do on " + who.gender.posAdj + times + " turn?",
                                            "Check stats", "Attack", "Use Technique", "Use Item", "Defend"])
                            clear()
                            if (what == 1):
                                print who.toString()
                                clearI()
                            elif (what == 2):
                                w = Fightable.selectFromCoords(coordinates, enemies, "Single")
                                clear()
                                if (w[0] != -1):
                                    gamePlanH.append("H " + x + " Attack " + w[0])
                                    deciding = False
                            elif (what == 3):
                                if (len(who.moves) > 0):
                                    choosing = True
                                    while (choosing):
                                        moves = []
                                        moves.append(Fightable.printCoordsS(coordinates,
                                                                            enemies) + "\n\n" + Fightable.printHeroes(
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
                            elif (what == 4):
                                if (len(who.inventory()) > 0):
                                    inventory = ["Which item?"]
                                    for m in range(0, len(who.inventory())):
                                        inventory.append(who.inventory()[m].name)
                                    inventory.append("Nevermind")
                                    item = ask(inventory)
                                    clear()
                                    if item != len(inventory):
                                        gamePlanH.append("H " + str(x) + " Item " + item)
                                        deciding = False
                                else:
                                    print("That inventory is empty.")
                                    clearI()
                            elif (what == 5):
                                gamePlanH.append("H " + str(x) + " Defend")
                                deciding = False
                            else:
                                if (ask(["Flee the battle?", "Yes", "No"]) == 1):
                                    print("You attempt to flee the battle...")
                                    print("But that isn't implemented yet so you fail.")
                                    clearI()
                                    deciding = False
                                    x = 100
                                    y = 100
                                clear()
                else:
                    print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(heroes,
                                                                                                        x) + "\n\n")
                    print(who.name + " is unconscious!")
                    clearI()
            for x in range(0, len(enemies)):
                en = enemies[x]
                if (en.health > 0):
                    who = None
                    while (who == None):
                        who = choice(heroes)
                        if (who.health == 0):
                            who = None
                    if (en.hasMovesLeft() and randint(0, 2) == 1):
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

            for x in range(0, len(combinedGamePlan)):
                action = combinedGamePlan[x]
                if action[0:1] == "H":
                    who = heroes[int(action[2:3])]
                    print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(heroes,
                                                                                                        heroes.index(
                                                                                                            who)) + "\n")
                    who.sufferEffects()
                    sleep(500)
                    clear()
                    if who.health > 0:
                        if (action == ("Attack")):
                            eWho = enemies[int(action[(action.index("Attack") + 7):])]
                            if (eWho.health > 0):
                                print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(
                                    heroes, heroes.index(who)) + "\n")
                                print(
                                        who.name + " " + who.weapon.verb + " " + who.gender.posAdj + " " + who.weapon.name + " at " + eWho.title + eWho.name)
                                sleep(500)
                                if (randint(0, 99) < eWho.agility):
                                    print(eWho.name + " dodges the attack!")
                                    clearI()
                                else:
                                    clear()
                                    for b in range(0, 3):
                                        if (3 % (b + 1) == 0):
                                            print(Fightable.printCoords(coordinates, enemies, [
                                                enemies.index(eWho)]) + "\n\n" + Fightable.printHeroes(heroes,
                                                                                                       heroes.index(
                                                                                                           who)) + "\n\n" + who.name + " " + who.weapon.verb + " " + who.gender.posAdj + " " + who.weapon.name + " at " + eWho.title + eWho.name)
                                        else:
                                            print(Fightable.printCoordsS(coordinates,
                                                                         enemies) + "\n\n" + Fightable.printHeroes(
                                                heroes, heroes.index(
                                                    who)) + "\n\n" + who.name + " " + who.weapon.verb + " " + who.gender.posAdj + " " + who.weapon.name + " at " + eWho.title + eWho.name)
                                        sleep(100)
                                        clear()

                                    amount = who.fight - eWho.defense
                                    if (amount <= 0):
                                        amount = 1
                                    eWho.health += (amount * -1)
                                    dead = ""
                                    if (eWho.health <= 0):
                                        dead = ("\n" + eWho.name + " has been defeated!")
                                        for e in range(0, len(coordinates)):
                                            for w in range(0, len(coordinates[0])):
                                                if (coordinates[e][w] == int(action[(action.index("Attack") + 7):])):
                                                    coordinates[e][w] = -1
                                    print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(
                                        heroes, heroes.index(who)) + "\n")
                                    print(eWho.name + " takes " + amount + " damage!" + dead)
                                    clearI()
                            else:
                                print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(
                                    heroes, heroes.index(who)) + "\n")
                                print(who.name + "'s target is already dead...")
                                clearI()
                        elif (action == ("Move")):
                            move = who.moves[int(action[9:10])]
                            print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(heroes,
                                                                                                                heroes.index(
                                                                                                                    who)) + "\n")
                            print(who.name + " uses " + move.name + "!")
                            targets = action[action.index("[") + 1:len(action) - 1]
                            targs = []
                            happenstances = ""
                            while (len(targets) > 0):
                                targ = None
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
                                    print(Fightable.printCoords(coordinates, enemies,
                                                                targs) + "\n\n" + Fightable.printHeroes(heroes,
                                                                                                        heroes.index(
                                                                                                            who)) + "\n\n" + who.name + " uses " + move.name + "!\n" + happenstances)
                                    sleep(200)
                                    clear()
                                    print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(
                                        heroes, heroes.index(
                                            who)) + "\n" + who.name + " uses " + move.name + "!\n\n" + happenstances)
                                    sleep(200)
                            clearI()
                        elif (action == ("Item")):
                            pass
                        elif (action == ("Defend")):
                            pass
                    else:
                        print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(heroes,
                                                                                                            heroes.index(
                                                                                                                who)) + "\n")
                        print(who.name + " has fainted!")
                        sleep(200)
                else:
                    who = enemies[(int(action[2:3]))]
                    print(Fightable.printCoords(coordinates, enemies,
                                                [enemies.index(who)]) + "\n\n" + Fightable.printHeroes(heroes) + "\n")
                    who.sufferEffects()
                    sleep(500)
                    clear()
                    if (who.health > 0):
                        if (action == ("Attack")):
                            hWho = heroes[int(action[(action.index("Attack") + 7):len(action) - 1])]
                            if (hWho.health > 0):
                                print(Fightable.printCoords(coordinates, enemies,
                                                            [enemies.index(who)]) + "\n\n" + Fightable.printHeroes(
                                    heroes) + "\n")
                                print(who.name + " " + who.verb + " at " + hWho.name)
                                sleep(500)
                                if (randint(0, 99) < hWho.agility):
                                    print(hWho.name + " dodges the attack!")
                                    clearI()
                                else:
                                    clear()
                                    for b in range(0, 3):
                                        if (3 % (b + 1) == 1):
                                            print(Fightable.printCoords(coordinates, enemies, [
                                                enemies.index(who)]) + "\n\n" + Fightable.printHeroes(heroes,
                                                                                                      heroes.index(
                                                                                                          hWho)) + "\n\n" + who.name + " " + who.verb + " at " + hWho.name)
                                        else:
                                            print(Fightable.printCoords(coordinates, enemies, [
                                                enemies.index(who)]) + "\n\n" + Fightable.printHeroes(
                                                heroes) + "\n\n" + who.name + " " + who.verb + " at " + hWho.name)
                                        sleep(100)
                                        clear()
                                    amount = who.fight - hWho.defense
                                    if (amount <= 0):
                                        amount = 1
                                    hWho.health += (amount * -1)
                                    print(Fightable.printCoords(coordinates, enemies,
                                                                [enemies.index(who)]) + "\n\n" + Fightable.printHeroes(
                                        heroes, heroes.index(hWho)) + "\n")
                                    print(hWho.name + " takes " + amount + " damage!")
                                    if (hWho.health <= 0):
                                        print(hWho.name + " has fainted!")
                                    clearI()
                            else:
                                print(Fightable.printCoords(coordinates, enemies,
                                                            [enemies.index(who)]) + "\n\n" + Fightable.printHeroes(
                                    heroes) + "\n")
                                print(who.name + "'s target is already down...")
                                clearI()
                                sleep(200)
                        elif (action == ("Move")):
                            pass
                        elif (action == ("Defend")):
                            pass
                        elif (action == ("Flee")):
                            pass


class Hero(Fightable):
    def __init__(self, name, moves, leveling, caste, gender, weapon, armor):
        super(Hero, self).__init__(name, 0, 0, 0, 0, moves)
        self._leveling = leveling
        self._caste = caste
        self._inventory = []
        self._level = 0
        self.levelUp()
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

    @property
    def fight(self):
        return self._fight + self.weapon.fight

    @fight.setter
    def fight(self, value):
        self._fight = value

    @property
    def defense(self):
        return self._defense + self.armor.defense

    @defense.setter
    def defense(self, value):
        self._defense = value

    def levelUp(self):
        self.level += 1
        self.maxHealth = (self.leveling[0][self.level - 1])
        self.maxFight = (self.leveling[1][self.level - 1])
        self.maxDefense = (self.leveling[2][self.level - 1])
        self.maxAgility = (self.leveling[3][self.level - 1])
        self.health = (self.leveling[0][self.level - 1])
        self.fight = (self.leveling[1][self.level - 1])
        self.defense = (self.leveling[2][self.level - 1])
        self.agility = (self.leveling[3][self.level - 1])
        if (len(self.learnableMoves) > 0 and (self.level) % (10 / len(self.learnableMoves)) == 0):
            m = self.learnableMoves[self.level / (10 / len(self.learnableMoves)) - 1]
            print(self.name + " has learned the new skill: " + m.name + ".")
            self.moves.append(m)

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
        if (self.fight != self.maxFight):
            string += "/" + str(self.maxFight)
            string += "\n"
        string += "Defense: " + str(self.defense)
        if (self.defense != self.maxDefense):
            string += "/" + str(self.maxDefense)
        string += "\n"
        string += "Agility: " + str(self.agility)
        if (self.agility != self.maxAgility):
            string += "/" + str(self.maxAgility)
        string += "\n"
        return string


class Enemy(Fightable):
    def __init__(self, name, desc, verb, title, health, fight, defense, agility, moves, drops, size, imageFolder):
        super(Enemy, self).__init__(name, fight, defense, agility, health, moves)
        self._verb = verb
        self._title = title
        self._drops = drops
        self._desc = desc
        self._size = size
        self._imageFolder = imageFolder

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
                     self.moves, self.drops, self.size);

    def generateImage(self):
        # This code is gonna be horrible
        if (self.name == "gnoll"):
            color = randint(1, 3)
            image = pygame.image.load("GameArt\Gnoll\Color{} Gnoll\Body.png".format(color))
            image.blit(pygame.image.load("GameArt\Gnoll\Color{} Gnoll\Head1.png".format(color)), (0, 0))
            mane = randint(1, 2)
            image.blit(pygame.image.load("GameArt\Gnoll\Color{} Gnoll\Mane{}.png".format(color, mane)), (0, 0))
            chin = randint(1, 2)
            chest = randint(1, 2)
            if chin == 1:
                image.blit(pygame.image.load("GameArt\Gnoll\Markings\Head1Chin.png"), (0, 0))
            if chest == 1:
                image.blit(pygame.image.load("GameArt\Gnoll\Markings\Chest.png"), (0, 0))
            if chin == 1 and chest == 1:
                image.blit(pygame.image.load("GameArt\Gnoll\Markings\ChinChestMid.png"), (0, 0))
            spots = randint(1, 2)
            if spots == 1:
                image.blit(pygame.image.load("GameArt\Gnoll\Markings\Head1HeadSpots.png"), (0, 0))
            spots = randint(1, 2)
            if spots == 1:
                image.blit(pygame.image.load("GameArt\Gnoll\Markings\Spots1.png"), (0, 0))
            else:
                image.blit(pygame.image.load("GameArt\Gnoll\Markings\Spots2.png"), (0, 0))

            image = pygame.transform.scale(image, (175, 280))
            return image
        else:
            return pygame.image.load(self._imageFolder)

    def __str__(self):
        string = self.name + "\n" + self.desc + "\n"
        string += "Health: " + str(self.health) + "/" + str(self.maxHealth) + "\n"
        string += "Fight: " + str(self.fight)
        if (self.fight != self.maxFight):
            string += "/" + str(self.maxFight)
            string += "\n"
        string += "Defense: " + str(self.defense)
        if (self.defense != self.maxDefense):
            string += "/" + str(self.maxDefense)
            string += "\n"
        string += "Agility: " + str(self.agility)
        if (self.agility != self.maxAgility):
            string += "/" + str(self.maxAgility)
            string += "\n"
        return string


Map = Map()

def menu():    
    font1 = pygame.font.SysFont('Arial', 90)
    font2 = pygame.font.SysFont('Arial', 60)
    selected = "start"
    bg_img = pygame.image.load("GameArt\Extra\menu.gif")
    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
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

        screen.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        screen.blit(text_start, (WIDTH/2 - (start_rect[2]/2), 300))
        screen.blit(text_quit, (WIDTH/2 - (quit_rect[2]/2), 360))
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
                    opt2 = font2.render("Mage", False, BLACK)
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

        screen.blit(title1, (WIDTH/2 - (title1_rect[2]/2), 80))
        screen.blit(title2, (WIDTH/2 - (title2_rect[2]/2), 160))
        screen.blit(opt1, (WIDTH/2 - (start_rect[2]/2), 300))
        screen.blit(opt2, (WIDTH/2 - (quit_rect[2]/2), 360))
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
    text3 = font.render("have that same look in your eyes all the other", False, BLACK)
    text4 = font.render("wannabe heros had.", False, BLACK)
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
                    text2 = font.render("same as they were before. Yennughu, the beast", False, BLACK)
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
                    text3 = font.render("that I'll gladly take them off your hands.", False, BLACK)
                    text4 = font.render("", False, BLACK)
                    i += 1
                elif i == 6:
                    text1 = font.render("I'll only open it after you finish clearing out", False, BLACK)
                    text2 = font.render("mall the enemies on a floor. Those monsters", False, BLACK)
                    text3 = font.render("are dangerous and I'm not gonna risk my life.", False, BLACK)
                    text4 = font.render("", False, BLACK)
                    i += 1
                elif i == 7:
                    text1 = font.render("That's all the help I can offer though. Don't", False, BLACK)
                    text2 = font.render("worry though, I'm sure you'll be able to pull", False, BLACK)
                    text3 = font.render("oit off.", False, BLACK)
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
        screen.blit(merchant, (WIDTH/2 - (merch_rect[2]/2), 50))
        screen.blit(box, (0, 475))
        screen.blit(text1, (10, 505))
        screen.blit(text2, (10, 540))
        screen.blit(text3, (10, 575))
        screen.blit(text4, (10, 610))
        pygame.display.update()   

def combat():
    combat = True
    while combat:
        screen.fill(BLUE)
        return

def changeFloor():
    global currentFloor    
    currentFloor = currentFloor.nextFloor
    Map.hero.column = 5
    Map.hero.row = 9
    Map.build()
    return
        
   
def gameMap():
    bg_img = pygame.image.load("GameArt\Extra\menu.gif")
    font = pygame.font.SysFont('Arial', 75)
    gameMap = True
    Map.build()
    
    while gameMap:
        Map.draw()

        if currentFloor == None:
            screen.blit(bg_img, bg_img.get_rect())
            
        for event in pygame.event.get():        #catching events
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Pos = pygame.mouse.get_pos()
                print Pos
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Map.hero.move("LEFT")
                    if Map.hero.collision("LEFT"):
                        combat()
                if event.key == pygame.K_RIGHT:
                    Map.hero.move("RIGHT")
                    if Map.hero.collision("RIGHT"):
                        combat()
                if event.key == pygame.K_UP:
                    Map.hero.move("UP")
                    if Map.hero.collision("UP"):
                        combat()
                if event.key == pygame.K_DOWN:
                    Map.hero.move("DOWN")
                    if Map.hero.collision("DOWN"):
                        combat()
                if event.key == pygame.K_RETURN:
                    changeFloor()
                if event.key == pygame.K_a:
                    popup()
                if event.key == pygame.K_b:
                    merchText()
                        
 
                    
        clock.tick(60)      #Limit to 60 fps or something
        pygame.display.update()     #Honestly not sure what this does, but it breaks if I remove it
        Map.update()
        
menu()
pygame.quit()
