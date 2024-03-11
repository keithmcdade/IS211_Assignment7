import random

players = []


class Player:
    score = 0
    is_turn = False

    def __init__(self, name):
        self.name = name

    def add_score(self, roll):
        self.score += roll

    def _is_turn(self, is_turn):
        pass


class Die:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def roll():
        roll = random.randint(1, 6)
        return roll


class Game:
    def __init__(self):
        pass

    def roll_one(self, player, roll, score, next_player):
        pass

    def check_win(self, score):
        pass


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


def scoring(player, *args):
    roll = Die.roll()
    if roll == 1:
        print(f"{player.name} rolled a {roll}, too bad.")
        return False
    else:
        player.add_score(roll)
        print(f"{player.name} rolled a {roll}.")
        print(f"{player.name}'s score is {player.score}.")
        return True


def check_score(score):
    if score >= 100:
        return False
    else:
        return True


def turn(player):

    cond = True
    while cond:
        choice = input(f"{player.name}'s turn. Type 'R' to roll.\n")
        # ensure player input is valid, if not go back to input until valid option is entered
        player_start = check_input(choice)
        if not player_start:
            turn(player)
        # begin phase 1, represents first roll where player cannot choose to hold
        else:
            if phase_1(choice):
                outcome = scoring(player)
                if not outcome:
                    break
                # begin phase 2, it is important that the player loop through
                # this section until they either roll a one or choose to hold
                elif outcome:
                    score = player.score
                    if score >= 20:
                        break
                    choice = input(f"{player.name}'s turn. Type 'R' to roll or 'H' to hold.\n")
                    player_continue = phase_2(player, choice)
                    if not player_continue:
                        break
                    else:
                        while player_continue:
                            outcome = scoring(player)
                            score = player.score
                            if score >= 20:
                                cond = False
                                break
                            if not outcome:
                                cond = False
                                break
                            else:
                                choice = input(f"{player.name}'s turn. Type 'R' to roll or 'H' to hold.\n")
                                player_continue = phase_2(player, choice)
                                if player_continue:
                                    continue
                                else:
                                    cond = False
                                    break
                    if not cond:
                        break


def main():
    print("Welcome to Pig! The rules are simple: each player repeatedly rolls a die until they roll a one or they "
          "decide to hold. If they roll a one they score nothing and must pass the die to the next player. If they roll"
          "any other number they add it to their score and can decide to roll again or hold and pass the die to the "
          "next player. Remember, if you roll a one at any point, your score reverts to what it was when the turn"
          "started. \nGood luck! \nPlayer 1 rolls first.")

    player_1 = Player("Player 1")
    player_2 = Player("Player 2")

    no_winner = True
    while no_winner:
        turn(player_1)
        if player_1.score >= 20:
            print(f"{player_1.name} has scored {player_1.score}. {player_1.name} won!")
            break

        turn(player_2)
        if player_2.score >= 20:
            print(f"{player_2.name} has scored {player_2.score}. {player_2.name} won!")
            break


if __name__ == '__main__':
    main()
