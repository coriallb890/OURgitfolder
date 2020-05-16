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
        return self._verb

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
        return StatusEffect(self.name, self.verb, self.stats, self.amounts, self.turns)


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
    def __init__(self, name, cost, grade, flavor):
        self._name = name
        self._cost = cost
        self._grade = grade
        self._flavor = flavor

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

    @property
    def flavor(self):
        return self._flavor

    @flavor.setter
    def flavor(self, value):
        self._flavor = value


class Weapon(Item):
    def __init__(self, name, cost, grade, flavor, fight, rang, accuracy, consistency, critRate):
        super(Weapon, self).__init__(name, cost, grade, flavor)
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
    def __init__(self, name, cost, grade, flavor, defense, durabillity):
        super(Armor, self).__init__(name, cost, grade, flavor)
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

class Consumable(Item):
    def __init__(self, name, cost, grade, flavor, statusEffect):
        super(Consumable, self).__init__(name, cost, grade, flavor)
        self._statusEffect = statusEffect

    @property
    def statusEffect(self):
        return self._statusEffect

    @statusEffect.setter
    def statusEffect(self, value):
        self._statusEffect = value

## Weapons
## name // cost // grade // flavor text // range // accuracy // accuracy // consistency // critRate

dagger = Weapon("Dagger", 10, 0, "You can't get more rogue-like than fighting with a dagger. It's nice and light, but not exactly the sharpest.", 1, 1, 80, 1, 10)
polished_dagger = Weapon("Polished Dagger", 20, 1, "Somehow, you found yourself a nice shiny dagger in this decrepit tower. It feels the same as your older dagger, but man... look how shiny it is!", 2, 1, 80, 1, 10)
sharpened_dagger = Weapon("Sharpened Dagger", 35, 2, "A beautiful dagger with a sharp, honed edge. It looks pretty dope, gotta say.", 4, 1, 80, 1, 12)

axe = Weapon("Axe", 35, 0, "It's more hefty than your original dagger, but it certainly packs a much larger punch. Er... cut?", 5, 3, 60, 1, 15)
red_axe = Weapon("Red Axe", 35, 1, "It's a nice, shiny red axe. You're not sure why, but something about it feels a bit anachronistic.", 6, 2, 60, 1, 15)
battle_axe = Weapon("Battle Axe", 40, 2, "It's a large, black battle axe, towering even over you. It's super sharp, super nice, and SUPER HEAVY.", 8, 2, 55, 1, 15)

sword = Weapon("Sword", 30, 0, "Yeah, it's a sword. What are you gonna do about it? You gotta carry a sword if you wanna fight monsters. It's the law.", 4, 3, 70, 1, 15)
big_sword = Weapon("Big Sword", 40, 1, "A wise man once asked, \"What's better than a regular-sized sword?\" Now you know the answer.", 5, 3, 70, 1, 15)
bigger_sword = Weapon("Bigger Sword", 45, 2, "Now, this is just ridiculous. Do you really NEED a sword THIS BIG?!? Yes you do.", 6, 3, 70, 1, 15)

glock = Weapon("Glock 18", 100, 100, "yeah i got a glock. the real question is... where am i getting all this ammo?", 100, 3, 100, 1, 100)

## Armor
## name // cost // grade // flavor text // defense // durability

leather = Armor("Leather Armor", 25, 0, "Some loose pieces of leather carelessly sewn together", 2, 100)
chainmail = Armor("Chainmail Armor", 75, 1, "An actual piece of armor. Better than nothing I suppose.", 4, 150)
metalA = Armor("Full-metal Armor", 150, 2, "A full on suit of armor. Now you can feel protected", 6, 200)

tree = Armor("Tree bark Shield", 25, 0, "Just a big piece of tree bark... Maybe it can help?", 3, 80)
actual = Armor("Actual Shield", 75, 1, "A wooden shield with an actual handle. Now we're getting somehwere.", 5, 120)
metalS = Armor("Metal Shield", 150, 2, "A sturdy metal shield that can protect you big time.", 7, 160)

## Status Effects
## name // verb // stats // amounts // turns

poison = StatusEffect("Poison", "poisoned", ["health"], [-3], 3)
strike = StatusEffect("Cheap Strike", "shanked", ["health"], ["F-150"], 1)

health1 = StatusEffect("Small Health", "drank", ["health"], [5], 1)
health2 = StatusEffect("Health", "drank", ["health"], [10], 1)
health3 = StatusEffect("Big Health", "drank", ["health"], [15], 1)

aura = StatusEffect("Boost Aura", "boosted", ["health", "fight"], [3, 2], 2)

fight1 = StatusEffect("Small Fight", "drank", ["fight"], [2], 2)
fight2 = StatusEffect("Fight", "drank", ["fight"], [4], 2)
fight3 = StatusEffect("Big Fight", "drank", ["fight"], [6], 3)

defense1 = StatusEffect("Small Defense", "drank", ["defense"], [2], 2)
defense2 = StatusEffect("Defense", "drank", ["defense"], [4], 2)
defense3 = StatusEffect("Big Defense", "drank", ["defense"], [6], 3)

agility1 = StatusEffect("Small Agility", "drank", ["agility"], [2], 2)
agility2 = StatusEffect("Agility", "drank", ["agility"], [4], 2)
agility3 = StatusEffect("Big Agility", "drank", ["agility"], [6], 3)

everything = StatusEffect("Big Everything", "drank", ["health", "fight", "agility", "defense"], [5, 4, 4, 4], 20)

## Consumables
## name // cost // grade // flavor text // status effect

healthp1 = Consumable("Small Health Potion", 75, 0, "\"Artifically Flavored.\" Comforting.", "health1")
healthp2 = Consumable("Health Potion", 100, 1, "", "health2")
healthp3 = Consumable("Big Health Potion", 150, 2, "", "health3")

fightp1 = Consumable("Small Fight Potion", 75, 0, "It's what's the plants crave.", "fight1")
fightp2 = Consumable("Fight Potion", 100, 2, "", "fight2")
fightp3 = Consumable("Big Fight Potion", 150, 2, "", "fight3")

defensep1 = Consumable("Small Defense Potion", 75, 1, "", "defense1")
defensep2 = Consumable("Defense Potion", 100, 1, "", "defense2")
defensep3 = Consumable("Big Defense Potion", 150, 2, "", "defense3")

agilityp1 = Consumable("Small Agility Potion", 75, 0, "", "agility1")
agilityp2 = Consumable("Agility Potion", 100, 1, "", "agility2")
agilityp3 = Consumable("Big Agility Potion", 150, 2, "", "agility3")

bigp = Consumable("Everything Potion", 200, 2, 'Known in some cultures as "Suicide."', "everything")

## List of items by grade
grade0Items = [dagger, axe, sword, leather, tree, healthp1, fightp1, defensep1, agilityp1]
grade1Items = [polished_dagger, red_axe, big_sword, chainmail, actual, healthp2, fightp2, defensep2, agilityp2]
grade2Items = [sharpened_dagger, battle_axe, bigger_sword, metalA, metalS, healthp3, fightp3, defensep3, agilityp3, bigp]
