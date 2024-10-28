import pygame
import math

# Define the board
board = [ [" ", " ", " "], [" ", " ", " "], [" ", " ", " "] ]

# Define the players
player1 = "X"
player2 = "O"

# Define the current player
current_player = player1

# Define the game state
game_over = False

# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the font
font = pygame.font.Font(None, 100)

# create the game window
window = pygame.display.set_mode((600, 600))

# load and display the image on the screen and update the display of pygame
background_image = pygame.image.load('grid.png')
window.blit(background_image, (0, 0))
pygame.display.update()

# Define the check_winner function
def check_winner():
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return row[0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[2][0] == board[1][1] == board[0][2] and board[2][0] != " ":
        return board[2][0]

    # Check for tie
    open_spots = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                open_spots += 1

    if open_spots == 0:
        return "It's a Tie!"
    else:
        return None

# Define the minimax function
def minimax(board, depth, is_maximizing):
    # Check if the game is over
    result = check_winner()
    if result != None:
        if result == player1:
            return -1
        elif result == player2:
            return 1
        else:
            return 0

    # Check if it's the maximizing player's turn
    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = player2
                    score = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = player1
                    score = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score

# Define the make_move function
def make_move():
    global current_player, game_over

    # Check if it's the human player's turn
    if current_player == player1:
        print("Player 1's turn")
        move_made = False
        while not move_made:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the position of the mouse click
                    x, y = pygame.mouse.get_pos()

                    # Determine the row and column of the clicked cell
                    row = y // 200
                    col = x // 200

                    # Check if the clicked cell is empty
                    if board[row][col] == " ":
                        # Update the board and switch to the other player
                        board[row][col] = current_player
                        current_player = player2
                        move_made = True

                        # Check if the game is over
                        result = check_winner()
                        if result != None:
                            print(result)
                            game_over = True
                            return
    else:
        print("Computer's turn")
        best_score = -math.inf
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = player2
                    score = minimax(board, 0, False)
                    board[i][j] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        board[best_move[0]][best_move[1]] = current_player
        current_player = player1

        # Check if the game is over
        result = check_winner()
        if result != None:
            print(result)
            game_over = True
            return

# Set the window caption and icon
pygame.display.set_caption("Tic Tac Toe")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Run the game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Make a move
    make_move()

    # Draw the board
    screen.fill((255, 255, 255))
    cell_size = screen_width // 3
    for i in range(3):
        for j in range(3):
            # Draw the X or O for the current cell
            cell_center_x = j * cell_size + cell_size // 2
            cell_center_y = i * cell_size + cell_size // 2
            cell_contents = font.render(board[i][j], True, (0, 0, 0))
            cell_contents_rect = cell_contents.get_rect(center=(cell_center_x, cell_center_y))
            screen.blit(cell_contents, cell_contents_rect)

            # Draw the grid lines for the current cell
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size), 1)

    # Update the screen
    pygame.display.flip()

