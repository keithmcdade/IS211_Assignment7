import random
import argparse
import inspect


random.seed(0)


class Player:
    score = 0
    wins = 0
    players = []

    def __init__(self, name):
        self.name = f"Player {name}"

    @classmethod
    def create_players(cls, num_players):
        for num in range(1, (num_players + 1)):
            player = Player(num)
            cls.players.append(player)
        return cls.players


class Die:
    dice = []

    def __init__(self, name, sides):
        self.name = name
        self.sides = int(sides)
        Die.dice.append(self)

    def roll(self):
        roll = random.randint(1, self.sides)
        return roll


class Game:
    # b/c the player can't hold at the start of their turn, each turn is split into 2 "phases"
    # the is_initial_phase variable is a flag to determine which phase of the player turn it is
    is_initial_phase = False
    current_turn_total = 0

    def __init__(self, players, name="Game", sides=6, winning_score=100):
        self.name = name
        self.die = Die(f"{self.name} die", sides)
        self.players = players
        self.winning_score = winning_score

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

    def turn(self, player):
        self.current_turn_total = 0
        self.is_initial_phase = True
        is_continue = True
        is_valid = self.parse_input(player)
        while is_continue:
            if is_valid:
                self.is_initial_phase = False
                is_good_roll = self.scoring(player)
                if is_good_roll:
                    is_continue = self.parse_input(player)
                else:
                    is_continue = False

    def scoring(self, player):
        roll = self.die.roll()
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

    def play_game(self):
        for player in self.players:
            player.score = 0
        no_winner = True
        while no_winner:
            for player in self.players:
                self.turn(player)
                if player.score >= self.winning_score:
                    print(f"{player.name} has scored {player.score}. {player.name} won!")
                    player.wins += 1
                    no_winner = False
                    break
                if not no_winner:
                    break


def main():
    parser = argparse.ArgumentParser(description="Program to play the game of Pig.")
    parser.add_argument("-n", "--name",
                        help="This is the name of an individual game.",
                        type=str,
                        default=inspect.signature(Game.__init__).parameters['name'].default)
    parser.add_argument("-p", "--numPlayers",
                        help="How many players you would like to play with, in integer format. The default is 2, the "
                             "minimum is 1, and the maximum is 10. You must enter a value within that range.",
                        type=int, choices=range(1, 11),
                        default=2)
    parser.add_argument("-d", "--numSides",
                        help="Amount of sides each game die has, in integer format. The default is 6, the "
                             "minimum is 4, and the maximum is 20. You must enter a value within that range.",
                        type=int, choices=range(4, 21),
                        default=inspect.signature(Game.__init__).parameters['sides'].default)
    parser.add_argument("-g", "--numGames",
                        help="Amount of games being created, in integer format. The default is 1, the "
                             "minimum is 1, and the maximum is 4. You must enter a value within that range."
                             "Each game will be played sequentially, when one game ends the next game begins until "
                             "all games have been completed.",
                        type=int, choices=range(1, 5),
                        default=1)
    parser.add_argument("-s", "--score",
                        help="Amount of points needed to win the game. Default is 100, minimum is 20 and maximum is "
                             "1000.",
                        type=int, choices=range(20, 1001),
                        default=inspect.signature(Game.__init__).parameters['winning_score'].default)
    args = parser.parse_args()

    if args.numGames == 1:
        text = f"is {args.numGames} game"
    else:
        text = f"are {args.numGames} games"

    print(f"Welcome to Pig! The rules are simple: each player repeatedly rolls a die until they roll a one or they "
          f"decide to hold. If they roll a one they score nothing and must pass the die to the next player.\nIf they "
          f"roll any other number they add it to their score and can decide to roll again or hold and pass the die to "
          f"the next player. Remember, if you roll a one at any point, your score reverts to what it was when the turn "
          f"started. There are currently {args.numPlayers} players, playing with a {args.numSides}-sided die, and "
          f"there {text}. The points needed to win is {args.score}. Player 1 rolls first.\nGood luck!\n")

    players = Player.create_players(args.numPlayers)
    for num in range(1, args.numGames + 1):
        game = Game(players, f"{args.name} {num}", args.numSides, args.score)
        game.play_game()


if __name__ == '__main__':
    main()
