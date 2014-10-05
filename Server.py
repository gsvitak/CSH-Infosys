from flask import Flask
from flask import jsonify 
from flask import request
from sqlite import sqlite
from BetaBrite

app = Flask(__name__)

@app.route('/spaces', methods=['POST'])
def requestFiles():
    global sqlite
    if not 'count' in request.form:
        return jsonify(result='failure', reason="missing count"), 412

    try:
        count = int(request.form['count'])
    except ValueError:
        return jsonify(result='failure', reason='count needs to be an int'), 412
    
    registration = sqlite.registerSpaces(count)

    if registration == False:
        return jsonify(results='failure', reason='Count is either too large or there is no space. Talk to an admin'), 412
   
    return jsonify(results='success', userKey=registration), 200
     

@app.route('/spaces', methods=['DELETE'])
def deleteFiles():
    global sqlite
    if not 'key' in request.form:
        return noKey()

    deleted = sqlite.deleteSpaces(request.form['key'])
    if deleted == False:
        return invalidKey() 
    return jsonify(result='success'), 204

@app.route('/spaces/<int:fileLabel>/strings', methods=['POST'])
def addString(fileLabel):
    global sqlite
    if not 'key' in request.form:
        return nokey()

    files = sqlite.getFileLabels(request.form['key'])
    if files == False:
        return invalidKey()

    if fileLabel < 0 or fileLabel >= len(files):
        return jsonify(result='failure', reason='file label is out of bounds'), 412

    if not 'string' in requests.form:
        return jsonify(result='failure', reason='No string given for string function'), 412

    #Start BetaBrite
    startPacket()
    startFile(files[fileLabel], 'WRITE STRING')
    addString(requests.form['string'])
    endFile()
    endPacket()
    #End BetaBrite
    return jsonify(result='success'), 204

@app.route('/spaces/<int:fileLabel>/texts', methods=['POST'])
def addText(fileLabel):
    global sqlite
    if not 'key' in request.form:
        return nokey()

    files = sqlite.getFileLabels(request.form['key'])
    if files == False:
        return invalidKey()

    if fileLabel < 0 or fileLabel >= len(files):
        return jsonify(result='failure', reason='file label is out of bounds'), 412 
    
    if not 'text' in requests.form:
        return jsonify(result='failure', reason='No text given for text function'), 412

    mode = 'HOLD'
    if 'mode' in requests.form and requests.form['mode'] in WRITE_MODES:
        mode = requests.form['mode']

    #Start BetaBrite
    startPacket()
    startFile(files[fileLabel])
    addText(files[fileLabel], mode)
    endFile()
    endPacket()
    #End BetaBrite
    return jsonify(results='success'), 204

def noKey():
    return jsonify(result='failure', reason='no key supplied'), 401

def invalidKey():
    return jsonify(result='failure', reason='No user, or more than one user, associted with this key.'), 401

if __name__ == "__main__":
    global sqlite
    sqlite = sqlite()
    sqlite.setup()
    app.debug = True
    app.run()

