import random


class Player:
    score = 0

    def __init__(self, name):
        self.name = name


class Game:
    def __init__(self):
        pass

    # @classmethod
    # def valid_input(cls, choice):
    #     if choice == 'R' or 'H':
    #         print("Ok.")
    #         return True
    #     else:
    #         print("Invalid input.")
    #         return False

    @classmethod
    def user_input(cls, player):
        choice = input(f"{player.name}'s turn. Type 'R' to roll.\n")
        while choice not in {'r'.lower(), 'h'.lower()}:
            print("Invalid input.")
            continue
        if choice == 'r'.lower():
            return True
        if choice == 'h'.lower():
            return False


    @classmethod
    def player_roll(cls):
        die = Die()
        roll = die.roll()
        return roll

    @classmethod
    def add_score(cls, player, roll):
        player.score += roll
        print(f"{player.name} rolled a {roll}, the score is {player.score}")
        choice_roll = input(f"Press 'R' to roll again or 'H' to hold.\n")
        return choice_roll.lower()

    @classmethod
    def player_hold(cls, player):
        pass


class Die:
    def __init__(self):
        pass

    def roll(self):
        roll = random.randint(1, 6)
        return roll


def play_pig():
    print("Welcome to Pig! The rules are simple: each player repeatedly rolls a die until they roll a one or they "
          "decide to hold. If they roll a one they score nothing and must pass the die to the next player. If they roll"
          "any other number they add it to their score and can decide to roll again or hold and pass the die to the "
          "next player. Remember, if you roll a one at any point, your score reverts to what it was when the turn"
          "started. \nGood luck! \nPlayer 1 rolls first.")

    die = Die()
    player_1 = Player("Player 1")
    player_2 = Player("Player 2")
    choice = Game.user_input(player_1)
    while choice:
        roll = Game.player_roll()
        this_turn = Game.add_score(player_1, roll)
    else:
        print("It is now Player 2's turn.")


    # user_init = input(f"{player_1.name}'s turn. Type 'R' to roll.\n")
    # if user_init != "R".lower():
    #     input(f"Invalid input. Type 'R' to roll\n")
    # else:
    #     roll = Game.player_roll()
    

if __name__ == '__main__':
    play_pig()

