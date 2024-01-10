import myhelp.filework as mf
import myhelp.interface as mi
import pyfirmata2 as pyfirmata
from flask import Flask, render_template, request
import requests
from datetime import date, datetime
from random import randint

try: open("data\\users.json").close()
except FileNotFoundError:
    tempPass = randint(0,1000)
    mf.jsDump("data\\users.json", [{"name":"admin", "pass":f"{tempPass}"}])
    print(f"Welcome to BeHome!\nThank you for using!\nYour temp account: name - admin, password - {tempPass}")
finally:
    users = mf.load("data\\users.json", 2)

sett = mf.load("data\\config.toml", 1)
app = Flask(__name__)
board = pyfirmata.Arduino(sett["device"]["arduinoPort"])


def getWeather(url, key, city):
    params = {"APPID": key, "q": city, "units": "metric"}
    result = requests.get(url, params=params)
    weather = result.json()
    inpt = {"full":weather, "main": weather["main"], "roundedTemp": int(round(weather["main"]["temp"], 0))}
    return inpt

def readPinsAr():
    outpinsrd = []
    for i in range(len(sett["output"]["pins"])):
        rd = board.digital[sett["output"]["pins"][i]].read()
        if rd == 1:
            outpinsrd.append(1)
        else:
            outpinsrd.append(0)
    return outpinsrd

def loginuser(name, password):
    if users == []:
        return "None Registred Users"
    else:
        allowed = False
        for i in range(len(users)):
            if name in users[i]["name"]:
                if password in users[i]["pass"]: allowed = True
        if allowed: return f"{allowed}"
        else: return f"{allowed}"

mi.aprint(sett["app"]["name"])

def adminpanel(username, password):
    rpnsar = readPinsAr()
    admpnl = render_template('adminpanel.html',temp=getWeather(sett["userData"]["openmapUrl"], sett["userData"]["openmapKey"], sett["userData"]["city"])["roundedTemp"], date=date.today(), city=sett["userData"]["city"], username=username,password=password, out1name=sett["output"]["names"][0], out2name=sett["output"]["names"][1], out3name=sett["output"]["names"][2], out4name=sett["output"]["names"][3], weatherTitle=getWeather(sett["userData"]["openmapUrl"], sett["userData"]["openmapKey"], sett["userData"]["city"])["full"]["weather"][0]["main"], readPins=rpnsar)
    return admpnl

@app.route('/')
def tryed():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data["username"]
    password = data["password"]
    alwd = loginuser(name=username, password=password)
    if alwd == "True":
            return adminpanel(username, password)
    else: return "Login Error"

@app.route('/adduser', methods=['POST'])
def adduser():
    
    data = request.form
    arldadd = False
    username = data["username"]
    password = data["password"]
    if username and not username == "" and password and not password == "":
        for i in range(len(users)):
            if username in users[i]["name"]: arldadd = True
        if arldadd == True: return "User Arleady Logined!"
        if users[0]["name"] == "admin":
            users.remove(users[0])
            mf.jsDump("data\\users.json", users)
        users.append({"name":username, "pass":password})
        mf.jsDump("data\\users.json", users)
        return "True"
    return "Form None Writed!"

@app.route('/removeuser', methods=['POST'])
def removeuser():
    data = request.form
    noonusers = False
    username = data["username"]
    password = data["password"]
    if username and not username == "" and password and not password == "":
        for i in range(len(users)):
            if username in users[i]["name"]: noonusers = True
        if noonusers == False: return "User Not Logined!"
        users.remove({"name":username, "pass":password})
        mf.jsDump("data\\users.json", users)
        return "True"
    return "Form None Writed!"

#Debug command

# @app.route('/test/login/<usernm>/<passwrd>')
# def testlogin(usernm, passwrd):
#     alwd = loginuser(usernm, passwrd)
#     if alwd == "True": return "ADMIN"
#     else: return "NON LOGINED"

@app.route('/error/<code>')
def viewError(code):
    return f"Error {code}", code

@app.route('/user/<username>/password/<password>/command/<cmd>')
@app.route('/<username>/<password>/<cmd>')
def main(username, password, cmd):
    alwd = loginuser(name=username, password=password)
    if alwd == "True":

            if cmd == "admin": return "YOU ADMIN"
            if cmd == "adduser": return render_template('adduser.html')
            if cmd == "removeuser": return render_template('removeuser.html')
            if cmd == "showConfig": return sett
            if cmd == "showUsers": return users
            if cmd == "time": return str(datetime.now().time())
            if cmd == "date": return str(date.today())
            if cmd == "roudedTemp": return str(getWeather(sett["userData"]["openmapUrl"], sett["userData"]["openmapKey"], sett["userData"]["city"])["roundedTemp"])
            if cmd == "weatherName": return str(getWeather(sett["userData"]["openmapUrl"], sett["userData"]["openmapKey"], sett["userData"]["city"])["full"]["weather"][0]["main"])
            if cmd == "weatherDesc": return str(getWeather(sett["userData"]["openmapUrl"], sett["userData"]["openmapKey"], sett["userData"]["city"])["full"]["weather"][0]["description"])
            if cmd == "weatherFullData": return getWeather(sett["userData"]["openmapUrl"], sett["userData"]["openmapKey"], sett["userData"]["city"])["full"]
            if cmd == "getOutNamesArray": return sett["output"]["names"]
            if cmd == "getOutPinsArray": return sett["output"]["pins"]
            if cmd == "getOutReadsArray": return readPinsAr()

            if cmd == "getOutNames":
                names = ""
                nameslst = sett["output"]["names"]
                for i in range(len(nameslst)):
                    names = names + ", " + nameslst[i]
                return names
            if cmd == "getOutPins":
                pins = ""
                pinslst = sett["output"]["pins"]
                for i in range(len(pinslst)):
                    pins = pins + ", " + pinslst[i]
                return pins
            if cmd == "getOutRead":
                outpinsrd = []
                outpinsnls = ""
                for i in range(len(sett["output"]["pins"])):
                    rd = board.digital[sett["output"]["pins"][i]].read()
                    if rd == 1:
                        outpinsnls = outpinsnls + "," + "1"
                    else: outpinsnls = outpinsnls + "," + "0"
                return outpinsnls
            
            if cmd == "out1":
                port = sett["output"]["pins"][0]
                if board.digital[port].read() == 1:
                    board.digital[port].write(0)
                else:
                    board.digital[port].write(1)

            if cmd == "out2":
                port = sett["output"]["pins"][1]
                if board.digital[port].read() == 1:
                    board.digital[port].write(0)
                else:
                    board.digital[port].write(1)

            if cmd == "out3":
                port = sett["output"]["pins"][2]
                if board.digital[port].read() == 1:
                    board.digital[port].write(0)
                else:
                    board.digital[port].write(1)

            if cmd == "out4":
                port = sett["output"]["pins"][3]
                if board.digital[port].read() == 1:
                    board.digital[port].write(0)
                else:
                    board.digital[port].write(1)

            return adminpanel(username, password)
    return "LOGIN ERROR"

@app.errorhandler(404)
def not_found_error(error):
    return "Error 404", 404

@app.errorhandler(500)
def internal_error(error):
    return "Error 500", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0")