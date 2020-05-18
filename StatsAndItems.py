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

    def __str__(self):
        return self.flavor


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

    def __str__(self):
        return Item.__str__(self)


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

    def __str__(self):
        return Item.__str__(self)


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

    def __str__(self):
        return Item.__str__(self)

