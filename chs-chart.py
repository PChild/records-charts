import tbapy
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

tba = tbapy.TBA(os.getenv("TBA_KEY"))
COMP_LEVEL = {'qm': 0, 'of': 1, 'qf': 2, 'sf': 3, 'f': 4}
plt.figure(figsize=(21, 15), dpi=100, layout='tight')

for team in tqdm(tba.district_teams('2023chs')):

    events = tba.team_events(team.key, simple=True)
    events = filter(lambda event: event.event_type <= 5, events)
    events = sorted(events, key=lambda event: event.start_date)

    # Get the team's matches
    wins = {}
    for i, event in enumerate(events):
        if wins == {}:
            wins[event.year] = [0]
        if event.year not in wins:
            wins[event.year] = [wins[events[i-1].year][-1]]

        matches = tba.team_matches(team.key, event.key, simple=True)
        matches = sorted(matches, key=lambda match: (
            COMP_LEVEL[match.comp_level], match.set_number, match.match_number))
        for match in matches:
            team_alliance = ''
            if team.key in match.alliances['blue']['team_keys']:
                team_alliance = 'blue'
            elif team.key in match.alliances['red']['team_keys']:
                team_alliance = 'red'
            else:
                continue

            if match.winning_alliance == team_alliance:
                wins[event.year].append(wins[event.year][-1] + 1)
            elif match.winning_alliance == '':
                wins[event.year].append(wins[event.year][-1])
            else:
                wins[event.year].append(wins[event.year][-1] - 1)

    x = [0]
    for year, data in wins.items():
        if len(data) <= 1:
            continue
        x = list(range(x[-1], x[-1] + len(wins[year])))
        # plt.fill_between(x, data, label=year, color=plt.cm.Paired(year % 12))
        plt.plot(x, data, color='black', linewidth=1)
        # ymin = min(data) if min(data) < ymin else ymin
        # ymax = max(data) if max(data) > ymax else ymax
        # x_coord = x[int((len(x) - 1) / 2)]
        # y_coord = data[int((len(data) - 1) / 2)]
        # y_coord = -1 if y_coord < 0 else y_coord
        # plt.annotate(year, (x_coord, y_coord),
        #              xycoords="data",
        #              textcoords="offset points",
        #              xytext=(0, 30), ha="center")
plt.title("Match Win Records for CHS teams", fontsize='x-large')

plt.box(False)
plt.grid(axis='y', linestyle='dotted')
plt.gca().get_xaxis().set_visible(False)
plt.ylabel("Net Match Wins", fontsize='large')
plt.savefig('CHS Win Records.png')
plt.close()
