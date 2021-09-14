from collections import namedtuple
import copy

PlayerStats = namedtuple('PlayerStats', ['name', 'position', 'cost', 'injured', 'team'])

class Squad():
    """Class to encompass all info about the constructed FPL squad including
    players and total cost"""

    def __init__(self, teams, budget=1000):

        # Player prices are reported in units of 0.1m in the API
        # e,g. a player price of 4.5m is stored as 45.
        # The starting budget is 100m or 1000 0.1m units
        self.budget = budget

        # Limits on number of players in team of each position
        # These are taken from the FPL website
        self.positions = {'Goalkeeper': 2, 'Defender': 5,
                         'Midfielder': 5, 'Forward': 3}

        # Tally of number of players from each team
        # The chosen team cannot have more than 3 players from the same team
        self.team_counts = {team: 0 for team in teams}

        # List used to store squad members
        self._squad = []


    @property
    def cost(self):
        """Total cost of the squad in units of 1m"""
        return sum([player.cost for player in self._squad])/10.0


    @property
    def players(self):
        """Player names in squad"""
        return tuple([player.name for player in self._squad])


    def add_player(self, player):
        """Add player to squad. Update availible budget, positions and teams count"""
        self._squad.append(player)
        self.budget -= player.cost
        self.positions[player.position] -= 1
        self.team_counts[player.team] += 1


    def is_player_eligible(self, player):
        """Check if:

        1) They are not injured
        2) They are not already in squad
        3) There are enough spaces for their position
        4) There are less than 3 players from their team already in squad
        5) There is enough room in the budget for them

        If these are all satisfied, then the player is eligible. It is on the user
        to call this method before adding a player.
        """
        if player.injured != 0:
            if player.name not in self.players:
                if self.positions[player.position] > 0:
                    if self.team_counts[player.team] < 3:
                        if player.cost <= self.budget:
                            return True
        return False

    def __str__(self):
        """Return formated string of players in squad and their information"""
        formatted_str = ""

        goalkeepers = [player for player in self._squad if player.position == 'Goalkeeper']
        defenders = [player for player in self._squad if player.position == 'Defender']
        midfielders = [player for player in self._squad if player.position == 'Midfielder']
        forwards = [player for player in self._squad if player.position == 'Forward']
        pos_lists = {"Goalkeepers": goalkeepers,
                     "Defenders": defenders,
                     "Midfielders": midfielders,
                     "Forwards": forwards}

        for pos, player_list in pos_lists.items():
            formatted_str += f"============{pos}==========\n"
            for player in player_list:
                formatted_str += f"Player: {player.name}, Cost: {player.cost}\n"
                formatted_str += "\n"

        return formatted_str
