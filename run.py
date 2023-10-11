import random
# Define ship lengths
SHIP_LENGTHS = {'Battleship': 4, 'Cruiser': 3, 'Destroyer': 2}

def set_grid_size(): 
    """Ask the user to enter the grid size and return the grid size."""
    while True:
        try:
            grid_size = int(input("Enter the grid size ( choose a number between 4 and 10, e.g., 8 for an 8x8 grid): "))
            if grid_size >= 4 and grid_size <= 10:
                return grid_size
            else:
                print("Invalid grid size. Please enter a number between 4 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def print_grid(grid):
    """Print the grid."""
    for row in grid:
        print(" ".join(row))
    print()

def place_computer_ships():
    computer_ships = {'Battleship': [], 'Cruiser': [], 'Destroyer': []}
    for ship in computer_ships:
        while True:
            try:
                print(f"Placing {ship}...")
                x = random.randint(0, grid_size - 1)
                y = random.randint(0, grid_size - 1)
                orientation = random.choice(['horizontal', 'vertical'])
                if orientation == 'horizontal':
                    if x + ship_lengths[ship] - 1 < grid_size:
                        for i in range(ship_lengths[ship]):
                            if computer_grid[x + i][y] == ' ':
                                computer_grid[x + i][y] = ship[0]
                                computer_ships[ship].append((x + i, y))
                            else:
                                raise ValueError
                    else:
                        raise ValueError
                else:
                    if y + ship_lengths[ship] - 1 < grid_size:
                        for i in range(ship_lengths[ship]):
                            if computer_grid[x][y + i] == ' ':
                                computer_grid[x][y + i] = ship[0]
                                computer_ships[ship].append((x, y + i))
                            else:
                                raise ValueError
                    else:
                        raise ValueError
            except ValueError:
                continue
            else:
                break
    return computer_ships


def place_player_ships():
    """
    Allows the player to place their ships on the game board.
    """
    for ship in SHIP_LENGTHS:
        print(f"Placing {ship}...")
        while True:
            try:
                x, y, orientation = input(f"Enter the starting coordinates and orientation for your {ship} (e.g., A1 H for horizontal, A1 V for vertical): ").split()
                x = ord(x.upper()) - 65
                y = int(y) - 1
                if orientation.upper() == "H":
                    for i in range(SHIP_LENGTHS[ship]):
                        if board[x+i][y] != EMPTY:
                            raise ValueError
                    for i in range(SHIP_LENGTHS[ship]):
                        board[x+i][y] = SHIP
                elif orientation.upper() == "V":
                    for i in range(SHIP_LENGTHS[ship]):
                        if board[x][y+i] != EMPTY:
                            raise ValueError
                    for i in range(SHIP_LENGTHS[ship]):
                        board[x][y+i] = SHIP
                else:
                    raise ValueError
                break
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")
    return board

# Function for the player's turn
def player_turn():
    while True:
        try:
            x = int(input("Enter row (0-7): "))
            y = int(input("Enter column (0-7): "))

            if is_valid_coordinate(x, y) and player_grid[x][y] == ' ':
                return x, y
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please enter numbers.")
    
# Function to check if a coordinate is on the grid
def is_valid_coordinate(x, y):
    return 0 <= x < grid_size and 0 <= y < grid_size

def check_if_hit():
    """Check if a ship has been hit."""
    for ship in computer_ships:
        if (x, y) in computer_ships[ship]:
            print("Hit!")
            player_grid[x][y] = 'X'
            break
    else:
        print("Miss!")
        player_grid[x][y] = 'O'

def check_if_sunk():
    """Check if a ship has been sunk."""
    for ship in computer_ships:
        if all(player_grid[x][y] == 'X' for x, y in computer_ships[ship]):
            print(f"You sunk the computer's {ship}!")
            break

def check_if_game_over():
    """Check if the game is over."""
    return all(all(cell == 'X' for cell in row) for row in player_grid)

def computer_turn():
    """The computer's turn."""
    while True:
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)
        if computer_grid[x][y] == ' ':
            break
    return x, y

def restart_game():
    """Ask the user if they want to play again."""
    while True:
        try:
            restart = input("Do you want to play again? (Y/N): ")
            if restart.upper() == 'Y':
                main()
            elif restart.upper() == 'N':
                print("Thanks for playing!")
                break
            else:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter Y or N.")

def main():
    print("Welcome to Battleships!")

    # Prompt the user to set the grid size
    grid_size = set_grid_size()

    # Initialize the game grid with the chosen size
    player_grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    computer_grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]

    player_ships = place_player_ships()
    computer_ships = place_computer_ships()

    while True:
        print("Your Grid:")
        print_grid(player_grid)

        # Player's turn
        player_x, player_y = player_turn()
        check_if_hit(player_x, player_y, computer_ships, player_grid)
        check_if_sunk(player_grid, computer_ships)
        if check_if_game_over(player_grid, computer_ships):
            break

        # Computer's turn
        computer_x, computer_y = computer_turn(grid_size, computer_grid)
        check_if_hit(computer_x, computer_y, player_ships, computer_grid)
        check_if_sunk(computer_grid, player_ships)
        if check_if_game_over(computer_grid, player_ships):
            break

        print("Computer's Grid:")
        print_grid(computer_grid)

    restart_game()