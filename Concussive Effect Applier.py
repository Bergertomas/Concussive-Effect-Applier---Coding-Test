# -*- coding: utf-8 -*-
"""
@author: Tomas Berger
"""

import random
import math
import gc

# DEFINES:
MAX_FLASH_RADIUS = 10
MAX_LOWRISK_RADIUS = 18
MAX_HIGHRISK_RADIUS = 50
MIN_FLASH_RADIUS = 8
MIN_LOWRISK_RADIUS = 15 
MIN_HIGHRISK_RADIUS = 40
MAX_BLINDNESS_SECONDS = 2
MAX_DEAFNESS_SECONDS = 60
LOW_EFFECT_DEAFNESS_SECONDS = 40
FLASH_RADIUS_INDEX = 0
LOWRISK_RADIUS_INDEX = 1
HIGHRISK_RADIUS_INDEX = 2


def setBlindness(soldier, duration):
    soldier.setBlindness(duration)

def setDeafness(soldier, duration):
    soldier.setDeafness(duration)

def randomize_sea_level():
    """
    returns a random value for the level's sea level (value<=100)
    """
    
    return int(random.random() * 100)  


def get_units_list():
    """Returns a list of all soldiers currently in the simulation."""
    soldiersList = []
    for obj in gc.get_objects():
        if isinstance(obj, Soldier):
            soldiersList.append(obj)
    return soldiersList


class Soldier(object):
    """
    A soldier who is present in the environment.
    """
    def __init__(self, name):
        """
        Initializes a Soldier object.
        """
        # Soldier ID is a randomly generated string consisting of 3 numbers.
        ID = str(round((random.uniform(100,999))))
        self.ID = ID
        # soldier's position is defaultly set to [0,0,0]
        self.position = [0,0,0]
        # blindness and deafness represent a number of seconds
        self.blindness = 0
        self.deafness = 0
        self.name = name
    def getID(self):
        # gets the ID number (string) of the instance
        print (self.ID)
    def getName(self):
        return(self.name)
    def setPosition(self, position):
        # sets the position (a list) of the soldier
        self.position = position
    def getPosition(self):
        # gets the position (list) of the soldier
        return(self.position)
    def setBlindness(self, blindness):
        #sets a blindness effect on the soldier; numbers represent seconds
        self.blindness = blindness
    def setDeafness(self, deafness):
        #sets a deafness effect on the soldier; numbers represent seconds
        self.deafness = deafness
    def getBlindness(self):
        #prints blindness status
        print(self.blindness)
    def getDeafness(self):
        #prins deafness status
        print(self.deafness)
    def reset_concussive_effects(self):
        #resets all concussive effects back to none
        self.blindness = 0
        self.deafness = 0
      

def caliber_to_radius(caliber):
    """
    assumes that caliber is a string of either '105mm' or '120'mm. returns the resulting radius for all three areas of effect.
    """
    flash_radius = 0
    low_risk_radius = 0
    high_risk_radius = 0
    if caliber == "120mm":
        #sets radius according to the 120mm caliber
        flash_radius = MAX_FLASH_RADIUS
        low_risk_radius = MAX_LOWRISK_RADIUS
        high_risk_radius = MAX_HIGHRISK_RADIUS
    elif caliber == "105mm":
        #sets radius according to the 105mm caliber
        flash_radius = MIN_FLASH_RADIUS
        low_risk_radius = MIN_LOWRISK_RADIUS
        high_risk_radius = MIN_HIGHRISK_RADIUS
    else:
        #in case of an unexpected caliber input 
        raise NameError
        print("caliber was not typed in correctly. please type in '120mm' or '105mm'")
    return flash_radius, low_risk_radius, high_risk_radius   
        

def randomize_soldier_position(soldiersList):
    """
    Gets as input a list of instances of soldiers, and assigns a random location to each one of the instances.
    """
    for i in soldiersList:
        # for the values of X and Y we generate a random floating point number extending to 3 digits. Z is predetermined and constant.
        X = round((random.uniform(-1,1) * 100), 3)
        Y = round((random.uniform(-1,1) * 100), 3)
        Z = seaLevel
        # sets the [X,Y,Z] values for each of the instances.
        i.setPosition([X,Y,Z])
        print(i.position)


def determine_concussive_severity(distance, radius, concussive, area=""):
    """
    Expects an input of the soldier's distance from the muzzle (in meters); the radius in accordance to the used caliber;
    concussive, a string describing the desired concussive effect to be inflicted upon the soldier; and
    area, the area in which the soldier is positioned, to which a default value of an empty string is assigned.
    Returns a float, rounded up to three decimal digits, representing the appropriate duration (in seconds)
    of the desired concussive effect, based on the soldier's angle
    relative to the muzzle and the soldier's distance from the muzzle.
    """
    severity = 1 - (distance/radius)
    if area == "Low Effect":
        if concussive == "Deafness":
            severity*= LOW_EFFECT_DEAFNESS_SECONDS
    else:
        if concussive == "Blindness":
            severity *= MAX_BLINDNESS_SECONDS
        elif concussive == "Deafness":
            severity *= MAX_DEAFNESS_SECONDS

    return round(severity, 3)



def calculate_soldier_area(soldierPos, muzzlePos, muzzleDir):
    """
    expects an input of soldierPos, muzzlePos and muzzleDir - lists, each consisting of [x,y] or [x,y,z] coordinates. 
    Returns the area of effect - the area in which the soldier is currently standing relative to the direction in which the muzzle is pointing,
    Based on the angle in which the muzzle is pointing and the relative angle of the soldier to the muzzle.
    """
    #calculates the radians of the muzzle direction vector
    muzzleRadians = math.atan2(muzzleDir[1], muzzleDir[0])
    #calculates the muzzle to person relative vector
    soldier_muzzle_ratio = [(soldierPos[0] - muzzlePos[0]), (soldierPos[1] - muzzlePos[1])]
    #calculates the radians of the gun to person vector
    soldierRadians = math.atan2(soldier_muzzle_ratio[1], soldier_muzzle_ratio[0])
    #converts the muzzle to person radians to degrees
    soldier_muzzle_angle = round((math.degrees(soldierRadians)), 3)
    #converts the muzzle direction radians to degrees
    muzzle_angle = round((math.degrees(muzzleRadians)), 3)
    #calculates the soldier's relative angle to the muzzle's direction
    soldier_area = soldier_muzzle_angle - muzzle_angle
    area_of_effect = ""
    #checks to see if the soldier is facing the muzzle
    if -45<=soldier_area<=45:
        area_of_effect = "Front"
    #otherwise, checks to see whether the soldier is either side of the muzzle
    elif -135<=soldier_area<=-46 or 46<=soldier_area<=135:
        area_of_effect = "Low Effect"
    #otherwise checks to see if the soldier is in the safe area behind the muzzle.
    elif soldier_area>135 or soldier_area<-135:
        area_of_effect = "Safe Zone"
    
    return area_of_effect
    

def calculate_soldier_distance(muzzlePos, soldierPos):
    """
    gets as input muzzlePos, a list of the muzzle's [x,y,z] coordinates, and soldierPos, the list of the soldier's [x,y,z] coordinates.
    returns a float, representing the distance between the soldier's position and the position of the muzzles in meters.
    """ 
    soldier_muzzle = [(soldierPos[0] - muzzlePos[0]), (soldierPos[1] - muzzlePos[1])]
    distance = math.hypot(soldier_muzzle[0], soldier_muzzle[1])
    
    return distance
    

def apply_concussive_effect(allUnits, muzzleCaliber, muzzleDir, muzzlePos):
    """
    expects as input: 
    allUnits - a list of all current soldiers present in the environment; 
    muzzleCaliber - a string describing the caliber of the gun in mm.
    muzzleDir - a list ([x,y,z]) describing the vector of the muzzle.
    muzzlePos - a list ([x,y,z]) describing the coordinates (in meters) of the muzzle when it fired, where Z is the height above sea level.
    Applies concussive effects (deafness and blindness) to soldiers standing too close to the weapon when it fired, in accordance with their
    relative angle to the muzzle's direction.
    """
    #calculates every area of effect's radius according to the caliber being used.
    radius = caliber_to_radius(muzzleCaliber)
    for soldier in allUnits:
        #gets the [x,y,z] position of each soldier in the allUnits list.
        soldierPos = soldier.getPosition()
        #calculates the direction and area in which the soldier is standing relative to the muzzle's direction.
        area_of_effect = calculate_soldier_area(soldierPos, muzzlePos, muzzleDir)
        #checks if the soldier is on either side of the muzzle
        if area_of_effect == "Low Effect":
            #if he is, calculates the distance between the soldier and the muzzle.
            soldierDistance = calculate_soldier_distance(muzzlePos, soldierPos)
            #if the distance is less than or equal to the radius of the low effect area:
            if soldierDistance < radius[LOWRISK_RADIUS_INDEX]:
                #calculates the duration (in seconds) of the deafness effect that will be applied to the soldier
                deafness = determine_concussive_severity(soldierDistance, radius[LOWRISK_RADIUS_INDEX], "Deafness", area_of_effect)
                #applies the deafness effect to the soldier
                setDeafness(soldier, deafness)
                #prints a message summarizing the concussive effect that was applied to the soldier
                print(soldier.getName(), "is in the Low Effect Area! applied", deafness, "seconds of deafness.")
            # if the soldier is far enough from the muzzle and is positioned outside of the radius of the low effect area:
            else:
                #prints a message informing that the soldier has not been harmed.
                print("No concussive effect has been applied to", soldier.getName(), "as he is far enough from the muzzle")
        #if the soldier is not on either sides of the muzzle, checks to see if he is positioned in front of the muzzle.
        elif area_of_effect == "Front":
            #calculates the distance between the soldier and the muzzle.
            soldierDistance = calculate_soldier_distance(muzzlePos, soldierPos)
            #checks if the soldier's distance from the muzzle is smaller or equal to the radius of the flash area
            if soldierDistance < radius[FLASH_RADIUS_INDEX]:
                #doubles the calculated radius of the flash area in order to balance the blindness damage dealt
                #inside the flash area.
                flash_damage_balancer = radius[FLASH_RADIUS_INDEX] * 2
                #calculates the duration (in seconds) of the blindess effect that will be applied to the soldier, as he is in the flash area.
                blindness = determine_concussive_severity(soldierDistance, flash_damage_balancer, "Blindness")
                #calculates the duration (in seconds) of the deafness effect that will be applied to the soldier.
                #the deafness effect is calculated in the same way whether the soldier is in the high risk area or in the flash area.
                #as such, the function takes in the radius of the high risk area to calculate deafness damage.
                deafness = determine_concussive_severity(soldierDistance, radius[HIGHRISK_RADIUS_INDEX], "Deafness")
                #applies the blindness effect to the soldier
                setBlindness(soldier, blindness)
                #applies the deafness effect to the soldier
                setDeafness(soldier, deafness)
                #prints a status message summarizing the concussive effects that have been applied to the soldier.
                print("Soldier", soldier.getName(), "is in the Flash Effect Area! applied", blindness, "seconds of blindness and", deafness, "seconds of deafness.")
            #if the soldier's distance from the muzzle is larger than the flash effect area radius but smaller than the high effect area radius, then the soldier is
            #in the high effect area.
            elif radius[FLASH_RADIUS_INDEX]<= soldierDistance < radius[HIGHRISK_RADIUS_INDEX]:
                #calculates the duration (in seconds) of the blindess effect that will be applied to the soldier, as he is in the flash area.
                #as the soldier is not inside of the flash effect area, blindness effect duration will be cut in half.
                blindness = (determine_concussive_severity(soldierDistance, radius[HIGHRISK_RADIUS_INDEX], "Blindness")) / 2
                #calculates the duration (in seconds) of the deafness effect that will be applied to the soldier.
                deafness = determine_concussive_severity(soldierDistance, radius[HIGHRISK_RADIUS_INDEX], "Deafness") 
                #applies the blindness effect to the soldier
                setBlindness(soldier, blindness)
                #applies the deafness effect to the soldier
                setDeafness(soldier, deafness)
                #prints a status message summarizing the concussive effects that have been applied to the soldier.
                print("Soldier", soldier.getName(), "is in the High Effect Area! applied", blindness, "seconds of blindness and", deafness, "seconds of deafness.")
            else:
                #if the soldier is far enough from the muzzle and is positioned outside of the radiuses of the flash and high effect areas:
                print("No concussive effect has been applied to Soldier", soldier.getName(), "as he is far enough from the muzzle")
        #if the soldier is positioned behind the muzzle and is at a safe distance from it,
        elif area_of_effect == "Safe Zone":
            #prints a status message saying that the soldier is in the safe area and has not been harmed.
            print("No concussive effect has been applied to", soldier.getName(), "as he is in the safe zone")
                      
#randomizes sea level for the environment      
seaLevel = randomize_sea_level()     

#initializes instances of soldiers in order to ease the testing of the function.
James = Soldier("James")
John = Soldier("John")
Andrew = Soldier("Andrew")
Bill = Soldier("Bill")
Rick = Soldier("Rick")
Tommy = Soldier("Tommy")
Daryl = Soldier("Daryl")
Merl = Soldier("Merl")
George = Soldier("George")
Joel = Soldier("Joel")
Carl = Soldier("Carl")

#creates a list of all soldiers currently in the environment to ease the testing of the function.        
allUnits = get_units_list()       
        








  