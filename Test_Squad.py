import unittest
from Squad import Squad, PlayerStats

class TestSquad(unittest.TestCase):

    # Example teams that are part of the premier league
    TEAMS = ['Wolves', 'Brentford', 'Crystal Palace', 'Burnley', 'Newcastle', 'Watford', 'Norwich', 'Spurs', 'West Ham', 'Leicester',
             'Liverpool', 'Leeds', 'Southampton', 'Arsenal', 'Everton', 'Chelsea', 'Brighton', 'Aston Villa', 'Man City', 'Man Utd']

    DEFAULT_BUDGET = 1000

    GKP_LIMIT = 2
    DEF_LIMIT = 5
    MID_LIMIT = 5
    FOR_LIMIT = 3

    POSITIONS = ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']

    def test_assessing_valid_player(self):
        """A player who is not injured, not too expensive, belongs to a valid team and has a valid position
        is considered eligible"""
        valid_player= PlayerStats('Name', 'Goalkeeper', 0, 1, self.TEAMS[0])
        squad = Squad(self.TEAMS)

        is_eligible = squad.is_player_eligible(valid_player)
        self.assertTrue(is_eligible)

    def test_assessing_expensive_player(self):
        """A player who has a higher cost than the remaining budget is considered ineligible"""
        expensive_player = PlayerStats('Name', 'Goalkeeper', 2**31, 1, self.TEAMS[0])
        squad = Squad(self.TEAMS, budget=0)

        is_eligible = squad.is_player_eligible(expensive_player)
        self.assertFalse(is_eligible)

    def test_assessing_injured_player(self):
        """A player who is injured is considered ineligible"""
        injured_player = PlayerStats('Name', 'Goalkeeper', 0, 0, self.TEAMS[0])
        squad = Squad(self.TEAMS)

        is_eligible = squad.is_player_eligible(injured_player)
        self.assertFalse(is_eligible)

    def test_assessing_duplicate_player(self):
        """A player who is already in the squad is considered ineligible"""
        valid_player= PlayerStats('Name', 'Goalkeeper', 0, 1, self.TEAMS[0])
        squad = Squad(self.TEAMS)
        squad.add_player(valid_player)

        is_eligible = squad.is_player_eligible(valid_player)
        self.assertFalse(is_eligible)

    def test_assessing_squad_with_filled_positions_player(self):
        """A squad that has filled all slots for a position will consider a player of that same
        position inelligible"""
        # GKP chosen as it has a lower limit than the team limit so the position limit will
        # reached first
        valid_player= PlayerStats('Name', 'Goalkeeper', 0, 1, self.TEAMS[0])
        squad = Squad(self.TEAMS)
        for _ in range(self.MID_LIMIT):
            squad.add_player(valid_player)

        is_eligible = squad.is_player_eligible(valid_player)
        self.assertFalse(is_eligible)

    def test_assessing_squad_reached_team_limit(self):
        """A squad that has filled all slots for a single team will consider a player of that same
        team inelligible"""
        # GKP chosen as it has a greaterlimit than the team limit so the team limit will
        # reached first
        valid_player= PlayerStats('Name', 'Midfielder', 0, 1, self.TEAMS[0])
        squad = Squad(self.TEAMS)
        for _ in range(3):
            squad.add_player(valid_player)

        is_eligible = squad.is_player_eligible(valid_player)
        self.assertFalse(is_eligible)


if __name__ == '__main__':
    unittest.main()
