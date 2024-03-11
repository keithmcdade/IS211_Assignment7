import random
import argparse


random.seed(0)


class Player:
    # initialize total score and current turn score, includes flag for determining player turn
    score = 0
    this_turn_total = 0
    is_turn = False

    def __init__(self, name):
        self.name = f"Player {name}"

    # sums total and current turn scores
    def add_score(self, roll):
        self.this_turn_total += roll
        self.score += roll

    # subtracts current turn score from total when player rolls a 1
    def rolled_one(self):
        self.score -= self.this_turn_total
        self.this_turn_total = 0


class Die:
    def __init__(self, name):
        self.name = name

    # class function for rolling die objects
    @staticmethod
    def roll():
        roll = random.randint(1, 6)
        return roll


def phase_1(choice):
    # each turn is split into phases, the first phase being the first roll where the player cannot choose to hold
    check = check_input(choice)
    if check:
        if choice not in {'r', 'R'}:
            print(f"Invalid input.")
            return False
        else:
            return True
    else:
        return False


def phase_2(player, choice):
    # second phase, here the player can choose to roll or to hold
    check = check_input(choice)
    if check:
        if choice in {'h', 'H'}:
            print(f"{player.name} holds.")
            return False
        else:
            return True
    else:
        return False


def check_input(choice):
    # checks to see if player inputted a valid string
    if choice not in {'r', 'R', 'h', 'H'}:
        print(f"Invalid input.")
        return False
    else:
        return True


def scoring(player, die):
    roll = die.roll()
    # if they roll a 1 run Player class function for subtracting their current turn score to their total score,
    # return False to break loop in turn() function
    if roll == 1:
        player.rolled_one()
        print(f"{player.name} rolled a {roll}, too bad. {player.name}'s score is {player.score}")
        return False
    # if player rolls 2-6 add the score to their total/turn scores, return True to turn() function
    else:
        player.add_score(roll)
        print(f"{player.name} rolled a {roll}.")
        print(f"{player.name}'s score is {player.score}. The current score for this turn is {player.this_turn_total}")
        return True


def _display_turn_flag(player_1, player_2):
    # this function is just for checking which player's turn it is,
    # it's not necessary for the game's functionality
    print(f"{player_1.name} turn = {player_1.is_turn}"
          f"\n{player_2[0].name} turn = {player_2[0].is_turn}")


def turn(player, die):
    cond = True
    while cond:
        player.is_turn = True
        choice = input(f"{player.name}'s turn. {player.name}'s score is {player.score}. "
                       f"Type 'R' to roll.\n")
        # ensure player input is valid, if not go back to input until valid option is entered
        player_start = check_input(choice)
        if not player_start:
            turn(player, die)
        # begin phase 1, represents first roll where player cannot choose to hold
        else:
            if phase_1(choice):
                outcome = scoring(player, die)
                # break if player rolls a 1
                if not outcome:
                    player.is_turn = False
                    break
                # begin phase 2, it is important that the player loop through
                # this section until they either roll a one or choose to hold
                elif outcome:
                    score = player.score
                    if score >= 100:
                        player.is_turn = False
                        break
                    choice = input(f"{player.name}'s turn.  Type 'R' to roll or 'H' to hold.\n")
                    player_continue = phase_2(player, choice)
                    # if player holds end turn
                    if not player_continue:
                        player.is_turn = False
                        player.this_turn_total = 0
                        break
                    else:
                        # if player chooses to roll
                        while player_continue:
                            outcome = scoring(player, die)
                            score = player.score
                            # break when player scores 100
                            if score >= 100:
                                player.is_turn = False
                                cond = False
                                break
                            # break if player rolls a 1
                            if not outcome:
                                player.is_turn = False
                                cond = False
                                break
                            else:
                                # if player rolls 2-6, choose to roll or hold
                                choice = input(f"{player.name}'s turn. Type 'R' to roll or 'H' to hold.\n")
                                player_continue = phase_2(player, choice)
                                # player chooses to roll, go back to top of current while loop
                                if player_continue:
                                    continue
                                # player chooses to hold, break loop move on to next player turn
                                else:
                                    player.is_turn = False
                                    player.this_turn_total = 0
                                    cond = False
                                    break
                    # break out of outer loop when turn ending condition is met in inner loop
                    if not cond:
                        player.is_turn = False
                        break


def main():
    # take in command line arg for amount of players, ranging between 2-10.
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

    # initialize the die and list of Player objects
    die = Die("The Die")
    players = []

    # convert numPlayers argument into Player objects and add them to player list
    for num in range(1, (args.numPlayers + 1)):
        player = Player(num)
        players.append(player)

    # this is where each player's turn is looped until they roll a 1, hold, or score 100.
    # when one of the first two conditions is met the game moves on to the next player,
    # when the last condition is met the loop ends and the game is over.
    no_winner = True
    while no_winner:
        for player in players:
            turn(player, die)
            if player.score >= 100:
                print(f"{player.name} has scored {player.score}. {player.name} won!")
                no_winner = False
                break
        if not no_winner:
            break


if __name__ == '__main__':
    main()
