from time import sleep
from random import randint
from random import choice


##################################################
# Simple output functions, will become obsolete  #
# after transfer to GUI. "Clear" functions do    #
# not work in all compilers.                     #
##################################################
# Clears the screen
def clear():
  print(chr(27)+'[2j')
  print('\033c')
  print('\x1bc')
# Clears the screen after the user presses enter
def clearI():
    raw_input("Press enter to continue.\n")
    clear()
# Formats print function to not cut off words
def output(string):
    x = 0
    y = 0
    string = str(string)
    while x < len(string):
        if string[x] == ' ' and y >= 50:
            y = 0
            string = string[:x + 1] + '\n' + string[x + 1:]
        if string[x] == "\n":
            y = 0
        x += 1
        y += 1
    print(string)
# Asks the user a question, returns number input
# corresponding to answer
def ask(responses):
    global cheats
    asking = True
    while asking:
        s = responses[0] + "\n"
        x = 1
        while x < len(responses):
            extraSpace = ""
            if len(responses) > 10 and x < 10:
                extraSpace = " "
            s += "{}. {}{}\n".format(x, extraSpace, responses[x])
            x += 1
        output(s)
        s = raw_input()
        s = int(s)
        if s <= 0 or s >= len(responses):
            clear()
            output("That is not a valid answer.\n")
        else:
          return s



##################################################
# StatusEffect Class                             #
##################################################
# PARAMETERS:                                    #
# Name   - The name of effect (String: "poison") #
# Verb   - Descriptor of effect (String:"burned")#
# Stats  - The stats the the StatuEffect affects # 
#          (String Array: ["health", "defense"]) #
# Amounts- The amount that each listed stat in   # 
#          "stats" is in/decreased respectively  #
#          (Integer Array: [-3, 4])              #
# Turns  - The number of turns the StatusEffect  #
#          lasts. (Positive Integer)             #
##################################################
# CLASS METHODS:                                 #
# doIt(self, who) - Causes a Fightable instance  #
#                   to undergo the stat changes  #
#                   of a StatusEffect. Who must  #
#                   be a Fightable.              #
# clone(self)     - Creates a clone of a Status- #
#                   Effect instance.             #
##################################################
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
    didSomething = False
    if(self.turns > 0):
      for x in range(0, len(self.stats)):
        didSomething = True
        if(self.stats[x] == "health"):
          who.changeHealth(self.amounts[x])
          verb = " loses "
          if(self.amounts[x] >= 0):
            verb = " gains "
          plural = "s"
          if(abs(self.amounts[x]) == 1):
            plural = ""
          print(who.name + verb + str(abs(self.amounts[x])) + " hitpoint" + plural + " from the " + self.name + "!")
        elif(self.stats[x].equals("fight")):
          who.changeFight(self.amounts[x])
          verb = ""
          if(abs(self.amounts[x]) > 4):
            verb = "greatly"
          elif(abs(self.amounts[x]) <=2):
            verb = "slightly"
          if(self.amounts[x] >= 0):
            verb = " is " + verb + " strengthened "
          else:
            verb = " is " + verb + " weakened "
          print(who.name + verb + "by the " + self.name + "!")
        elif(self.stats[x].equals("defense")):
          who.changeDefense(self.amounts[x])
          verb = ""
          if(abs(self.amounts[x]) > 4):
            verb = "greatly"
          elif(abs(self.amounts[x]) <=2):
            verb = "slightly"
          if(self.amounts[x] >= 0):
            verb = "'s defenses are " + verb + " reinforced "
          else:
            verb = "'s defenses are " + verb + " diminished "
          print(who.name + verb + "by the " + self.name + "!")
        elif(self.stats[x] == "agility"):
          who.changeAgility(self.amounts[x])
          verb = ""
          if(abs(self.amounts[x]) > 4):
            verb = "greatly"
          elif(abs(self.amounts[x]) <=2):
            verb = "slightly"
          if(self.amounts[x] >= 0):
            verb = "'s speed is " + verb + " increased "
          else:
            verb = "'s speed is " + verb + " decreased "
          print(who.name + verb + "by the " + self.name + "!")
      self.turns -= 1
    if not(didSomething):
      who.statusEffects().pop(self)

  def clone(self):
    return StatusEffect(self.name, self.verb, self.stat, self.amount, self.turns)

##################################################
# Move Class                                     #
##################################################
# PARAMETERS:                                    #
# Name   - The name of the move ("Poison Smog")  #
# Verb   - Who the move can target (String:      #
#          "Single", "Vert Line", etc.)          #
# Uses   - Number of times move can be used per  #
#          rest. (Positive Integer)              #
# StatEfs- All statuseffects the move inflicts   #
#          (StatusEffect Array: [burn, poison])  #
##################################################
# CLASS METHODS:                                 #
# Just getters and setters.                      #
##################################################
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

##################################################
# Gender Class                                   #
##################################################
# PARAMETERS:                                    #
# Name  - Gender name (String: "Male", "Female") #
# Subj  - Subject pronoun (String: "He", "She")  #
# Obj   - Object pronoun  (String: "Him", "Her") #
# PosAdj- PosAdj pronoun  (String: "His", "Her") #
# PosPro- PosPro pronoun  (String: "His", "Hers")#
# Refl  - Reflexive(String: "Himself", "Herself")#
##################################################
# CLASS METHODS:                                 #
# Just getters and setters.                      #
##################################################
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

##################################################
# Item Class                                     #
# Children: Weapon, Armor                        #
##################################################
# PARAMETERS:                                    #
# Name  - Item name (String: "Shiny Locket")     #
# Cost  - Item gold cost  (Poitive Integer)      #
# Value - Item drop value (Poitive Integer)      #
##################################################
# CLASS METHODS:                                 #
# Just getters and setters.                      #
##################################################
class Item(object):
  def __init__(self, name, cost, value):
    self._name = name
    self._cost = cost
  
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
  def value(self):
      return self._value
  @value.setter
  def value(self, value):
      self._value = value


##################################################
# Weapon Class                                   #
# Mother: Item Class                             #
##################################################
# PARAMETERS:                                    #
# Name    - Name         (String: "Greatsword")  #
# Cost    - Gold cost    (Poitive Integer)       #
# Value   - Drop value   (Poitive Integer)       #
# Fight   - Attack bonus (Poitive Integer)       #
# Range   - Range        (Poitive Integer)       #
# Accuracy- Hit rate     (Poitive Integer)       #
# Consist - Attack Bonus Variance                #
#                        (Poitive Integer)       #
# CritRate- Crit rate    (Poitive Integer)       #
##################################################
# CLASS METHODS:                                 #
# Just getters and setters.                      #
##################################################
class Weapon(Item):
  def __init__(self, name, cost, value, fight, rang, accuracy, consistency, critRate):
    super(Weapon, self).__init__(name, cost, value)
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

##################################################
# Armor Class                                    #
# Mother: Item Class                             #
##################################################
# PARAMETERS:                                    #
# Name    - Name          (String: "Chainmail")  #
# Cost    - Gold cost     (Poitive Integer)      #
# Value   - Drop value    (Poitive Integer)      #
# Defense - Defense bonus (Poitive Integer)      #
# Durabil - Armor health  (Poitive Integer)      #
##################################################
# CLASS METHODS:                                 #
# Just getters and setters.                      #
##################################################
class Armor(Item):
  def __init__(self, name, cost, value, defense, durabillity):
    super(Armor, self).__init__(name, cost, value)
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


##################################################
# Fightable Class                                #
# Children: Hero, Enemy                          #
##################################################
# PARAMETERS:                                    #
# Name   - Name                (String: "HERO")  #
# maxFight  - Attack           (Poitive Integer) #
# maxDefense- Damage Absorption(Poitive Integer) #
# maxAgility- Dodge/TurnOrder  (Poitive Integer) #
# maxHealth - Health           (Poitive Integer) #
# learnMoves- All possible moves (Moves Array)   #
# Gender - Gender defaults "it"(Gender)          #
#                                                #
# Other Variables:                               #
# Moves  - Currenly known moves(String: "HERO")  #
# Fight  - Current attack      (Poitive Integer) #
# Defense- Current defense     (Poitive Integer) #
# Agility- Current agility     (Poitive Integer) #
# Health - Current health      (Poitive Integer) #
# Statuseffects - Current status effects         #
#                 (StatusEffect Array)           #
##################################################
# CLASS METHODS:                                 #
# healthColor(self) - Returns a color (green,    #
#                     yellow, orange, red) that  #
#                     corresponds to current     #
#                     health/maxhealth ratio.    #
# getEffect(self, m)- Afflicts the Fightable     #
#                     with the status effects of #
#                     a move. (m: Move)          #
# oneAndDone(self, st)- Afflicts the Fightable   #
#                     with the status effects of #
#                     a move that lasts one turn.#
#                     (m: Move)                  #
# sufferEffects(self)- Causes Fightable to under #
#                      go its current stateffects#
# hasMovesLeft(self)- Returns true if the object #
#                     has any moves remaining    #
# revert(self) - Sets Fightable's attack, defense#
#                and agility back to their max.  #
#                                                #
# Static Methods:                                #
# area(t) - returns the total physical size of a #
#           group of enemies. (t: Enemy Array)   #
# totalHealth(t) - returns the total health of a #
#                  group. (t: Fightable Array)   #
# fight(h, e) - function that allows the user to #
#               fight enemies. (h: Hero array    #
#               e: Enemy array)                  #
#                                                #
# Obsolete Methods to be replaced by GUI:        #
# selectFromCoords - User selects enemy to hit   #
# printHeroes - Prints the heroes and their stats#
# printCoordsS- Invokes printCoords with no one  #
#               highlighted                      # 
# printCoords - Prints enemies, possibly with one#
#               highlighted.                     #
##################################################
class Fightable(object):
  def __init__(self, name, fight, defense, agility, health, moves, gender = Gender("it", "it", "it", "its", "its", "itself")):
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
    if(value > 0):
      self._fight = value
  @property
  def maxFight(self):
      return self._maxFight
  @maxFight.setter
  def maxFight(self, value):
    if(value > 0):
      self._maxFight = value
  @property
  def defense(self):
      return self._defense
  @defense.setter
  def defense(self, value):
    if(value > 0):
      self._defense = value
  @property
  def maxDefense(self):
      return self._maxDefense
  @maxDefense.setter
  def maxDefense(self, value):
    if(value > 0):
      self._maxDefense = value
  @property
  def agility(self):
      return self._agility
  @agility.setter
  def agility(self, value):
    if(value > 0):
      self._agility = value
  @property
  def maxAgility(self):
      return self._maxAgility
  @maxAgility.setter
  def maxAgility(self, value):
    if(value > 0):
      self._maxAgility = value
  @property
  def health(self):
      return self._health
  @health.setter
  def health(self, value):
    if(value >-1):
      self._health = value
  @property
  def maxHealth(self):
      return self._maxHealth
  @maxHealth.setter
  def maxHealth(self, value):
    if(value > 0):
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
    if(self.health >= self.maxHealth * .75):
      return "\033[46m"
    if(self.health >= self.maxHealth * .5):
      return "\033[0;103m"
    if(self.health >= self.maxHealth * .25):
      return "\033[43m"
    return "\033[0;101m"
  def healthColorT(self):
    if(self.health > self.maxHealth * .75):
      return "\033[0;36m"
    if(self.health > self.maxHealth * .5):
      return "\033[0;93m"
    if(self.health > self.maxHealth * .25):
      return "\033[33m"
    if(self.health>0):
      return "\033[0;91m"
    return "\033[0;90m"

  def getEffect(self, m):
    blurb = ""
    x = 0
    while(x<len(m.statusEffects())):
      x+=1
      if(m.statusEffects()[x].turns()>0):
        self.statusEffects.append(m.statusEffects()[x].clone())
        blurb += "{} has been {}".format(self.name, m.statusEffects()[x].verb)
      else:
        blurb += (self.oneAndDone(m.statusEffects()[x]))
    return blurb

  def oneAndDone(self, st):
    suffered = ""
    x=0
    while(x<len(st.stat())):
      if(x!=0):
        suffered += "\n"

      if(st.stat()[x] == "health"):
        self.changeHealth(st.amount()[x])
        verb = " loses "
        if(st.amount()[x] >= 0):
          verb = " gains "
        plural = "s"
        if(abs(st.amount()[x]) == 1):
          plural = ""
        suffered += self.name + verb + str(abs(st.amount()[x])) + " hitpoint" + plural + "!"

      elif(st.stat()[x] == ("fight")):
        self.changeFight(st.amount()[x])
        verb = ""
        if(abs(st.amount()[x]) > 4):
          verb = "greatly"
        elif(abs(st.amount()[x]) <=2):
          verb = "slightly"
        if(st.amount()[x] >= 0):
          verb = " is " + verb + " strengthened"
        else:
          verb = " is " + verb + " weakened"
        suffered += self.name + verb + "!"

      elif(st.stat()[x] == ("defense")):
        self.changeDefense(st.amount()[x])
        verb = ""
        if(abs(st.amount()[x]) > 4):
          verb = "greatly"
        elif(abs(st.amount()[x]) <=2):
          verb = "slightly"
        if(st.amount()[x] >= 0):
          verb = "'s defenses are " + verb + " reinforced"
        else:
          verb = "'s defenses are " + verb + " diminished"
        suffered += self.name + self.verb + "!"

      elif(st.stat()[x] == ("agility")):
        self.changeAgility(st.amount()[x])
        verb = ""
        if(abs(st.amount()[x]) > 4):
          verb = "greatly"
        elif(abs(st.amount()[x]) <=2):
          verb = "slightly"
        if(st.amount()[x] >= 0):
          verb = "'s speed is " + verb + " increased"
        else:
          verb = "'s speed is " + verb + " decreased"
        suffered += self.name + self.verb + "!"
      x+=1

    return suffered
  
  def sufferEffects(self):
    x=0
    while(x<len(self.statusEffects)):
      self.statusEffects[x].doIt(self)
      x+=1
  def hasMovesLeft(self):
    x = 0
    while(x<len(self.moves)):
      if(self.moves[x].left() > 0):
        return True
      x+=1
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
    x=0
    while(x<len(team)):
      health += team[x].health
      x+=1
    return health

  @staticmethod
  def selectFromCoords(coords, enemies, target):
    highlight = [-1]
    highlighted = []
    while(True):
      if(target.find("Single") != -1):
        if(len(highlighted) <= len(enemies)):
          y = 0
          x = 0
          while(y<len(coords[0]) and highlight[0] == -1):
            while(x<len(coords) and highlight[0] == -1):
              if(coords[x][y] != -1  and coords[x][y] in highlighted):
                highlighted.append(coords[x][y])
                highlight = [coords[x][y]]
              x+=1
            y+=1
        else:
          highlight = [-1]
      elif(target.find("Vert Line") != -1):
        if(len(highlighted) <= len(enemies)):
          highlight = []
          unused = False
          x = 0
          while(x<4 and not(unused)):
            y=0
            while(y<len(coords[0]) and not(unused)):
              if(coords[x][y] != -1 and not(coords[x][y] in highlighted)):
                highlighted.append(coords[x][y])
                unused = True
              y += 1
            x += 1
          x-=1
          if(unused):
            y=0
            while(y<len(coords[0])):
              if(coords[x][y] != -1):
                if(not((coords[x][y]) in highlighted)):
                  highlighted.append(coords[x][y])
                highlight.append(coords[x][y])
              y+=1
          else:
            highlight = [-1]
        else:
          highlight = [-1]
      elif(target.find("Hori Line") != -1):
        if(len(highlighted) <= len(enemies)):
          highlight = []
          unused = False
          y = 0
          while(y<len(coords[0]) and not(unused)):
            x = 0
            while(x<len(coords) and not(unused)):
              if(coords[x][y] != -1 and not(coords[x][y] in highlighted)):
                highlighted.append(coords[x][y])
                unused = True
              x += 1
            y += 1
          y-=1
          if(unused):
            x = 0
            while(x<len(coords)):
              if(coords[x][y] != -1):
                if(not(coords[x][y] in highlighted)):
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
      if(highlight[0] == -1):
        nev = "\033[0;93mBack\033[0m"
      print("Which enemy? (Press enter to scroll through options, type a key and press enter to select)\n{}\n\n{}".format(Fightable.printCoords(coords, enemies, highlight), nev))
      if(not(raw_input() == "")):
        return highlight
      if(highlight[0] == -1):
        highlighted = []
      highlight = [-1]
      clear()

  @staticmethod
  def printHeroes(heroes):
    return Fightable.printHeroes(heroes, -1)

  @staticmethod
  def printHeroes(heroes, highlighted):
    string = " ------------------------------------------------ \n|"
    for x in range(0,4):
      try:
        string += heroes[x].healthColorT()
        if(highlighted == x):
          string += "\033[1;37m"
        string += heroes[x].name + "\033[0m"
        d = 0
        while(d<11-len(heroes[x].name)):
          string += " "
          d+=1
        if(x == 2):
          string += " "
        string += "|"
      except:
        string += "\033[0m           "
        if(x == 2):
          string += " "
        string += "|"
    string += "\n|"
    for x in range(0,4):
      try:
        stats = str(heroes[x].health) + "/" + str(heroes[x].maxHealth) + " HP"
        string += heroes[x].healthColorT()
        if(highlighted == x):
          string += "\033[1;37m"
        string += stats + "\033[0m"
        d = 0
        while(d<11-len(stats)):
          string += " "
          d+=1
        if(x == 2):
          string += " "
        string += "|"
      except:
        string += "           "
        if(x == 2):
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
        if(coordinates[x][z] != -1):
          if(coordinates[x][z] in highlight):
            printMe += "\033[0;93m"
          else:
            printMe += enemies[coordinates[x][z]].healthColor()
          printedAName = False
          if(x > 0):
            if(coordinates[x-1][z] != coordinates[x][z]):
              printMe += "\033[0m"
              printMe += "\b|"
              if(coordinates[x][z] in highlight):
                printMe += "\033[0;93m"
              else:
                printMe += enemies[coordinates[x][z]].healthColor()
            else:
              printMe += " "
          if((enemies[coordinates[x][z]]).size == 2):
            if(x > 0):
              if(coordinates[x-1][z] != coordinates[x][z]):
                printMe += enemies[coordinates[x][z]].name
                printedAName = True
              else:
                printMe += "            "
            else:
              printMe += enemies[coordinates[x][z]].name
              printedAName = True
          elif(enemies[coordinates[x][z]].size == 3):
            if(z > 0):
              if(coordinates[x][z-1] != coordinates[x][z]):
                printMe += enemies[coordinates[x][z]].name
                printedAName = True
              else:
                printMe += "            "
            else:
              printMe += enemies[coordinates[x][z]].name
              printedAName = True
          elif(enemies[coordinates[x][z]].size == 4):
            if(x > 0 or z > 0):
              if((x < len(coordinates)-1 and coordinates[x+1][z] == coordinates[x][z]) and z < len(coordinates[0])-1 and coordinates[x][z+1] == coordinates[x][z]):
                printMe += enemies[coordinates[x][z]].name
                printedAName = True
              else:
                if(z > 0 and coordinates[x][z] == coordinates[x][z-1]):
                  printMe += "            "
                  if(x < len(coordinates)-2 and coordinates[x][z] == coordinates[x+1][z]):
                    printMe += "\b"
                else:
                  printMe += "            "
                  if(x > 0 and coordinates[x][z] == coordinates[x-1][z] and x!= len(coordinates)-1):
                    printMe += "\b"
            else:
              printMe += enemies[coordinates[x][z]].name
              printedAName = True
          else:
            printMe += enemies[coordinates[x][z]].name
            printedAName = True
          if(printedAName):
            y = 0
            while(y<11-len(enemies[coordinates[x][z]].name)):
              printMe += " "
              y+=1
          
          if(enemies[coordinates[x][z]].size == 2 or enemies[coordinates[x][z]].size == 4):
            if(x == len(coordinates)-1 or coordinates[x+1][z] != coordinates[x][z]):
              if(enemies[coordinates[x][z]].size == 4 and x > 0 and z > 0 and coordinates[x-1][z] == coordinates[x][z] and coordinates[x][z-1] == coordinates[x][z]):
                printMe += "\b"
              elif(enemies[coordinates[x][z]].size == 2 and x != len(coordinates)-1):
                printMe += "\b"
              printMe += "\033[0m"
              printMe += "|"
              if(coordinates[x][z] in highlight):
                printMe += "\033[0;93m"
              else:
                printMe += enemies[coordinates[x][z]].healthColor()
          if(enemies[coordinates[x][z]].size == 3):
            if(x == len(coordinates)-1 or coordinates[x+1][z] != coordinates[x][z]):
              if(x < len(coordinates)-1 and z > 0 and coordinates[x][z-1] == coordinates[x][z]):
                printMe += "\b"
              elif(x == len(coordinates)-1 and (z == 0 or coordinates[x][z-1] != coordinates[x][z])):
                printMe += " "
              printMe += "\033[0m"
              printMe += "|"
              if(coordinates[x][z] in highlight):
                printMe += "\033[0;93m"
              else:
                printMe += enemies[coordinates[x][z]].healthColor()
          elif(enemies[coordinates[x][z]].size == 1):
            if(x == len(coordinates)-1):
              printMe += " "
            printMe += "\033[0m"
            printMe += "|"
            if(coordinates[x][z] in highlight):
              printMe += "\033[0;93m"
            else:
              printMe += enemies[coordinates[x][z]].healthColor()
          printMe += "\033[0m"
        else:
          printMe += "            "
      if(coordinates[len(coordinates)-1][z] == -1):
        printMe += "|"
      printMe += "\n|"
      for x in range(0, len(coordinates)):
        if(x > 0):
          if(coordinates[x-1][z] != coordinates[x][z]):
            printMe += "\033[0m"
            printMe += "\b|"
        if(coordinates[x][z]!=-1):
          if(coordinates[x][z] in highlight):
            printMe += "\033[0;93m"
          else:
            printMe += enemies[coordinates[x][z]].healthColor()
        printMe += "            "
        printMe += "\033[0m"
        if(x == len(coordinates)-1 and coordinates[x][z] != -1):
          printMe += " "
        if(coordinates[x][z] != -1 and (enemies[coordinates[x][z]].size%2 != 0 or x == len(coordinates) -1)):
          printMe += "\033[0m"
          printMe += "\b|"
      if(coordinates[len(coordinates)-1][z] == -1):
        printMe += "|"
      printMe += "\n"
      if(z == len(coordinates[0])-1):
        printMe += " ------------------------------------------------"
      else:
        printMe += "|"
        for x in range(0, len(coordinates)):
          printMe += "\033[0m"
          if(coordinates[x][z] != -1 and not((enemies[coordinates[x][z]].size == 3 or enemies[coordinates[x][z]].size == 4))):
            printMe += "------------"
          elif(z < len(coordinates[0])-1 and coordinates[x][z+1] != -1 and coordinates[x][z] != coordinates[x][z+1]):
            printMe += "------------"
          elif(coordinates[x][z] != -1 and (enemies[coordinates[x][z]].size == 3 or enemies[coordinates[x][z]].size == 4) and coordinates[x][z+1] == -1):
            printMe += "------------"
          elif(coordinates[x][z] != -1 and enemies[coordinates[x][z]].size == 3 and coordinates[x][z+1] != -1):
            printMe += "\033[0m"
            printMe += "\b|"
            if(coordinates[x][z] in highlight):
              printMe += "\033[0;93m"
            else:
              printMe += enemies[coordinates[x][z]].healthColor()
            printMe += "           "
            if(x != len(coordinates)-1):
              printMe += "\033[0m"
              printMe += "|"
              if(coordinates[x][z] in highlight):
                printMe += "\033[0;93m"
              else:
                printMe += enemies[coordinates[x][z]].healthColor()
            else:
              printMe += " "
          elif(coordinates[x][z] != -1 and enemies[coordinates[x][z]].size == 4 and z < len(coordinates[0])-1 and coordinates[x][z+1] != -1):
            if(x > 0 and coordinates[x-1][z] != coordinates[x][z]):
              printMe += "\033[0m"
              printMe += "\b|"
            if(coordinates[x][z] in highlight):
              printMe += "\033[0;93m"
            else:
              printMe += enemies[coordinates[x][z]].healthColor()
            printMe += "           "
            if(x != len(coordinates)-1 and coordinates[x+1][z] != coordinates[x][z]):
              printMe += "\033[0m"
              printMe += "|"
              if(coordinates[x][z] in highlight):
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
  def fight(heroes, enemies):
    trySize = 0
    while((trySize + 1)*4 < Fightable.area(enemies)):
      trySize+=1
    coordinates = None
    while coordinates == None:
      trySize += 1
      coordinates = [[],[],[],[]]
      for o in range(0, trySize):
        for t in range(0, 4):
          coordinates[t].append(-1)
      tries = 0
      j = 0
      while(j<len(enemies) and tries < 5000):
        e = enemies[j]
        if(e.size == 1):
          x = -1
          y = -1
          attempts = 0
          while(x == -1 and attempts < 50):
            x = randint(0, len(coordinates)-1)
            y = randint(0, len(coordinates[0])-1)
            if(coordinates[x][y] == -1):
              coordinates[x][y] = j
            else:
              x = -1
              y = -1
            attempts += 1
          if(x==-1):
            coordinates = [[],[],[],[]]
            for o in range(0, trySize):
              for t in range(0, 4):
                coordinates[t].append(-1)
            tries += 1
            j = -1
        elif(e.size == 2):
          x = -1
          y = -1
          attempts = 0
          while(x == -1 and attempts < 50):
            attempts += 1
            x = randint(0, len(coordinates)-1)
            y = randint(0, len(coordinates[0])-1)
            if(coordinates[x][y] == -1):
              if(x-1 > 0):
                if(x+1 < len(coordinates)):
                  first = -1
                  if(randint(0, 1) == 1):
                    first = 1
                  if(coordinates[x+first][y] == -1):
                    coordinates[x][y] = j
                    coordinates[x+first][y] = j
                  elif(coordinates[x+(first*-1)][y] == -1):
                    coordinates[x][y] = j
                    coordinates[x+(first*-1)][y] = j
                  else:
                    x = -1
                else:
                  if(coordinates[x-1][y] == -1):
                    coordinates[x][y] = j
                    coordinates[x-1][y] = j
                  else:
                    x = -1
              else:
                if(coordinates[x+1][y] == -1):
                  coordinates[x][y] = j
                  coordinates[x+1][y] = j
                else:
                  x = -1
            else:
              x = -1
              y = -1
          if(x==-1):
            coordinates = [[],[],[],[]]
            for o in range(0, trySize):
              for t in range(0, 4):
                coordinates[t].append(-1)
            tries += 1
            j = -1
        elif(e.size == 3):
          x = -1
          y = -1
          potentials = []
          for d in range(0, len(coordinates)):
            for f in range(0, len(coordinates[0])):
              potentials.append([d, f])
          while(x == -1 and y == -1 and len(potentials) > 0):
            attempt = potentials.pop(randint(0,len(potentials)-1))
            if(coordinates[attempt[0]][attempt[1]] == -1 and coordinates[attempt[0]][attempt[1]+1] == -1):
              x = attempt[0]
              y = attempt[1]
          if(x != -1):
            coordinates[x][y] = j
            coordinates[x][y+1] = j
          else:
            coordinates = [[],[],[],[]]
            for o in range(0, trySize):
              for t in range(0, 4):
                coordinates[t].append(-1)
            tries += 1
            j = -1
        elif(e.size == 4):
          x = -1
          y = -1
          potentials = []
          for d in range(0, len(coordinates)-1):
            for f in range(0, len(coordinates[0])-1):
              potentials.append([f, f+1, d, d+1])
          while(x == -1 and y == -1 and len(potentials) > 0):
            attempt = potentials.pop(randint(0, len(potentials)-1))
            if(coordinates[attempt[2]][attempt[0]] == -1 and coordinates[attempt[3]][attempt[0]] == -1 and coordinates[attempt[2]][attempt[1]] == -1 and coordinates[attempt[3]][attempt[1]] == -1):
              x = attempt[2]
              y = attempt[0]
          if(x != -1):
            coordinates[x][y] = j
            coordinates[x][y+1] = j
            coordinates[x+1][y] = j
            coordinates[x+1][y+1] = j
          else:
            coordinates = [[],[],[],[]]
            for o in range(0, trySize):
              for t in range(0, 4):
                coordinates[t].append(-1)
            tries += 1
            j = -1
        j += 1
      if(tries == 5000):
        coordinates = None
    
    while Fightable.totalHealth(heroes) > 0 and Fightable.totalHealth(enemies) > 0: 
      gamePlanH = []
      gamePlanE = []
      for x in range(0, len(heroes)):
        who = heroes[x]
        who.sufferEffects()
        if(who.health > 0):
          for y in range(0, (who.agility/10)+1):
            deciding = True
            while(deciding):
              times = ""
              if(y==1):
                times = " second"
              elif(y==2):
                times = " third"
              elif(y==3):
                times = " fourth"
              elif(y>0):
                times = " next"
              what = -1
              if(who.gender.subj == "you"):
                what = ask([Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(heroes, x) + "\n\nWhat should you do on your" + times + " turn?\n", "Check stats", "Attack", "Use Technique", "Use Item", "Defend", "Flee"])
              else:
                what = ask([Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(heroes, x) + "\n\nWhat should " + who.name + " do on " + who.gender.posAdj + times + " turn?", "Check stats", "Attack", "Use Technique", "Use Item", "Defend"])
              clear()
              if(what == 1):
                print who.toString()
                clearI()
              elif(what == 2):
                w = Fightable.selectFromCoords(coordinates, enemies, "Single")
                clear()
                if(w[0] != -1):
                  gamePlanH.append("H " + x + " Attack " + w[0])
                  deciding = False
              elif(what == 3):
                if(len(who.moves) > 0):
                  choosing = True
                  while(choosing):
                    moves = []
                    moves.append(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(heroes, x) +"\n\nWhich technique?")
                    for m in range(0, len(who.moves)):
                      moves.append(who.moves[m].name)
                    moves.append("Nevermind")
                    move = ask(moves)-1
                    clear()
                    if(move != len(moves)-1):
                      hi = Fightable.selectFromCoords(coordinates, enemies, heroes[x].moves[move].target)
                      clear()
                      if(hi[0]!=-1):
                        gamePlanH.append("H " + str(x) + " Move " + str(move) + "-" + str(hi))
                        deciding = False
                        choosing = False
                    else:
                      choosing = False
                else:
                  print("No known techniques.")
                  clearI()
              elif(what == 4):
                if(len(who.inventory()) > 0):
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
              elif(what == 5):
                gamePlanH.append("H " + str(x) + " Defend")
                deciding = False
              else:
                if(ask(["Flee the battle?", "Yes", "No"])==1):
                  print("You attempt to flee the battle...")
                  print("But that isn't implemented yet so you fail.")
                  clearI()
                  deciding = False
                  x = 100
                  y = 100
                clear()
        else:
          print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(heroes, x) + "\n\n")
          print(who.name + " is unconscious!")
          clearI()
      for x in range(0, len(enemies)):
        en = enemies[x]
        if(en.health > 0):
            who = None
            while(who == None):
              who = choice(heroes)
              if(who.health == 0):
                who = None
            if(en.hasMovesLeft() and randint(0, 2) == 1):
              move = -1
              while(move == -1):
                move = randint(0, len(en.moves-1))
                if(en.moves[move].left() == 0):
                  move = -1
              gamePlanE.append("E " + str(x) + " Move " + move + "-" + heroes.index(who))
            else:
              gamePlanE.append("E " + str(x) + " Attack " + str(heroes.index(who)))
      
      combinedGamePlan = []

      speeds = []
      for c in range(0, len(gamePlanH)):
        index = int(gamePlanH[c][2:3])
        speeds.append(heroes[index].agility)
        if(speeds[c] > 10):
          if(c > 0):
            divisions = 0
            while(c-divisions > 0 and int(gamePlanH[c-divisions][2:3]) == int(gamePlanH[c][2:3])):
              divisions += 1
            divisions -= 1
            if(divisions>0):
              speeds[c] = speeds[c]-(divisions*10)
          else:
            speeds[c] = 10
        if(speeds[c] == 0):
          speeds[c] = 1
        speeds[c]*=1000
        speeds[c] += c
      for c in range(0, len(speeds)-1):
        if(speeds[c] < speeds[c+1]):
          hold = speeds[c]
          speeds[c] = speeds[c+1]
          speeds[c+1] = hold
          c-=2
          if(c<-1):
            c = -1
      newGamePlanH = []
      for c in range(0, len(speeds)):
        newGamePlanH.append(gamePlanH[(speeds[c]%1000)])
      gamePlanH = newGamePlanH

      while(len(gamePlanH) > 0 or len(gamePlanE) > 0):
        if(len(gamePlanH) > 0):
          if(len(gamePlanE) > 0):
            s1 = heroes[int(gamePlanH[0][2:3])].agility
            s2 = enemies[int(gamePlanE[0][2:3])].agility
            if(s1 > s2):
              combinedGamePlan.append(gamePlanH.pop(0))
            elif(s1 < s2):
              combinedGamePlan.append(gamePlanE.pop(0))
            else:
              if(randint(0, 1) == 1):
                combinedGamePlan.append(gamePlanH.pop(0))
              else:
                combinedGamePlan.append(gamePlanE.pop(0))
          else:
            combinedGamePlan.append(gamePlanH.pop(0))
        else:
          combinedGamePlan.append(gamePlanE.pop(0))

      for x in range(0, len(combinedGamePlan)):
        action = combinedGamePlan[x]
        if(action[0:1] == "H"):
          who = heroes[int(action[2:3])]
          print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(heroes, heroes.index(who)) + "\n")
          who.sufferEffects()
          sleep(500)
          clear()
          if(who.health>0):
            if(action == ("Attack")):
              eWho = enemies[int(action[(action.index("Attack") + 7):])]
              if(eWho.health > 0):
                print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(heroes, heroes.index(who)) + "\n")
                print(who.name + " " + who.weapon.verb + " " + who.gender.posAdj + " " + who.weapon.name + " at " + eWho.title + eWho.name)
                sleep(500)
                if(randint(0, 99) < eWho.agility):
                  print(eWho.name + " dodges the attack!")
                  clearI()
                else:
                  clear()
                  for b in range(0, 3):
                    if(3%(b+1) == 0):
                      print(Fightable.printCoords(coordinates, enemies, [enemies.index(eWho)]) + "\n\n" + Fightable.printHeroes(heroes, heroes.index(who)) + "\n\n" + who.name + " " + who.weapon.verb + " " + who.gender.posAdj + " " + who.weapon.name + " at " + eWho.title + eWho.name)
                    else:
                      print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(heroes, heroes.index(who)) + "\n\n" + who.name + " " + who.weapon.verb + " " + who.gender.posAdj + " " + who.weapon.name + " at " + eWho.title + eWho.name)
                    sleep(100)
                    clear()

                  amount = who.fight - eWho.defense
                  if(amount<=0) :
                    amount = 1
                  eWho.changeHealth(amount * -1)
                  dead = ""
                  if(eWho.health<=0):
                    dead = ("\n" + eWho.name + " has been defeated!")
                    for e in range(0, len(coordinates)):
                      for w in range(0,len(coordinates[0])):
                        if(coordinates[e][w] == int(action[(action.index("Attack") + 7):])):
                          coordinates[e][w] = -1
                  print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(heroes, heroes.index(who)) + "\n")
                  print(eWho.name + " takes " + amount + " damage!" + dead)
                  clearI()
              else:
                print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(heroes, heroes.index(who)) + "\n")
                print(who.name + "'s target is already dead...")
                clearI()
            elif(action == ("Move")):
              move = who.moves[int(action[9:10])]
              print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(heroes, heroes.index(who)) + "\n")
              print(who.name + " uses " + move.name + "!")
              targets = action[action.index("[")+1:len(action)-1]
              targs = []
              happenstances = ""
              while(len(targets) > 0):
                targ = None
                if(targets.index(",") != -1):
                  targ = enemies[int(targets[0:targets.index(",")])]
                  targets = targets[targets.index(" ")+1:]
                else:
                  targ = enemies[int(targets)]
                  targets = ""
                if(targ.health>0):
                  for s in range(0, len(move.statusEffects())):
                    st = move.statusEffects()[s]
                    happenstances += "\n" + targ.getEffect(move) + "\n"
                  if(targ.health<=0):
                    happenstances += (targ.name + " has been defeated!\n\n")
                    for e in range(0, len(coordinates)):
                      for w in range(0,len(coordinates[0])):
                        if(coordinates[e][w] == enemies.index(targ)):
                          coordinates[e][w] = -1
                  targs.append(enemies.index(targ))
                  clear()
                  print(Fightable.printCoords(coordinates, enemies, targs) + "\n\n" + Fightable.printHeroes(heroes, heroes.index(who)) + "\n\n" + who.name + " uses " + move.name + "!\n" + happenstances)
                  sleep(200)
                  clear()
                  print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(heroes, heroes.index(who)) + "\n" + who.name + " uses " + move.name + "!\n\n" + happenstances)
                  sleep(200)
              clearI()
            elif(action == ("Item")):
              pass
            elif(action == ("Defend")):
              pass
          else:
            print(Fightable.printCoordsS(coordinates, enemies) + "\n\n" + Fightable.printHeroes(heroes, heroes.index(who)) + "\n")
            print(who.name + " has fainted!")
            sleep(200)
        else:
          who = enemies[(int(action[2:3]))]
          print(Fightable.printCoords(coordinates, enemies, [enemies.index(who)]) + "\n\n" + Fightable.printHeroes(heroes) + "\n")
          who.sufferEffects()
          sleep(500)
          clear()
          if(who.health > 0):
            if(action == ("Attack")):
              hWho = heroes[int(action[(action.index("Attack") + 7):len(action)-1])]
              if(hWho.health > 0):
                print(Fightable.printCoords(coordinates, enemies, [enemies.index(who)]) + "\n\n" + Fightable.printHeroes(heroes) + "\n")
                print(who.name + " " + who.verb + " at " + hWho.name)
                sleep(500)
                if(randint(0, 99) < hWho.agility):
                  print(hWho.name + " dodges the attack!")
                  clearI()
                else:
                  clear()
                  for b in range(0, 3):
                    if(3%(b+1) == 1):
                      print(Fightable.printCoords(coordinates, enemies, [enemies.index(who)]) + "\n\n" + Fightable.printHeroes(heroes, heroes.index(hWho)) + "\n\n" + who.name + " " + who.verb + " at " + hWho.name)
                    else:
                      print(Fightable.printCoords(coordinates, enemies, [enemies.index(who)]) + "\n\n" + Fightable.printHeroes(heroes) + "\n\n" + who.name + " " + who.verb + " at " + hWho.name)
                    sleep(100)
                    clear()
                  amount = who.fight - hWho.defense
                  if(amount<=0):
                    amount = 1
                  hWho.changeHealth(amount * -1)
                  print(Fightable.printCoords(coordinates, enemies, [enemies.index(who)]) + "\n\n" + Fightable.printHeroes(heroes, heroes.index(hWho)) + "\n")
                  print(hWho.name + " takes " + amount + " damage!")
                  if(hWho.health<=0):
                    print(hWho.name + " has fainted!")
                  clearI()
              else:
                print(Fightable.printCoords(coordinates, enemies, [enemies.index(who)]) + "\n\n" + Fightable.printHeroes(heroes) + "\n")
                print(who.name + "'s target is already down...")
                clearI()
                sleep(200)
            elif(action == ("Move")):
              pass
            elif(action == ("Defend")):
              pass
            elif(action == ("Flee")):
              pass



##################################################
# Hero Class                                     #
# Mother: Fightable Class                        #
##################################################
# PARAMETERS:                                    #
# Name      - Name         (String: "HERO")      #
# learnMoves- All possible moves (Moves Array)   #
# Leveling  - Amount that stats increase each    #
#             each level (Positive Integer Array)#
# Caste     - Hero class (String: "Cleric")      #
# Gender    - Hero gender(Gender)                #
# Weapon    - Hero weapon(Weapon)                #
# Armor     - Hero armor (Armor)                 #
#                                                #
# Other Variables:                               #
# Inventory - Hero's inventory (Item Array)      #
##################################################
# CLASS METHODS:                                 #
# levelUp(self) - Increases the hero's level and #
#                 updates their stats accordingly#
##################################################
class Hero(Fightable):
  def __init__(self, name, moves, leveling, caste, gender, weapon, armor):
    super(Hero, self).__init__(name, 0, 0, 0, 0, moves)
    self._leveling = leveling
    self._caste = caste
    self._inventory = []
    self._level = 1
    self.setGender(gender)
    self._weapon = weapon
    self._armor = armor
  
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
    self.changeMaxHealth(self.leveling[0][self.level-1])
    self.changeMaxFight(self.leveling[1][self.level-1])
    self.changeMaxDefense(self.leveling[2][self.level-1])
    self.changeMaxAgility(self.leveling[3][self.level-1])
    self.changeHealth(self.leveling[0][self.level-1])
    self.changeFight(self.leveling[1][self.level-1])
    self.changeDefense(self.leveling[2][self.level-1])
    self.changeAgility(self.leveling[3][self.level-1])
    if(len(self.learnableMoves) > 0 and (self.level)%(10/len(self.learnableMoves)) == 0):
      m = self.learnableMoves[self.level/(10/len(self.learnableMoves))-1]
      print(self.name + " has learned the new skill: " + m.name + ".")
      self.moves.append(m)

  def __str__(self):
    string = self.name + ", " + self.caste + "\n"
    string += "Level " + str(self.level) + "\n"
    string += "Health: " + str(self.health) + "/" + str(self.maxHealth) + "\n"
    string += "Fight: " + str(self.fight)
    if(self.fight != self.maxFight):
      string += "/" + str(self.maxFight)
      string += "\n"
    string += "Defense: " + str(self.defense)
    if(self.defense != self.maxDefense):
      string += "/" + str(self.maxDefense)
    string += "\n"
    string += "Agility: " + str(self.agility)
    if(self.agility != self.maxAgility):
      string += "/" + str(self.maxAgility)
    string += "\n"
    return string


##################################################
# Enemy Class                                    #
# Mother: Fightable Class                        #
##################################################
# PARAMETERS:                                    #
# Name    - Enemy name (String: "Slime")         #
# Desc    - Enemy desc (String: "A simple slime")#
# Title   - Enemy article (String: "the", "a")   #
# Health  - Enemy health (Positive Integer)      #
# Fight   - Enemy fight (Positive Integer)       #
# Defense - Enemy defense (Positive Integer)     #
# Agility - Enemy agility (Positive Integer)     #
# Moves   - All enemy moves (Moves Array)        #
# Drops   - Possible enemy drops (Item Array)    #
# Size    - Space enemy takes up on field        #
##################################################
# CLASS METHODS:                                 #
# clone(self) - Creates a clone of enemy object  #
##################################################
class Enemy(Fightable):
  def __init__(self, name, desc, title, health, fight, defense, agility, moves, drops, size):
    super(Enemy, self).__init__(name, fight, defense, agility, health, moves)
    self._title = title
    self._drops = drops
    self._desc = desc
    self._size = size
    
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
    return Enemy(self.name, self.desc, self.verb, self.title, self.health, self.fight, self.defense, self.agility, self.moves, self.drops, self.size);

  def __str__(self):
    string = self.name + "\n" + self.desc + "\n"
    string += "Health: " + str(self.health) + "/" + str(self.maxHealth) + "\n"
    string += "Fight: " + str(self.fight)
    if(self.fight != self.maxFight):
      string += "/" + str(self.maxFight)
      string += "\n"
    string += "Defense: " + str(self.defense)
    if(self.defense != self.maxDefense):
      string += "/" + str(self.maxDefense)
      string += "\n"
    string += "Agility: " + str(self.agility)
    if(self.agility != self.maxAgility):
      string += "/" + str(self.maxAgility)
      string += "\n"
    return string


##################################################
# Tile Class                                     #
##################################################
# PARAMETERS:                                    #
# None                                           #
#                                                #
# Other variables:                               #
# Player - True if tile holds player (Bool)      #
# Known  - True if player has visited tile (Bool)#
##################################################
# CLASS METHODS:                                 #
# Just getters and setters.                      #
##################################################
class Tile:
  def __init__(self):
    self._player = False
    self._known = True

  @property
  def player(self):
    return self._player
  @player.setter
  def player(self, value):
    self._player = value
  @property
  def known(self):
    return self._known
  @known.setter
  def known(self, value):
    self._known = value

##################################################
# Floor Class                                    #
##################################################
# PARAMETERS:                                    #
# pX     - Player Starting x location (Integer)  #
# pY     - Player starting Y location (Integer)  #
# spaces - Number of tiles on floor (Integer)    #
#                                                #
# Other variables:                               #
# map - 7x7 array holding layout of floor        #
#       (Integer Array)                          #
##################################################
# CLASS METHODS:                                 #
#                                                #
# Static Methods:                                #
# create(secLay) - creates a floor from a string #
#                  (secLay: String)              #
##################################################
class Floor:
  def __init__(self, pX = randint(0, 6), pY = randint(0, 6), spaces = randint(0, 10)+20):
    self._map = []
    for x in range(0, 7):
      self._map.append([None, None, None, None, None, None, None])
    if(pX < 0 or pX > 6):
      pX = 6
    if(pY < 0 or pY > 6):
      pY = 3
    self._map[pX][pY] = Tile()
    self._map[pX][pY].player = True
    j = 1
    while(j<spaces):
        addx = 0
        addy = 0
        while((addx == 0 and addy == 0) or (addx !=0 and addy != 0)):
          addx = randint(-1, 1)
          addy = randint(-1, 1)
          if(pX==6 and addx>0):
            addx = randint(-1,0)
          if(pX==0 and addx<0):
            addx = randint(0,1)
          if(pY==6 and addy>0):
            addy = randint(-1,0)
          if(pY==0 and addy<0):
            addy = randint(0,1)
        pY += addy
        pX += addx

        if(self._map[pX][pY] == None):
          self._map[pX][pY] = Tile()
          j += 1

  @staticmethod
  def create(secLay):
    floor = Floor(-1, -1, False)
    floor.map = []
    for x in range(0, 7):
      floor.map.append([None, None, None, None, None, None, None])
    n = long(secLay)
    bin = format(n, 'b')
    bin = bin.replace("", " ").strip();
    binary = ""
    for i in range(bin.length()-1, -1):
      binary += bin.charAt(i)
    
    z = 0
    while len(binary) > 0:
      if(binary[0] == "1"):
        floor.map[z/7][z%7] = Tile()
      z += 1
      binary = binary[2:]

    return floor


  @property
  def map(self):
    return self._map
  @map.setter
  def map(self, value):
    self._map = value

  def __str__(self):
    string = " ------- ------- ------- ------- ------- ------- -------"
    for x in range(0, 7):
      for y in range(0, 7):
        if(self.map[x][y]!=None and self.map[x][y].known):
          if(x==0):
            string+=""
          else:
            string+=" -------"
        elif(x>0 and self.map[x-1][y]!=None and self.map[x-1][y].known):
          string+=" -------"
        elif(x!=0):
          string+="        "
      string+="\n"
      for y in range(0, 7):
        if(self.map[x][y]!=None and self.map[x][y].known):
          string+="|"+"\033[44m"+"  "
          string+="     "
          string += "\033[00m"
        elif(y==0):
          string+="|       "
        elif(y>0 and self.map[x][y-1]!=None and self.map[x][y-1].known):
          string+="|       "
        else:
          string+="        "
      string +="|\n"
      for y in range(0, 7):
        if(self.map[x][y]!=None and self.map[x][y].known):
          string+="|"+"\033[44m"+"  "
          string+="     ";
          string += "\033[0m";
        elif(y==0):
          string+="|       "
        elif(y>0 and self.map[x][y-1]!=None and self.map[x][y-1].known):
          string+="|       "
        else:
          string+="        "
      string+="|\n"
      for y in range(0, 7):
        if(self.map[x][y]!=None and self.map[x][y].known):
          string+="|"+"\033[44m"+"   "
          if(self.map[x][y]!=None and self.map[x][y].known):
            if(self.map[x][y].player):
              string += "x   "
            else:
              string+="    "
          else:
              string+="    "
          string += "\033[0m"
        elif(y==0):
          string+="|       "
        elif(y>0 and self.map[x][y-1]!=None and self.map[x][y-1].known):
          string+="|       "
        else:
          string+="        "
      string+="|\n"
    string += " ------- ------- ------- ------- ------- ------- -------"
    return string


##################################################
# Dungeon Class                                  #
##################################################
# PARAMETERS:                                    #
# None                                           #
#                                                #
# Other variables:                               #
# floors - All dungeon floors (Floor Array)      #
##################################################
# CLASS METHODS:                                 #
# dunToBin(self) - Converts dungeon to string    #
#                                                #
# Static Methods:                                #
# binToDun(dun) - Converts string to dungeon     #
#                 (dun: String)                  #
##################################################
class Dungeon:
  def __init__(self):
    self._floors = []
    self._floors.append(Floor(-1, -1))
    for x in range(0, 10):
      self._floors.append(Floor())
    self._floors.append(Floor())

  @property
  def floors(self):
    return self._floors

  @staticmethod
  def binToDun(dun):
    dungeon = Dungeon()
    dungeon.floors = []
    while(len(dun)>1):
      secLay = dun[0:dun.index("/")]
      dun = dun[0:dun.index("/")+1]
      stairLay = dun[0:dun.index("-")]
      dun = dun[0:dun.index("-")]
      dungeon.floors.append(Floor.create(secLay))
    return dungeon

  def equals(self, other):
    return self.convert() == other.convert()

  def dunToBin(self):
    string = "";
    for x in range(0, 12):
      val = 0;
      for z in range(0, 49):
        if(self.floors[x].map()[(z/7)][z%7]!=None):
          val+=(pow(2, (z+1)))
      string += str(val) + " / "
      val = 0
      for z in range(0, 49):
        if(self.floors[x].map()[(z/7)][z%7]!=None):
          if(self.floors[x].map()[(z/7)][z%7].stairs):
            val+=(pow(2, (z+1)))
      string += val + " - "
    return string

  def __str__(self):
    string = ""
    for x in range(0, 12):
      string+=str(self.floors[x])+"\n\n"
    return string




dungeon = Dungeon()
# The dungeon has floors, and the floors
# have an array of arrays that holds each
# tile. This is what must be converted to
# GUI.
print Dungeon()
