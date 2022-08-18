from RealEstateGame import *
import discord
import os
import logging
from discord.ext import commands
from dotenv import load_dotenv

# load token from environment variables
load_dotenv()
token = os.environ['TOKEN']

client = discord.Client()
bot = commands.bot.Bot(command_prefix="!")

# error logging
handler = logging.FileHandler(filename='funmonopolybot.log', encoding='utf-8', mode='w')

game = RealEstateGame()
rents = [
    50,
    50,
    50,
    75,
    75,
    75,
    100,
    100,
    100,
    150,
    150,
    150,
    200,
    200,
    200,
    250,
    250,
    250,
    300,
    300,
    300,
    350,
    350,
    350,
]


@bot.command(help="creates a game of Monopoly",
             brief="creates a game of Monopoly",
             name="create",
             )
async def start_new_game(ctx):
    """Starts a new game"""
    user = ctx.author
    game.create_spaces(200, rents)
    await ctx.channel.send(f"{user} has created a game of Monopoly. Type !join to get in before it begins!")


@bot.command(name="join")
async def join_game(ctx):
    """Adds a player to the game"""
    user = ctx.author
    if not game.check_started():
        game.create_spaces(200, rents)
    game.create_player(user, 1500)
    await ctx.channel.send(f"{user} has joined the game")


@bot.command()
async def add_bot(ctx, bot_name):
    if not game.check_started():
        game.create_spaces(200, rents)

    game.create_player(bot_name, 1500)
    await ctx.channel.send(f"{bot_name} has joined the game")


@bot.command(name="begin")
async def begin_game(ctx):
    game.set_started()
    player_going_first = game.get_active_player()
    await ctx.channel.send(f"The game has begun! It is {player_going_first}'s turn first." + "\n" \
                           + "Type !roll to play your turn")


@bot.command()
async def roll(ctx, bot_player=None):
    user = ctx.author
    if bot_player:
        user = bot_player

    users_turn = game.get_active_player() == user
    game_started = game.check_started()
    msg = ""
    if game_started:
        if users_turn:
            player = game.get_player(user)
            dice_roll = player.roll_dice()           # a tuple of two die rolls
            msg = f"{user} rolled a {dice_roll[0]} and a {dice_roll[1]}\n"
            pair = dice_roll[0] == dice_roll[1]
            if pair:
                msg += f"That's a pair! {user} will go again.\n"
            game.move_player(user, dice_roll[0] + dice_roll[1])
            msg = ""
        else:
            msg = "It is " + game.get_active_player() + "'s turn"




bot.run(token) # , log_handler=handler, log_level=logging.DEBUG