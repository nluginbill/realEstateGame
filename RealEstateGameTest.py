# Author: Nathaniel Luginbill
# GitHub username: nluginbill
# Date: 5/25/2022
# Description: Contains test cases for RealEstateGame.py

import unittest
from RealEstateGame import RealEstateGame, Player, Space


class UnitTest(unittest.TestCase):
    """Contains unit tests for RealEstateGame.py"""

    def just_messin(self):
        game = RealEstateGame()

        rents = [50, 50, 50, 75, 75, 75, 100, 100, 100, 150, 150, 150, 200, 200, 200, 250, 250, 250, 300, 300, 300, 350,
                 350, 350]
        game.create_spaces(50, rents)

        game.create_player("Player 1", 1000)
        game.create_player("Player 2", 1000)
        game.create_player("Player 3", 1000)

        game.move_player("Player 1", 6)
        game.buy_space("Player 1")
        game.move_player("Player 2", 6)

        print(game.get_player_account_balance("Player 1"))
        print(game.get_player_account_balance("Player 2"))

        print(game.check_game_over())


test = UnitTest()
test.just_messin()
