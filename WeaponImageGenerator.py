from PIL import Image, ImageDraw, ImageFont
import textwrap
import hashlib

DEFAULT_IMAGE_WIDTH = 548
DEFAULT_IMAGE_HEIGHT = 191
DEFAULT_TEXT_WIDTH = 65
DEFAULT_FONT_SIZE = 16

# set to False if working locally for a single image file
uniqueImageFile = True

class WeaponImage:
    def __init__( self, weaponName, weaponType, weaponText, effAgainst ):
        self.weaponName = weaponName
        self.weaponType = weaponType
        self.weaponText = weaponText
        self.effAgainst = effAgainst
        self.fixedSize = False
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
        lines = len( textwrap.wrap( self.weaponText, width=DEFAULT_TEXT_WIDTH ) )
        print( lines )
        baseImageFile = "FEHTempEff.png" if self.effAgainst else "FEHTemp.png"
        if lines < 6 or self.fixedSize:
            # Small description or fixed size
            size = ( DEFAULT_IMAGE_WIDTH, DEFAULT_IMAGE_HEIGHT )
        else:
            size = ( DEFAULT_IMAGE_WIDTH, DEFAULT_IMAGE_HEIGHT + ( ( lines - 5 ) * DEFAULT_FONT_SIZE ) )
        self.baseImage = Image.new( 'RGBA', size, ( 255, 0, 0, 0 ) )
        self.templateImage = Image.open( "static/FEHImages/" + baseImageFile )
        self.draw = ImageDraw.Draw( self.baseImage )
    
    def createImage( self ):
        # Create backrop from template
        lines = len( textwrap.wrap( self.weaponText, width=DEFAULT_TEXT_WIDTH ) )
        if lines < 6 or self.fixedSize:
            self.baseImage.paste( self.templateImage, ( 0, 0 ), self.templateImage )
        else:
            # Get top half
            topCrop = self.templateImage.crop( ( 0, 0, DEFAULT_IMAGE_WIDTH, 155 ) )
            self.baseImage.paste( topCrop, ( 0, 0 ), topCrop )
            # Get bottom half
            bottomCrop = self.templateImage.crop( ( 0, 154, DEFAULT_IMAGE_WIDTH, self.templateImage.height ) )
            self.baseImage.paste( bottomCrop, ( 0, self.baseImage.height - bottomCrop.height ), bottomCrop )
            # Fill in the middle gaps
            midSection = self.templateImage.crop( ( 0, 138, DEFAULT_IMAGE_WIDTH, 155 ) )
            for i in range( lines - 5 ):
                self.baseImage.paste( midSection, ( 0, 155 + ( i * 16 ) ), midSection )

        # Weapon Name
        nameFont = ImageFont.truetype( "static/nimbus-sans-l.bold-italic.otf", 40 )
        self.draw.text( ( 82, 24 ), self.weaponName, ( 0, 0, 0 ), font=nameFont )

        # Might and Range
        mightRangeFont = ImageFont.truetype( "static/nimbus-sans-l.bold-italic.otf", 24 )
        self.draw.text( ( 85, 67 ), str( self.might ), ( 0, 0, 0 ), font=mightRangeFont )
        self.draw.text( ( 187, 67 ), str( self.range ), ( 0, 0, 0 ), font=mightRangeFont )

        effImageXcoord = 264
        effImageYcoord = 63
        if "flying" in self.effAgainst:
            effImage = Image.open( "static/FEHImages/FEHFlier.png" )
            effImage = effImage.resize( ( 26, 26 ) )
            self.baseImage.paste( effImage, ( effImageXcoord, effImageYcoord ), effImage )
            effImageXcoord += 31
        if "armored" in self.effAgainst:
            effImage = Image.open( "static/FEHImages/FEHArmor.png" )
            effImage = effImage.resize( ( 26, 26 ) )
            self.baseImage.paste( effImage, ( effImageXcoord, effImageYcoord ), effImage )
            effImageXcoord += 31
        if "cavalry" in self.effAgainst:
            effImage = Image.open( "static/FEHImages/FEHCavalry.png" )
            effImage = effImage.resize( ( 26, 26 ) )
            self.baseImage.paste( effImage, ( effImageXcoord, effImageYcoord ), effImage )
            effImageXcoord += 31
        if "dragon" in self.effAgainst:
            effImage = Image.open( "static/FEHImages/DragonEff.png" )
            effImage = effImage.resize( ( 105, 30 ) )
            self.baseImage.paste( effImage, ( effImageXcoord, effImageYcoord ), effImage )
            effImageXcoord += 110
        if "beast" in self.effAgainst:
            effImage = Image.open( "static/FEHImages/BeastEff.png" )
            effImage = effImage.resize( ( 105, 30 ) )
            self.baseImage.paste( effImage, ( effImageXcoord, effImageYcoord ), effImage )
            effImageXcoord += 110
        
        # Weapon text
        width = DEFAULT_TEXT_WIDTH
        fontSize = DEFAULT_FONT_SIZE
        maxLines = 5
        if self.fixedSize:
            # Fixed image size
            # Loop shrinks font and increases text wrap width if description is long
            while( len( textwrap.wrap( self.weaponText, width=width ) ) > maxLines ):
                fontSize -= 2
                width += 2 * ( maxLines - 1 )
                maxLines += 1
        descriptionLines = textwrap.wrap( self.weaponText, width=width )
        descriptionFont = ImageFont.truetype( "static/nimbus-sans-l.regular-italic.otf", fontSize )
        height = 92
        for line in descriptionLines:
            self.draw.text( ( 39, height ), line, ( 0, 0, 0 ), font=descriptionFont )
            height += fontSize

        self.baseImage.save( self.outputFile )