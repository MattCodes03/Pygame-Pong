from objects import *
import math
import pygame
pygame.init()


WIDTH, HEIGHT = 1000, 800
PADDEL_WIDTH, PADDEL_HEIGHT = 10, 100
BALL_RADIUS = 10
FPS = 60

font = pygame.font.SysFont('comicsans', 50)

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")


def draw_to_screen(win, player, ball, ai):
    # Set Background Colour
    win.fill((0, 0, 0))

    # Draw line through middle of screen seperating player and ai's court
    pygame.draw.line(win, (255, 255, 255), (WIDTH/2, 0), (WIDTH/2, HEIGHT), 10)

    # Render the scores and then blit to screen
    player_score = font.render(f'{player.score}', 1, (255, 255, 255))
    ai_score = font.render(f'{ai.score}', 1, (255, 255, 255))

    win.blit(player_score, (WIDTH // 4 - player_score.get_width() // 2, 20))
    win.blit(ai_score, (WIDTH * 3 // 4 - ai_score.get_width() // 2, 20))

    # Call object draw functions, this will draw both paddles and the ball
    ball.draw(win)
    player.draw(win)
    ai.draw(win)

    pygame.display.update()


def ball_collision(ball, player, ai):
    # Check Balls collision at side of screen so points can be incremented, and reset ball position after it goes out of screen
    rand_y = random.randint(0, HEIGHT)
    if ball.x <= 0:
        ai.get_point()
        ball.reset(WIDTH/2 + BALL_RADIUS, rand_y)
    if ball.x >= WIDTH:
        player.get_point()
        ball.reset(WIDTH/2 + BALL_RADIUS, HEIGHT/2)

    # Check Collision with Top and Bottom of Screen by seeing if the Ball's Y Coord is greater than or less than the screen Height
    if ball.y + BALL_RADIUS >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - BALL_RADIUS <= 0:
        ball.y_vel *= -1

    # Check if the player's paddle (Left Paddle) has collided with the ball and set Ball's X Directional Velocity (It basically just bounces the ball backwards)
    if ball.x_vel < 0:
        if ball.y >= player.y and ball.y <= player.y + PADDEL_HEIGHT:
            if ball.x - BALL_RADIUS <= player.x + PADDEL_WIDTH:
                ball.x_vel *= -1

                # Calculate Ball's new Y Directional Velocity
                middle_y = player.y + PADDEL_HEIGHT / 2
                # Work out the angle the ball will come off paddle at
                difference_in_y = middle_y - ball.y
                # Clamps the angle so the ball is directed in the correct direction
                reduction_factor = (PADDEL_HEIGHT / 2) / ball.MAX_VEL
                # Calculate the Directional Velocity of the Ball after colliding with paddel
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel * -1

     # Check if the ai's paddle (Right Paddle) has collided with the ball and set Ball's X Directional Velocity (It basically just bounces the ball backwards)
    else:
        if ball.y >= ai.y and ball.y <= ai.y + PADDEL_HEIGHT:
            if ball.x + BALL_RADIUS >= ai.x:
                ball.x_vel *= -1

                # Calculate Ball's new Y Directional Velocity
                middle_y = ai.y + PADDEL_HEIGHT / 2
                # Work out the angle the ball will come off paddle at
                difference_in_y = middle_y - ball.y
                # Clamps the angle so the ball doesn't just go flying away
                reduction_factor = (PADDEL_HEIGHT / 2) / ball.MAX_VEL
                # Calculate the Directional Velocity of the Ball after colliding with paddel
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel * -1


def main(window):
    clock = pygame.time.Clock()

    # Declare Player Paddle
    player = Paddel(20, HEIGHT // 2 - PADDEL_HEIGHT, PADDEL_WIDTH,
                    PADDEL_HEIGHT, (255, 255, 255), 0)

    # Declare AI Paddle
    ai = AI(WIDTH - 20 - PADDEL_WIDTH, HEIGHT // 2 - PADDEL_HEIGHT, PADDEL_WIDTH,
            PADDEL_HEIGHT, (255, 255, 255), 0)

    # Declare Ball Object
    ball = Ball(WIDTH/2 + BALL_RADIUS, HEIGHT/2,
                BALL_RADIUS, (255, 255, 255))

    running = True
    while running:
        clock.tick(FPS)

        keys = pygame.key.get_pressed()
        # If Up Arrow Pressed move player paddle (Left Paddle) on Y-Axis accordingly and Check Paddle Collision with Top and Bottom of Screen
        if keys[pygame.K_UP] and player.y - player.VEL >= 0:
            player.move(-1)
         # If Down Arrow Pressed move player paddle (left Paddle) on Y-Axis accordingly
        if keys[pygame.K_DOWN] and player.y + PADDEL_HEIGHT + player.VEL <= HEIGHT:
            player.move(1)

        # AI Paddle Collision for Top and Bottom of Screen
        if ai.y - ai.VEL >= 0:
            ai.y = 0
        if ai.y + PADDEL_HEIGHT + ai.VEL <= HEIGHT:
            ai.y = HEIGHT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Call Functions
        ball.move()
        ai.move(ball.y)
        ball_collision(ball, player, ai)
        draw_to_screen(window, player, ball, ai)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main(window)
