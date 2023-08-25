## import random library for random.randint
import random

## import competitors class and gadgets class (with its inherits)
from vilian_and_gadgets import *


# Global variables:
## (The gadgets attributes):
## weapons [..,  {energy, damage, resources}, ..]
gru_weapons = [
    [50, 11, "inf"],
    [88, 18, 5],
    [92, 10, 3],
    [120, 20, 1],
]  ## third weapon has special power
vector_weapons = [[40, 8, "inf"], [56, 13, 8], [100, 22, 3]]

gru_shields = [[20, 0.4, "inf"], [50, 0.9, 2]]
vector_shields = [
    [15, 0.32, "inf"],
    [40, 0.8, 3],
]  ## both shields can't avoid Kalman missle

## Fight class
class Fight:
    # Function where the actual fight between the two competitors goes on
    def fight(self, gru: Competitor, vector: Competitor):
        # return value of the function, gru_won == 1 means gru won, gru_won == 2 means gru lost, gru_won == 3 means it's a tie
        gru_won = 0
        round_counter = 1
        while gru.getHealth() > 0 and vector.getHealth() > 0:
            print("__________________________________________________________\n")
            print("Round {}\n".format(round_counter))
            round_counter += 1
            print(
                "HP:   GRU -> {}   Vector -> {}\n".format(
                    gru.getHealth(), vector.getHealth()
                )
            )
            print(
                "Energy:   GRU -> {}   Vector -> {}\n".format(
                    gru.getEnergy(), vector.getEnergy()
                )
            )

            vector_energy = vector.getEnergy()
            gru_energy = gru.getEnergy()

            vector_shield = vector.getShield()
            vector_shield_energy = vector_shield.getEnergy()
            vector_shield_res = vector_shield.getResources()

            vector_save = 0
            # if he can use the shield
            if vector_energy >= vector_shield_energy and (
                vector_shield_res > 0 or vector_shield_res == -999
            ):
                ## Use shield
                vector.setEnergy(vector_energy, vector_shield_energy)
                vector_save = vector_shield.getSavePrecent()
                vector.setEnergy(vector_energy, vector_shield_energy)
                if vector_shield_res != -999:
                    vector_shield.decResources()
                print("Vector wore his Shield.\n")
            else:
                print("Vector is going on without his Shield.\n")

            gru_weapon = gru.getWeapon()
            gru_weapon_energy = gru_weapon.getEnergy()
            gru_weapon_resources = gru_weapon.getResources()
            if gru_weapon.getDamage() == 20:  ## Kalman Missle
                vector_save = 0
            vector_discount_damage = 0

            # if he can use the weapon
            if gru_weapon_energy <= gru_energy and (
                gru_weapon_resources > 0 or gru_weapon_resources == -999
            ):
                ## Use weapon

                if gru_weapon.getDamage() == 10:  ## Mega Magnet
                    vector_discount_damage = 1 - 0.2
                vector.damaged(gru_weapon.getDamage(), vector_save)
                if gru_weapon_resources != -999:
                    gru_weapon.decResources()
                gru.setEnergy(gru_energy, gru_weapon_energy)
                print("Gru has shot a bullet on Vector.\n")
            else:
                vector_discount_damage = 0
                print("Gru held his fire.\n")

            gru_shield = gru.getShield()
            gru_shield_energy = gru_shield.getEnergy()
            gru_shield_res = gru_shield.getResources()

            # if he can use the shield
            if gru_energy >= gru_shield_energy and (
                gru_shield_res > 0 or gru_shield_res == -999
            ):
                ## Use shield
                gru.setEnergy(gru_energy, gru_shield_energy)
                gru_save = gru_shield.getSavePrecent()
                gru.setEnergy(gru_energy, gru_shield_energy)
                if gru_shield_res != -999:
                    gru_shield.decResources()
                print("Gru wore his Shield.\n")
            else:
                print("Gru is going on without his Shield.\n")

            vector_weapon = vector.getWeapon()
            vector_weapon_energy = vector_weapon.getEnergy()
            vector_weapon_resources = vector_weapon.getResources()

            # if he can use the weapon
            if vector_weapon_energy <= vector_energy and (
                vector_weapon_resources > 0 or vector_weapon_resources == -999
            ):
                gru.damaged(
                    vector_weapon.getDamage() * vector_discount_damage, gru_save
                )
                if vector_weapon_resources != -999:
                    vector_weapon.decResources()
                vector.setEnergy(vector_energy, vector_weapon_energy)
                print("Vector has shot a bullet on Gru.\n")
            else:
                print("Vector has held his fire.\n")
            if gru.getHealth() <= 0 and vector.getHealth() <= 0:
                gru_won = self.tieBreaker(gru, vector)
                break
            if gru.getHealth() <= 0:
                gru_won = 2
                break
            if vector.getHealth() <= 0:
                gru_won = 1
                break
            if (
                gru.getEnergy() <= gru.getShield().getEnergy()
                and vector.getEnergy() <= vector.getShield().getEnergy()
            ):
                ## they both don't have energy to fight (shield's energy is always lower than  weapon energy)
                gru_won = self.tieBreaker(gru, vector)
                break
            if (
                gru.getWeapon().getResources() <= 0
                and vector.getWeapon().getResources() <= 0
            ):
                if (
                    gru.getWeapon().getResources() != -999
                    and vector.getWeapon().getResources() != -999
                ):
                    gru_won = self.tieBreaker(gru, vector)
                    break
            # if gru's ammo finished
            if (
                gru.getWeapon().getResources() <= 0
                and gru.getWeapon().getResources() != -999
                and gru.getShield().getResources() <= 0
                and gru.getShield().getResources() != -999
            ):
                gru_won = 2
                break
            # if vector's ammo finished
            if (
                vector.getWeapon().getResources() <= 0
                and vector.getWeapon().getResources() != -999
                and vector.getShield().getResources() <= 0
                and vector.getShield().getResources() != -999
            ):
                gru_won = 1
                break
        print("GAME OVER!\n")
        print(
            "Final HP:   Gru ->  {}     Vector ->  {}\n".format(
                gru.getHealth(), vector.getHealth()
            )
        )
        print(
            "Final Energy:   GRU -> {}   Vector -> {}\n".format(
                gru.getEnergy(), vector.getEnergy()
            )
        )
        ammo_gru = gru.getWeapon().getResources()
        if ammo_gru == -999:
            ammo_gru = "inf"
        ammo_vec = vector.getWeapon().getResources()
        if ammo_vec == -999:
            ammo_vec = "inf"
        print("Final Ammo:  Gru -> {}   Vector ->  {}\n".format(ammo_gru, ammo_vec))

        return gru_won

    # function to give advantage if a scenario of ties is happening
    # for example, if both competitors' ammos are finished at same time..
    # we will look at who has the higher health points
    def tieBreaker(self, gru: Competitor, vector: Competitor):
        if gru.getHealth() > vector.getHealth():
            return 1  ## gru won
        elif gru.getHealth() < vector.getHealth():
            return 2  ## gru lost
        else:
            return 3  ## tie


## Game class to print out the game outcome
class Game:
    # Function returns true if gru won
    def outcome(self, competitor):
        if competitor == 1:  # 1 if Gru won
            print("GRU WON!\n")
            return True
        elif competitor == 2:
            print("GRU LOST :(\n")
            return False  ## 2 if Gru lost
        else:
            print("TIE!\n")  ## 3 if tie
            return False

    # Function of the start of the game
    def play_game(self):
        print("Welcome to the Game!\n\n")
        gru = Competitor(isVillian=False)
        vector = Competitor(isVillian=True)
        print("It is time for Gru to choose his weapon...\n")
        print("   Name          Energy    Damage    Resources")
        print("1. Freeze Gun      50        11         Inf\n")
        print("2. Electric Prod   88        18          5\n")
        print("3. Mega Magnet     92        10          3\n")
        print("4. Kalman Missle  120        20          1\n")
        option_gru = int(input("Enter desired weapon for Gru: "))
        grus_weapon = Weapon(
            gru_weapons[option_gru - 1][0],
            gru_weapons[option_gru - 1][1],
            gru_weapons[option_gru - 1][2],
        )
        gru.setWeapon(grus_weapon)
        print("It is time for Gru to choose his shield...\n")
        print("   Name          Energy     Save    Resources")
        print("1. BarrierGun      20        40 %         Inf\n")
        print("2. Selective Perm  50        90 %          2\n")
        option_gru_s = int(input("Enter desired shield for Gru: "))
        grus_shield = Shield(
            gru_shields[option_gru_s - 1][0],
            gru_shields[option_gru_s - 1][1],
            gru_shields[option_gru_s - 1][2],
        )
        gru.setShield(grus_shield)
        ## taking second approach: letting vector choose his weapon and chield randomly by probablistic measurement
        print("Now, Vector is choosing his gadgets...\n")
        vector_w_names = ["Laser Blasters", "Plasma Grenades", "Sonic Resonance Cannon"]
        vector_s_names = ["Energy Net Trap", "Quantum Deflector"]
        vector_w = random.randint(
            0, 2
        )  ## randomly choosing a weapon from 0 to 2 included
        vector_s = random.randint(0, 1)  ## choosing a shield
        print("\n\n")
        print(
            "Oh wow! Vector has chosen "
            + vector_w_names[vector_w]
            + " as his weapon.\n"
        )
        print(
            "He is going ultra-defensive!\nHe has chosen "
            + vector_s_names[vector_s]
            + " as his shield.\n"
        )
        vectors_weap = Weapon(
            vector_weapons[vector_w][0],
            vector_weapons[vector_w][1],
            vector_weapons[vector_w][2],
        )
        vectors_shield = Shield(
            vector_shields[vector_s][0],
            vector_shields[vector_s][1],
            vector_shields[vector_s][2],
        )

        vector.setShield(vectors_shield)
        vector.setWeapon(vectors_weap)
        curr_fight = Fight()
        who_won = curr_fight.fight(gru, vector)
        self.outcome(who_won)