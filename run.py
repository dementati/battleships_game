import random
# Define ship lengths
SHIP_LENGTHS = {'Battleship': 4, 'Cruiser': 3, 'Destroyer': 2}
SHIP_ICONS = {'Battleship': 'B', 'Cruiser': 'C', 'Destroyer': 'D'}
EMPTY = '.'


def set_grid_size():
    """Ask the user to enter the grid size and return the grid size."""
    while True:
        try:
            grid_size = int(input(
                "Enter the grid size (between 4 and 10, "
                "e.g., 8 for an 8x8 grid): "
            ))
            if 4 <= grid_size <= 10:
                return grid_size
            else:
                print(
                    "Invalid grid size. Please enter a number between 4"
                    " and 10."
                )
        except ValueError:
            print("Invalid input. Please enter a number.")


def print_grid(grid):
    """Print the grid."""
    for row in grid:
        print(
            " ".join([SHIP_ICONS[x] if x in SHIP_ICONS else '.' for x in row])
        )
    print()


def get_computer_ships(computer_grid):
    """Randomize the computer ships coordinates."""
    computer_ships = {'Battleship': [], 'Cruiser': [], 'Destroyer': []}
    for ship in computer_ships:
        while True:
            try:
                print(f"Placing {ship}...")
                x, y, orientation = input(
                    "Enter the starting coordinates and"
                    f" orientation for your {ship} (e.g."
                    " A1 H for horizontal, "
                    "A1 V for vertical): "
                ).split()
                x = ord(x.upper()) - 65
                y = int(y) - 1
                if orientation.upper() == "H":
                    for i in range(SHIP_LENGTHS[ship]):
                        if computer_grid[x+i][y] != EMPTY:
                            raise ValueError
                    for i in range(SHIP_LENGTHS[ship]):
                        computer_grid[x+i][y] = ship
                        computer_ships[ship].append((x+i, y))
                elif orientation.upper() == "V":
                    for i in range(SHIP_LENGTHS[ship]):
                        if computer_grid[x][y+i] != EMPTY:
                            raise ValueError
                    for i in range(SHIP_LENGTHS[ship]):
                        computer_grid[x][y+i] = ship
                        computer_ships[ship].append((x, y+i))
                else:
                    raise ValueError
                break
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")
    return computer_ships


def get_player_ships(player_grid):
    """Ask the user to place their ships and return the player ships."""
    player_ships = {'Battleship': [], 'Cruiser': [], 'Destroyer': []}
    for ship in player_ships:
        while True:
            try:
                print(f"Placing {ship}...")
                x, y, orientation = input(
                    "Enter the starting coordinates and"
                    f" orientation for your {ship} (e.g."
                    " A1 H for horizontal, "
                    "A1 V for vertical): "
                ).split()
                x = ord(x.upper()) - 65
                y = int(y) - 1
                if orientation.upper() == "H":
                    for i in range(SHIP_LENGTHS[ship]):
                        if player_grid[x+i][y] != EMPTY:
                            raise ValueError
                    for i in range(SHIP_LENGTHS[ship]):
                        player_grid[x+i][y] = ship
                        player_ships[ship].append((x+i, y))
                elif orientation.upper() == "V":
                    for i in range(SHIP_LENGTHS[ship]):
                        if player_grid[x][y+i] != EMPTY:
                            raise ValueError
                    for i in range(SHIP_LENGTHS[ship]):
                        player_grid[x][y+i] = ship
                        player_ships[ship].append((x, y+i))
                else:
                    raise ValueError
                break
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")
    return player_ships


def place_ships(grid, ships):
    """
    Places the ships on the board using the coordinates and orientation
    given by the user or the computer.
    """
    for ship in ships:  # Iterate through the ships
        x, y, orientation = ship  # Unpack the ship tuple
        if orientation == 'horizontal':
            for i in range(SHIP_LENGTHS[ship]):
                grid[y][x + i] = SHIP_ICONS[ship]
        elif orientation == 'vertical':
            for i in range(SHIP_LENGTHS[ship]):
                grid[y + i][x] = SHIP_ICONS[ship]
        else:
            print(f"Invalid ship orientation: {orientation}")
    return grid


# Function for the player's turn
def player_turn(player_grid):
    while True:
        try:
            x = int(input("Enter row (0-7): "))
            y = int(input("Enter column (0-7): "))

            if is_valid_coordinate(x, y, len(player_grid)):  # Check if valid
                return x, y
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please enter numbers.")


# Function to check if a coordinate is on the grid
def is_valid_coordinate(x, y, grid_size):
    return 0 <= x < grid_size and 0 <= y < grid_size


def check_if_hit(x, y, computer_ships, player_grid):
    """Check if a ship has been hit."""
    for ship in computer_ships:
        if (x, y) in computer_ships[ship]:
            print("Hit!")
            player_grid[x][y] = 'X'
            break
    else:
        print("Miss!")
        player_grid[x][y] = 'O'


def check_if_sunk(computer_ships, player_grid):
    """Check if a ship has been sunk."""
    for ship in computer_ships:
        if all(player_grid[x][y] == 'X' for x, y in computer_ships[ship]):
            print(f"You sunk the computer's {ship}!")
            break


def check_if_game_over(player_grid):
    """Check if the game is over."""
    return all(all(cell == 'X' for cell in row) for row in player_grid)


def computer_turn(grid_size, computer_grid):
    """The computer's turn."""
    while True:
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)
        if computer_grid[x][y] == ' ':
            break
    return x, y


def main():
    print("Welcome to Battleships!")

    # Prompt the user to set the grid size
    grid_size = set_grid_size()

    # Initialize the game grid with the chosen size
    player_grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    computer_grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]

    player_ships = get_player_ships(player_grid)
    computer_ships = get_computer_ships(computer_grid)

    while True:
        print("Your Grid:")
        print_grid(player_grid)

        # Player's turn
        print("Your Turn:")
        player_x, player_y = player_turn(player_grid)  # Pass player_grid
        check_if_hit(player_x, player_y, computer_ships, player_grid)
        check_if_sunk(computer_ships, player_grid)
        if check_if_game_over(player_grid):
            print("Congratulations! You won!")
            break

        # Computer's turn
        print("Computer's Turn:")
        computer_x, computer_y = computer_turn(grid_size, computer_grid)
        check_if_hit(computer_x, computer_y, player_ships, computer_grid)
        check_if_sunk(player_ships, computer_grid)
        if check_if_game_over(computer_grid):
            print("Sorry, you lost. The computer won.")
            break

        print("Computer's Grid:")
        print_grid(computer_grid)

    restart = input("Do you want to play again? (Y/N): ")
    if restart.upper() == 'Y':
        main()
    elif restart.upper() == 'N':
        print("Thanks for playing!")
    else:
        print("Invalid input. Exiting the game.")


main()
