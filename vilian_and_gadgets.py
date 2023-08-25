class Gadget():
    def __init__(self, energy, resources):
        self._energy = energy
        self._resources = resources

    ## function to get the energy cost of the gadget
    def getEnergy(self):
        return self._energy

    # function returns the amount of gadgets left
    def getResources(self):
        return self._resources

    # function decreases the amount of gadgets left upon usage
    def decResources(self):
        self._resources = self._resources - 1


## Weapon class
class Weapon(Gadget):
    def __init__(self, energy, damage, resources):
        self._energy = energy
        self._damage = damage
        if resources == "inf":  ## considering -999 to be infinity
            self._resources = -999
        else:
            self._resources = resources

    # function returns the damage caused by the weapon
    def getDamage(self):
        return self._damage


## Shield class
class Shield(Gadget):
    def __init__(self, energy, save_precentage, resources):
        self._energy = energy
        self._save_precentage = save_precentage
        if resources == "inf":  ## considering -999 to be infinity
            self._resources = -999
        else:
            self._resources = resources

    # Function returns the save precentage of the shield
    def getSavePrecent(self):
        return self._save_precentage

# -----------------------------------------------------------------------------------

# Competitor class, the villian's class (Gru/Vector)
class Competitor:
    def __init__(self, health=100, energy=500, isVillian=True):
        self._health = health
        self._energy = energy
        # determine if the competitor evil or not
        self.isVilian = isVillian

    # Function to take damage by the weapon, causes the health to decrease by a certain value
    # the saveprecen is the competitor's shield save precentage
    def damaged(self, value, savePrecen):
        self._health = self._health - value * (1 - savePrecen)

    # Function equippies the competitor with the chosen weapon
    def setWeapon(self, weapon: Weapon):
        self._weapon = Weapon(
            weapon.getEnergy(), weapon.getDamage(), weapon.getResources()
        )

    # Function returns the equippied Weapon
    def getWeapon(self):
        return self._weapon

    # Function equippies the competitor with the chosen shield
    def setShield(self, shield: Shield):
        self._shield = Shield(
            shield.getEnergy(), shield.getSavePrecent(), shield.getResources()
        )

    # Function checks if the current villian is Gru or an evil villian
    def isGru(self):
        return not self.isVilian

    # Function returns current health points
    def getHealth(self):
        return self._health

    # Function returns current energy
    def getEnergy(self):
        return self._energy

    # Function returns the equippied shield
    def getShield(self):
        return self._shield

    # Function decreases the energy by a certain 'value', which is the energy cost of using a specific gadget
    def setEnergy(self, energy, value):
        self._energy = self._energy - value