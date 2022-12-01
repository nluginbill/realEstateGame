import random

class RealEstateGame:
    """A class that creates a RealEstateGame object. The game mimics Monopoly. It is for 2 or more players. The game has
    a 'board' that consists of 25 game spaces in a loop. The first space is the GO space. The players move around
    the board by rolling one six-sided die. All of the spaces can be purchased. Purchased spaces will charge rent to
    the player that lands on them (unless that player owns the space). Players lose when they run out of money. The last
    player with money wins."""

    def __init__(self):
        """Constructs a game. Takes in no parameters. Initializes an empty gameboard (a list of spaces) and an empty
        roster of players (a dictionary of players)"""
        self._go_bonus = 0
        self._active_players = {}
        self._turn_list = []
        self._gameboard = []
        self._turns = 0
        self._interaction_phase = "setup"
        self._started = False

    def get_turns(self):
        """Returns how many turns have been played"""
        return self._turns

    def create_spaces(self, go_bonus, rents):
        """Takes in go_bonus: the amount of money players receive when landing on or passing go. Takes in rents: a
        list of the rents for 24 game spaces. The function then creates a GO space, and 24 Spaces with the given
        rents. It adds these spaces to the gameboard."""
        # set the GO bonus
        self._go_bonus = go_bonus

        # create the GO space
        go_space = Space("GO")

        # add it to the list of spaces on the board, gameboard
        self._gameboard.append(go_space)

        # create a list of names to give the incoming 24 spaces
        name_list = ["United States", "Canada", "Mexico", "Panama", "Haiti", "Jamaica", "Peru", "Republic Dominican",
                     "Cuba", "Caribbean", "Greenland", "El Salvador", "Puerto Rico", "Colombia", "Venezuela",
                     "Honduras", "Guyana", "Guatemala", "Bolivia", "Argentina", "Ecuador", "Chile", "Brazil",
                     "Costa Rica"]

        # create 24 spaces with the list of names and the given rents, adding each to gameboard
        for index in range(24):
            space = Space(name_list[index], rents[index])
            self._gameboard.append(space)

    def get_player(self, name):
        if name in self._active_players:
            return self._active_players[name]

    def create_player(self, name, initial_balance):
        """Takes in name: a unique name to give the new Player. If the name is not unique, the player will not be
        created, and an error will be raised. Takes in initial_balance: a number representing the amount that the
        Player starts with. Players are added to the go space, so can only be used after create_spaces(). """
        # create the player, passing the name and initial balance
        player = Player(name, initial_balance)
        # add the player to the dictionary of active players
        self._active_players[player.get_name()] = player
        self._turn_list.append(player.get_name())

    def get_player_account_balance(self, player_name):
        """Takes in player_name: the name of the Player whose balance is returned. Returns their balance."""
        # return the player's balance from the dictionary
        player = self._active_players[player_name]
        return player.get_balance()

    def get_player_current_position(self, player_name):
        """Takes in player_name: the name of the Player whose position on the board is returned. Returns their position.
        """
        # in the active_players dictionary, look up the location of the given player_name, and return it
        player = self._active_players[player_name]
        return player.get_location()

    def buy_space(self, player_name):
        """Takes in player_name. If the player named is located on a Space that does not already have an owner, and
        the player has more money in their account than the purchase_price of the Space then: The purchase_price is
        subtracted from the player's account, and the player is set as the owner of the space they're located at.
        Returns true Space is bought, and false if not."""

        player = self._active_players[player_name]

        # look up the player's location
        location = self._gameboard[player.get_location()]
        # whether player can afford space's purchase_price
        can_afford = player.get_balance() > location.get_purchase_price()
        # whether they're on the go space
        is_go_space = location == self._gameboard[0]
        # check if that location has an owner and can afford the purchase (and that it's not the GO space)
        if location.get_owner() is None and can_afford and not is_go_space:
            self._gameboard[player.get_location()].change_owner(player.get_name())
            balance = player.get_balance()
            new_balance = balance - location.get_purchase_price()
            self._active_players[player.get_name()].set_balance(new_balance)
            return True
        return False

    def move_player(self, player_name, distance):
        """Takes in player_name. Also takes in distance: an integer between 1 and 6. If the player's balance is 0, the
        function will return without doing anything. Advances the player the given number of Spaces across the board.
        If the player lands on or passes go, they will receive the go_bonus. After moving to the new location, the
        player may need to pay rent. This will occur only if there is an owner of the new location that is not the
        player themselves. If the player does pay rent the following occurs: the rent amount is deducted from the
        player's account balance, and moved to the owner's balance. If the rent payer's balance reaches 0, that player
        is removed from the active_players dictionary, and only their remaining balance will be transferred to the
        owner."""

        player = self._active_players[player_name]

        # if player account balance 0, return
        balance = player.get_balance()
        if balance <= 0:
            return

        # add the distance to be moved to the player's location, looping  around to 0 at 24
        # if looping around (passing/landing on GO) occurs, reward go_bonus
        new_location = player.get_location() + distance
        if new_location > 24:
            # reward go_bonus
            player.set_balance(balance + self._go_bonus)
            new_location -= 25
        player.set_location(new_location)

        # check the Space at that location, check if rent needs to be paid
        location = self._gameboard[new_location]
        owner = self._gameboard[new_location].get_owner()
        if owner is not None and owner != player.get_name(): # if rent needs to be paid
            if balance > location.get_rent():  # if the rent payer has enough money
                # get the owner's current balance, add the rent to it, and set the new balance for the owner
                owner_balance = self._active_players[owner].get_balance()
                new_owner_balance = owner_balance + location.get_rent()
                self._active_players[owner].set_balance(new_owner_balance)

                # deduct the rent from the moving player's balance
                balance -= location.get_rent()
                self._active_players[player_name].set_balance(balance)
            else:
                # put what remains in the moving player's account into the location owner's account
                owner_balance = self._active_players[owner].get_balance()
                owner_balance += balance
                self._active_players[owner].set_balance(owner_balance)

                # set moving player's balance to 0
                self._active_players[player_name].set_balance(0)

                # any properties that this player owned, set their owner value to None
                for space in self._gameboard:
                    if space.get_owner() == player.get_name():
                        space.change_owner(None)

                # the only case where the game can end is when someone has to pay rent but can't cover it
                # so we check here
                self.check_game_over()
        # if no one owns it, set interaction_phase
        elif owner is None:
            self._interaction_phase = player, 'buy'
            return location

    def check_game_over(self):
        """Checks if the game is over. The game is over if all of the players but one have an account balance of 0.
        If the game is over, the winning player's name is returned. If the game is not over, an empty string is
        returned."""
        # loop through active_players dictionary, and see if there is only 1 player with a positive account balance
        positive_balance_count = 0
        winner = ""
        for player in self._active_players.values():
            if player.get_balance() > 0:
                positive_balance_count += 1
                winner = player.get_name()

        if positive_balance_count < 2:
            return winner
        return ""

    def check_created(self):
        return len(self._gameboard) > 0

    def check_started(self):
        """Checks if the game has been started (i.e., gameboard initialized, at least 2 players)"""
        return self._started

    def set_started(self):
        """Start the game"""
        self._started = True

    def get_active_player(self):
        """Returns the player whose turn it is"""
        return self._turn_list[self._turns % len(self._turn_list)]

    def set_interaction_phase(self, player, phase):
        """Updates the interaction phase of the game"""
        self._interaction_phase = player, phase


class Player:
    """A class that represents a Player in the RealEstateGame. The game will create players. Players will be able to
    interact with the Space (tiles on the board) objects by residing on them, and by purchasing and owning them."""

    def __init__(self, name, balance):
        """Constructs a player for the game. Names the player and gives the player a starting balance with arguments.
        Location is an integer that points to the Space on the gameboard. It starts at 0, or the GO space."""
        self._name = name
        self._balance = balance
        self._location = 0

    def get_name(self):
        """return the Player name"""
        return self._name

    def get_balance(self):
        """return the Player's balance"""
        return self._balance

    def set_balance(self, new_balance):
        """change the balance"""
        self._balance = new_balance

    def get_location(self):
        """return the location (an integer between 0 and 24)"""
        return self._location

    def set_location(self, new_location):
        """change the location property to be an integer between 0 and 24"""
        # set the Player's location
        self._location = new_location

    def roll_dice(self) -> (int, int):
        """rolls 2 six-sided dice, returning the results in a tuple"""
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        return die1, die2

    def __str__(self):
        return f"Hi! I'm {self._name}. I'm on space {self._location}. I have ${self._balance}."


class Space:
    """A class that represents a game tile (space) on the game board (which is a list of Spaces). A space will have
    a unique name, a rent amount, and a purchase price (which is 5 x rent amount). These are the properties that will
    be set with arguments. A Space will also track which Player owns it, and which Players reside on it (a list)."""

    def __init__(self, name, rent=0):
        """Constructs a Space for the gameboard. A Space is initialized with a given name and rent. It also has an owner
        property. Rent parameter defaults to 0 so that GO space is created just by sending the name 'GO'."""
        self._name = name
        self._rent = rent
        self._purchase_price = rent * 5
        self._owner = None

    def get_name(self):
        """returns Space's name"""
        return self._name

    def get_rent(self):
        """returns Space's rent"""
        return self._rent

    def get_purchase_price(self):
        """returns Space's purchase price"""
        return self._purchase_price

    def get_owner(self):
        """returns Space's owner (Player)"""
        return self.owner

    def change_owner(self, purchaser):
        """replaces the owner with the given purchaser (player name)"""
        self._owner = purchaser


"""
DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS

1. Determining how to store the spaces and players
    The spaces will be stored as objects from the Space class, in a list named gameboard, which is an attribute of the
RealEstateGame class. The players will be stored in the active_players dictionary with their names as keys and the
Player objects as the values. 

2. Initializing the board spaces and players
    Initializing the board spaces and players will be done with create_spaces() and create_players(). create_spaces()
will first create the GO space, which will be named GO, and have None for rent. Then it will loop through the given
list of rents, and create named spaces with those given rents. Then it will add the GO space, and the rest of the 
gameboard spaces, to the gameboard list. The players will be created by create_players(). Player objects track their
position with 'location'. When they are initialized, the Player locat ion is set to 0, or the GO space. The created
players are added to the active_players list.

3. Determining how to implement player piece movement
    Player piece movement will be tied to the Player object's location. Players can be moved with Player.move(). It will
in turn be called by RealEstateGame.move_player(). Move_player() takes in which player to move and how far. The distance
to move will be added to the Player.location, an integer between 0 and 24, circling back to 0 at the top of the range.
This location number can be used to index the gameboard list, and will retrieve the corresponding Space that the Player
is located on.

4. Determining how to buy board spaces, and pay and receive rents
    RealEstateGame.buy_space() will handle buying board spaces. RealEstateGame.move_player() will handle rent payments.
buy_space() takes in a player's name. It will look up that player in the active_players dictionary, and check their
location. Then that location is used to check the Spaces purchase_price and whether it has an owner already. If the 
purchase_price is smaller than the Player's account balance (and there is no owner, then the purchase_price will be 
removed from the Player's account balance, and the player's name will be the value in Space.owner.
    move_player() will handle rent payment. Rent payment occurs when a Player lands on a Space that is owned by another
Player. This means that the logic for rent payment will occur when a Player updates its location, that location is
used as the index for the RealEstateGame.gameboard list, to find the Space the Player landed on. Then Space.owner is 
checked. If there is indeed an owner value, and the owner is not the same as Player, then rent payment occurs. Rent 
payment will look up Space.get_rent(), deduct that from Player's account balance with Player.get_balance() and 
Player.set_balance(). Then, it will use Space.owner to find the Player with that name on the active_players list. The
rent amount will be added to that player's balance.

5. Determining how to pass GO and receive the pay amount
    Passing GO will only occur during player movement, move_player(). When adding the distance to the Player's 
location, if the location plus the distance is greater than 24, then they will receive the go_bonus. Player.balance
will be adjusted with Player.set_balance(). 

6. Determining when the game has ended
    Because paying rent is the only way to lose the game, and paying rent only occurs on movement, our check_game_over()
function should only need to be called in move_player(). It will scan through the active_players dictionary. If only 
1 Player has a positive account balance, the game will end. 
"""
