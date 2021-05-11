import random
import json

#TODO 5/7
# Add a bunch of conds, and benefits
# Wrazzle Dazzle
# Picture formatting?

# Json object formatting
# type = What type of effect of condition or benefit, used for not getting duplicates
# text = Text string that might be formatted
# flavor = List of options that will be randomly picked to be in the sting, includes weight for power calcing
# flavor2 = Second list of options, include weight for power calcing
# stats = grants random number from 5 to 7 for any stats in phrase
# combat = "during combat"
# turn = "at start of turn"
# after = "after combat"
# always = effect always happens, i.e. Pass
# weight = power calcing
# reroll = chance of not selecting phrase, so less common phrases picked less than average. High reroll = rare. Null reroll = No reroll
# Some types are shared, for these, there are usual conditions (no reroll) and rare conditions (high reroll)

def newPhraseCheck( curWeight, addedWeight, weightMax, randomCheck ):
    if curWeight + addedWeight > weightMax:
        return False
    return random.random() < randomCheck

def formatBenefitPhrase( benefitPhrase, modifier, condPhrase ):
    if modifier == "combat":
        benefitPhrase = benefitPhrase + " during combat"
    if modifier == "turn":
        if not condPhrase:
            benefitPhrase = "at start of turn, " + benefitPhrase
        if "grant" in benefitPhrase and "Special cooldown count-" not in benefitPhrase \
            and "restores" not in benefitPhrase:
            benefitPhrase = benefitPhrase + " for 1 turn"
    if modifier == "after":
        benefitPhrase = "after combat, " + benefitPhrase
        if "grant" in benefitPhrase and "Special cooldown count-" not in benefitPhrase \
            and "restores" not in benefitPhrase:
            benefitPhrase = benefitPhrase + " for 1 turn"
    return benefitPhrase

def renderWeaponText( weaponType, moveType, power ):
    # Weight is how good the description is based off of set values
    # assigned to different parts of the description
    print( "\n\n\n\n\n")
    weight = 0
    powerToWeight = {
        "weak" : 8,
        "decent" : 15,
        "strong" : 23,
        "broken" : 30
    }
    # used for calculating basic effects
    maxPower = powerToWeight[ "broken" ]
    modifierToWeight = {
        "combat" : 3,
        "turn" : 2,
        "after" : 1,
        "always" : 2
    }
    weightMax = powerToWeight[ power ]
    previous = None
    condPhrase = ""
    benefitPhrase = ""
    description = ""
    types = {
        "combat" : True,
        "turn" : True,
        "after" : True,
        "always" : True
    }

    # Load json files
    with open( "FehConds.json" ) as file:
        condData = json.load( file )
    with open( "FehBenefits.json" ) as file:
        benefitData = json.load( file )

    # Gets all phrases based on current
    def getPhraseFiltered( data ):
        nonlocal weight
        nonlocal previous
        nonlocal weaponType
        nonlocal types
        nonlocal condPhrase
        filteredData = [ phrase for phrase in data if ( "combat" in phrase and types[ "combat" ] )
                                                    or ( "turn" in phrase and types[ "turn" ] )
                                                    or ( "after" in phrase and types[ "after" ] )
                                                    or ( "always" in phrase and types[ "always" ] ) ]
        # 40% bias towards StatBuffs
        filteredPhrase = filteredData[ 0 ] if filteredData[ 0 ][ "type" ] == "StatBuff" \
            and condPhrase and random.random() < .40 else random.choice( filteredData )
        i = 1
        while ( previous == filteredPhrase[ "type" ]
            or ( "reroll" in filteredPhrase and random.random() < filteredPhrase[ "reroll" ] )
            or ( weaponType == "dagger" and filteredPhrase[ "type" ] == "InflictDebuffSmoke" )
            or ( weaponType == "staff" and ( filteredPhrase[ "type" ] == "Firesweep" or filteredPhrase[ "type" ] == "Raven" ) ) ):
            print( 'REROLL: ' + filteredPhrase["type"] )
            if ( "reroll" in filteredPhrase ):
                print( "Reroll chance " + str( filteredPhrase[ "reroll" ] ) )
            filteredPhrase = random.choice( filteredData )
            i += 1
            if i > 20:
                print( description )
                print( types )
                assert( False )

        previous = filteredPhrase[ "type" ]
        
        types[ "combat" ] = "combat" in filteredPhrase and types[ "combat" ]
        types[ "turn" ] = "turn" in filteredPhrase and types[ "turn" ]
        types[ "after" ] = "after" in filteredPhrase and types[ "after" ]
        types[ "always" ] = "always" in filteredPhrase and types[ "always" ]
        print( previous )
        filteredString = filteredPhrase[ "text" ]
        print( types )
        print( filteredString )
        filteredFormat = ()

        # String formatting
        if "flavor" in filteredPhrase:
            flavor = random.choice( filteredPhrase[ "flavor" ] )
            filteredFormat += tuple( flavor )
            weight += list( flavor.values() )[ 0 ]
        if "stats" in filteredPhrase:
            filteredFormat += ( random.choice( [ 5, 6, 7] ), )
        if "flavor2" in filteredPhrase:
            flavor2 = random.choice( filteredPhrase[ "flavor2" ] )
            filteredFormat += tuple( flavor2 )
            weight += list( flavor2.values() )[ 0 ]
        filteredString = filteredPhrase[ "text" ] % filteredFormat
        # Update weight for benefits
        if "weight" in filteredPhrase:
            weight += filteredPhrase[ "weight" ]
        return filteredString

    # reduce dagger max weight to possibly stack debuffs at end
    if weaponType == "dagger":
        weight += 5

    # Basic starter effects, based on power level
    if random.random() < powerToWeight[ power ] / ( maxPower * 2.5 ):
        effDamage = random.choice( [ "armored", "cavalry", "flying", "dragon", "beast", "armored and cavalry", "beast and dragon "] )
        # Bow inate flier effectiveness
        if weaponType == "bow":
            effDamage = ( "flying, " + effDamage ) if "and" in effDamage else ( "flying and " + effDamage )
        description += "Effective against %s foes. " % effDamage
        weight += 2
    # Bow inate flier efectiveness, no weight
    elif weaponType == "bow":
        description += "Effective against flying foes. "
    # staff gets one of wrazzle dazzle
    if weaponType == "staff":
        description += random.choice( [ "Foe cannot counterattack. ", "Calcuates damage from staff like other weapons. " ] )
    # Basic stat buff
    if random.random() < powerToWeight[ power ] / maxPower:
        stat = random.choice( [ "Atk", "Spd", "Def", "Res" ] )
        description += "Grants %s+3. " % stat
        weight += 1
    # Slaying effect
    if random.random() < powerToWeight[ power ] / ( maxPower * 2 ) and weaponType != "staff":
        description += "Accelerates Special trigger (cooldown count-1). "
        weight += 2
    # 25% chance of neutralizing an effective bonus, but not both
    if moveType != "infantry" and random.random() < powerToWeight[ power ] / ( maxPower * 3 ):
        description += "Neutralizes \"effective against %s\" bonuses. " % moveType
        weight += 2
    elif ( weaponType == "dragon" or weaponType == "beast" ) and random.random() < powerToWeight[ power ] / ( maxPower * 3 ):
        description += "Neutralizes \"effective against %s\" bonuses. " % weaponType
        weight += 2
    
    if weaponType == "dragon":
        description += "If foe's Range = 2, calculates damage using the lower of foe's Def or Res. "

    while weight < weightMax:
        # Reset phrase filters
        types = dict.fromkeys( types, True )
        condPhrase = ""
        previous = None
        # 40% chance of being conditionless
        if newPhraseCheck( weight, 3, weightMax, .60 ):
            # conditionless
            weight += 3
        else:
            # Get first condition
            condPhrase = "If " + getPhraseFiltered( condData )
            # 70% chance of only having 1 condition
            if newPhraseCheck( weight, 1, weightMax, .7 ):
                # single condition
                weight += 3
            else:
                # two conditions
                # 80% chance of "or" or "and" conditional
                if newPhraseCheck( weight, 3, weightMax, .8 ):
                    condPhrase += ", or if "
                    weight += 3
                else:
                    # no weight on two conditional "and"
                    condPhrase += ", and if "
                secondCondPhrase = getPhraseFiltered( condData )
                while ( secondCondPhrase in condPhrase ):
                    secondCondPhrase = getPhraseFiltered( condData )
                condPhrase += secondCondPhrase

            condPhrase += ", "
        # Benefit phrase always happens
        benefitPhrase = getPhraseFiltered( benefitData )
        benefitPhrase2 = ""
        # 50% chance of two benefits, needs an if statement
        if condPhrase and newPhraseCheck( weight, 0, weightMax, .5 ):
            # two benefits
            benefitPhrase2 = getPhraseFiltered( benefitData )
            # If both benefits have the same modifier, apply the same formatting to avoid redundancy
            benefitPhrase = benefitPhrase + " and " + benefitPhrase2
        # Chose string modifier based on current phrases
        modifiers = { k:v for ( k,v ) in types.items() if v }
        modifier = ""
        modifier = random.choice( list( modifiers ) )
        benefitPhrase = formatBenefitPhrase( benefitPhrase, modifier, condPhrase )
        weight += modifierToWeight[ modifier ]
        if not condPhrase:
            # .capitalize doesn't work because it lowercases all other letters
            benefitPhrase = "%s%s" % ( benefitPhrase[ 0 ].upper(), benefitPhrase[ 1: ] )
        elif modifier == "turn":
            condPhrase = "At start of turn, i" + condPhrase[ 1: ]
        description += condPhrase + benefitPhrase + ". "

    # beast innate transformation skill
    if weaponType == "beast":
        beastMoveSkill = {
            "infantry" : "grants Atk+2 and deals +10 damage when Special triggers.",
            "cavalry" : "grants Atk+2, and if unit initiates combat, inflicts Atk/Def-4 on foe during combat and foe cannot make a follow-up attack.",
            "flying" : "unit can move 1 extra space. (That turn only. Does not stack.) If unit transforms, grants Atk+2.",
            "armored" : "grants Atk+2, and unit can counterattack regardless of foe's range."
        }
        description += "At start of turn, if unit is adjacent to only beast or dragon allies or if unit is not adjacent "\
            "to any ally, unit transforms (otherwise, unit reverts). If unit transforms, " + beastMoveSkill[ moveType ]
    # dagger innate smoke skill
    if weaponType == "dagger":
        weight -= 5
        daggerSmoke = next( ( benefit for benefit in benefitData if benefit[ "type" ] == "InflictDebuffSmoke" ), None )
        # 25% shot of something better than basic def/res smoke
        if newPhraseCheck( weight, 3, weightMax, .25 ):
            flavor = random.choice( daggerSmoke[ "flavor" ][ 2: ] )
        else:
            flavor = daggerSmoke[ "flavor" ][ 0 ]
        flavorText = list( flavor.keys() )[ 0 ]
        if "Def/Res" not in flavorText:
            flavorText += " and Def/Res-7"
        flavorText = flavorText.replace( "Def/Res-7", "[Dagger 7]" )
        description += "After combat, " + ( daggerSmoke[ "text" ] % flavorText ) + "."
        
    return description