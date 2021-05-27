import random
import json

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

class WeaponText:
    def __init__( self, weaponType, moveType, power ):
        self.weaponType = weaponType
        self.moveType = moveType
        self.power = power
        self.weight = 0
        self.description = ""
        self.previous = ""
        self.condPhrase = ""
        self.benefitPhrase = ""
        powerToWeight = {
            "weak" : 8,
            "decent" : 15,
            "strong" : 23,
            "broken" : 30
        }
        # used for calculating basic effects probability
        self.maxPower = powerToWeight[ "broken" ]
        self.weightMax = powerToWeight[ power ]
        # used for filtering phrases based on currently sentence
        self.types = {
            "combat" : True,
            "turn" : True,
            "after" : True,
            "always" : True
        }
        self.effAgainst = ""
        # Load json files
        with open( "FehConds.json" ) as file:
            self.condData = json.load( file )
        with open( "FehBenefits.json" ) as file:
            self.benefitData = json.load( file )

    def newPhraseCheck( self, addedWeight, randomCheck ):
        if self.weight + addedWeight > self.weightMax:
            return False
        return random.random() < randomCheck

    def formatBenefitPhrase( self, modifier ):
        if modifier == "combat":
            self.benefitPhrase = self.benefitPhrase + " during combat"
        if modifier == "turn":
            if not self.condPhrase:
                self.benefitPhrase = "at start of turn, " + self.benefitPhrase
            if "grant" in self.benefitPhrase and "Special cooldown count-" not in self.benefitPhrase \
                and "restores" not in self.benefitPhrase:
                self.benefitPhrase = self.benefitPhrase + " for 1 turn"
        if modifier == "after":
            self.benefitPhrase = "after combat, " + self.benefitPhrase
            if "grant" in self.benefitPhrase and "Special cooldown count-" not in self.benefitPhrase \
                and "restores" not in self.benefitPhrase:
                self.benefitPhrase = self.benefitPhrase + " for 1 turn"

    # Gets all phrases based on current sentence
    def getPhraseFiltered( self, data ):
        filteredData = [ phrase for phrase in data if ( "combat" in phrase and self.types[ "combat" ] )
                                                    or ( "turn" in phrase and self.types[ "turn" ] )
                                                    or ( "after" in phrase and self.types[ "after" ] )
                                                    or ( "always" in phrase and self.types[ "always" ] ) ]
        # 40% bias towards StatBuffs
        filteredPhrase = filteredData[ 0 ] if filteredData[ 0 ][ "type" ] == "StatBuff" \
            and self.condPhrase and random.random() < .40 else random.choice( filteredData )
        i = 1
        while ( self.previous == filteredPhrase[ "type" ]
            or ( "reroll" in filteredPhrase and random.random() < filteredPhrase[ "reroll" ] )
            or ( self.weaponType == "dagger" and filteredPhrase[ "type" ] == "InflictDebuffSmoke" )
            or ( self.weaponType == "staff" and ( filteredPhrase[ "type" ] == "Firesweep" or filteredPhrase[ "type" ] == "Raven" ) ) ):
            filteredPhrase = random.choice( filteredData )
            i += 1
            if i > 20:
                print( self.description )
                print( self.types )
                assert( False )

        self.previous = filteredPhrase[ "type" ]
        
        self.types[ "combat" ] = "combat" in filteredPhrase and self.types[ "combat" ]
        self.types[ "turn" ] = "turn" in filteredPhrase and self.types[ "turn" ]
        self.types[ "after" ] = "after" in filteredPhrase and self.types[ "after" ]
        self.types[ "always" ] = "always" in filteredPhrase and self.types[ "always" ]
        filteredString = filteredPhrase[ "text" ]
        filteredFormat = ()

        # String formatting
        if "flavor" in filteredPhrase:
            flavor = random.choice( filteredPhrase[ "flavor" ] )
            filteredFormat += tuple( flavor )
            self.weight += list( flavor.values() )[ 0 ]
        if "stats" in filteredPhrase:
            filteredFormat += ( random.choice( [ 5, 6, 7] ), )
        if "flavor2" in filteredPhrase:
            flavor2 = random.choice( filteredPhrase[ "flavor2" ] )
            filteredFormat += tuple( flavor2 )
            self.weight += list( flavor2.values() )[ 0 ]
        filteredString = filteredPhrase[ "text" ] % filteredFormat
        # Update weight for benefits
        if "weight" in filteredPhrase:
            self.weight += filteredPhrase[ "weight" ]
        return filteredString

    def newWeaponText( self ):
        modifierToWeight = {
            "combat" : 3,
            "turn" : 2,
            "after" : 1,
            "always" : 2
        }

        # reduce dagger max weight to possibly stack debuffs at end
        if self.weaponType == "dagger":
            self.weight += 5

        # Basic starter effects, based on power level
        if random.random() < self.weightMax / ( self.maxPower * 2.5 ):
            effDamage = random.choice( [ "armored", "cavalry", "flying", "dragon", "beast", "armored and cavalry", "beast and dragon "] )
            # Bow inate flier effectiveness
            if self.weaponType == "bow" and effDamage != "flying":
                effDamage = ( "flying, " + effDamage ) if "and" in effDamage else ( "flying and " + effDamage )
            self.description += "Effective against %s foes. " % effDamage
            self.effAgainst = effDamage
            self.weight += 2
        # Bow inate flier efectiveness, no weight
        elif self.weaponType == "bow":
            self.effAgainst = "flying"
            self.description += "Effective against flying foes. "
        # staff gets one of wrazzle dazzle
        if self.weaponType == "staff":
            self.description += random.choice( [ "Foe cannot counterattack. ", "Calcuates damage from staff like other weapons. " ] )
        # Basic stat buff
        if random.random() < self.weightMax / self.maxPower:
            stat = random.choice( [ "Atk", "Spd", "Def", "Res" ] )
            self.description += "Grants %s+3. " % stat
            self.weight += 1
        # Slaying effect
        if random.random() < self.weightMax / ( self.maxPower * 2 ) and self.weaponType != "staff":
            self.description += "Accelerates Special trigger (cooldown count-1). "
            self.weight += 2
        # 25% chance of neutralizing an effective bonus, but not both
        if self.moveType != "infantry" and random.random() < self.weightMax / ( self.maxPower * 3 ):
            self.description += "Neutralizes \"effective against %s\" bonuses. " % self.moveType
            self.weight += 2
        elif ( self.weaponType == "dragon" or self.weaponType == "beast" ) and random.random() < self.weightMax / ( self.maxPower * 3 ):
            self.description += "Neutralizes \"effective against %s\" bonuses. " % self.weaponType
            self.weight += 2
        
        if self.weaponType == "dragon":
            self.description += "If foe's Range = 2, calculates damage using the lower of foe's Def or Res. "

        while self.weight < self.weightMax:
            # Reset phrase filters
            self.types = dict.fromkeys( self.types, True )
            self.condPhrase = ""
            self.previous = None
            # 40% chance of being conditionless
            if self.newPhraseCheck( 3, .60 ):
                # conditionless
                self.weight += 3
            else:
                # Get first condition
                self.condPhrase = "If " + self.getPhraseFiltered( self.condData )
                # 70% chance of only having 1 condition
                if self.newPhraseCheck( 1, .7 ):
                    # single condition
                    self.weight += 3
                else:
                    # two conditions
                    # 80% chance of "or" or "and" conditional
                    if self.newPhraseCheck( 3, .8 ):
                        self.condPhrase += ", or if "
                        self.weight += 3
                    else:
                        # no weight on two conditional "and"
                        self.condPhrase += ", and if "
                    secondCondPhrase = self.getPhraseFiltered( self.condData )
                    self.condPhrase += secondCondPhrase

                self.condPhrase += ", "
            # Benefit phrase always happens
            self.benefitPhrase = self.getPhraseFiltered( self.benefitData )
            benefitPhrase2 = ""
            # 50% chance of two benefits, needs an if statement
            if self.condPhrase and self.newPhraseCheck( 0, .5 ):
                # two benefits
                benefitPhrase2 = self.getPhraseFiltered( self.benefitData )
                # If both benefits have the same modifier, apply the same formatting to avoid redundancy
                self.benefitPhrase = self.benefitPhrase + " and " + benefitPhrase2
            # Chose string modifier based on current phrases
            modifiers = { k:v for ( k,v ) in self.types.items() if v }
            modifier = ""
            modifier = random.choice( list( modifiers ) )
            self.formatBenefitPhrase( modifier )
            self.weight += modifierToWeight[ modifier ]
            if not self.condPhrase:
                # .capitalize doesn't work because it lowercases all other letters
                self.benefitPhrase = "%s%s" % ( self.benefitPhrase[ 0 ].upper(), self.benefitPhrase[ 1: ] )
            elif modifier == "turn":
                self.condPhrase = "At start of turn, i" + self.condPhrase[ 1: ]
            self.description += self.condPhrase + self.benefitPhrase + ". "

        # beast innate transformation skill
        if self.weaponType == "beast":
            beastMoveSkill = {
                "infantry" : "grants Atk+2 and deals +10 damage when Special triggers.",
                "cavalry" : "grants Atk+2, and if unit initiates combat, inflicts Atk/Def-4 on foe during combat and foe cannot make a follow-up attack.",
                "flying" : "unit can move 1 extra space. (That turn only. Does not stack.) If unit transforms, grants Atk+2.",
                "armored" : "grants Atk+2, and unit can counterattack regardless of foe's range."
            }
            self.description += "At start of turn, if unit is adjacent to only beast or dragon allies or if unit is not adjacent "\
                "to any ally, unit transforms (otherwise, unit reverts). If unit transforms, " + beastMoveSkill[ self.moveType ]
        # dagger innate smoke skill
        if self.weaponType == "dagger":
            self.weight -= 5
            daggerSmoke = next( ( benefit for benefit in self.benefitData if benefit[ "type" ] == "InflictDebuffSmoke" ), None )
            # 25% shot of something better than basic def/res smoke
            if self.newPhraseCheck( 3, .25 ):
                flavor = random.choice( daggerSmoke[ "flavor" ][ 2: ] )
            else:
                flavor = daggerSmoke[ "flavor" ][ 0 ]
            flavorText = list( flavor.keys() )[ 0 ]
            if "Def/Res" not in flavorText:
                flavorText += " and Def/Res-7"
            flavorText = flavorText.replace( "Def/Res-7", "[Dagger 7]" )
            self.description += "After combat, " + ( daggerSmoke[ "text" ] % flavorText ) + "."