

#DEFAULTS#
WIDE_PROJECTILE_STRENGTH = 0.45 #thick wire
NORMAL_PROJECTILE_STRENGTH = WIDE_PROJECTILE_STRENGTH * (2/3) #.3, normal wire
SKINNY_PROJECTILE_STRENGTH = WIDE_PROJECTILE_STRENGTH * (1/3) #.15, thin wire

DEFAULT_PROB_ENTER = 1 #probability of gopher entering trap (not intention)

HUNGER_WEIGHT = 0

def initializeVariables(pref):
    
    global DEFAULT_PROB_ENTER
    DEFAULT_PROB_ENTER = pref["defaultProbEnter"]

    global WIDE_PROJECTILE_STRENGTH
    WIDE_PROJECTILE_STRENGTH = pref["maxProjectileStrength"]

    global NORMAL_PROJECTILE_STRENGTH
    NORMAL_PROJECTILE_STRENGTH = WIDE_PROJECTILE_STRENGTH * (2/3)

    global SKINNY_PROJECTILE_STRENGTH
    SKINNY_PROJECTILE_STRENGTH = WIDE_PROJECTILE_STRENGTH * (1/3)

    global HUNGER_WEIGHT
    HUNGER_WEIGHT = pref["hungerWeight"]
