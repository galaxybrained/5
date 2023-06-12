import random
import os
import time

# Game constants
WIDTH = 20
HEIGHT = 10
SNAKE_HEAD = 'O'
SNAKE_BODY = '*'
FOOD = '@'
UP = 'w'
DOWN = 's'
LEFT = 'a'
RIGHT = 'd'

# Initialize the game state
snake = [(4, 4), (4, 3), (4, 2)]
direction = RIGHT
food = (random.randint(1, WIDTH), random.randint(1, HEIGHT))

# Function to draw the game board
def draw_board():
    os.system('clear')
    print(' ' + '-' * WIDTH)
    for y in range(HEIGHT):
        line = '|'
        for x in range(WIDTH):
            if (x, y) == snake[0]:
                line += SNAKE_HEAD
            elif (x, y) in snake[1:]:
                line += SNAKE_BODY
            elif (x, y) == food:
                line += FOOD
            else:
                line += ' '
        line += '|'
        print(line)
    print(' ' + '-' * WIDTH)

# Function to move the snake
def move_snake():
    global direction
    head = snake[0]
    x, y = head
    if direction == UP:
        y -= 1
    elif direction == DOWN:
        y += 1
    elif direction == LEFT:
        x -= 1
    elif direction == RIGHT:
        x += 1
    snake.insert(0, (x, y))

# Function to check for collisions
def check_collisions():
    head = snake[0]
    x, y = head
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True
    if head in snake[1:]:
        return True
    return False

# Main game loop
while True:
    draw_board()

    # Get user input
    new_direction = ''
    while new_direction not in [UP, DOWN, LEFT, RIGHT]:
        new_direction = input('Enter direction (w/a/s/d): ')
    if (new_direction == UP and direction != DOWN) or \
       (new_direction == DOWN and direction != UP) or \
       (new_direction == LEFT and direction != RIGHT) or \
       (new_direction == RIGHT and direction != LEFT):
        direction = new_direction

    # Move the snake
    move_snake()

    # Check for collisions
    if check_collisions():
        print('Game over!')
        break

    # Check if snake ate the food
    if snake[0] == food:
        food = (random.randint(1, WIDTH), random.randint(1, HEIGHT))
    else:
        snake.pop()

    time.sleep(0.2)  # Adjust game speed here

