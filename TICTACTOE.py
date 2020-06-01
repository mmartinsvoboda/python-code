from random import randint
from copy import deepcopy

# Graphics
def show_state(state):
    print()
    for each in state:
        print(" ".join(str(char) for char in each))
    for i in range(len(state[0])):
        print("-", end=" ")
    print()
    for i in range(len(state[0])):
        print(i, end=" ")
    print()

# Main function
def tictactoe(rows, cols, human_starts=True):
    game_plan = game_prep(rows, cols)
    game_end = 0
    player = "X"
    PC = "O"
    players_turn = human_starts
    filled = []
    show_state(game_plan)
    print()
    while game_end == 0:
        if players_turn:
            print("It's your turn.")
            move = None
            while move == None:
                while True:
                    try:
                        move = int(input("Choose a column: "))
                    except:
                        continue
                    break
                move = move_check(move, game_plan)
            filled = fill_plan(game_plan, player, move)
            symbol = player
        else:
            print("It's computer's turn.")
            move, filled = strategy(game_plan, PC)
            symbol = PC
        show_state(game_plan)
        players_turn = not(players_turn)
        game_end = win_check(move, filled, symbol,
                             game_plan, tie_check(game_plan))
        print()
        print()
    if game_end == 1:
        print("The player wins!!!")
    elif game_end == 2:
        print("The computer wins!!!")
    else:
        print("It's a tie!")
    input()

# Tie check
def tie_check(game_plan):
    for symbol in game_plan[0]:
        if symbol == " ":
            return False
    return True

# Win check
def win_check(move, filled, symbol, game_plan, is_tie):
    # Vertically
    for i in range(len(game_plan) - 3):
        if (game_plan[i][move] == symbol and
            game_plan[i + 1][move] == symbol and
            game_plan[i + 2][move] == symbol and
                game_plan[i + 3][move] == symbol):
            if symbol == "X":
                return 1
            else:
                return 2
    # Horizontally
    for i in range(len(filled) - 3):
        if (filled[i] == symbol and
            filled[i + 1] == symbol and
            filled[i + 2] == symbol and
                filled[i + 3] == symbol):
            if symbol == "X":
                return 1
            else:
                return 2
    # Diagonally 1
    for i in range(len(game_plan) - 3):
        for j in range(len(game_plan[0]) - 3):
            if (game_plan[i][j] == symbol and
                game_plan[i + 1][j + 1] == symbol and
                game_plan[i + 2][j + 2] == symbol and
                    game_plan[i + 3][j + 3] == symbol):
                if symbol == "X":
                    return 1
                else:
                    return 2
    # Diagonally 2
    for i in range(len(game_plan) - 3):
        for j in range(len(game_plan[0]) - 3):
            if (game_plan[i][len(game_plan[0]) - j - 1] == symbol and
                game_plan[i + 1][len(game_plan[0]) - j - 2] == symbol and
                game_plan[i + 2][len(game_plan[0]) - j - 3] == symbol and
                    game_plan[i + 3][len(game_plan[0]) - j - 4] == symbol):
                if symbol == "X":
                    return 1
                else:
                    return 2
    if is_tie:
        return 3
    else:
        return 0

# Fills the spot - Makes the move
def fill_plan(plan, symbol, move):
    for line in reversed(plan):
        if line[move] == " ":
            line[move] = symbol
            return line

# Checks whether the move is possible
def move_check(move, game_plan):
    if move < 0 or move > len(game_plan[0]) - 1:
        return None
    if game_plan[0][move] != " ":
        return None
    return move

# Creates the main array
def game_prep(rows, cols):
    game_plan = []
    help_array = []
    del game_plan[:]
    for i in range(rows):
        del help_array[:]
        for j in range(cols):
            help_array.append(" ")
        game_plan.append(help_array[:])
    del help_array[:]
    return game_plan[:]


"""
COMPUTER LOGIC - AI

AI does these moves in this order:
    1. Tries to win - Tries to find 3-in-a-rows or their versions (XX_X or X_XX)
    2. Stops an opponent from winning - As above
    3. If there is a possibility to create a fork, creates it
    4. If an opponent has a possibility to create a fork, denies it
    5. Tries to create a 3-in-a-row
    6. Tries to stop an opponent from creating a 3-in-a-row
    7. If none from above possible, places a mark nearby any mark it owns
    8. Plays randomly
    ------------------------
    9. A few other strategies for few first rounds

Before it makes any move, it makes sure, that the move would NOT help an opponent to win.
If it does help opponent to win, it tries to find another move.

I have done a lot of testing and I believe that it is pretty smart.
"""
def strategy(state, symbol):
    move = three_in_a_row(state, symbol)
    if move != None:
        print("I play '{}', because {}.".format(move, "I have 3 in a row"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = three_in_a_row(state, "X")
    if move != None:
        print("I play '{}', because {}.".format(move, "You have 3 in a row"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = three_in_a_row_2(state, symbol)
    if move != None:
        print("I play '{}', because {}.".format(
            move, "I have 3 out of 4 in a row"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = three_in_a_row_2(state, "X")
    if move != None:
        print("I play '{}', because {}.".format(
            move, "You have 3 out of 4 in a row"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = best_move_attack(state)
    if move != None:
        print("I play '{}', because {}.".format(move, "it's the fastest way to win"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = best_move_defend(state)
    if move != None:
        print("I play '{}', because {}.".format(move, "otherwise you could quickly execute"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = two_in_a_row_1(state, symbol, "X")
    if move != None:
        print("I play '{}', because {}.".format(move, "I have 2 in a row"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = two_in_a_row_2(state, symbol, "X")
    if move != None:
        print("I play '{}', because {}.".format(
            move, "I have 2 out of 4 in a row"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = two_in_a_row_1(state, "X", symbol)
    if move != None:
        print("I play '{}', because {}.".format(
            move, "You have a go on 3 in a row"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = bottom_line(state, symbol)
    if move != None:
        print("I play '{}', because {}.".format(
            move, "it feels like the best move"))
        filled = fill_plan(state, symbol, move)
        return move, filled
    
    move = one_full_under(state, symbol, "X")
    if move != None:
        print("I play '{}', because {}.".format(move, "I go for a line"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = fork(state, symbol, "X")
    if move != None:
        print("I play '{}', because {}.".format(
            move, "I create a fork this way"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = fork(state, "X", symbol)
    if move != None:
        print("I play '{}', because {}.".format(
            move, "You could create a fork"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = top_2_in_a_row(state, symbol, "X")
    if move != None:
        print("I play '{}', because {}.".format(
            move, "I have 2 in a row vertically"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = diag_2_in_a_row(state, symbol, "X")
    if move != None:
        print("I play '{}', because {}.".format(
            move, "I have 2 in a row diagonaly"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = one_on_the_board(state, symbol, "X")
    if move != None:
        print("I play '{}', because {}.".format(move, "it's my best option"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = none_on_the_board(state)
    if move != None:
        print("I play '{}', because {}.".format(
            move, "it's the best start position"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = unplayable(state, symbol, "X")
    if move != None:
        print("I play '{}', because {}.".format(
            move, "it feels like the best option"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    move = two_in_a_row_2(state, "X", symbol)
    if move != None:
        print("I play '{}', because {}.".format(
            move, "You have 2 out of 4 in a row"))
        filled = fill_plan(state, symbol, move)
        return move, filled

    i = 1
    while move == None:
        move = randint(0, len(state[0]) - 1)
        move = move_check(move, state)
        if move != None and not win_predict(state, move) and not win_predict2(state, move) and i > 0 and i < 3 * len(state[0]):
            move = None
            i += 1
    print("I play '{}', because {}.".format(
        move, "there is not a single good move"))
    filled = fill_plan(state, symbol, move)
    return move, filled


"""
Checks for a 3-in-a-row without any space
Checking for AI and then Player
"""
def three_in_a_row(state, symbol):
    # 3 in a row vertically
    for i in range(len(state) - 1, -1, -1):
        for j in range(len(state[0]) - 2):
            if state[i][j] == symbol and state[i][j + 1] == symbol and state[i][j + 2] == symbol:
                if (j - 1 >= 0 and state[i][j - 1] == " ") and (i + 1 == len(state) or state[i + 1][j - 1] != " "):
                    return j - 1
                if (j + 3 < len(state[0]) and state[i][j + 3] == " ") and (i == len(state) - 1 or state[i + 1][j + 3] != " "):
                    return j + 3
    # 3 in a row horizontally
    for j in range(len(state[0])):
        for i in range(len(state) - 3):
            if state[i][j] == " " and state[i + 1][j] == symbol and state[i + 2][j] == symbol and state[i + 3][j] == symbol:
                return j
    # 3 in a row diagonally
    for i in range(len(state) - 2):
        for j in range(len(state[0]) - 2):
            if state[i][j] == symbol and state[i + 1][j + 1] == symbol and state[i + 2][j + 2] == symbol:
                if j - 1 >= 0 and i - 1 >= 0 and state[i - 1][j - 1] == " " and state[i][j - 1] != " ":
                    return j - 1
                if j + 3 < len(state[0]) and i + 3 < len(state) and state[i + 3][j + 3] == " " and (i + 4 == len(state) or state[i + 4][j + 3] != " "):
                    return j + 3
    # 3 in a row diagonally 2
    for i in range(len(state) - 1, 1, -1):
        for j in range(len(state[0]) - 2):
            if state[i][j] == symbol and state[i - 1][j + 1] == symbol and state[i - 2][j + 2] == symbol:
                if j - 1 >= 0 and i + 1 < len(state) and state[i + 1][j - 1] == " " and (i + 2 == len(state) or state[i + 2][j - 1] != " "):
                    return j - 1
                if j + 3 < len(state[0]) and i - 3 >= 0 and state[i - 3][j + 3] == " " and state[i - 2][j + 3] != " ":
                    return j + 3
    return None

"""
Checks for a 3-in-a-row with a space inside
Checking for AI and then Player
"""
def three_in_a_row_2(state, symbol):
    for i in range(len(state)):
        for j in range(len(state[0]) - 3):
            if state[i][j] == symbol and state[i][j + 1] == symbol and state[i][j + 2] == " " and state[i][j + 3] == symbol and (i == len(state) - 1 or state[i + 1][j + 2] != " "):
                return j + 2
            if state[i][j] == symbol and state[i][j + 1] == " " and state[i][j + 2] == symbol and state[i][j + 3] == symbol and (i == len(state) - 1 or state[i + 1][j + 1] != " "):
                return j + 1
    # 3 in a row 2 diagonally
    for i in range(len(state) - 3):
        for j in range(len(state[0]) - 3):
            if state[i][j] == symbol and state[i + 1][j + 1] == " " and state[i + 2][j + 2] == symbol and state[i + 3][j + 3] == symbol:
                if state[i + 2][j + 1] != " ":
                    return j + 1
            if state[i][j] == symbol and state[i + 1][j + 1] == symbol and state[i + 2][j + 2] == " " and state[i + 3][j + 3] == symbol:
                if state[i + 3][j + 2] != " ":
                    return j + 2
    # 3 in a row 2 diagonally 2
    for i in range(len(state) - 1, 2, -1):
        for j in range(len(state[0]) - 3):
            if state[i][j] == symbol and state[i - 1][j + 1] == " " and state[i - 2][j + 2] == symbol and state[i - 3][j + 3] == symbol:
                if state[i][j + 1] != " ":
                    return j + 1
            if state[i][j] == symbol and state[i - 1][j + 1] == symbol and state[i - 2][j + 2] == " " and state[i - 3][j + 3] == symbol:
                if state[i - 1][j + 2] != " ":
                    return j + 2
    return None

"""
Tries to find a spot, where would an opponent be able to win
in more than 1 way. Stops him.
"""
def best_move_defend(ar):
    test = []
    test = deepcopy(ar)
    for j in range(len(test[0])):
        if move_check(j, test) != None:
            test2 = deepcopy(test)
            fill_plan(test2, "X", j)
            if win_predict2_counter(test2, "X") > 1:
                return j
    return None

"""
Tries to find a spot, where would be able to win
in more than 1 way. Makes the move.
"""
def best_move_attack(ar):
    test = []
    test = deepcopy(ar)
    for j in range(len(test[0])):
        if move_check(j, test) != None:
            test2 = deepcopy(test)
            fill_plan(test2, "O", j)
            if win_predict2_counter(test2, "O") > 1 and win_predict(test, j):
                return j
    return None

"""
Checks for a 2-in-a-row which could end up in the win
Checking for AI and then Player
"""
def two_in_a_row_1(state, symbol, opponent):
    for i in range(len(state)):
        for j in range(1, len(state[0]) - 3):
            if (state[i][j - 1] == " " and state[i][j] == symbol and state[i][j + 1] == symbol and state[i][j + 2] == " " and state[i][j + 3] == " "
                    and (i + 1 == len(state) or (state[i + 1][j + 2] != " " and state[i + 1][j + 3] != " ")) and win_predict(state, j + 2)):
                return j + 2
            if (state[i][j - 1] == " " and state[i][j] == " " and state[i][j + 1] == symbol and state[i][j + 2] == symbol and state[i][j + 3] == " "
                    and (i + 1 == len(state) or (state[i + 1][j] != " " and state[i + 1][j - 1] != " ")) and win_predict(state, j)):
                return j
            if (state[i][j - 1] == " " and state[i][j] == symbol and state[i][j + 1] == " " and state[i][j + 2] == symbol and state[i][j + 3] == " "
                    and (i + 1 == len(state) or (state[i + 1][j + 1] != " " and (state[i + 1][j - 1] != " " or state[i + 1][j + 3] != " "))) and win_predict(state, j + 1)):
                return j + 1
    return None

"""
Checks for a 2-in-a-row
Checking for AI and then Player
"""
def two_in_a_row_2(state, symbol, opponent):
    for i in range(len(state)):
        for j in range(len(state[0]) - 3):
            if state[i][j] == " " and state[i][j + 1] == symbol and state[i][j + 2] == symbol and state[i][j + 3] == " ":
                if i + 1 == len(state) and win_predict(state, j) and win_predict2(state, j):
                    return j
                if state[i + 1][j] != " " and win_predict(state, j) and win_predict2(state, j):
                    return j
                if state[i + 1][j + 3] != " " and win_predict(state, j + 3) and win_predict2(state, j + 3):
                    return j + 3
    for i in range(len(state)):
        for j in range(len(state[0]) - 3):
            if state[i][j] == " " and state[i][j + 1] == " " and state[i][j + 2] == symbol and state[i][j + 3] == symbol:
                if i + 1 == len(state) and win_predict(state, j + 1) and win_predict2(state, j + 1):
                    return j + 1
                if state[i + 1][j + 1] != " " and win_predict(state, j + 1) and win_predict2(state, j + 1):
                    return j + 1
    for i in range(len(state)):
        for j in range(len(state[0]) - 3):
            if state[i][j] == symbol and state[i][j + 1] == symbol and state[i][j + 2] == " " and state[i][j + 3] == " ":
                if i + 1 == len(state) and win_predict(state, j + 2) and win_predict2(state, j + 2):
                    return j + 2
                if state[i + 1][j + 2] != " " and win_predict(state, j + 2) and win_predict2(state, j + 2):
                    return j + 2
    for i in range(len(state)):
        for j in range(len(state[0]) - 3):
            if state[i][j] == symbol and state[i][j + 1] == " " and state[i][j + 2] == " " and state[i][j + 3] == symbol:
                if i + 1 == len(state) and win_predict(state, j + 1) and win_predict2(state, j + 1):
                    return j + 1
                if state[i + 1][j + 1] != " " and win_predict(state, j + 1) and win_predict2(state, j + 1):
                    return j + 1
    for i in range(len(state)):
        for j in range(len(state[0]) - 3):
            if state[i][j] == symbol and state[i][j + 1] == " " and state[i][j + 2] == symbol and state[i][j + 3] == " ":
                if i + 1 == len(state) and win_predict(state, j + 1) and win_predict2(state, j + 1):
                    return j + 1
                if state[i + 1][j + 1] != " " and win_predict(state, j + 1) and win_predict2(state, j + 1):
                    return j + 1
                if i + 1 == len(state) and win_predict(state, j + 3) and win_predict2(state, j + 3):
                    return j + 3
                if state[i + 1][j + 3] != " " and win_predict(state, j + 3) and win_predict2(state, j + 3):
                    return j + 3
    for i in range(len(state)):
        for j in range(len(state[0]) - 3):
            if state[i][j] == " " and state[i][j + 1] == symbol and state[i][j + 2] == " " and state[i][j + 3] == symbol:
                if i + 1 == len(state) and win_predict(state, j) and win_predict2(state, j):
                    return j
                if state[i + 1][j] != " " and win_predict(state, j) and win_predict2(state, j):
                    return j
                if i + 1 == len(state) and win_predict(state, j + 2) and win_predict2(state, j + 2):
                    return j + 2
                if state[i + 1][j + 2] != " " and win_predict(state, j + 2) and win_predict2(state, j + 2):
                    return j + 2
    for i in range(len(state) - 3):
        for j in range(len(state[0]) - 3):
            if state[i][j] == " " and state[i + 1][j + 1] == symbol and state[i + 2][j + 2] == " " and state[i + 3][j + 3] == symbol:
                if state[i + 1][j] != " " and win_predict(state, j) and win_predict2(state, j):
                    return j
                if state[i + 3][j + 2] != " " and win_predict(state, j + 2) and win_predict2(state, j + 2):
                    return j + 2
            if state[i][j] == symbol and state[i + 1][j + 1] == " " and state[i + 2][j + 2] == symbol and state[i + 3][j + 3] == " ":
                if state[i + 2][j + 1] != " " and win_predict(state, j + 1) and win_predict2(state, j + 1):
                    return j + 1
                if i + 4 < len(state) and state[i + 4][j + 3] != " " and win_predict(state, j + 3) and win_predict2(state, j + 3):
                    return j + 3
            if state[i][j] == symbol and state[i + 1][j + 1] == " " and state[i + 2][j + 2] == " " and state[i + 3][j + 3] == symbol:
                if state[i + 2][j + 1] != " " and win_predict(state, j + 1) and win_predict2(state, j + 1):
                    return j + 1
                if state[i + 3][j + 2] != " " and win_predict(state, j + 2) and win_predict2(state, j + 2):
                    return j + 2
            if state[i][j] == " " and state[i + 1][j + 1] == symbol and state[i + 2][j + 2] == symbol and state[i + 3][j + 3] == " ":
                if state[i + 1][j] != " " and win_predict(state, j) and win_predict2(state, j):
                    return j
                if i + 4 < len(state) and state[i + 4][j + 3] != " " and win_predict(state, j + 3) and win_predict2(state, j + 3):
                    return j + 3
    for i in range(len(state) - 1, 2, -1):
        for j in range(len(state[0]) - 3):
            if state[i][j] == symbol and state[i - 1][j + 1] == " " and state[i - 2][j + 2] == symbol and state[i - 3][j + 3] == " ":
                if state[i][j + 1] != " " and win_predict(state, j + 1) and win_predict2(state, j + 1):
                    return j + 1
                if state[i - 2][j + 3] != " " and win_predict(state, j + 3) and win_predict2(state, j + 3):
                    return j + 3
            if state[i][j] == " " and state[i - 1][j + 1] == symbol and state[i - 2][j + 2] == " " and state[i - 3][j + 3] == symbol:
                if i + 1 < len(state) and state[i + 1][j] != " " and win_predict(state, j) and win_predict2(state, j):
                    return j
                if state[i - 1][j + 2] != " " and win_predict(state, j + 2) and win_predict2(state, j + 2):
                    return j + 2
            if state[i][j] == symbol and state[i - 1][j + 1] == " " and state[i - 2][j + 2] == " " and state[i - 3][j + 3] == symbol:
                if state[i][j + 1] != " " and win_predict(state, j + 1) and win_predict2(state, j + 1):
                    return j + 1
                if state[i - 1][j + 2] != " " and win_predict(state, j + 2) and win_predict2(state, j + 2):
                    return j + 2
            if state[i][j] == " " and state[i - 1][j + 1] == symbol and state[i - 2][j + 2] == symbol and state[i - 3][j + 3] == " ":
                if i + 1 < len(state) and state[i + 1][j] != " " and win_predict(state, j) and win_predict2(state, j):
                    return j
                if state[i - 2][j + 3] != " " and win_predict(state, j + 3) and win_predict2(state, j + 3):
                    return j + 3
    return None

"""
Moves for a bottom line only
"""
def bottom_line(state, symbol):
    i = len(state) - 1
    for j in range(len(state[0]) - 2):
        if state[i][j] == "X" and state[i][j + 1] == "X":
            if j - 1 >= 0 and state[i][j - 1] == " ":
                return j - 1
            if j + 2 < len(state[0]) and state[i][j + 2] == " ":
                return j + 2
    return None

"""
Looks for it's own mark, checks whether 3 spots around are empty
and if any of the spots under 3 empty spots is it's own mark,
places a mark
"""
def one_full_under(state, symbol, opponent):
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] == symbol:
                # first pos
                if j + 3 < len(state[0]) and state[i][j + 1] == " " and state[i][j + 2] == " " and state[i][j + 3] == " ":
                    if i == len(state) - 1 and win_predict(state, j + 1 and win_predict2(state, j + 1)):
                        return j + 1
                    if state[i + 1][j + 1] != " " and state[i + 1][j + 2] != " " and state[i + 1][j + 3] != " ":
                        if state[i + 1][j + 1] == symbol and win_predict(state, j + 1) and win_predict2(state, j + 1):
                            return j + 1
                        if state[i + 1][j + 2] == symbol and win_predict(state, j + 2) and win_predict2(state, j + 2):
                            return j + 2
                        if state[i + 1][j + 3] == symbol and win_predict(state, j + 3) and win_predict2(state, j + 3):
                            return j + 3
                # second pos
                if j - 1 >= 0 and j + 2 < len(state[0]) and state[i][j - 1] == " " and state[i][j + 1] == " " and state[i][j + 2] == " ":
                    if i == len(state) - 1 and win_predict(state, j + 1) and win_predict2(state, j + 1):
                        return j + 1
                    if state[i + 1][j - 1] != " " and state[i + 1][j + 1] != " " and state[i + 1][j + 2] != " ":
                        if state[i + 1][j - 1] == symbol and win_predict(state, j - 1) and win_predict2(state, j - 1):
                            return j - 1
                        if state[i + 1][j + 1] == symbol and win_predict(state, j + 1) and win_predict2(state, j + 1):
                            return j + 1
                        if state[i + 1][j + 2] == symbol and win_predict(state, j + 2) and win_predict2(state, j + 2):
                            return j + 2
                # third pos
                if j - 2 >= 0 and j + 1 < len(state[0]) and state[i][j - 2] == " " and state[i][j - 1] == " " and state[i][j + 1] == " ":
                    if i == len(state) - 1 and win_predict(state, j + 1) and win_predict2(state, j + 1):
                        return j - 1
                    if state[i + 1][j - 2] != " " and state[i + 1][j - 1] != " " and state[i + 1][j + 1] != " ":
                        if state[i + 1][j - 2] == symbol and win_predict(state, j - 2) and win_predict2(state, j - 2):
                            return j - 2
                        if state[i + 1][j - 1] == symbol and win_predict(state, j - 1) and win_predict2(state, j - 1):
                            return j - 1
                        if state[i + 1][j + 1] == symbol and win_predict(state, j + 1) and win_predict2(state, j + 1):
                            return j + 1
                # fourth pos
                if j - 3 >= 0 and state[i][j - 3] == " " and state[i][j - 2] == " " and state[i][j - 1] == " ":
                    if i == len(state) - 1 and win_predict(state, j + 1) and win_predict2(state, j + 1):
                        return j - 1
                    if state[i + 1][j - 3] != " " and state[i + 1][j - 2] != " " and state[i + 1][j - 1] != " ":
                        if state[i + 1][j - 3] == symbol and win_predict(state, j - 3) and win_predict2(state, j - 3):
                            return j - 3
                        if state[i + 1][j - 2] == symbol and win_predict(state, j - 2) and win_predict2(state, j - 2):
                            return j - 2
                        if state[i + 1][j - 1] == symbol and win_predict(state, j - 1) and win_predict2(state, j - 1):
                            return j - 1

"""
Looking for a fork possibilities
"""
def fork(state, symbol, opponent):
    fork_count = 1
    fork_pos = None
    for i in range(len(state) - 1):
        for j in range(len(state[0])):
            if state[i][j] == " " and (i == len(state) - 1 or state[i + 1][j] != " "):
                count = 0
                #two - right
                if j + 2 < len(state[0]) and state[i][j + 1] == symbol and state[i][j + 2] == symbol:
                    count += 1
                # two - bottom right diagonal
                if i + 2 < len(state) and j + 2 < len(state[0]) and state[i + 1][j + 1] == symbol and state[i + 2][j + 2] == symbol:
                    count += 1
                #two - under
                if i + 2 < len(state) and state[i + 1][j] == symbol and state[i + 2][j] == symbol:
                    count += 1
                # two - bottom left diagonal
                if i + 2 < len(state) and j - 2 >= 0 and state[i + 1][j - 1] == symbol and state[i + 2][j - 2] == symbol:
                    count += 1
                #two - left
                if j - 2 >= 0 and state[i][j - 1] == symbol and state[i][j - 2] == symbol:
                    count += 1
                # two - top left diagonal
                if i - 2 >= 0 and j - 2 >= 0 and state[i - 1][j - 1] == symbol and state[i - 2][j - 2] == symbol:
                    count += 1
                # two - top right diagonal
                if i - 2 >= 0 and j + 2 < len(state[0]) and state[i - 1][j + 1] == symbol and state[i - 2][j + 2] == symbol:
                    count += 1
                #one - left and right
                if j - 1 >= 0 and j + 1 < len(state[0]) and state[i][j - 1] == symbol and state[i][j + 1] == symbol:
                    count += 1

                # fork possible?
                if count > 1 and win_predict(state, j) and win_predict2(state, j):
                    if count > fork_count:
                        fork_count = count
                        fork_pos = j

                if fork_pos != None:
                    return fork_pos
    return None

"""
Checks for a 2-in-a-row on each other
"""
def top_2_in_a_row(state, symbol, opponent):
    for j in range(len(state[0])):
        for i in range(1, len(state) - 2):
            if state[i][j] == " " and state[i + 1][j] == symbol and state[i + 2][j] == symbol and win_predict(state, j) and win_predict2(state, j):
                return j
    return None

"""
Checks for a 2-in-a-row diagonally
"""
def diag_2_in_a_row(state, symbol, opponent):
    for i in range(len(state) - 1):
        for j in range(len(state[0]) - 1):
            if state[i][j] == symbol and state[i + 1][j + 1] == symbol:
                if j - 1 >= 0 and i - 1 >= 0 and state[i - 1][j - 1] == " " and state[i][j - 1] != " " and win_predict(state, j - 1) and win_predict2(state, j - 1):
                    return j - 1
                if j + 3 < len(state[0]) and i + 2 < len(state) and state[i + 2][j + 2] == " " and (i + 3 == len(state) or state[i + 3][j + 2] != " ")and win_predict(state, j + 3) and win_predict2(state, j + 3):
                    return j + 3
    for i in range(len(state) - 1, 1, -1):
        for j in range(len(state[0]) - 2):
            if state[i][j] == symbol and state[i - 1][j + 1] == symbol:
                if j - 1 >= 0 and i + 1 < len(state) and state[i + 1][j - 1] == " " and (i + 2 == len(state) or state[i + 2][j - 1] != " ") and win_predict(state, j - 1) and win_predict2(state, j - 1):
                    return j - 1
                if j + 2 < len(state[0]) and i - 2 >= 0 and state[i - 2][j + 2] == " " and state[i - 1][j + 2] != " " and win_predict(state, j + 2) and win_predict2(state, j + 2):
                    return j + 2
    return None

"""
Tries to create a 2-in-a-row
"""
def one_on_the_board(state, symbol, opponent):
    for j in range(len(state[0]) - 3):
        i = len(state) - 1
        if state[i][j] == symbol and state[i][j + 1] == " " and state[i][j + 2] == " " and state[i][j + 3] == " ":
            return j + 1
        if state[i][j] == " " and state[i][j + 1] == symbol and state[i][j + 2] == " " and state[i][j + 3] == " ":
            return j + 2
        if state[i][j] == " " and state[i][j + 1] == " " and state[i][j + 2] == symbol and state[i][j + 3] == " ":
            return j + 1
        if state[i][j] == " " and state[i][j + 1] == " " and state[i][j + 2] == " " and state[i][j + 3] == symbol:
            return j + 2
    for i in range(len(state) - 2, -1, -1):
        for j in range(len(state[0]) - 3):
            i = len(state) - 1
            if state[i][j] == " " and state[i][j + 1] == symbol and state[i][j + 2] == " " and state[i][j + 3] == " ":
                if state[i + 1][j + 2] != " ":
                    return j + 2
                if state[i + 1][j + 3] != " ":
                    return j + 3
                if state[i + 1][j] != " ":
                    return j
            if state[i][j] == " " and state[i][j + 1] == " " and state[i][j + 2] == symbol and state[i][j + 3] == " ":
                if state[i + 1][j + 1] != " ":
                    return j + 1
                if state[i + 1][j + 3] != " ":
                    return j + 3
                if state[i + 1][j] != " ":
                    return j
            if state[i][j] == symbol and state[i][j + 1] == " " and state[i][j + 2] == " " and state[i][j + 3] == " ":
                if state[i + 1][j + 1] != " ":
                    return j + 1
                if state[i + 1][j + 2] != " ":
                    return j + 2
                if state[i + 1][j + 3] != " ":
                    return j + 3
            if state[i][j] == " " and state[i][j + 1] == " " and state[i][j + 2] == " " and state[i][j + 3] == symbol:
                if state[i + 1][j + 2] != " ":
                    return j + 2
                if state[i + 1][j + 1] != " ":
                    return j + 1
                if state[i + 1][j] != " ":
                    return j
    return None

"""
First move
"""
def none_on_the_board(state):
    if (all(v == " " for v in state[len(state) - 1])):
        return len(state[0]) // 2
    if (all(v != "O" for v in state[len(state) - 1])):
        i = len(state) - 1
        for j in range(len(state[0]) - 2):
            if state[i][j] == "X":
                return j + 1
        return j
    return None

"""
If there isn't any better move, makes a move nearby it's own move
"""
def unplayable(state, symbol, opponent):
    for i in range(len(state) - 1, -1, -1):
        for j in range(len(state[0]) - 4):
            if state[i][j] == " " and state[i][j + 1] == " " and state[i][j + 2] == " " and state[i][j + 3] == " ":
                if i == len(state) - 1 and win_predict(state, j + 1) and win_predict2(state, j + 1):
                    return j + 1
                else:
                    if state[i + 1][j + 1] != " " and win_predict(state, j + 1) and win_predict2(state, j + 1):
                        return j + 1
                    if state[i + 1][j + 2] != " " and win_predict(state, j + 2) and win_predict2(state, j + 2):
                        return j + 2
                    if state[i + 1][j] != " " and win_predict(state, j) and win_predict2(state, j):
                        return j
                    if state[i + 1][j + 3] != " " and win_predict(state, j + 3) and win_predict2(state, j + 3):
                        return j + 3
        for j in range(len(state[0]) - 3):
            if state[i][j] == symbol and state[i][j + 1] == symbol and state[i][j + 2] == symbol:
                if state[i - 1][j] == " " and win_predict(state, j) and win_predict2(state, j):
                    return j
                if state[i - 1][j + 2] == " " and win_predict(state, j + 2) and win_predict2(state, j + 2):
                    return j + 2
                if state[i - 1][j + 1] == " " and win_predict(state, j + 1) and win_predict2(state, j + 1):
                    return j + 1
        for j in range(len(state[0]) - 1):
            if state[i][j] == symbol and state[i][j + 1] == symbol:
                if state[i - 1][j + 1] == " " and win_predict(state, j + 1) and win_predict2(state, j + 1):
                    return j + 1
                if state[i - 1][j] == " " and win_predict(state, j) and win_predict2(state, j):
                    return j
        for j in range(len(state[0])):
            if state[i][j] == symbol:
                if state[i - 1][j] == " " and win_predict(state, j) and win_predict2(state, j):
                    return j
        for j in range(len(state[0])):
            if state[i][j] == symbol:
                if j + 1 < len(state[0]) and state[i][j + 1] == " " and i + 1 < len(state) and state[i + 1][j + 1] != " " and win_predict(state, j + 1) and win_predict2(state, j + 1):
                    return j + 1
                if j - 1 >= 0 and state[i][j - 1] == " " and i + 1 < len(state) and state[i + 1][j - 1] != " " and win_predict(state, j - 1) and win_predict2(state, j - 1):
                    return j - 1
        for i in range(len(state) - 1, -1, -1):
            for j in range(len(state[0])):
                if state[i][j] == symbol:
                    if i - 1 >= 0 and j - 1 >= 0 and state[i - 1][j - 1] == " " and state[i][j - 1] != " " and win_predict(state, j - 1):
                        return j - 1
                    if i - 1 >= 0 and j + 1 < len(state[0]) and state[i - 1][j + 1] == " " and state[i][j + 1] != " " and win_predict(state, j + 1):
                        return j + 1
    return None

"""
Two functions, which check, whether the move wouldn't help
an opponent to win in very next 2 rounds.
--------------------------------------------------------------
Checks, if the move won't give an opponent fillable 3-in-a-row
"""
def win_predict(ar, move):
    test = []
    test = deepcopy(ar)
    test_move = move
    fill_plan(test, "O", test_move)
    move = three_in_a_row(test, "X")
    if move != None:
        return False
    move = three_in_a_row_2(test, "X")
    if move != None:
        return False
    return True

"""
In an test array does a move and checks if an opponent
doesn't have more than 1 way to win.
If he does, AI won't make the move.
"""
def win_predict2(ar, move):
    test = []
    test = deepcopy(ar)
    test_move = move
    fill_plan(test, "O", test_move)

    for j in range(len(test[0])):
        if move_check(j, test) != None:
            test2 = deepcopy(test)
            fill_plan(test2, "X", j)
            if win_predict2_counter(test2, "X") > 1:
                return False
    return True

"""
Counter for win_predict2
Counter for best_move_attack
Counter for best_move_defend
----------------------------
Counts how many ways would be an opponent able to win
after making a move.
If that count is more than 1, doesn't make the move.
"""
def win_predict2_counter(test, symbol):
    count = 0
    move_check = []
    for i in range(len(test) - 1, -1, -1):
        for j in range(len(test[0]) - 2):
            if test[i][j] == symbol and test[i][j + 1] == symbol and test[i][j + 2] == symbol:
                if (j - 1 >= 0 and test[i][j - 1] == " ") and (i + 1 == len(test) or test[i + 1][j - 1] != " ") and j - 1 not in move_check:
                    count += 1
                    move_check.append(j - 1)
                if (j + 3 < len(test[0]) and test[i][j + 3] == " ") and (i == len(test) - 1 or test[i + 1][j + 3] != " ") and j + 3 not in move_check:
                    count += 1
                    move_check.append(j + 3)
    # 3 in a row horizontally
    for j in range(len(test[0])):
        for i in range(len(test) - 3):
            if test[i][j] == " " and test[i + 1][j] == symbol and test[i + 2][j] == symbol and test[i + 3][j] == symbol and j not in move_check:
                count += 1
                move_check.append(j)
    # 3 in a row diagonally
    for i in range(len(test) - 2):
        for j in range(len(test[0]) - 2):
            if test[i][j] == symbol and test[i + 1][j + 1] == symbol and test[i + 2][j + 2] == symbol:
                if j - 1 >= 0 and i - 1 >= 0 and test[i - 1][j - 1] == " " and test[i][j - 1] != " " and j - 1 not in move_check:
                    count += 1
                    move_check.append(j - 1)
                if j + 3 < len(test[0]) and i + 3 < len(test) and test[i + 3][j + 3] == " " and (i + 4 == len(test) or test[i + 4][j + 3] != " ") and j + 3 not in move_check:
                    count += 1
                    move_check.append(j + 3)
    # 3 in a row diagonally 2
    for i in range(len(test) - 1, 1, -1):
        for j in range(len(test[0]) - 2):
            if test[i][j] == symbol and test[i - 1][j + 1] == symbol and test[i - 2][j + 2] == symbol:
                if j - 1 >= 0 and i + 1 < len(test) and test[i + 1][j - 1] == " " and (i + 2 == len(test) or test[i + 2][j - 1] != " ") and j - 1 not in move_check:
                    count += 1
                    move_check.append(j - 1)
                if j + 3 < len(test[0]) and i - 3 >= 0 and test[i - 3][j + 3] == " " and test[i - 2][j + 3] != " " and j + 3 not in move_check:
                    count += 1
                    move_check.append(j + 3)

    for i in range(len(test)):
        for j in range(len(test[0]) - 3):
            if test[i][j] == symbol and test[i][j + 1] == symbol and test[i][j + 2] == " " and test[i][j + 3] == symbol and (i == len(test) - 1 or test[i + 1][j + 2] != " ") and j + 2 not in move_check:
                count += 1
                move_check.append(j + 2)
            if test[i][j] == symbol and test[i][j + 1] == " " and test[i][j + 2] == symbol and test[i][j + 3] == symbol and (i == len(test) - 1 or test[i + 1][j + 1] != " ") and j + 2 not in move_check:
                count += 1
                move_check.append(j + 1)
    # 3 in a row 2 diagonally
    for i in range(len(test) - 3):
        for j in range(len(test[0]) - 3):
            if test[i][j] == symbol and test[i + 1][j + 1] == " " and test[i + 2][j + 2] == symbol and test[i + 3][j + 3] == symbol:
                if test[i + 2][j + 1] != " " and j + 1 not in move_check:
                    count += 1
                    move_check.append(j + 1)
            if test[i][j] == symbol and test[i + 1][j + 1] == symbol and test[i + 2][j + 2] == " " and test[i + 3][j + 3] == symbol:
                if test[i + 3][j + 2] != " " and j + 2 not in move_check:
                    count += 1
                    move_check.append(j + 2)

    # 3 in a row 2 diagonally 2
    for i in range(len(test) - 1, 2, -1):
        for j in range(len(test[0]) - 3):
            if test[i][j] == symbol and test[i - 1][j + 1] == " " and test[i - 2][j + 2] == symbol and test[i - 3][j + 3] == symbol:
                if test[i][j + 1] != " " and j + 1 not in move_check:
                    count += 1
                    move_check.append(j + 1)
            if test[i][j] == symbol and test[i - 1][j + 1] == symbol and test[i - 2][j + 2] == " " and test[i - 3][j + 3] == symbol:
                if test[i - 1][j + 2] != " " and j + 2 not in move_check:
                    count += 1
                    move_check.append(j + 2)
    return count

tictactoe(8,10)
