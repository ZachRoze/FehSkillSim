from flask import Flask, render_template, request, redirect, url_for
from FehLib import *
from WeaponImageGenerator import *

app = Flask(__name__)
app.config[ 'SEND_FILE_MAX_AGE_DEFAULT' ] = 0

@app.route( "/", methods=[ "POST", "GET" ] )
def index():
    weaponName = ""
    weaponText = ""
    weaponType = ""
    moveType = ""
    power = ""
    imagePath = ""
    if request.method == "POST" and "weaponName" in request.form:
        weaponName = request.form[ "weaponName" ]
        if "weapon" in request.form:
            weaponType = request.form[ "weapon" ]
        if "move" in request.form:
            moveType = request.form[ "move" ]
        if "power" in request.form:
            power = request.form[ "power" ]
        if weaponName:
            weaponTextGenerator = WeaponText( weaponType, moveType, power )
            weaponTextGenerator.newWeaponText()
            weaponText = weaponTextGenerator.description
            newImage = WeaponImage( weaponName, weaponType, weaponTextGenerator.description, weaponTextGenerator.effAgainst )
            newImage.createImage()
            imagePath = url_for( "static", filename=( "NewWeapon.png" ) )
            print( imagePath )
    return render_template( "index.html", weaponName=weaponName, weaponText=weaponText, weaponType=weaponType, moveType=moveType, power=power, imagePath=imagePath )

if __name__ == "__main__":
    app.run( debug=True )