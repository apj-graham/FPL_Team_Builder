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

    TEAM_LIMIT = 3

    def test_add_player_to_squad(self):
        """ Adding a player to a squad to should:
        1) Add ther PlayerStats tuple to the squad
        2) Deduct cost of player from budget
        3) Update squad position limits
        4) Update squad team counts
        """
        valid_player= PlayerStats('Name', 'Goalkeeper', 500, 1, self.TEAMS[0])
        squad = Squad(self.TEAMS)
        squad.add_player(valid_player)

        exp_squad = [valid_player]
        exp_squad_cost = (1000 - valid_player.cost) / 10 # Cost returned in units of 1 mil
        exp_squad_position_limit = self.GKP_LIMIT - 1
        exp_squad_team_limit = 1

        self.assertEqual(squad._squad, exp_squad)
        self.assertEqual(squad.cost, exp_squad_cost)
        self.assertEqual(squad.positions[valid_player.position], exp_squad_position_limit)
        self.assertEqual(squad.team_counts[valid_player.team], exp_squad_team_limit)

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
        for _ in range(self.TEAM_LIMIT):
            squad.add_player(valid_player)

        is_eligible = squad.is_player_eligible(valid_player)
        self.assertFalse(is_eligible)


if __name__ == '__main__':
    unittest.main()
