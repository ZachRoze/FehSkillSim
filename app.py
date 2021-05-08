from flask import Flask, render_template, request, redirect, url_for
from FehLib import *

app = Flask(__name__)

def getImagePath( weaponType ):
    if weaponType == "staff":
        return "FEHImages/FEHStaff.png"
    elif weaponType == "melee":
        return "FEHImages/AllMelee.png"
    return "FEHImages/All%ss.png" % weaponType

@app.route("/", methods=['POST', 'GET'])
def index():
    weaponName = ""
    weaponText = ""
    weaponType = ""
    moveType = ""
    power = ""
    imagePath = ""
    if request.method == 'POST' and 'weaponName' in request.form:
        weaponName = request.form['weaponName']
        if 'weapon' in request.form:
            weaponType = request.form['weapon']
        if 'move' in request.form:
            moveType = request.form['move']
        if 'power' in request.form:
            power = request.form['power']
        if weaponName:
            weaponText = renderWeaponText( weaponType=weaponType, moveType=moveType, power=power )
        #imagePath = url_for( 'static', filename=( getImagePath( weaponType ) ) )
    return render_template('index.html', weaponName=weaponName, weaponText=weaponText, weaponType=weaponType, moveType=moveType, power=power, imagePath=imagePath )

if __name__ == "__main__":
    app.run(debug=True)