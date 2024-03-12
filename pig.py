import random
import argparse


random.seed(0)


class Player:
    score = 0

    def __init__(self, name):
        self.name = f"Player {name}"


class Die:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def roll():
        roll = random.randint(1, 6)
        return roll


class Game:
    # b/c the player can't hold at the start of their turn, each turn is split into 2 "phases"
    # the is_initial_phase variable is a flag to determine which phase of the player turn it is
    is_initial_phase = False
    current_turn_total = 0
    winning_score = 100

    def __init__(self, name):
        self.name = name

    def parse_input(self, player):
        while True:
            if self.is_initial_phase:
                choice = input(f"{player.name}'s turn. {player.name}'s score is {player.score}. Type 'r' to roll.\n")
                if choice != 'r':
                    print(f"Invalid input.")
                    continue
                else:
                    self.is_initial_phase = False
                    return True
            else:
                choice = input(f"{player.name}'s turn. {player.name}'s score is {player.score}. "
                               f"Type 'r' to roll or 'h' to hold.\n")
                if choice == 'h':
                    print(f"{player.name} holds. {player.name}'s score is {player.score}.")
                    return False
                elif choice == 'r':
                    return True
                else:
                    print(f"Invalid input.")
                    continue

    def scoring(self, player, die):
        roll = die.roll()
        if roll == 1:
            self.rolled_one(player)
            print(f"{player.name} rolled a {roll}, too bad. {player.name}'s score is {player.score}")
            return False
        else:
            self.add_score(player, roll)
            if player.score >= self.winning_score:
                print(f"{player.name} rolled a {roll}.")
                return False
            else:
                print(f"{player.name} rolled a {roll}.")
                print(f"{player.name}'s score is {player.score}. The current score for this turn is "
                      f"{self.current_turn_total}")
            return True

    def add_score(self, player, roll):
        self.current_turn_total += roll
        player.score += roll

    def rolled_one(self, player):
        player.score -= self.current_turn_total
        self.current_turn_total = 0

    def turn(self, player, die):
        self.current_turn_total = 0
        self.is_initial_phase = True
        is_valid = self.parse_input(player)
        is_continue = True
        while is_continue:
            if is_valid:
                self.is_initial_phase = False
                is_good_roll = self.scoring(player, die)
                if is_good_roll:
                    is_continue = self.parse_input(player)
                else:
                    is_continue = False


def main():
    parser = argparse.ArgumentParser(description="Program to play the game of Pig.")
    parser.add_argument("-p", "--numPlayers",
                        help="How many players you would like to play with, in integer format. The default and minimum "
                             "number of players is 2, and the maximum is 10. You must enter a value within that range.",
                        type=int, choices=range(1, 11), default=2)
    args = parser.parse_args()

    print(f"Welcome to Pig! The rules are simple: each player repeatedly rolls a die until they roll a one or they "
          f"decide to hold. If they roll a one they score nothing and must pass the die to the next player.\nIf they "
          f"roll any other number they add it to their score and can decide to roll again or hold and pass the die to "
          f"the next player. Remember, if you roll a one at any point, your score reverts to what it was when the turn "
          f"started. There are currently {args.numPlayers} players. Player 1 rolls first.\nGood luck!\n")

    pig = Game("pig")
    die = Die("The Die")
    players = []

    for num in range(1, (args.numPlayers + 1)):
        player = Player(num)
        players.append(player)

    no_winner = True
    while no_winner:
        for player in players:
            pig.turn(player, die)
            if player.score >= pig.winning_score:
                print(f"{player.name} has scored {player.score}. {player.name} won!")
                no_winner = False
                break
            if not no_winner:
                break


if __name__ == '__main__':
    main()
