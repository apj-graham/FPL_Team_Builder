from constants import FPL_Constants
import unittest
from Squad import Squad, PlayerStats

class TestSquad(unittest.TestCase, FPL_Constants):

    # Example teams that are part of the premier league
    TEAMS = ['Wolves', 'Brentford', 'Crystal Palace', 'Burnley', 'Newcastle', 'Watford', 'Norwich', 'Spurs', 'West Ham', 'Leicester',
             'Liverpool', 'Leeds', 'Southampton', 'Arsenal', 'Everton', 'Chelsea', 'Brighton', 'Aston Villa', 'Man City', 'Man Utd']

    # Cost, injured status and team chosen to be compatible with a blank team
    VALID_GKP = PlayerStats('Name', 'Goalkeeper', 40, 1, TEAMS[0])
    # Player that, realistically, no team will ever have a budget for
    EXPENSIVE_PLAYER = PlayerStats('Name', 'Goalkeeper', 2**31, 1, TEAMS[0])
    # Injured player
    INJURED_PLAYER = PlayerStats('Name', 'Goalkeeper', 0, 0, TEAMS[0])

    def test_add_player(self):
        expected_squad = [self.VALID_GKP]
        expected_budget = self.DEFAULT_BUDGET - self.VALID_GKP.cost

        expected_positions = self.POSITION_LIMITS
        expected_positions[self.VALID_GKP.position] -= 1

        expected_team_counts = {team: 0 for team in self.TEAMS}
        expected_team_counts[self.VALID_GKP.team] = 1

        squad = Squad(self.TEAMS)
        squad.add_player(self.VALID_GKP)

        self.assertEqual(squad._squad, expected_squad)
        self.assertEqual(squad.budget, expected_budget)
        self.assertEqual(squad.positions, expected_positions)
        self.assertEqual(squad.team_counts, expected_team_counts)


    def test_players_property(self):
        """squad.players returns a tuple containing the names of added players"""
        expected_players = tuple([self.VALID_GKP.name])

        squad = Squad(self.TEAMS)
        squad.add_player(self.VALID_GKP)
        players = squad.players

        self.assertIsInstance(players, tuple)
        self.assertIn(self.VALID_GKP.name, players)
        # Check tuple contains only the player names we have added
        self.assertEqual(expected_players, players)

    def test_cost_property(self):
        """squad.cost returns the cost returns the sum of the prices of the added players in 
        units of 1mil"""
        expected_cost = (2 * self.VALID_GKP.cost) / 10
        
        squad = Squad(self.TEAMS)
        squad.add_player(self.VALID_GKP)
        squad.add_player(self.VALID_GKP)
        cost = squad.cost

        self.assertEqual(cost, expected_cost)

    def test_assessing_valid_player(self):
        """A player who is not injured, not too expensive, belongs to a valid team and has a valid position
        is considered eligible"""
        squad = Squad(self.TEAMS)
        is_eligible = squad.is_player_eligible(self.VALID_GKP)
        self.assertTrue(is_eligible)

    def test_assessing_expensive_player(self):
        """A player who has a higher cost than the remaining budget is considered ineligible"""
        squad = Squad(self.TEAMS, budget=0)
        is_eligible = squad.is_player_eligible(self.EXPENSIVE_PLAYER)
        self.assertFalse(is_eligible)

    def test_assessing_injured_player(self):
        """A player who is injured is considered ineligible"""
        squad = Squad(self.TEAMS)
        is_eligible = squad.is_player_eligible(self.INJURED_PLAYER)
        self.assertFalse(is_eligible)

    def test_assessing_player_already_in_team(self):
        """A player already in the team is considered ineligible"""
        squad = Squad(self.TEAMS)
        squad.add_player(self.VALID_GKP)
        is_eligible = squad.is_player_eligible(self.VALID_GKP)
        self.assertFalse(is_eligible)
    
    def test_assessing_player_max_pos_limit(self):
        """A player is considered ineligible if there are no more slots for their field position"""
        squad = Squad(self.TEAMS)
        squad.positions['Goalkeeper'] = 0
        is_eligible = squad.is_player_eligible(self.VALID_GKP)
        self.assertFalse(is_eligible)
    
    def test_assessing_player_max_team_limit(self):
        """A player is considered ineligible if there are no more slots for their team"""
        squad = Squad(self.TEAMS)
        squad.team_counts[self.VALID_GKP.team] = self.TEAM_LIMIT
        is_eligible = squad.is_player_eligible(self.VALID_GKP)
        self.assertFalse(is_eligible)

if __name__ == '__main__':
    unittest.main()
