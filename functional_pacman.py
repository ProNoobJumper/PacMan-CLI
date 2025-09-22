import random
from termcolor import colored


def make_board():
    return [
        "|--------|",
        "|G..|..G.|",
        "|...PP...|",
        "|G....@|.|",
        "|...P..|.|",
        "|--------|"
    ]


def ui_elements():
    ui_wall = [
        "......",
        "......",
        "......",
        "......"
    ]

    ui_ghost = [
        " .-.  ",
        "| OO| ",
        "|   | ",
        "'^^^' "
    ]

    ui_hero = [
        " .--. ",
        "/ _.-'",
        "\\  '-.",
        " '--' "
    ]

    ui_empty = [
        "      ",
        "      ",
        "      ",
        "      "
    ]

    ui_pill = [
        "      ",
        " .-.  ",
        " '-'  ",
        "      "
    ]

    return ui_wall, ui_ghost, ui_hero, ui_empty, ui_pill


def find_coords(board, target):
    coords = []
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == target:
                coords.append((x, y))
    return coords


def render_board(board, ui_wall, ui_ghost, ui_hero, ui_empty, ui_pill,
                 wall_color, ghost_color, pacman_color, pill_color,
                 final_color=None):
    for row in board:
        for piece in range(4):
            for point in row:
                # If a final_color is provided, override element colors for end-state
                ghost_c = final_color if final_color is not None else ghost_color
                wall_c = final_color if final_color is not None else wall_color
                pacman_c = final_color if final_color is not None else pacman_color
                pill_c = final_color if final_color is not None else pill_color

                if point == 'G':
                    print(colored(ui_ghost[piece], ghost_c), end='')
                elif point == '|' or point == '-':
                    print(colored(ui_wall[piece], wall_c), end='')
                elif point == '@':
                    print(colored(ui_hero[piece], pacman_c), end='')
                elif point == '.':
                    print(ui_empty[piece], end='')
                elif point == 'P':
                    print(colored(ui_pill[piece], pill_c), end='')

            print("", end='\n')


def in_bounds(x, y, board):
    return 0 <= x < len(board) and 0 <= y < len(board[0])


def move_ghosts(board, pill_coords):
    all_ghosts = find_coords(board, 'G')
    for (old_ghost_x, old_ghost_y) in all_ghosts:
        possible_directions = [
            (old_ghost_x, old_ghost_y + 1),
            (old_ghost_x + 1, old_ghost_y),
            (old_ghost_x, old_ghost_y - 1),
            (old_ghost_x - 1, old_ghost_y),
        ]
        next_ghost_x, next_ghost_y = random.choice(possible_directions)
        if not in_bounds(next_ghost_x, next_ghost_y, board):
            continue
        target_char = board[next_ghost_x][next_ghost_y]
        is_wall = target_char == '|' or target_char == '-'
        is_ghost = target_char == 'G'
        is_pacman = target_char == '@'

        if not is_wall and not is_ghost:
            if is_pacman:
                return True  # pacman caught
            # restore underlying pill or dot
            if (old_ghost_x, old_ghost_y) in pill_coords:
                board[old_ghost_x] = board[old_ghost_x][:old_ghost_y] + 'P' + board[old_ghost_x][old_ghost_y+1:]
            else:
                board[old_ghost_x] = board[old_ghost_x][:old_ghost_y] + '.' + board[old_ghost_x][old_ghost_y+1:]
            # place ghost
            board[next_ghost_x] = board[next_ghost_x][:next_ghost_y] + 'G' + board[next_ghost_x][next_ghost_y+1:]
    return False


def get_pacman_coords(board):
    coords = find_coords(board, '@')
    return coords[0] if coords else (-1, -1)


def apply_pacman_move(board, pill_coords, key):
    pacman_x, pacman_y = get_pacman_coords(board)
    next_pacman_x, next_pacman_y = pacman_x, pacman_y
    if key == 'a':
        next_pacman_y -= 1
    elif key == 's':
        next_pacman_x += 1
    elif key == 'w':
        next_pacman_x -= 1
    elif key == 'd':
        next_pacman_y += 1

    if not in_bounds(next_pacman_x, next_pacman_y, board):
        return False, False  # invalid move, not caught
    if board[next_pacman_x][next_pacman_y] in ('|', '-'):
        return False, False
    if board[next_pacman_x][next_pacman_y] == 'G':
        return True, False

    # leave behind a dot
    board[pacman_x] = board[pacman_x][:pacman_y] + '.' + board[pacman_x][pacman_y+1:]
    # eat pill if present
    if board[next_pacman_x][next_pacman_y] == 'P':
        pill_coords.discard((next_pacman_x, next_pacman_y))
    board[next_pacman_x] = board[next_pacman_x][:next_pacman_y] + '@' + board[next_pacman_x][next_pacman_y+1:]
    return False, False


def game_loop():
    board = make_board()
    ui_wall, ui_ghost, ui_hero, ui_empty, ui_pill = ui_elements()
    wall_color = 'blue'
    ghost_color = 'red'
    pacman_color = 'yellow'
    pill_color = 'grey'

    pill_coords = set(find_coords(board, 'P'))

    game_finished = False
    win = False

    while not game_finished:
        render_board(board, ui_wall, ui_ghost, ui_hero, ui_empty, ui_pill,
                     wall_color, ghost_color, pacman_color, pill_color)

        # move ghosts
        caught = move_ghosts(board, pill_coords)
        if caught:
            game_finished = True
            win = False
            break

        # pacman input
        while True:
            try:
                key = input("Please input only the input controls: w a s d -> ")
            except Exception:
                print("[input error] please enter one of: w a s d")
                continue
            key = key.lower()
            if key and len(key) == 1 and key in ('a', 's', 'w', 'd'):
                break
            print("Invalid input. Please press only: w a s d")

        caught, _ = apply_pacman_move(board, pill_coords, key)
        if caught:
            game_finished = True
            win = False
            break

        total_pills = len(pill_coords)
        if total_pills == 0:
            win = True
            game_finished = True
            break

    final_board_color = 'green' if win else 'red'
    render_board(board, ui_wall, ui_ghost, ui_hero, ui_empty, ui_pill,
                 wall_color, ghost_color, pacman_color, pill_color,
                 final_color=final_board_color)

    if win:
        print("You win! :)")
    else:
        print("You lost! :/")


if __name__ == '__main__':
    game_loop()
