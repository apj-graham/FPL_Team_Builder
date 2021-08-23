import requests
import pandas as pd
from collections import namedtuple
from pprint import pprint
from Squad import Squad


PlayerStats = namedtuple('PlayerStats', ['name', 'position', 'cost', 'injured', 'team'])

def main():
    data = get_fpl_data()
    squad = create_team(data)
    print(squad)
    print(squad.cost)

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

<<<<<<< HEAD
def create_team(data, budget=1000, star_player_limit=2):
    """Populate a team with star_player_limit top point scoring players and best value players
    Value is taken as total_point/now_cost"""
    teams = set(data['team'].values)
=======
def create_team(data, budget=1000, star_player_limit=3):
    """Populate a team with star_player_limit top point scoring players and best value players
    Value is taken as total_point/now_cost"""
    teams = set(data['team'].values)
    print(teams)
>>>>>>> 83dfac6aa392c1c87e491fc0ef81949f0d5227b0
    squad = Squad(teams, budget)

    for player in top_players_by('total_points', data):
        if squad.is_player_eligible(player) and star_player_limit > 0:
            squad.add_player(player)
            star_player_limit -= 1
    for player in top_players_by('value', data):
        if squad.is_player_eligible(player):
            squad.add_player(player)

    return squad

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
