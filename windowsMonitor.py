import random
import win32gui
from datetime import datetime
import os
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pynput import keyboard

w=win32gui


class Window:
    def __init__(self, title, timeOpened, timeClosed):
        self.title = title
        self.timeOpened = timeOpened
        self.timeClosed = timeClosed

    def setTimeClosed(self, timeClosed):
        self.timeClosed = timeClosed

windows = [Window(w.GetWindowText(w.GetForegroundWindow()), datetime.now().strftime("%H:%M:%S"), None)]
prevName = ''
path = 'C:\\Users\\' + os.getlogin() + '\\timesheets\\'
if not os.path.exists(path):
    os.makedirs(path)


if os.path.exists(f'{path}/timesheets_{datetime.now().date().strftime("%d-%m-%Y")}.json'):
    with open(f'{path}/timesheets_{datetime.now().date().strftime("%d-%m-%Y")}.json', 'r',encoding='utf_8') as f:
        dict = json.load(f)
else:
    dict = {w.GetWindowText (w.GetForegroundWindow()):{
                "name": w.GetWindowText (w.GetForegroundWindow()),
                "totalTime": 0,
                "times":[(datetime.now().strftime("%H:%M:%S"), None)]
            }}


while True:
    name = w.GetWindowText (w.GetForegroundWindow())
    if name != prevName:
        if len(prevName) > 2 and len(name) > 2:
            windows[-1].setTimeClosed(datetime.now().strftime("%H:%M:%S"))
            dict[prevName]["times"][-1] = (dict[prevName]["times"][-1][0], datetime.now().strftime("%H:%M:%S"))
            dict[prevName]["totalTime"] += (datetime.strptime(dict[prevName]["times"][-1][1], "%H:%M:%S") - datetime.strptime(dict[prevName]["times"][-1][0], "%H:%M:%S")).total_seconds()
                
            print(f'"{name}"')
        if len(name) > 2:
            windows.append(Window(name, datetime.now().strftime("%H:%M:%S"), None))
            if name in dict:
                dict[name]["times"].append((datetime.now().strftime("%H:%M:%S"), None))
            else:
                dict[name] = {
                    "name": name,
                    "totalTime": 0,
                    "times":[(datetime.now().strftime("%H:%M:%S"), None)]
                }
            prevName = name

        
            
        with open(f'{path}/timesheets_{datetime.now().date().strftime("%d-%m-%Y")}.txt', 'a',encoding='utf_8') as f:
            f.write(f'{windows[-1].title}: {windows[-1].timeOpened} - {windows[-1].timeClosed}\n')
        # export json file
        with open(f'{path}/timesheets_{datetime.now().date().strftime("%d-%m-%Y")}.json', 'w',encoding='utf_8') as f:
            json.dump(dict, f, indent=4, ensure_ascii=False)

        

