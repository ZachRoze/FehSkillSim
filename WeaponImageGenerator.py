from PIL import Image, ImageDraw, ImageFont
import textwrap
import hashlib

# set to False if working locally for a single image file
uniqueImageFile = True

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
        if uniqueImageFile:
            # Hash of weaponText and grab 8 final digits
            self.outputFile = "static/NewWeapon" + hashlib.sha1( self.weaponText.encode( 'utf-8' ) ).hexdigest()[ :16 ] + ".png"
        else:
            self.outputFile = "static/NewWeapon.png"
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
        width = 67
        fontSize = 16
        maxLines = 5
        # Loop shrinks font and increases text wrap width if description is long
        while( len( textwrap.wrap( self.weaponText, width=width ) ) > maxLines ):
            fontSize -= 2
            width += 12
            maxLines += 1
        descriptionLines = textwrap.wrap( self.weaponText, width=width )
        print( width )
        print( fontSize )
        print( maxLines )
        print( len( descriptionLines ) )
        descriptionFont = ImageFont.truetype( "static/nimbus-sans-l.regular-italic.otf", fontSize )
        height = 92
        for line in descriptionLines:
            self.draw.text( ( 39, height ), line, ( 0, 0, 0 ), font=descriptionFont )
            height += fontSize

        self.baseImage.save( self.outputFile )

