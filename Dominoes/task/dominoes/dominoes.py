# Write your code here
import random


def shuffle():
    global stock, player, computer, dominoes_list
    dominoes = dominoes_list[:]
    for _ in range(14):
        choice = dominoes.pop(random.randrange(len(dominoes)))
        stock.append(choice)
    for _ in range(7):
        choice = dominoes.pop(random.randrange(len(dominoes)))
        player.append(choice)
    for _ in range(7):
        choice = dominoes.pop(random.randrange(len(dominoes)))
        computer.append(choice)


def find_max_double(dominoes):
    doubles = (dom[0] for dom in dominoes if dom[0] == dom[1])
    return max(doubles) if doubles != [] else -1


def print_field():
    output = ""
    if len(snake) > 6:
        for domino in snake[:3]:
            output += str(domino)
        output += "..."
        for domino in snake[-3:]:
            output += str(domino)
    else:
        for domino in snake:
            output += str(domino)
    print(output)


def computer_move():
    global stock, computer, snake
    ratings = []
    for index in range(len(computer)):
        first = str(computer[index][0])
        second = str(computer[index][1])
        ratings.append([index, str(snake).count(first) + str(snake).count(second)
                        + str(computer).count(first) + str(computer).count(second)])
    ratings = sorted(ratings, key=lambda tup: tup[1], reverse=True)

    for _ in range(len(ratings)):
        index = ratings[_][0]
        if check_move(computer[index], "left"):
            place_domino(computer.pop(index), "left")
            return True
        if check_move(computer[index], "right"):
            place_domino(computer.pop(index), "right")
            return True
    if len(stock) > 0:
        computer.append(stock.pop(random.randrange(len(stock))))
        return True
    return False


def player_move(move_):
    global stock, player, snake
    if not move_.lstrip("-").isdigit():
        print("Invalid input. Please try again.")
        return False
    move_ = int(move_)
    if move_ == 0:
        if len(stock) > 0:
            player.append(stock.pop(random.randrange(len(stock))))
            return True
        else:
            print("No more dominoes")
            return False
    if abs(move_) not in range(1, len(player) + 1):
        print("Invalid input. Please try again.")
        return False
    if move_ < 0:
        if check_move(player[abs(move_) - 1], "left"):
            # snake.insert(0, player.pop(abs(move_) - 1))
            place_domino(player.pop(abs(move_) - 1), "left")
            return True
    else:
        if check_move(player[abs(move_) - 1], "right"):
            # snake.append(player.pop(abs(move_) - 1))
            place_domino(player.pop(abs(move_) - 1), "right")
            return True
    print("Illegal move. Please try again")
    return False


def check_move(domino, side):
    global snake
    if side == "left":
        if snake[0][0] == domino[0] or snake[0][0] == domino[1]:
            return True
    if side == "right":
        if snake[-1][1] == domino[0] or snake[-1][1] == domino[1]:
            return True
    return False


def place_domino(domino, side):
    global snake
    if side == "left":
        if snake[0][0] == domino[1]:
            snake.insert(0, domino)
        else:
            snake.insert(0, domino[::-1])
    if side == "right":
        if snake[-1][1] == domino[0]:
            snake.append(domino)
        else:
            snake.append(domino[::-1])


random.seed(100504)
dominoes_list = [[0, 0], [0, 1], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6],
                 [0, 2], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6],
                 [0, 3], [3, 3], [3, 4], [3, 5], [3, 6],
                 [0, 4], [4, 4], [4, 5], [4, 6],
                 [0, 5], [5, 5], [5, 6],
                 [0, 6], [6, 6]]

stock = []
player = []
computer = []
status = ""
snake = []
shuffle()
player_max = find_max_double(player)
computer_max = find_max_double(computer)

if player_max == -1 and computer_max == -1:
    shuffle()
else:
    if player_max > computer_max:
        player.remove([player_max, player_max])
        status = "computer"
        snake.append([player_max, player_max])
    else:
        computer.remove([computer_max, computer_max])
        status = "player"
        snake.append([computer_max, computer_max])

while True:
    print("=" * 70)
    print("Stock size: {}".format(len(stock)))
    print("Computer pieces: {}".format(len(computer)))
    print()
    print_field()

    print()

    if len(player) == 0:
        print("Status: The game is over. You won!")
        break
    if len(computer) == 0:
        print("Status: The game is over. The computer won!")
        break
    if len(stock) == 0:
        "Status: The game is over. It's a draw!"
        break

    print("Your pieces:")

    for dom in range(len(player)):
        print("{}:{}".format(dom + 1, player[dom]))

    print()
    print("Status: It's your turn to make a move. Enter your command." if status == "player"
          else "Status: Computer is about to make a move. Press Enter to continue...")
    move = input()
    if status == "player":
        if not player_move(move):
            continue
    else:
        computer_move()
    status = "player" if status == "computer" else "computer"
