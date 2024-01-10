import myhelp.filework as mf
import myhelp.interface as mi
import requests
from datetime import date, datetime

try: open("data\\scripts.json").close()
except FileNotFoundError: mf.jsDump("data\\script.json", [])
finally:
    scripts = mf.load("data\\scripts.json", 2)

if scripts == []:
    exit()

while True:
    now = datetime.now()
    timeNow = [int(now.strftime("%H")), int(now.strftime("%M"))]
    for i in range(len(scripts)):
        script = scripts[i]
        if script["type"] == "on time":
            timeToON = script["timeToON"]
            timeToOFF = script["timeToOFF"]
            if timeToON[0] >= timeNow[0] and timeToON[1] >= timeNow[1]:
                print(f"{script["outdToWrite"]} ON")
            else: print(f"{script["outdToWrite"]} OFF")
    mi.asleep(1)