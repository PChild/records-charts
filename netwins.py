import tbapy
import matplotlib.pyplot as plt
import os
import csv

dist = '2023fim'
tba = tbapy.TBA(os.getenv("TBA_KEY"))
teams = tba.district_teams(dist, keys=True)

plt.figure(figsize=(21, 15), dpi=100, layout='tight')

chs_data = {}
with open('netwins.csv', mode='r')as file:
    csvFile = csv.reader(file)

    for line in csvFile:
        if line[0] in teams:
            if line[0] not in chs_data:
                chs_data[line[0]] = {'match': [], 'netwins': []}
            chs_data[line[0]]['match'].append(int(line[1]))
            chs_data[line[0]]['netwins'].append(int(line[5]))

ymin = 0
ymax = 0
xmax = 0

top10 = [0] * 10
top10names = [''] * 10

min_val = 0
min_team = ''

focus = ['frc900', 'frc614', 'frc6377', 'frc1293', 'frc2713', 'frc6328']


for team in chs_data:
    data = chs_data[team]
    plt.plot(data['match'], data['netwins'],
             color='black', linewidth=0.4, alpha=0.4)

    ymin = min(data['netwins']) if min(data['netwins']) < ymin else ymin
    ymax = max(data['netwins']) if max(data['netwins']) > ymax else ymax
    xmax = max(data['match']) if max(data['match']) > xmax else xmax

    if data['netwins'][-1] < min_val:
        min_val = data['netwins'][-1]
        min_team = team

    if data['netwins'][-1] > min(top10):
        idx = top10.index(min(top10))
        top10.pop(idx)
        top10names.pop(idx)
        top10.append(data['netwins'][-1])
        top10names.append(team)

    if team in focus:
        plt.plot(data['match'], data['netwins'],
                 color='black', linewidth=1, alpha=1)

        x_coord = data['match'][-1]
        y_coord = data['netwins'][-1]
        plt.annotate(team[3:], (x_coord, y_coord),
                     xycoords="data",
                     textcoords="offset points",
                     xytext=(0, 10), ha="center")

print(min_team, min_val)

for team in top10names:
    data = chs_data[team]
    plt.plot(data['match'], data['netwins'], linewidth=1, alpha=1)

    x_coord = data['match'][-1]
    y_coord = data['netwins'][-1]
    plt.annotate(team[3:], (x_coord, y_coord),
                 xycoords="data",
                 textcoords="offset points",
                 xytext=(0, 10), ha="center")

plt.title("Match Win Records for " +
          dist[4:].upper() + " teams", fontsize='xx-large')
plt.xlim([-0.05, xmax + 0.05])
plt.ylim([ymin - 1, ymax + 1])
plt.box(False)
plt.grid(axis='y', linestyle='dotted')
plt.gca().get_xaxis().set_visible(False)
plt.ylabel("Net Match Wins", fontsize='x-large')
plt.show()
# plt.savefig('CHS Win Records.png')
# plt.close()
