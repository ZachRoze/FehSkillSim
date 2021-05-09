import random
import json

#TODO 5/7
# Add a bunch of conds, and benefits
# Wrazzle Dazzle
# Picture formatting?

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
        benefitPhrase = benefitPhrase + " for 1 turn"
    if modifier == "after":
        benefitPhrase = "after combat, " + benefitPhrase
        if "grants" in benefitPhrase:
            benefitPhrase = benefitPhrase + " for 1 turn"
    return benefitPhrase

def renderWeaponText( weaponType, moveType, power ):
    # Weight is how good the description is based off of set values
    # assigned to different parts of the description
    weight = 0
    powerToWeight = {
        "weak" : 8,
        "decent" : 13,
        "strong" : 18,
        "broken" : 23
    }
    modifierToWeight = {
        "combat" : 3,
        "turn" : 2,
        "after" : 1,
        "always" : 2
    }
    weightMax = powerToWeight[ power ]
    previous = None
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
    def getPhraseFiltered( data, update=True ):
        nonlocal weight
        nonlocal previous
        nonlocal weaponType
        filteredData = [ phrase for phrase in data if ( phrase[ "combat" ] and types[ "combat" ] )
                                                    or ( phrase[ "turn" ] and types[ "turn" ] )
                                                    or ( phrase[ "after" ] and types[ "after" ] )
                                                    or ( phrase[ "always" ] and types[ "always" ] ) ]
        filteredPhrase = random.choice( filteredData )
        i = 1
        while ( previous == filteredPhrase[ "type" ] \
            or ( weaponType == "dagger" and filteredPhrase[ "type" ] == "InflictDebuffSmoke" )
            or ( previous == "Blow" and filteredPhrase[ "type" ] == "Stance")
            or ( previous == "Stance" and filteredPhrase[ "type" ] == "Blow") ):
            filteredPhrase = random.choice( filteredData )
            i += 1
            if i > 20:
                print( description )
                print( types )
                assert( False )
        previous = filteredPhrase[ "type" ]
        if update:
            types[ "combat" ] = filteredPhrase[ "combat" ] and types[ "combat" ]
            types[ "turn" ] = filteredPhrase[ "turn" ] and types[ "turn" ]
            types[ "after" ] = filteredPhrase[ "after" ] and types[ "after" ]
            types[ "always" ] = filteredPhrase[ "always" ] and types[ "always" ]
        filteredString = filteredPhrase[ "text" ]
        print( filteredString)
        # Format string if checks
        if "stats" in filteredPhrase and filteredPhrase[ "flavor" ] and filteredPhrase[ "stats" ]:
            flavor = random.choice( filteredPhrase[ "flavor" ] )
            weight += list( flavor.values() )[ 0 ]
            if "flavor2" in filteredPhrase:
                flavor2 = random.choice( filteredPhrase[ "flavor2" ] )
                weight += list( flavor2.values() )[ 0 ]
                filteredString = filteredString % ( list( flavor.keys() )[ 0 ], random.choice( [ 4, 5, 6, 7] ), list( flavor2.keys() )[ 0 ] )
            else:
                filteredString = filteredString % ( list( flavor.keys() )[ 0 ], random.choice( [ 4, 5, 6, 7 ] ) )
        elif filteredPhrase[ "flavor" ]:
            flavor = random.choice( filteredPhrase[ "flavor" ] )
            weight += list( flavor.values() )[ 0 ]
            if "flavor2" in filteredPhrase:
                flavor2 = random.choice( filteredPhrase[ "flavor2" ] )
                weight += list( flavor2.values() )[ 0 ]
                filteredString = filteredString % ( list( flavor.keys() )[ 0 ], list( flavor2.keys() )[ 0 ] )
            else:
                filteredString = filteredString % list( flavor.keys() )[ 0 ]
        elif "stats" in filteredPhrase and filteredPhrase[ "stats" ]:
            print( filteredString )
            if "flavor2" in filteredPhrase:
                flavor2 = random.choice( filteredPhrase[ "flavor2" ] )
                weight += list( flavor2.values() )[ 0 ]
                filteredString = filteredString % ( random.choice( [ 4, 5, 6, 7 ] ), list( flavor2.keys() )[ 0 ] )
            else:
                filteredString = filteredString % random.choice( [ 4, 5, 6, 7 ] )
        # Update weight for benefits
        if "weight" in filteredPhrase:
            weight += filteredPhrase[ "weight" ]
        return filteredString

    # reduce dagger max weight to possibly stack debuffs at end
    if weaponType == "dagger":
        weightMax -= 5

    # Basic starter effects
    # 25% chance of effective damage
    if random.random() < .25:
        effDamage = random.choice( [ "armored", "cavalry", "flying", "dragon", "beast", "armored and cavalry", "beast and dragon "] )
        # Bow inate flier effectiveness
        if weaponType == "bow":
            effDamage = ( "flying, " + effDamage ) if "and" in effDamage else ( "flying and " + effDamage )
        description += "Effective against %s foes. " % effDamage
        weight += 2
    # Bow inate flier efectiveness, no weight
    elif weaponType == "bow":
        description += "Effective against flying foes. "
    # 75% chance of having a basic stat buff
    if random.random() < .75:
        stat = random.choice( [ "Atk", "Spd", "Def", "Res" ] )
        description += "Grants %s+3. " % stat
        weight += 1
    # 40% chance of slaying
    if random.random() < .40:
        description += "Accelerates Special trigger (cooldown count-1). "
        weight += 2
    # 25% chance of neutralizing an effective bonus, but not both
    if moveType != "" and moveType != "infantry" and random.random() < .25:
        description += "Neutralizes \"effective against %s\" bonuses. " % moveType
        weight += 2
    elif weaponType != "" and ( weaponType == "dragon" or weaponType == "beast" ) and random.random() < .25:
        description += "Neutralizes \"effective against %s\" bonuses. " % weaponType
        weight += 2
    
    if weaponType == "dragon":
        description += "If foe's Range = 2, calculates damage using the lower of foe's Def or Res. "

    while weight < weightMax:
        # Reset phrase filters
        types = dict.fromkeys( types, True )
        weight += 1
        condPhrase = ""
        previous = None
        # 40% chance of being conditionless
        if newPhraseCheck( weight, 3, weightMax, .40 ):
            # conditionless
            weight += 3
        else:
            # Get first condition
            condPhrase = "If " + getPhraseFiltered( condData )
            # 70% chance of only having 1 condition
            if newPhraseCheck( weight, 1, weightMax, .7 ):
                # single condition
                weight += 1
            else:
                # two conditions
                # 50% chance of "or" or "and" conditional
                if newPhraseCheck( weight, 2, weightMax, .5 ):
                    condPhrase += ", or if "
                    weight += 2
                else:
                    # no weight on two conditional "and"
                    condPhrase += ", and if "
                secondCondPhrase = getPhraseFiltered( condData )
                while ( secondCondPhrase in condPhrase ):
                    secondCondPhrase = getPhraseFiltered( condData )
                condPhrase += secondCondPhrase

            condPhrase += ", "
        # Benefit phrase always happens
        # If we have 2 benefits, they could have mutually exclusive modifiers
        typesCopy = types.copy()
        benefitPhrase = getPhraseFiltered( benefitData )
        benefitPhrase2 = ""
        # Chose string modifier based on current phrases
        modifiers = { k:v for ( k,v ) in types.items() if v }
        modifier = random.choice( list( modifiers ) )
        weight += modifierToWeight[ modifier ]
        modifier2 = ""
        # 50% chance of two benefits, only with a conditional
        if condPhrase and newPhraseCheck( weight, 2, weightMax, .5 ):
            # two benefits
            weight += 2
            # Revert modifiers back to conditional only
            types = typesCopy
            benefitPhrase2 = getPhraseFiltered( benefitData )
            modifiers2 = { k:v for ( k,v ) in types.items() if v }
            modifier2 = random.choice( list( modifiers2 ) )
            weight += modifierToWeight[ modifier2 ]
        # If both benefits have the same modifier, apply the same formatting to avoid redundancy
        if modifier == modifier2:
            benefitPhrase = benefitPhrase + " and " + benefitPhrase2
        benefitPhrase = formatBenefitPhrase( benefitPhrase, modifier, condPhrase )
        if benefitPhrase2 and modifier != modifier2:
            benefitPhrase = benefitPhrase + " and " + formatBenefitPhrase( benefitPhrase2, modifier2, condPhrase )
        if not condPhrase:
            # .capitalize doesn't work because it lowercases all other letters
            benefitPhrase = "%s%s" % ( benefitPhrase[ 0 ].upper(), benefitPhrase[ 1: ] )
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
        weightMax = powerToWeight[ power ]
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