import requests
import pandas as pd
import numpy as np
import matplotlib
import copy
from collections import namedtuple
from pprint import pprint

from matplotlib import pyplot as plt

PlayerStats = namedtuple('PlayerStats', ['name', 'position', 'cost', 'injured', 'team'])

def main():
    data = get_fpl_data()
    team = create_team(data)
    pprint(team)

def get_fpl_data():
    """Get player data for this season from the fpl API. Convert some fields to appropriate types"""

    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    res = requests.get(url)
    json = res.json()

    # String values used to replace number values for readability later
    elements_df = pd.DataFrame(json['elements'])
    elements_types_df = pd.DataFrame(json['element_types'])
    teams_df = pd.DataFrame(json['teams'])

    # Map values to strings for readability e.g. 3 (position) -> goalkeeper
    elements_df['position'] = elements_df.element_type.map(elements_types_df.set_index('id').singular_name)
    elements_df['team'] = elements_df.team.map(teams_df.set_index('id').name)

    # Treat prices as floats rather than strings
    elements_df['value'] = elements_df.value_season.astype(float)

    return elements_df

def create_team(data, budget=1000, star_player_limit=3, gkp=2, df=5, mid=5, fwd=3):
    """Populate a team with star_player_limit top point scoring players and best value players
    Value is taken as total_point/now_cost"""
    teams = set(data['team'].values)
    teams_count = {team: 0 for team in teams}

    fpl_team = []
    positions = {'Goalkeeper': gkp, 'Defender': df,
                 'Midfielder': mid, 'Forward': fwd}
    for player in top_players_by('total_points', data):
        if budget >= player.cost and positions[player.position] > 0 and star_player_limit > 0 and player.injured != 0 and teams_count[player.team] <= 3:
            fpl_team.append(player)
            budget -= player.cost
            positions[player.position] -= 1
            star_player_limit -= 1
            teams_count[player.team] += 1
    for player in top_players_by('value', data):
        if player not in fpl_team and budget >= player.cost and player.injured != 0 and positions[player.position] > 0:
            fpl_team.append(player)
            budget -= player.cost
            positions[player.position] -= 1
            teams_count[player.team] += 1

    return fpl_team

def top_players_by(measure, data):
    """Return players from dataframe in descending order of 'measure'"""

    count = 0
    data = data.sort_values(measure, ascending=False)
    while count <= data.shape[1]: # Does not exceed number of rows in df
        player_info = data.iloc[count]
        player = PlayerStats(
            player_info['web_name'],
            player_info['position'],
            player_info['now_cost'],
            player_info['chance_of_playing_this_round'],
            player_info['team']
        )
        yield player
        count += 1

if __name__ == "__main__":
    main()
