from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

class WeaponImage:
    def __init__( self, weaponName, weaponType, weaponText, effAgainst ):
        self.weaponName = weaponName
        self.weaponType = weaponType
        self.weaponText = weaponText
        self.effAgainst = effAgainst
        weaponTypeToMtRng = {
            "melee" : ( 16, 1 ),
            "tome" : ( 14, 2 ),
            "bow" : ( 14, 2 ),
            "dagger" : ( 14, 2 ),
            "staff" : ( 14, 2 ),
            "dragon" : ( 16, 1 ),
            "beast" : ( 14, 1 )
        }
        mtRng = weaponTypeToMtRng[ self.weaponType ]
        self.might = mtRng[ 0 ]
        self.range = mtRng[ 1 ]
        self.outputFile = os.path.join( "static", "NewWeapon.png" )
        baseImageFile = "FEHTempEff.png" if self.effAgainst else "FEHTemp.png"

        self.baseImage = Image.open( "static/FEHImages/" + baseImageFile )
        self.draw = ImageDraw.Draw( self.baseImage )
    
    def createImage( self ):
        # Weapon Name
        nameFont = ImageFont.truetype( "static/nimbus-sans-l.bold-italic.otf", 40 )
        self.draw.text( ( 82, 24 ), self.weaponName, ( 0, 0, 0 ), font=nameFont )

        # Might and Range
        mightRangeFont = ImageFont.truetype( "static/nimbus-sans-l.bold-italic.otf", 24 )
        self.draw.text( ( 85, 67 ), str( self.might ), ( 0, 0, 0 ), font=mightRangeFont )
        self.draw.text( ( 187, 67 ), str( self.range ), ( 0, 0, 0 ), font=mightRangeFont )

        # TODO Effective images need to be pasted
        # Should I combine beast and dragon eff into a single image?
        
        # Weapon text
        # TODO smaller font sizes need to increase the width of text wrapping
        # but they kind of depend on each other so...
        width = 67
        descriptionLines = textwrap.wrap( self.weaponText, width=width )
        fontSize = 16 if len( descriptionLines ) <= 5 else 16 - ( len( descriptionLines ) - 5 ) * 2
        descriptionFont = ImageFont.truetype( "static/nimbus-sans-l.regular-italic.otf", fontSize )
        height = 92
        for line in descriptionLines:
            self.draw.text( ( 39, height ), line, ( 0, 0, 0 ), font=descriptionFont )
            height += fontSize

        self.baseImage.save( self.outputFile )

