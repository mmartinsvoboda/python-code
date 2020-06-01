from random import randint
from copy import deepcopy

line = "============================================="

# --------------------------------------------------------
#   Prisera
# --------------------------------------------------------


class Creature(object):
    """Reprezentace jednoduche prisery.

    Attributes:
        name: (str) Jmeno prisery.
        full_health: (int) Pocet bodu zivota (health points) pri plnem zdravi.
        full_energy: (int) Pocet bodu energie (energy points) pri plne energii.
        speed: (int) Prirozene cislo vyjadrujici rychlost prisery.
        attacks: Kolekce utoku prisery (AttackCollection nebo seznam).
        health: (int) Aktualni zdravi prisery (0-full_health).
        energy: (int) Aktualni energie prisery (0-full_energy).
    """

    def __init__(self, name, max_hp, max_e, speed, attacks):
        """Inicialize atributu objektu
        """
        self.name = name
        self.max_hp = max_hp
        self.max_e = max_e
        self.speed = speed
        self.attacks = attacks
        self.hp = max_hp
        self.e = max_e
        self.computer = False

    def __str__(self):
        """Vraci textovou reprezentaci prisery.
        """
        return '%s\t   %s\t   %s\t    %s' % (
            self.name, self.hp, self.e, self.speed)

    def is_down(self):
        if self.hp == 0:
            return True
        return False

    def got_hit(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0

    def attacked(self, en):
        self.e -= en

    def rest(self):
        self.e += int(0.1 * self.max_e)
        if self.e > self.max_e:
            self.e = self.max_e

    def attack(self):
        possible = False
        for attack in self.attacks:
            if possible is not True and attack.difficulty <= self.e:
                possible = True
        if possible is False:
            return -1, "rest"

        move = self.choose_move()

        if move == 0:
            return -1, "Rest"

        if move.gonna_hit():
            return move.get_realdmg(), move
        else:
            return 0, move

    def choose_move(self):
        if self.computer is True:
            print("=============   ", self.name, " ===============")
            print("Attack\t\t\tPower\tAcc\tEnergy")
            for attack in self.attacks:
                print(attack)
            for x in range(4):
                if self.e >= self.attacks[x].difficulty:
                    print()
                    return self.attacks[x]
        else:
            print("=============   ", self.name, " ===============")
            print("Choose an attack:")
            print("\tAttack\t\t\tPower\tAcc\tEnergy")
            x = 0
            for attack in self.attacks:
                x += 1
                print("[", x, "]", attack)
            print("[ 5 ] Rest         \t\t0\t100\t0")

            print()
            x = ""
            while x not in ["1", "2", "3", "4", "5"]:
                try:
                    x = input("Select your move: ")
                    if x == "5":
                        return 0
                    if not self.e >= self.attacks[int(x) - 1].difficulty:
                        x = ""
                        print("Not enougth energy.")
                except:
                    x = ""

            print()
            x = int(x)
            return self.attacks[x - 1]

# --------------------------------------------------------
#   Utok
# --------------------------------------------------------


class Attack(object):

    def __init__(self, name, power, accuracy, difficulty):
        """Inicialize atributu objektu
        """
        self.name = name
        self.power = power
        self.accuracy = accuracy
        self.difficulty = difficulty

    def __str__(self):
        """Vraci textovou reprezentaci prisery.
        """
        return '%s\t\t%s\t%s\t%s' % (
            self.name, self.power, self.accuracy, self.difficulty)

    def gonna_hit(self):
        x = randint(1, 100)
        if x <= self.accuracy:
            return True
        return False

    def get_realdmg(self):
        x = randint(70, 130)
        result = self.power * x / 100
        return int(result)

# --------------------------------------------------------
#  Zapas
# --------------------------------------------------------


class Match(object):
    """Trida reprezentujici stav zapasu mezi dvema priserami.

    Attributes:
      creatures: Seznam dvou zapasicich priser.
      attacker: Prisera, ktera v aktualnim kole utoci.
      defender: Prisera, na kterou je aktualne utoceno.
    """

    def __init__(self, one, two):
        self.one = one
        self.two = two

    def header(self):
        print()
        print(line)
        print("Name\t\t   HP\tEnergy\tSpeeed")
        print("#1 ", self.one)
        print("#2 ", self.two)
        print(line)

    def start(self):
        print()
        print(line)
        print(self.one.name, "  VS  ", self.two.name)
        print(line)
        print()

        if self.faster():
            self.attack(self.one, self.two)
        else:
            self.attack(self.two, self.one)

    def faster(self):
        if self.one.speed >= self.two.speed:
            return True
        return False

    def attack(self, att, deff):
        print()
        if att == self.one:
            print("Player one plays")
        else:
            print("Player two plays")
        x, attack = att.attack()

        if x == 0:
            print(att.name, " has missed the attack ", attack.name)
            att.attacked(attack.difficulty)
        elif x == -1:
            att.rest()
            print("Resting...")
        else:
            deff.got_hit(x)
            att.attacked(attack.difficulty)
            print("{} has used {}".format(att.name, attack.name))
            print("{} did {}dmg.".format(attack.name, x))
            print("{} now has {}HP".format(deff.name, deff.hp))

        deff.rest()

        self.header()

        try:
            input("\nPress enter to continue...")
        except SyntaxError:
            pass

        if att.is_down() is False and deff.is_down() is False:
            self.attack(deff, att)


# --------------------------------------------------------
#  Main Function
# --------------------------------------------------------
class Main():

    def create_stuff():
        # Pikachu
        Thunder_Shock = Attack("Thunder Shock", 60, 50, 30)
        Quick_Attack = Attack("Quick Attack ", 50, 80, 30)
        Feint = Attack("Feint        ", 30, 90, 10)
        Electro_Ball = Attack("Electro Ball ", 20, 100, 5)

        p_attacks = []
        p_attacks.append(Electro_Ball)
        p_attacks.append(Feint)
        p_attacks.append(Quick_Attack)
        p_attacks.append(Thunder_Shock)

        # Squirtle
        Tackle = Attack("Tackle       ", 20, 100, 5)
        Water_Gun = Attack("Water Gun    ", 35, 90, 15)
        Hydro_Pump = Attack("Hydro Pump   ", 50, 50, 20)
        Aqua_Tail = Attack("Aqua Tail    ", 60, 60, 50)

        s_attacks = []
        s_attacks.append(Tackle)
        s_attacks.append(Water_Gun)
        s_attacks.append(Aqua_Tail)
        s_attacks.append(Hydro_Pump)

        # Charmander
        Ember = Attack("Ember        ", 20, 100, 5)
        Fire_Fang = Attack("Fire Fang     ", 30, 80, 15)
        Inferno = Attack("Inferno      ", 50, 50, 30)
        Flamethrower = Attack("Flamethrower", 60, 60, 50)

        c_attacks = []
        c_attacks.append(Ember)
        c_attacks.append(Fire_Fang)
        c_attacks.append(Inferno)
        c_attacks.append(Flamethrower)

        # Bulbasaur
        Vine_Whip = Attack("Vine Whip    ", 20, 100, 5)
        Razor_Leaf = Attack("Razor Leaf  ", 55, 55, 45)
        Seed_Bomb = Attack("Seed Bomb   ", 40, 70, 35)
        Double_Edge = Attack("Double-Edge", 90, 30, 10)

        b_attacks = []
        b_attacks.append(Vine_Whip)
        b_attacks.append(Seed_Bomb)
        b_attacks.append(Razor_Leaf)
        b_attacks.append(Double_Edge)

        global Pikachu
        global Squirtle
        global Charmander
        global Bulbasaur
        Pikachu = Creature("Pikachu   ", 80, 100, 70, p_attacks)
        Squirtle = Creature("Squirtle  ", 100, 80, 50, s_attacks)
        Charmander = Creature("Charmander", 90, 90, 60, c_attacks)
        Bulbasaur = Creature("Bulbasaur ", 110, 70, 40, b_attacks)

    def computer_plays():
        print("How many players will play?")
        print(line)
        print("[1] ... One player")
        print("[2] ... Two players")
        print(line)
        x = input("Select number of players: ")
        while x not in ["1", "2"]:
            x = input("Select number of players: ")
        print()

        if x == "1":
            return True
        else:
            return False

    def pokemon_select():
        print(line)
        print("Name\t\t   HP\tEnergy\tSpeeed")
        print("[1]", Pikachu)
        print("[2]", Squirtle)
        print("[3]", Charmander)
        print("[4]", Bulbasaur)
        print(line)

        x = input("Select your Pokemon: ")
        while x not in ["1", "2", "3", "4"]:
            x = input("Select your Pokemon: ")
        print()
        if x == "1":
            return Pikachu
        elif x == "2":
            return Squirtle
        elif x == "3":
            return Charmander
        return Bulbasaur

    def main():
        # Ve funkci main vytvorte kolekci (seznam) utoku a priser,
        # nechejte vybrat mod hry a priseru/prisery,
        # vytvorte novy zapas (instance tridy Match)
        # a spuste ho (napr. match.run()).

        Main.create_stuff()
        computer_play = Main.computer_plays()

        first = deepcopy(Main.pokemon_select())

        if computer_play is True:
            x = randint(1, 4)
            if x == 1:
                second = Pikachu
            elif x == 2:
                second = Squirtle
            elif x == 3:
                second = Charmander
            else:
                second = Bulbasaur
            second.computer = True
        else:
            second = deepcopy(Main.pokemon_select())

        match = Match(first, second)
        match.start()

        if first.is_down():
            print(
                "{} has fainted. {} is the winner!".format(
                    first.name, second.name))
        else:
            print(
                "{} has fainted. {} is the winner!".format(
                    second.name, first.name))

        print("\n\nThe match is over...")
        input()

Main.main()
