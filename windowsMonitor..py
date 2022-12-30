import random
import win32gui
from datetime import datetime
import os
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pynput import keyboard

w=win32gui
# w.GetWindowText (w.GetForegroundWindow())
# run continuously and keep track of the windows that are open
# if a new window is opened, add it to the list
# when the window is added add the time it was opened to the list
# if a window is closed, add the time it was closed to the list


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

    # create a plot with the x axis being the time and the y axis being the window
    # show when a window was opened and closed
    # show the total time spent on each window in the legend
    # show the total time spent on all windows in the title

plot = plt.figure()
plot.suptitle(f'Total time spent: {sum([dict[key]["totalTime"] for key in dict])} seconds')
for key in dict:
    dict[key]['color']=f'#{random.randint(0, 0xFFFFFF):06x}'
    if dict[key]["totalTime"] > 60:
        # set key color to a random color
        for time in dict[key]["times"]:
            if time[0] != None and time[1] != None:
                # if time[0] or time[1] is before 9am or after 6pm, don't show it
                if datetime.strptime(time[0], "%H:%M:%S").hour >= 9 and datetime.strptime(time[1], "%H:%M:%S").hour <= 18:
                    # set the same color for the same window
                    # plt.plot([datetime.strptime(time[0], "%H:%M:%S"), datetime.strptime(time[1], "%H:%M:%S")], [key, key], label=dict[key]["name"], linewidth=5)
                    plt.plot([datetime.strptime(time[0], "%H:%M:%S"), datetime.strptime(time[1], "%H:%M:%S")], [key, key], label=dict[key]["name"], linewidth=5, color=dict[key]['color'])
# show the time correctly on the x axis
# the time is currently shown as 00:00:00
# it should be shown as 00:00
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
# left 0.4
plt.gcf().subplots_adjust(left=0.4)
# show the plot
plt.show()
# save the plot
plot.savefig(f'{path}/timesheets_{datetime.now().date().strftime("%d-%m-%Y")}.png')


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

        

