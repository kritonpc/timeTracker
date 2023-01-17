from datetime import datetime, timedelta
import os
import json
import random

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import gitlab

import argparse

gitlab_token = 'YOUR_TOKEN'
gitlab_url = 'https://gitlab.com'
author_name = 'Kriton Georgiou'

parser = argparse.ArgumentParser(description='Create a plot of the time spent on each window.')
parser.add_argument('-d', '--date', help='The date of the plot to create. Format: dd-mm-yyyy')
parser.add_argument('-r', '--range', help='The range of dates to create plots for. Format: dd-mm-yyyy-dd-mm-yyyy')
parser.add_argument('-a', '--all', help='Create plots for all the dates in the timesheets folder', action='store_true')
parser.add_argument('-t', '--today', help='Create a plot for today', action='store_true')
parser.add_argument('-m', '--minTime', help='The minimum time spent on a window to be included in the plot. Default: 60 seconds', type=int)
parser.add_argument('-s', '--show', help='Show the plot. Default: False', action='store_true')
parser.add_argument('-w', '--workingHours', help='Only include windows that were opened during working hours. Default: False', action='store_true')
parser.add_argument('-g', '--gitlab', help='Fetch GitLab commits by me for the specific time period', action='store_true')
args = parser.parse_args()

workingHours = args.workingHours
minTime = args.minTime if args.minTime else 60

path = 'C:\\Users\\' + os.getlogin() + '\\timesheets\\'
# check if output folder exists
if not os.path.exists(path + 'output'):
    os.makedirs(path + 'output')

def createPlot(date):
    # check if timesheets file exists
    if args.gitlab:
        day = datetime.strptime(date, '%d-%m-%Y')
        commits = project.commits.list(ref_name='master', since=day, until=day+timedelta(days=1), get_all=True)
        messages = []
        for commit in commits:
            if commit.author_name == author_name:
                messages.append(commit.title)
        print(f'Commits for {date}: {messages}')
    if os.path.exists(f'{path}/timesheets_{date}.json'):
        with open(f'{path}/timesheets_{date}.json', 'r',encoding='utf_8') as f:
            dict = json.load(f)
            plot = plt.figure()
            plot.suptitle(f'Total time spent: {round(sum([dict[key]["totalTime"] for key in dict])/3600,2)} hours')
            # reorder the dict by descending total time
            dict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1]['totalTime'], reverse=False)}
            for key in dict:
                dict[key]['color']=f'#{random.randint(0, 0xFFFFFF):06x}'
                if dict[key]["totalTime"] > minTime:
                    # set key color to a random color
                    for time in dict[key]["times"]:
                        if time[0] != None and time[1] != None:
                            if workingHours:
                                if datetime.strptime(time[0], "%H:%M:%S").hour >= 9 and datetime.strptime(time[1], "%H:%M:%S").hour <= 18:
                                    plt.plot([datetime.strptime(time[0], "%H:%M:%S"), datetime.strptime(time[1], "%H:%M:%S")], [key, key], label=dict[key]["name"], linewidth=5, color=dict[key]['color'])
                            else:
                                plt.plot([datetime.strptime(time[0], "%H:%M:%S"), datetime.strptime(time[1], "%H:%M:%S")], [key, key], label=dict[key]["name"], linewidth=5, color=dict[key]['color'])

            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            plt.gcf().subplots_adjust(left=0.4, right=0.99, top=0.95, bottom=0.1)
            # show the plot
            # plt.show()
            plt.gcf().set_size_inches(1920/100, 1080/100)
            # show gitlab commits
            plt.text(0.01, 0.01, f'Commits for {date}: {messages}', transform=plt.gcf().transFigure, fontsize=8)
            plot.savefig(f'{path}/output/{date}.png', bbox_inches='tight', pad_inches=0.2)
    else:
        print(f'No timesheets file found for {date}')
        return
        
if args.gitlab:
    gl = gitlab.Gitlab(gitlab_url,private_token=gitlab_token)
    gl.auth()
    # get project sfcc-mirakl
    project = gl.projects.list(search='sfcc-mirakl')[0]
    

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
    start = datetime.now().replace(day=1)
    end = datetime.now()
elif args.today:
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = datetime.now()
    createPlot(datetime.now().date().strftime('%d-%m-%Y'))
else:
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = datetime.now()
    createPlot(datetime.now().date().strftime('%d-%m-%Y'))


if args.show:
    plt.show()
