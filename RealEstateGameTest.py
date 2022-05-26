# Author: Nathaniel Luginbill
# GitHub username: nluginbill
# Date: 5/25/2022
# Description: Contains test cases for RealEstateGame.py

import unittest
import random
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

        turn = 1
        while game.check_game_over() == "" and turn < 15:
            for player in game.active_players.values():
                game.move_player(player.get_name(), random.randint(1, 6))
                buy = random.choice([True, False])
                print(player)
                if buy:
                    print(f"And I'm buying {game.gameboard[player.get_location()].get_name()}")
                    game.buy_space(player.get_name())
            turn += 1







test = UnitTest()
test.just_messin()
