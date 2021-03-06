from StatsAndItems import *
from random import randint
from time import sleep
from math import ceil
import pygame
import random

BLACK = (0, 0, 0)  # fill
WHITE = (255, 255, 255)  # floor
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 97, 3)
RED = (255, 0, 0)
WIDTH = 716
HEIGHT = 716


def checkList(inventory, screen):
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


def useItem(item, who, screen, inventory):
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
        Fightable.flavorText(who.name + " " + item.statusEffect.verb + " the " + item.name + "!", screen)
        sleep(1.25)
        who.getEffect(item.statusEffect, screen)
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
    def posPro(self):
        return self._posPro

    @posPro.setter
    def posPro(self, value):
        self._posPro = value

    @property
    def refl(self):
        return self._refl

    @refl.setter
    def refl(self, value):
        self._refl = value


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

    def getEffect(self, m, screen):
        if isinstance(m, Move):
            x = 0
            while x < len(m.statusEffects):
                if m.statusEffects[x].turns > 0:
                    self.statusEffects.append(m.statusEffects[x].clone())
                    Fightable.flavorText("{} has been {}".format(self.name, m.statusEffects[x].verb), screen)
                else:
                    self.oneAndDone(m.statusEffects[x], screen)
                x += 1
        else:
            if m.turns > 0:
                self.statusEffects.append(m.clone())
            else:
                self.oneAndDone(m, screen)

    def oneAndDone(self, st, screen):
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
                    verb = "greatly "
                elif abs(st.amounts[x]) <= 2:
                    verb = "slightly "
                if st.amounts[x] >= 0:
                    verb = " is " + verb + "strengthened"
                else:
                    verb = " is " + verb + "weakened"
                suffered += self.name + verb + "!"

            elif st.stats[x] == ("defense"):
                self.defense += (st.amounts[x])
                verb = ""
                if abs(st.amounts[x]) > 4:
                    verb = "greatly "
                elif abs(st.amounts[x]) <= 2:
                    verb = "slightly "
                if st.amounts[x] >= 0:
                    verb = "'s defenses are " + verb + "reinforced"
                else:
                    verb = "'s defenses are " + verb + "diminished"
                suffered += self.name + verb + "!"

            elif st.stats[x] == "agility":
                self.agility += (st.amounts[x])
                verb = ""
                if abs(st.amounts[x]) > 4:
                    verb = "greatly "
                elif abs(st.amounts[x]) <= 2:
                    verb = "slightly "
                if st.amounts[x] >= 0:
                    verb = "'s speed is " + verb + "increased"
                else:
                    verb = "'s speed is " + verb + "decreased"
                suffered += self.name + verb + "!"
            x += 1

        Fightable.flavorText(suffered, screen)
        sleep(1.5)

    def sufferEffects(self):
        things = []
        for x in self.statusEffects:
            things.append(x.doIt(self))
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
        for x in range(len(t)):
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
    def selectFromCoords(coords, screen, target):
        screenshot = screen.copy()
        locations = []
        img = None


        l = 0
        while Fightable.firstOf(coords[l]) == -1:
            l += 1

        if target == "Single" or target == "Vert Line":
            locations = [(185, 300 + 100 * len(coords[0])), (285, 300 + 100 * len(coords[0])),
                         (390, 300 + 100 * len(coords[0])), (490, 300 + 100 * len(coords[0]))]
            for i in range(4):
                if Fightable.firstOf(coords[i]) == -1:
                    locations[i] = None

            img = pygame.image.load("GameArt\Buttons\This.png")
        elif target == "Hori Line":
            for x in range(len(coords[0])):
                locations.append((300, (x * 100 + 200)))
            img = pygame.image.load("GameArt\Buttons\This.png")
        else:
            locations = [(0, 0)]
            img = pygame.image.load("GameArt\Buttons\Empty.png")

        screen.blit(img, locations[l])


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        l -= 1
                        while l < 0 or locations[l] == None:
                            l -= 1
                            if l < 0:
                                l = len(locations)
                                break
                        screen.blit(screenshot, (0, 0))
                        if l < len(locations):
                            screen.blit(img, locations[l])
                        else:
                            screen.blit(pygame.image.load("GameArt\Buttons\Back.png"), (650, 650))
                    if event.key == pygame.K_RIGHT:
                        l += 1
                        while l > len(locations) or (l != len(locations) and locations[l] == None):
                            l += 1
                            if l > len(locations):
                                l = 0
                                while Fightable.firstOf(coords[l]) == -1:
                                    l+=1
                                break
                        screen.blit(screenshot, (0, 0))
                        print l
                        if l < len(locations):
                            screen.blit(img, locations[l])
                        else:
                            screen.blit(pygame.image.load("GameArt\Buttons\Back.png"), (650, 650))
                    if event.key == pygame.K_RETURN:
                        if l == len(locations):
                            return [-1]
                        if target == "Single":
                            return [Fightable.firstOf(coords[l])]
                        if target == "Vert Line":
                            picks = []
                            for i in range(len(coords[0])):
                                if coords[l][i] != -1:
                                    picks.append(coords[l][i])
                            return picks
                        if target == "All":
                            everyone = []
                            for i in range(len(coords)):
                                for t in range(len(coords[i])):
                                    if coords[i][t] != -1:
                                        everyone.append(coords[i][t])
                            return everyone
            pygame.display.update()

    @staticmethod
    def printHeroes(heroes, screen, highlight=-1, yellow=-1):
        font = pygame.font.SysFont('Arial', 25)
        colors = [WHITE, WHITE, WHITE]
        if yellow != -1:
            colors[yellow] = RED
        if highlight == 0:
            pygame.draw.rect(screen, colors[0], [35, 0, 216, 120])
            heroes[0].blurtStats(font, (40, 25), screen)
        else:
            pygame.draw.rect(screen, colors[0], [35, 0, 216, 100])
            heroes[0].blurtStats(font, (40, 5), screen)
        if highlight == 1:
            pygame.draw.rect(screen, colors[1], [252, 0, 216, 120])
            if len(heroes) > 1:
                heroes[1].blurtStats(font, (257, 25), screen)
        else:
            pygame.draw.rect(screen, colors[1], [252, 0, 216, 100])
            if len(heroes) > 1:
                heroes[1].blurtStats(font, (257, 5), screen)
        if highlight == 2:
            pygame.draw.rect(screen, colors[2], [469, 0, 216, 120])
            if len(heroes) > 2:
                heroes[2].blurtStats(font, (474, 25), screen)
        else:
            pygame.draw.rect(screen, colors[2], [469, 0, 216, 100])
            if len(heroes) > 2:
                heroes[2].blurtStats(font, (474, 5), screen)

    @staticmethod
    def printCoords(coordinates, enemies, screen, highlight=-1, attacking=-1):
        rects = []
        for y in range(len(coordinates[0])):
            rec = []
            for x in range(4):
                if coordinates[x][y] == -1:
                    rec.append(None)
                else:
                    color = enemies[coordinates[x][y]].healthColor()
                    if highlight == coordinates[x][y] or (isinstance(highlight, list) and coordinates[x][y] in highlight):
                        color = WHITE
                    rec.append(pygame.draw.rect(screen, color, [160 + (x * 100), 270 + (y * 100), 100, 100]))
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
    def flavorText(string, screen):
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
    def printScreen(coordinates, enemies, heroes, screen, attacking=-1):
        bg = pygame.image.load("GameArt\Extra\combat_bg.png")
        screen.blit(bg, (0, 0))

        Fightable.printCoords(coordinates, enemies, screen, attacking, attacking)
        Fightable.printHeroes(heroes, screen)

        pygame.display.update()

    @staticmethod
    def ask(screen):
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
    def combat(heroes, enemies, screen, inventory):
        trySize = 0
        while (trySize + 1) * 4 < Fightable.area(enemies):
            trySize += 1
        coordinates = None
        while coordinates is None:
            trySize += 1
            coordinates = [[], [], [], []]
            for o in range(trySize):
                for t in range(4):
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
                        for o in range(trySize):
                            for t in range(4):
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
                        for o in range(trySize):
                            for t in range(4):
                                coordinates[t].append(-1)
                        tries += 1
                        j = -1
                elif (e.size == 3):
                    x = -1
                    y = -1
                    potentials = []
                    for d in range(len(coordinates)):
                        for f in range(len(coordinates[0]) - 1):
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
                        for o in range(trySize):
                            for t in range(4):
                                coordinates[t].append(-1)
                        tries += 1
                        j = -1
                elif e.size == 4:
                    x = -1
                    y = -1
                    potentials = []
                    for d in range(len(coordinates) - 1):
                        for f in range(len(coordinates[0]) - 1):
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
                        for o in range(trySize):
                            for t in range(4):
                                coordinates[t].append(-1)
                        tries += 1
                        j = -1
                j += 1
            if tries == 5000:
                coordinates = None

        Fightable.printScreen(coordinates, enemies, heroes, screen)
        screenshot = screen.copy()
        while Fightable.totalHealth(heroes) > 0 and Fightable.totalHealth(enemies) > 0:
            gamePlanH = []
            gamePlanE = []
            for x in range(len(heroes)):
                Fightable.printHeroes(heroes, screen, x)
                zoop = screen.copy()
                pygame.display.update()
                who = heroes[x]
                if who.health > 0:
                    for y in range((who.agility / 10) + 1):
                        deciding = True
                        while deciding:
                            screen.blit(zoop, (0, 0))
                            Fightable.printHeroes(heroes, screen, x)
                            what = Fightable.ask(screen)
                            if what == "fight":
                                w = Fightable.selectFromCoords(coordinates, screen, "Single")
                                if w[0] != -1:
                                    gamePlanH.append("H {} Attack {}".format(x, w[0]))
                                    deciding = False
                            elif what == "defend":
                                thing = "takes"
                                if who.name == "You":
                                    thing = "take"
                                Fightable.flavorText(who.name + " {} a defensive stance!".format(thing), screen)
                                sleep(1)
                                screen.blit(screenshot, (0, 0))
                                who.oneAndDone(StatusEffect("", "", ["defense"], [int(ceil(who.maxDefense*(2.0/3.0)))], 1), screen)
                                deciding = False
                                gamePlanH.append("H {} Defend".format(x))
                            elif what == "special":
                                if (len(who.moves) > 0):
                                    move = checkList(who.moves, screen)
                                    if move != None:
                                        deciding = False
                                        effected = []
                                        if not move in helpingMoves:
                                            effected = Fightable.selectFromCoords(coordinates, screen, move.target)
                                        else:
                                            effected = Fightable.chooseAlly(screen, move.target)
                                        gamePlanH.append("H {} {} Move {}".format(x, who.moves.index(move), effected))
                                        print gamePlanH[len(gamePlanH)-1]
                                else:
                                    Fightable.flavorText("No known special moves.", screen)
                                    sleep(1)
                                    screen.blit(screenshot, (0, 0))
                            elif what == "item":
                                if (len(inventory) > 0):
                                    item = checkList(inventory, screen)
                                    screen.blit(screenshot, (0, 0))
                                    print item.name
                                    if item != None:
                                        deciding = not(useItem(item, who, screen, inventory))
                                else:
                                    Fightable.flavorText("Inventory is empty.", screen)
                                    sleep(1)
                else:
                    Fightable.flavorText(who.name + " is unconscious!", screen)
                    sleep(1.5)
                    screen.blit(screenshot, (0, 0))
                screen.blit(screenshot, (0, 0))
                pygame.display.update()
                strings = who.sufferEffects()
                print strings
                for s in strings:
                    for t in s:
                        Fightable.flavorText(t, screen)
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
            for c in range(len(gamePlanH)):
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
            for c in range(len(speeds) - 1):
                if (speeds[c] < speeds[c + 1]):
                    hold = speeds[c]
                    speeds[c] = speeds[c + 1]
                    speeds[c + 1] = hold
                    c -= 2
                    if (c < -1):
                        c = -1
            newGamePlanH = []
            for c in range(len(speeds)):
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
            for x in range(len(combinedGamePlan)):
                pygame.event.pump()
                screenshot = screen.copy()
                action = combinedGamePlan[x]
                print action
                if action[0:1] == "H":
                    who = heroes[int(action[2:3])]
                    Fightable.printHeroes(heroes, screen, int(action[2:3]))
                    pygame.display.update()
                    if who.health > 0:
                        if("Attack" in action):
                            eWho = enemies[int(action[(action.index("Attack") + 7):])]
                            if (eWho.health > 0):
                                Fightable.printCoords(coordinates, enemies, screen, enemies.index(eWho))
                                screenshot = screen.copy()
                                Fightable.flavorText(who.name + " " + who.weapon.verb + " " + who.gender.posAdj + " "
                                                     + who.weapon.name + " at " + eWho.title + eWho.name, screen)
                                pygame.display.update()
                                sleep(1.5)
                                if (randint(0, 99) < eWho.agility):
                                    sleep(1.25)
                                    Fightable.flavorText(eWho.title.capitalize() + eWho.name + " dodges the attack!", screen)
                                    pygame.display.update()
                                    sleep(1)
                                else:
                                    amount = who.fightT() - eWho.defense
                                    if (amount <= 0):
                                        amount = 1
                                    eWho.health += (amount * -1)
                                    screen.blit(screenshot, (0, 0))
                                    Fightable.printCoords(coordinates, enemies, screen)
                                    other = screen.copy()
                                    screen.blit(screenshot, (0, 0))
                                    pygame.display.update()
                                    for b in range(5):
                                        if (3 % (b + 1) == 0):
                                            screen.blit(screenshot, (0, 0))
                                        else:
                                            screen.blit(other, (0, 0))
                                        pygame.display.update()
                                        sleep(.1)
                                    dead = ""
                                    print eWho.health
                                    if (eWho.health <= 0):
                                        dead = (eWho.title.capitalize() + eWho.name + " has been defeated!")
                                        for e in range(len(coordinates)):
                                            for w in range(len(coordinates[0])):
                                                if (coordinates[e][w] == int(action[(action.index("Attack") + 7):])):
                                                    coordinates[e][w] = -1
                                    Fightable.flavorText(eWho.title.capitalize() + eWho.name + " takes {} damage! ".format(amount) + dead, screen)
                                    sleep(1.25)
                                    pygame.display.update()
                                    if dead != "":
                                        sleep(1.25)
                                        for x in coordinates:
                                            for y in x:
                                                if y == enemies.index(eWho):
                                                    y = -1
                            else:
                                Fightable.flavorText(who.name + "'s target is already dead...", screen)
                                pygame.display.update()
                                sleep(1.5)
                                screen.blit(screenshot, (0, 0))
                                pygame.display.update()
                        elif("Move" in action):
                            move = who.moves[int(action[4:5])]
                            shot = screen.copy()
                            Fightable.flavorText(who.name + " uses " + move.name + "!", screen)
                            pygame.display.update()
                            sleep(1)
                            targets = action[action.index("[") + 1:len(action) - 1].split(", ")
                            if not move in helpingMoves:
                                targets.reverse()
                                targs = []
                                for i in range(len(targets)):
                                    targets[i] = int(targets[i])
                                    targs.append(enemies[targets[i]])
                                high = []
                                for t in targets:
                                    high.append(t)
                                    Fightable.printCoords(coordinates, enemies, screen, high)
                                    pygame.display.update()
                                for targ in targs:
                                    if (targ.health > 0):
                                        for s in range(len(move.statusEffects)):
                                            st = move.statusEffects[s].clone()
                                            for q in range(len(st.amounts)):
                                                if isinstance(st.amounts[q], str):
                                                    amount = st.amounts[q]
                                                    if amount[0] == "H":
                                                        amount = int(int(amount[1:len(amount)])/100)*who.health
                                                    elif amount[0] == "F":
                                                        amount = int(int(amount[1:len(amount)])/100)*who.fight
                                                    elif amount[0] == "D":
                                                        amount = int(int(amount[1:len(amount)])/100)*who.defense
                                                    elif amount[0] == "A":
                                                        amount = int(int(amount[1:len(amount)])/100)*who.agility
                                                    st.amounts[q] = amount
                                                    print st.amounts
                                            targ.getEffect(st, screen)
                                            sleep(.8)
                                            screen.blit(shot, (0, 0))
                                            pygame.display.update()
                                    pygame.display.update()
                                    if (targ.health <= 0):
                                        for e in range(len(coordinates)):
                                                for w in range(len(coordinates[0])):
                                                    if (coordinates[e][w] == enemies.index(targ)):
                                                        coordinates[e][w] = -1
                        elif("Defend" in action):
                            Fightable.flavorText(who.name + " has " + who.gender.posAdj + " guard up!", screen)
                            undefend.append(who)
                            sleep(1.25)
                            screen.blit(screenshot, (0, 0))
                    else:
                        Fightable.flavorText(who.name + " is unconscious!", screen)
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
                                Fightable.printCoords(coordinates, enemies, screen, [enemies.index(who)])
                                Fightable.flavorText(who.title.capitalize() + who.name + " " + who.verb + " at " + hWho.name, screen)
                                pygame.display.update()
                                sleep(1.5)
                                Fightable.printScreen(coordinates, enemies, heroes, screen, enemies.index(who))
                                pygame.display.update()
                                sleep(.1)
                                screen.blit(screenshot, (0, 0))
                                pygame.display.update()
                                if (randint(0, 99) < hWho.agility):
                                    Fightable.flavorText(hWho.name + " dodges the attack!", screen)
                                    pygame.display.update()
                                    sleep(1)
                                else:
                                    amount = who.fight - hWho.defenseT()
                                    if (amount <= 0):
                                        amount = 1
                                    hWho.health += (amount * -1)
                                    Fightable.printHeroes(heroes, screen, -1, heroes.index(hWho))
                                    highlighted = screen.copy()
                                    Fightable.printHeroes(heroes, screen)
                                    screenshot = screen.copy()
                                    for b in range(5):
                                        if (3 % (b + 1) == 1):
                                            screen.blit(highlighted, (0, 0))
                                        else:
                                            screen.blit(screenshot, (0, 0))
                                        pygame.display.update()
                                        sleep(.1)
                                    thing = "takes"
                                    if hWho.name == "You":
                                        thing = "take"
                                    Fightable.flavorText(hWho.name + " {} {} damage!".format(thing, amount), screen)
                                    pygame.display.update()
                                    sleep(1)
                                    if (hWho.health <= 0):
                                        Fightable.flavorText(hWho.name + " has fainted!", screen)
                                        pygame.display.update()
                                        sleep(1.25)

                            else:
                                Fightable.flavorText(who.title.capitalize() + who.name + "'s target is already down...", screen)
                                sleep(1.5)
                        elif "Move" in action:
                            pass
                        else:
                            pass
                Fightable.printScreen(coordinates, enemies, heroes, screen)
                screenshot = screen.copy()
                pygame.display.update()
                if Fightable.totalHealth(heroes) <= 0:
                    break

            for h in undefend:
                h.defense -= int(ceil(h.maxDefense *(2.0/3.0)))
        pygame.event.clear()
        if Fightable.totalHealth(heroes) <= 0:
            return False
        print player.moves
        return True


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
            self.gender = Gender("???", "they", "them", "their", "theirs", "themself")

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
        bonus = self.weapon.fight + randint(self.weapon.consistency*-1, self.weapon.consistency)
        if bonus < 0:
            bonus = 0
        return self.fight + bonus

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
        self.revert()

    def revert(self):
        self.fight = self.maxFight
        self.defense = self.maxDefense
        self.agility = self.maxAgility

    def blurtStats(self, font, coords, screen):
        screen.blit(font.render(self.name + " | " + self.caste, True, (255, 0, 0)), coords)
        screen.blit(font.render("{}/{} HP".format(self.health, self.maxHealth), True, (255, 0, 0)),
                    (coords[0], coords[1] + 30))
        string = ""
        for x in self.statusEffects:
            string += x.name[0]
        screen.blit(font.render(string, True, (255, 0, 0)), (coords[0], coords[1] + 60))

    def clone(self):
        return Hero(self.name, self.moves, self.leveling, self.caste, self.gender, self.weapon, self.armor)

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
                     self.moves, self.drops, self.size, self._imageFolder)

    def generateImage(self):
        # This code is gonna be horrible
        if self._imageFolder == "Gnoll":
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

# getting some descriptions out of the way because im lazy
GNOLL_DESC = "It's a Gnoll: savage, feral, and hungry."
HILLGIANT_DESC = "A giant from the hills."
FLIND_DESC = "It's a Flind: it's shorter but just as dangerous as a gnoll."
### Instances go here
## name // desc // verb // title // health // fight // defense // agility // moves // drops [exp, gold] // size // imageFolder

f1hill_giant = Enemy("Hill Giant", HILLGIANT_DESC, "punches", "", 10, 3, 2, 1, [toHit, bludg], [2, 2], 1, "")
f1gnoll = Enemy("Gnoll", GNOLL_DESC, "lashes out", "the ", 12, 4, 2, 2, [bludg, score], [4, 4], 1, "Gnoll")

f2hill_giant = Enemy("Hill Giant", HILLGIANT_DESC, "punches", "", 11, 4, 3, 1, [toHit, bludg], [4, 3], 1, "")
f2gnoll = Enemy("Gnoll", GNOLL_DESC, "lashes out", "the ", 13, 5, 2, 3, [bludg, score], [5, 6], 1, "Gnoll")

f3hill_giant = Enemy("Hill Giant", HILLGIANT_DESC, "smashes", "", 12, 6, 4, 2, [toHit, bludg], [5, 4], 1, "")
f3gnoll = Enemy("Gnoll", GNOLL_DESC, "lashes out", "the ", 14, 8, 2, 3, [bludg, score], [6, 8], 1, "Gnoll")

miniboss1 = Enemy("Gnoll", "It seems bigger than the other Gnolls you've seen...", "slashes", "the ", 50, 5, 2, 5, [demo, wham, deepCut], [20, 25], 1, "Gnoll")
miniboss2 = Enemy("Gnoll", "It seems angrier than the other Gnolls you've seen...", "lashes out", "the ", 75, 10, 2, 2, [demo, wham, deepCut], [20, 25], 1, "Gnoll")

f5hill_giant = Enemy("Hill Giant", HILLGIANT_DESC, "smashes", "", 14, 4, 4, 2, [bludg, wham], [8, 5], 1, "")
f5gnoll = Enemy("Gnoll", GNOLL_DESC, "lashes out", "the ", 18, 6, 3, 4, [bludg, score, scratch], [10, 6], 1, "Gnoll")

f6gnoll = Enemy("Gnoll", GNOLL_DESC, "lashes out", "the ", 20, 7, 3, 4, [bludg, score, scratch], [12, 8], 1, "Gnoll")

f7gnoll = Enemy("Gnoll", GNOLL_DESC, "lashes out", "the ", 22, 7, 4, 4, [bludg, score, scratch], [14, 10], 1, "Gnoll")
f7flind = Enemy("Flind", FLIND_DESC, "slashes", "", 18, 6, 2, 2, [bludg, score, infectStrike], [15, 12], 1, "")

miniboss3 = Enemy("Flind", "The Flind is aggressively staring into you.", "slashes", "", 75, 10, 5, 10, [demo, pulverize, decimate, infectStrike], [30, 45], 1, "")
miniboss4 = Enemy("Flind", "Just the presence of the Flind intimidates you...", "slashes", "", 100, 5, 15, 5, [demo, pulverize, decimate, infectStrike], [30, 45], 1, "")

f9gnoll = Enemy("Gnoll", GNOLL_DESC, "slashes", "", 25, 8, 3, 3, [score, scratch, deepCut], [15, 12], 1, "")
f9flind = Enemy("Flind", FLIND_DESC, "slashes", "", 20, 7, 3, 3, [bite, score, infectStrike, deepCut, scratch], [20, 18], 1, "")

f10flind = Enemy("Flind", FLIND_DESC, "slashes", "", 25, 8, 4, 3, [score, infectStrike, deepCut, scratch], [28, 25], 1, "")

f11flind = Enemy("Flind", FLIND_DESC, "slashes", "", 30, 8, 5, 3, [score, infectStrike, deepCut, scratch], [35, 30], 1, "")

finalboss = Enemy("Yennoghu", "This is it.", "attacks", "", 200, 15, 12, 10, [deepCut, demo, pulverize, decimate, intimidate, finalblow], [], 1, "")

# Vskewer #HwideSlice #Aplague #SBinspire #ABauraHeal

gallant = Hero("Gallant", [skewer, wideSlice, plague, inspire, auraHeal], [
        [15, 1, 1, 1, 1, 1, 3, 1, 3, 2, 4],
        [3, 1, 2, 1, 2, 0, 0, 2, 2, 3, 4],
        [5, 1, 1, 1, 2, 1, 1, 1, 1, 2, 3],
        [1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 2]], "Knight", 1, bigger_sword, chainmail)


for i in range(10):
    gallant.levelUp()
gallant.health = gallant.maxHealth


throureum = Hero("Throurem", [], [
        [12, 2, 1, 1, 1, 1, 1, 1, 1, 2, 3],
        [4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [2, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]], "Mage", 2, fortified_staff, leather)

knithenpf = Hero("Knithenpf", [], [
        [10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
        [3, 0, 0, 0, 0, 3, 0, 0, 0, 3, 4],
        [2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 2],
        [3, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3]], "Rogue", 69, dagger, leather)

frethenei = Hero("Frethenei", [], [
        [20, 0, 0, 0, 5, 0, 0, 0, 5, 0, 10],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 1, 0, 1, 1, 0, 1, 1, 0, 1, 5],
        [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 5]], "Healer", 2, cross, robes)

player = Hero("Player", [], [
    [15, 1, 1, 1, 1, 2, 2, 2, 3, 4, 5],
    [5, 2, 1, 1, 2, 1, 1, 1, 1, 2, 5],
    [1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 5],
    [5, 2, 1, 1, 2, 1, 1, 1, 1, 2, 5]], "Hero", 420, dagger, leather)