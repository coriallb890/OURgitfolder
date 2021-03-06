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

    def doIt(self, who, doer=-1):
        blurb = []
        if self.turns > 0:
            for x in range(0, len(self.stats)):
                amount = self.amounts[x]
                if self.stats[x] == "health":
                    who.health += amount
                    verb = " loses "
                    if amount >= 0:
                        verb = " gains "
                    plural = "s"
                    if abs(amount) == 1:
                        plural = ""
                    blurb.append(who.name + verb + str(
                        abs(amount)) + " hitpoint" + plural + " from the " + self.name + "!")
                elif self.stats[x] == "fight":
                    who.fight += amount
                    verb = ""
                    if abs(amount) > 4:
                        verb = "greatly "
                    elif abs(amount) <= 2:
                        verb = "slightly "
                    if amount >= 0:
                        verb = " is " + verb + "strengthened "
                    else:
                        verb = " is " + verb + "weakened "
                    blurb.append(who.name + verb + "by the " + self.name + "!")
                elif self.stats[x] == "defense":
                    who.defense += amount
                    verb = ""
                    if abs(amount) > 4:
                        verb = "greatly "
                    elif abs(amount) <= 2:
                        verb = "slightly "
                    if amount >= 0:
                        verb = "'s defenses are " + verb + "reinforced "
                    else:
                        verb = "'s defenses are " + verb + "diminished "
                    blurb.append(who.name + verb + "by the " + self.name + "!")
                elif self.stats[x] == "agility":
                    who.agility += amount
                    verb = ""
                    if abs(amount) > 4:
                        verb = "greatly "
                    elif abs(amount) <= 2:
                        verb = "slightly "
                    if amount >= 0:
                        verb = "'s speed is " + verb + "increased "
                    else:
                        verb = "'s speed is " + verb + "decreased "
                    blurb.append(who.name + verb + "by the " + self.name + "!")
            self.turns -= 1
            return blurb
        else:
            who.statusEffects.pop(self)

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

    def clone(self):
        return Move(self.name, self.target, self.uses, self.statusEffects)


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
    def __init__(self, name, verb, cost, grade, flavor, fight, range, accuracy, consistency, critRate):
        super(Weapon, self).__init__(name, cost, grade, flavor)
        self._fight = fight
        self.verb = verb
        self._range = range
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

    def clone(self):
        return Weapon(self.name, self.verb, self.cost, self.grade, self.flavor, self.fight, self.range, self.accuracy, self.consistency, self.critRate)


class Armor(Item):
    def __init__(self, name, cost, grade, flavor, defense, durability):
        super(Armor, self).__init__(name, cost, grade, flavor)
        self._defense = defense
        self._durability = durability

    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self, value):
        self._defense = value

    @property
    def durability(self):
        return self._durability

    @durability.setter
    def durability(self, value):
        self._durability = value

    def clone(self):
        return Armor(self.name, self.cost, self.grade, self.flavor, self.defense, self.durability)


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

    def clone(self):
        return Consumable(self.name, self.cost, self.grade, self.flavor, self.statusEffect)

## Weapons
## name // cost // grade // flavor text // fight // range // accuracy // consistency // critRate

cross = Weapon("Cross", "used", 20, 1, "Name: Cross  Attack: 0  Range: 0  Cost: 20", 0, 0, 0, 0, 0)

dagger = Weapon("Dagger", "stabs", 10, 0, "Name: Dagger  Attack: 1  Range: 1  Cost: 10", 1, 1, 80, 1, 10)
polished_dagger = Weapon("Polished Dagger", "stabs", 20, 1, "Name: Polished Dagger  Attack: 2  Range: 1  Cost: 20", 2, 1, 80, 1, 10)
sharpened_dagger = Weapon("Sharpened Dagger", "stabs", 35, 2, "Name: Sharpened Dagger  Attack: 4  Range: 1  Cost: 35", 4, 1, 80, 1, 12)

staff = Weapon("Staff", "casts with", 20, 0, "Name: Staff  Attack: 1,  Range: 2  Cost: 15", 2, 2, 70, 2, 10)
fortified_staff = Weapon("Fortified Staff", "casts with", 30, 1, "Name: Fortified Staff  Attack: 4  Range: 3  Cost: 30", 4, 3, 75, 2, 15)
obsidian_staff = Weapon("Obsidian Staff", "casts with", 45, 2, "Name: Obsidia Staff  Attack: 6  Range: 4  Cost: 45", 6, 4, 80, 2, 20)

axe = Weapon("Axe", "swings", 35, 0, "Name: Axe  Attack: 4  Range: 2  Cost: 35", 4, 2, 60, 3, 15)
red_axe = Weapon("Red Axe", "swings", 40, 1, "Name: Red Axe  Attack: 6  Range: 2  Cost: 40", 6, 2, 60, 3, 15)
battle_axe = Weapon("Battle Axe", "swings", 50, 2, "Name: Battle Axe  Attack: 8  Range: 2  Cost: 50", 8, 2, 55, 3, 15)

sword = Weapon("Sword", "slashes", 30, 0, "Name: Sword  Attack: 4  Range: 3  Cost: 30", 4, 3, 70, 2, 15)
big_sword = Weapon("Big Sword", "slashes", 40, 1, "Name: Big Sword  Attack: 5  Range: 3  Cost: 40", 5, 3, 70, 2, 15)
bigger_sword = Weapon("Bigger Sword", "slashes", 45, 2, "Name: Bigger Sword  Attack: 7  Range: 3  Cost: 45", 6, 3, 70, 2, 15)

glock = Weapon("Glock 18", "shoots", 100, 100, "GLOCK.", 100, 3, 100, 1, 100)

## Armor
## name // cost // grade // flavor text // defense // durability

robes = Armor("Holy Robes", 10, 1, "Name: Holy Robes  Defense: 2  Durability: 50  Cost: 10", 2, 50)

leather = Armor("Leather Armor", 25, 0, "Name: Leather Armor  Defense: 2  Durability: 100  Cost: 25", 2, 100)
chainmail = Armor("Chainmail Armor", 75, 1, "Name: Chainmail Armor  Defense: 4  Durability: 150  Cost: 75", 4, 150)
metalA = Armor("Full-metal Armor", 150, 2, "Name: Leather Armor  Defense: 6  Durability: 200  Cost: 150", 6, 200)

tree = Armor("Tree bark Shield", 25, 0, "Name: Tree Bark Shield  Defense: 3  Max Durability: 80  Cost: 25", 3, 80)
actual = Armor("Actual Shield", 75, 1, "Name: Actual Shield  Defense: 5  Max Durability: 120  Cost: 75", 5, 120)
metalS = Armor("Metal Shield", 150, 2, "Name: Metal Shield  Defense: 7  Max Durability: 160  Cost: 150", 7, 160)


## Status Effects
## name // verb // stats // amounts // turns

# Damage over time type deals
minorBleed = StatusEffect("Minor Bleeding", "bled", ["health"], ["F-25"], 3)
bleed = StatusEffect("Bleeding", "hemorrhaged", ["health"], ["F-50"], 4)
poison = StatusEffect("Poison", "poisoned", ["health"], ["F-75"], 3)

# Generic Attacks
hit = StatusEffect("Generic Hit", "hit", ["health"], ["F-50"], 0)
bludgeon = StatusEffect("Bludgeon", "hit", ["health"], ["F-100"], 0)
bite = StatusEffect("Bite", "bit", ["health"], ["F-125"], 0)
whammy = StatusEffect("Whammy", "whammied", ["health"], ["F-150"], 0)

# Mage-type casts (HAHA TYPECAST JO- not funny.)
shocked = StatusEffect("Shock", "shocked", ["health"], ["F-150"], 0)
burn = StatusEffect("Burn", "burned", ["health"], ["F-100"], 2)
frostbite = StatusEffect("Frostbite", "frostbit", ["health", "agility", "defense"], ["F-50", -3, 1], 2)
plague = StatusEffect("Plague", "plagued", ["health", "defense"], ["F-75", -3], 3)

# Metroidvania Rogue-like (Rogue stuff)
strike = StatusEffect("Cheap Strike", "shanked", ["health"], ["A-100"], 0)
disoriented = StatusEffect("Disorient", "disoriented", ["defense", "agility"], ["D-75", "D100"], 3)
stab = StatusEffect("Stab", "stabbed", ["health"], ["A-125"], 0)
skirted = StatusEffect("Skirt", "skirted", ["health"], ["F-125"], 0)
backstabbed = StatusEffect("Backstab", "stabbed", ["health"], ["A-200"], 0)

# GOOD KNIGHT
swung = StatusEffect("Swung", "swung their sword", ["health"], ["F-100"], 0)
inspired = StatusEffect("Inspiration Strike", "struck", ["fight", "defense"], ["F-125", "D100"], 2)
charged = StatusEffect("Charge", "charged", ["health"], ["F-150"], 0)
skewered = StatusEffect("Skewer", "skewered", ["health"], ["F-100"], 0)
wideSliced = StatusEffect("Wide Slice", "sliced", ["health"], ["F-100"], 0)

# This is the stuff that you use to heal. Probably.
healAura = StatusEffect("Healing Aura", "healed", ["health"], ["H100"], 3)
boostAura = StatusEffect("Boost Aura", "boosted", ["health", "fight"], ["H75", "H125"], 2)
blessedShield = StatusEffect("Blessed Shield", "shielded", ["health", "defense"], ["H75", "H125"], 2)
taylorAura = StatusEffect("Swift Aura", "quickened", ["health", "agility"], ["H75", "H125"], 2)

# Boss crap
demolish = StatusEffect("Demolish", "demolished", ["health"], ["F-120"], 0)
pulv = StatusEffect("Pulverize", "pulverized", ["health"], ["F-140"], 0)
decim8 = StatusEffect("Decimate", "decimated", ["health"], ["F-160"], 0)
fB = StatusEffect("Final Blow", "destroyed", ["health"], ["F-180"], 0)
intimid8 = StatusEffect("Intimidate", "intimidated", ["fight", "defense", "agility"], [15, 12, 10], 3)

# Potion effects and miscellaneous stuff

health1 = StatusEffect("Small Health Potion", "drank", ["health"], [5], 0)
health2 = StatusEffect("Health Potion", "drank", ["health"], [10], 0)
health3 = StatusEffect("Big Health Potion", "drank", ["health"], [15], 0)

fight1 = StatusEffect("Small Fight Potion", "drank", ["fight"], [2], 2)
fight2 = StatusEffect("Fight Potion", "drank", ["fight"], [4], 2)
fight3 = StatusEffect("Big Fight Potion", "drank", ["fight"], [6], 3)

defense1 = StatusEffect("Small Defense Potion", "drank", ["defense"], [2], 2)
defense2 = StatusEffect("Defense Potion", "drank", ["defense"], [4], 2)
defense3 = StatusEffect("Big Defense Potion", "drank", ["defense"], [6], 3)

agility1 = StatusEffect("Small Agility Potion", "drank", ["agility"], [2], 2)
agility2 = StatusEffect("Agility Potion", "drank", ["agility"], [4], 2)
agility3 = StatusEffect("Big Agility Potion", "drank", ["agility"], [6], 3)

everything = StatusEffect("Big Everything Potion", "drank", ["health", "fight", "agility", "defense"], [5, 4, 4, 4], 20)

## Consumables
## name // cost // grade // flavor text // status effect

healthp1 = Consumable("Small Health Potion", 75, 0, "Name: Small Health Potion  Cost: 75", health1)
healthp2 = Consumable("Health Potion", 100, 1, "Name: Health Potion  Cost: 100", health2)
healthp3 = Consumable("Big Health Potion", 150, 2, "Name: Big Health Potion  Cost: 150", health3)

fightp1 = Consumable("Small Fight Potion", 75, 0, "Name: Small Fight Potion  Cost: 75", fight1)
fightp2 = Consumable("Fight Potion", 100, 1, "Name: Fight Potion  Cost: 100", fight2)
fightp3 = Consumable("Big Fight Potion", 150, 2, "Name: Big Fight Potion  Cost: 150", fight3)

defensep1 = Consumable("Small Defense Potion", 75, 0, "Name: Small Defense Potion  Cost: 75", defense1)
defensep2 = Consumable("Defense Potion", 100, 1, "Name: Defense Potion  Cost: 100", defense2)
defensep3 = Consumable("Big Defense Potion", 150, 2, "Name: Big Defense Potion  Cost: 150", defense3)

agilityp1 = Consumable("Small Agility Potion", 75, 0, "Name: Small Agility Potion  Cost: 75", agility1)
agilityp2 = Consumable("Agility Potion", 100, 1, "Name: Agility Potion  Cost: 100", agility2)
agilityp3 = Consumable("Big Agility Potion", 150, 2, "Name: Big Agility Potion  Cost: 150", agility3)

bigp = Consumable("Everything Potion", 200, 2, "Name: Everything Potion  Cost: 200", everything)

### Moves
## name // target // uses // status effect
## Stronger at the bottom, I guess.

# Generic Attacks
toHit = Move("Attack", "Single", 10, [hit])
bludg = Move("Bludgeon", "Single", 5, [bludgeon])
byte = Move("Bite", "Single", 5, [bite])
wham = Move("Whammy", "Single", 2, [whammy])

# Healer-type dealios
auraHeal = Move("Healing Aura", "All", 5, [healAura])
swiftAura = Move("Swift Aura", "All", 5, [taylorAura])
blessedShield = Move("Blessed Shield", "All", 5, [blessedShield])
rejuvHeal = Move("Rejuvinating Heal", "Single", 5, [boostAura])

# Knight-type deals
swing = Move("Swing", "Single", 5, [swung])
inspire = Move("Inspiration", "Single", 3, [inspired])
charge = Move("Charge", "Single", 3, [charged])
skewer = Move("Skewer", "Vert Line", 3, [skewered])
wideSlice = Move("Wide Slice", "Hori Line", 3, [wideSliced])

# Mage-type cast (haha get it, like typecasting!!!!!.... :\)
shock = Move("Shock", "Single", 5, [shocked])
freeze = Move("Freeze", "Single", 4, [frostbite])
burn = Move("Burn", "Single", 3, [burn])
plague = Move("Plague", "All", 2, [plague])

# Rogue-type stuff
cheapStrike = Move("Cheap Strike", "Single", 5, [strike])
disorient = Move("Disorient", "Single", 5, [disoriented])
skirt = Move("Skirt", "Single", 3, [skirted])
backstab = Move("Backstab", "Single", 2, [backstabbed])

# Bleeding and generic damage-over-time types
score = Move("Score", "Single", 3, [stab, minorBleed])
infectStrike = Move("Infected Bite", "Single", 2, [bite, poison])
scratch = Move("Scratch", "Hori Line", 2, [skirted, minorBleed])
deepCut = Move("Deep Cut", "Single", 1, [stab, bleed])
noAttack = Move("Pass", "Single", 100, [])

# Boss stuff... I guess?
demo = Move("Demolish", "Single", 5, [demolish])
pulverize = Move("Pulverize", "Single", 5, [pulv])
decimate = Move("Decimate", "Single", 5, [decim8])
finalblow = Move("Final Blow", "Single", 1, [fB])
intimidate = Move("Charm", "Single", 3, [intimid8])

# As opposed to hurting moves
helpingMoves = [inspire, healAura, taylorAura, blessedShield, boostAura]

## List of items by grade
grade0Items = [dagger, staff, axe, sword, leather, tree, healthp1, fightp1, defensep1, agilityp1]
grade1Items = [polished_dagger, fortified_staff, red_axe, big_sword, chainmail, actual, healthp2, fightp2, defensep2, agilityp2]
grade2Items = [sharpened_dagger, obsidian_staff, battle_axe, bigger_sword, metalA, metalS, healthp3, fightp3, defensep3, agilityp3, bigp]
items = [dagger, axe, sword, leather, tree, healthp1, fightp1, defensep1, agilityp1, polished_dagger, red_axe, big_sword, chainmail, actual, healthp2, fightp2, defensep2, agilityp2,
         sharpened_dagger, battle_axe, bigger_sword, metalA, metalS, healthp3, fightp3, defensep3, agilityp3, bigp]
