import cmdinterface as ci 
import pyfirmata2 as pyfirmata
from flask import Flask

sett = ci.load("config.toml", 1)
app = Flask(__name__)
board = pyfirmata.Arduino(sett["device"]["arduinoPort"])

if len(sett["guard"]["users"]) == len(sett["guard"]["passwords"]):
    pass
else:
    print("GUARD ERROR")
    exit()

@app.route('/')
def tryed():
    return "The BeHome Started!"

@app.route('/user/<username>/password/<password>/command/<cmd>')
def main(username, password, cmd):
    if username in sett["guard"]["users"] and password in sett["guard"]["passwords"]:
        usnmindx = sett["guard"]["users"].index(username)
        if password == sett["guard"]["passwords"][usnmindx]:
            if cmd == "admin": return "YOU ADMIN"
            
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
                return "True"
            if cmd == "out2":
                port = sett["output"]["pins"][1]
                if board.digital[port].read() == 1:
                    board.digital[port].write(0)
                else:
                    board.digital[port].write(1)
                return "True"
            if cmd == "out3":
                port = sett["output"]["pins"][2]
                if board.digital[port].read() == 1:
                    board.digital[port].write(0)
                else:
                    board.digital[port].write(1)
                return "True"
            if cmd == "out4":
                port = sett["output"]["pins"][3]
                if board.digital[port].read() == 1:
                    board.digital[port].write(0)
                else:
                    board.digital[port].write(1)
                return "True"

            return "CMD ERROR"
        
        return "LOGIN ERROR"
    return "LOGIN ERROR"



if __name__ == '__main__':
    app.run(host="0.0.0.0")