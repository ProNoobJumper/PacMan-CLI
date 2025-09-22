import random
from termcolor import colored

# . -> empty space (ghosts and pacman can walk)
# | and - -> wall, no one can go through it
# @ -> our hero: Pacman
# G -> ghosts, they are the bad folks
# P -> pills. Pacman needs to eat them
board = [
    "|--------|",
    "|G..|..G.|",
    "|...PP...|",
    "|G....@|.|",
    "|...P..|.|",
    "|--------|"
]

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
# UI Elements are defined as lists

wall_color = "blue"
ghost_color = "red"
pacman_color = "yellow"
pill_color = "grey"

# UI Elements colours are defined using termcolour from coloured library

game_finished = False
win = False
# Store initial pill coordinates once and treat as persistent across frames
pill_coords = set()
for x in range(len(board)):
    for y in range(len(board[x])):
        if board[x][y] == 'P':
            pill_coords.add((x, y))
while not game_finished:
    for row in board:
        for piece in range(4):
            for point in row:
                if point == 'G':
                    print(colored(ui_ghost[piece], ghost_color), end='')
                elif point == '|' or point == '-':
                    print(colored(ui_wall[piece], wall_color), end='')
                elif point == '@':
                    print(colored(ui_hero[piece], pacman_color), end='')
                elif point == '.':
                    print(ui_empty[piece], end='')
                elif point == 'P':
                    print(colored(ui_pill[piece], pill_color), end='')

            print("", end='\n')
 
# Gamestate while running

    # Build list of ghost coordinates (pill_coords is persistent)
    all_ghosts = []
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == 'G':
                all_ghosts.append([x, y])
    # Ghosts startstate
    for ghost in all_ghosts:
        old_ghost_x = ghost[0]
        old_ghost_y = ghost[1]
    # Change of Ghost State from future to current
        possible_directions = [
            [old_ghost_x, old_ghost_y + 1],  
            [old_ghost_x + 1, old_ghost_y],  
            [old_ghost_x, old_ghost_y - 1],  
            [old_ghost_x - 1, old_ghost_y]
        ]
        # Potential Movement Logic Ghost 
        # choose one of four directions
        next_ghost_x, next_ghost_y = random.choice(possible_directions)
        # Random Movement Logic Ghost 
        y_is_valid = next_ghost_y >= 0 and next_ghost_y < len(board[0])
        x_is_valid = next_ghost_x >= 0 and next_ghost_x < len(board)
        
        if not (y_is_valid and x_is_valid):
            continue
        target_char = board[next_ghost_x][next_ghost_y]
        is_wall = target_char == '|' or target_char == '-'
        is_ghost = target_char == 'G'
        is_pill = target_char == 'P'
        is_pacman = target_char == '@'

        if not is_wall and not is_ghost:
            if is_pacman:
                game_finished = True
            else:
                # When ghost leaves its old tile, restore a pill if it was originally under the ghost
                # (we consider pill_coords as the authoritative set of pill locations)
                if (old_ghost_x, old_ghost_y) in pill_coords:
                    board[old_ghost_x] = board[old_ghost_x][0:old_ghost_y] + "P" + board[old_ghost_x][old_ghost_y + 1:]
                else:
                    board[old_ghost_x] = board[old_ghost_x][0:old_ghost_y] + "." + board[old_ghost_x][old_ghost_y + 1:]

                # Move ghost onto new tile. If it moves over a pill, keep the ghost there but don't remove the pill from pill_coords
                board[next_ghost_x] = board[next_ghost_x][0:next_ghost_y] + "G" + board[next_ghost_x][next_ghost_y + 1:]
        # Movement Error Check


    if game_finished:
        break
    pacman_x = -1
    pacman_y = -1
    # Pacman Game Endstate
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == '@':
                pacman_x = x
                pacman_y = y
    # Pacman Spawn State Location
    next_pacman_x = pacman_x
    next_pacman_y = pacman_y
    # Change of Pacman State from future to current
    
    
    # Read input and block until a valid movement key is entered
    while True:
        try:
            key = input("Please input only the input controls: w a s d -> ")
        except Exception:
            # On input error, just prompt again
            print("[input error] please enter one of: w a s d")
            continue

        # Normalise to lowercase so uppercase WASD are accepted
        key = key.lower()

        if key and len(key) == 1 and key in ('a', 's', 'w', 'd'):
            break
        # Invalid input and instruct the user and continue prompting
        print("Invalid input. Please press only: w a s d")

    if key == 'a':
        next_pacman_y -= 1
    elif key == 's':
        next_pacman_x += 1
    elif key == 'w':
        next_pacman_x -= 1
    elif key == 'd':
        next_pacman_y += 1
    # Movement Controls
    y_is_valid = next_pacman_y >= 0 and next_pacman_y < len(board[0])
    x_is_valid = next_pacman_x >= 0 and next_pacman_x < len(board)
    if not (x_is_valid and y_is_valid):
        continue
    # Pacman unbostructed interaction
    is_wall = board[next_pacman_x][next_pacman_y] == '|' or board[next_pacman_x][next_pacman_y] == '-'
    if is_wall:
        continue
    # Pacman and wall interaction
    is_ghost = board[next_pacman_x][next_pacman_y] == 'G'
    if is_ghost:
        game_finished = True
        win = False
    # Ghost and Pacman interaction

    # If Pacman moves off a pill, ensure we correctly update the pill set
    if (pacman_x, pacman_y) in pill_coords:
        # Pacman was standing on a pill (shouldn't normally happen), put a dot behind
        board[pacman_x] = board[pacman_x][0:pacman_y] + "." + board[pacman_x][pacman_y+1:]
    else:
        board[pacman_x] = board[pacman_x][0:pacman_y] + "." + board[pacman_x][pacman_y+1:]

    # If Pacman moves onto a pill, remove it from the pill set so counting is accurate
    if board[next_pacman_x][next_pacman_y] == 'P':
        pill_coords.discard((next_pacman_x, next_pacman_y))

    board[next_pacman_x] = board[next_pacman_x][0:next_pacman_y] + "@" + board[next_pacman_x][next_pacman_y + 1:]

# Pacman (user) movement, collision and powerup logic

    # Recompute total pills from pill_coords
    total_pills = len(pill_coords)

    if total_pills == 0:
        win = True
        game_finished = True
        break

# Powerup spawning logic

final_board_color = "green" if win else "red"

for row in board:
    for piece in range(4):
        for point in row:
            if point == 'G':
                print(colored(ui_ghost[piece], final_board_color), end='')
            elif point == '|' or point == '-':
                print(colored(ui_wall[piece], final_board_color), end='')
            elif point == '@':
                print(colored(ui_hero[piece], final_board_color), end='')
            elif point == '.':
                print(colored(ui_empty[piece], final_board_color), end='')
            elif point == 'P':
                print(colored(ui_pill[piece], final_board_color), end='')

        print("", end='\n')

# Final Board colour endstate

if win:
    print("You win! :)")
else:
    print("You lost! :/")

# Win/Loss Display Message