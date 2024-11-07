import pygame
import random
import sqlite3
import os
import traceback

try:
    # Set the video driver for Windows
    os.environ["SDL_VIDEODRIVER"] = "windib"  # Use windib for Windows instead of directx
    print("Starting the Snake Game...")

    pygame.init()

    # Check if pygame initialized correctly
    if pygame.get_init():
        print("Pygame initialized successfully.")
    else:
        print("Pygame failed to initialize.")

    # Colors
    white = (255, 255, 255)
    yellow = (255, 255, 102)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (50, 153, 213)

    # Display settings
    dis_width = 600
    dis_height = 400
    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('Snake Game')

    # Snake settings
    snake_block = 10
    snake_speed = 15

    # Fonts
    font_style = pygame.font.SysFont(None, 50)
    score_font = pygame.font.SysFont(None, 35)

    # Initialize database
    conn = sqlite3.connect("snake_game_scores.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS scores
                  (id INTEGER PRIMARY KEY, score INTEGER)''')
    conn.commit()

    # Functions
    def save_score(score):
        """Save the score to the SQLite database."""
        print(f"Saving score: {score}")
        cursor.execute("INSERT INTO scores (score) VALUES (?)", (score,))
        conn.commit()

    def display_score(score):
        """Display the score on the screen."""
        value = score_font.render("Score: " + str(score), True, yellow)
        dis.blit(value, [0, 0])

    def draw_snake(snake_block, snake_list):
        """Draw the snake on the screen."""
        for x in snake_list:
            pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

    def message(msg, color):
        """Display a message on the screen."""
        mesg = font_style.render(msg, True, color)
        dis.blit(mesg, [dis_width / 6, dis_height / 3])

    def gameLoop():
        """Main function to run the game."""
        print("Game loop started")
        game_over = False
        game_close = False

        x1 = dis_width / 2
        y1 = dis_height / 2

        x1_change = 0
        y1_change = 0

        snake_List = []
        Length_of_snake = 1

        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        clock = pygame.time.Clock()

        while not game_over:

            while game_close:
                dis.fill(blue)
                message("You Lost! Press Q-Quit or C-Play Again", red)
                display_score(Length_of_snake - 1)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            gameLoop()

                save_score(Length_of_snake - 1)  # Save score when the game is over

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit event detected.")
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = snake_block
                        x1_change = 0

            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_close = True

            x1 += x1_change
            y1 += y1_change
            dis.fill(blue)

            pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
            snake_Head = [x1, y1]
            snake_List.append(snake_Head)

            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            draw_snake(snake_block, snake_List)
            display_score(Length_of_snake - 1)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                Length_of_snake += 1

            clock.tick(snake_speed)

        save_score(Length_of_snake - 1)  # Save the score once before quitting
        conn.close()
        pygame.quit()
        quit()

    # Run the game
    gameLoop()

except Exception as e:
    print("An error occurred:", e)
    traceback.print_exc()