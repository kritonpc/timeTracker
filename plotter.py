# create a script that will create a plot for each day
# the plot will show the time spent on each window

# it will be able to create a plot for all the days in the timesheets folder
# it will be able to create a plot for a specific day
# it will be able to create a plot for a range of days
# this will be done by using the command line arguments

# the plot will be saved in the timesheets/output folder

# the plot will be saved as a png file

from datetime import datetime
import os
import json
import random

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import argparse

parser = argparse.ArgumentParser(description='Create a plot of the time spent on each window.')
parser.add_argument('-d', '--date', help='The date of the plot to create. Format: dd-mm-yyyy')
parser.add_argument('-r', '--range', help='The range of dates to create plots for. Format: dd-mm-yyyy-dd-mm-yyyy')
parser.add_argument('-a', '--all', help='Create plots for all the dates in the timesheets folder', action='store_true')
parser.add_argument('-t', '--today', help='Create a plot for today', action='store_true')
args = parser.parse_args()

workingHours = False

path = 'C:\\Users\\' + os.getlogin() + '\\timesheets\\'
# check if output folder exists
if not os.path.exists(path + 'output'):
    os.makedirs(path + 'output')

def createPlot(date):
    # check if timesheets file exists
    if os.path.exists(f'{path}/timesheets_{date}.json'):
        with open(f'{path}/timesheets_{date}.json', 'r',encoding='utf_8') as f:
            dict = json.load(f)
            plot = plt.figure()
            plot.suptitle(f'Total time spent: {sum([dict[key]["totalTime"] for key in dict])} seconds')
            for key in dict:
                dict[key]['color']=f'#{random.randint(0, 0xFFFFFF):06x}'
                if dict[key]["totalTime"] > 0:
                    # set key color to a random color
                    for time in dict[key]["times"]:
                        if time[0] != None and time[1] != None:
                            if workingHours:
                                if datetime.strptime(time[0], "%H:%M:%S").hour >= 9 and datetime.strptime(time[1], "%H:%M:%S").hour <= 18:
                                    plt.plot([datetime.strptime(time[0], "%H:%M:%S"), datetime.strptime(time[1], "%H:%M:%S")], [key, key], label=dict[key]["name"], linewidth=5, color=dict[key]['color'])
                            else:
                                plt.plot([datetime.strptime(time[0], "%H:%M:%S"), datetime.strptime(time[1], "%H:%M:%S")], [key, key], label=dict[key]["name"], linewidth=5, color=dict[key]['color'])

            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            # left 0.4
            plt.gcf().subplots_adjust(left=0.4)
            # show the plot
            plt.show()
            # save the plot
            plot.savefig(f'{path}/output/timesheets_{datetime.now().date().strftime("%d-%m-%Y")}.png')
    else:
        print(f'No timesheets file found for {date}')
        return
        

if args.date:
    createPlot(args.date)
elif args.range:
    dates = args.range.split('-')
    start = datetime.strptime(dates[0], '%d-%m-%Y')
    end = datetime.strptime(dates[1], '%d-%m-%Y')
    while start <= end:
        createPlot(start.strftime('%d-%m-%Y'))
        start += timedelta(days=1)
elif args.all:
    for file in os.listdir(path):
        if file.startswith('timesheets_'):
            createPlot(file.split('_')[1].split('.')[0])
elif args.today:
    createPlot(datetime.now().date().strftime('%d-%m-%Y'))
else:
    print('No arguments provided. Use -h or --help to see the help message.')
