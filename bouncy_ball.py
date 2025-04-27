# Advanced Bouncy Ball Simulation with Doubling and Live Boundary Switching

import pygame
import random
import math
import time

# Initialize pygame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bouncy Ball Simulation - Advanced')

# Set background color
BACKGROUND_COLOR = (0, 0, 0)

# Define boundary options
BOUNDARY_TYPE = 'circle'  # Default: 'circle' or 'square'

# Circle boundary center and radius
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
CIRCLE_RADIUS = min(WIDTH, HEIGHT) // 2 - 10  # Slight margin

# Constants
BALL_RADIUS = 15
CENTER_ZONE_RADIUS = 20  # How close to center to trigger doubling

BACKGROUND_MODE = 'black'  # Options: 'black', 'orange', 'blue'

# Ball class
class Ball:
    def __init__(self, x=None, y=None, vx=None, vy=None, color=None):
        # (Same as before initialization...)
        if x is not None and y is not None:
            self.x = x
            self.y = y
        else:
            while True:
                self.x = random.randint(CENTER_X - CIRCLE_RADIUS + BALL_RADIUS, CENTER_X + CIRCLE_RADIUS - BALL_RADIUS)
                self.y = random.randint(CENTER_Y - CIRCLE_RADIUS + BALL_RADIUS, CENTER_Y + CIRCLE_RADIUS - BALL_RADIUS)
                if math.hypot(self.x - CENTER_X, self.y - CENTER_Y) + BALL_RADIUS <= CIRCLE_RADIUS:
                    break

        self.vx = vx if vx is not None else random.choice([-4, -3, -2, 2, 3, 4])
        self.vy = vy if vy is not None else random.choice([-4, -3, -2, 2, 3, 4])
        self.color = color if color else self.random_gradient_color()

        self.last_split_time = 0  # Time since last duplication (initialize to 0)
        self.has_hit_boundary = False  # NEW FLAG

    def random_gradient_color(self):
        r = random.randint(100, 255)
        g = random.randint(50, 200)
        b = random.randint(100, 255)
        return (r, g, b)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1

        if BOUNDARY_TYPE == 'square':
            if self.x - BALL_RADIUS <= 0 or self.x + BALL_RADIUS >= WIDTH:
                self.vx *= -1
                self.has_hit_boundary = True  # Mark that it hit wall
            if self.y - BALL_RADIUS <= 0 or self.y + BALL_RADIUS >= HEIGHT:
                self.vy *= -1
                self.has_hit_boundary = True
        elif BOUNDARY_TYPE == 'circle':
            dx = self.x - CENTER_X
            dy = self.y - CENTER_Y
            dist = math.hypot(dx, dy)
            if dist + BALL_RADIUS >= CIRCLE_RADIUS:
                nx = dx / dist
                ny = dy / dist
                dot = self.vx * nx + self.vy * ny
                self.vx -= 2 * dot * nx
                self.vy -= 2 * dot * ny
                overlap = (dist + BALL_RADIUS) - CIRCLE_RADIUS
                self.x -= overlap * nx
                self.y -= overlap * ny
                self.has_hit_boundary = True  # Mark that it hit wall

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), BALL_RADIUS)

    def is_ready_to_split(self):
        # Returns True if the ball is near center and cooldown time passed
        dist_to_center = math.hypot(self.x - CENTER_X, self.y - CENTER_Y)
        now = time.time()
        return dist_to_center <= CENTER_ZONE_RADIUS and (now - self.last_split_time > 1.0)

def draw_background():
    if BACKGROUND_MODE == 'black':
        screen.fill((0, 0, 0))
    elif BACKGROUND_MODE == 'orange':
        # Gradient from dark orange to light orange
        for y in range(HEIGHT):
            r = 255
            g = int(140 + (115 * (y / HEIGHT)))  # from 140 to 255
            b = 0
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
    elif BACKGROUND_MODE == 'blue':
        # Gradient from dark blue to light blue
        for y in range(HEIGHT):
            r = 0
            g = int(120 + (100 * (y / HEIGHT)))  # from 120 to 220
            b = int(200 + (55 * (y / HEIGHT)))  # from 200 to 255
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))



def draw_boundary():
    if BOUNDARY_TYPE == 'square':
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, HEIGHT), 5)
    elif BOUNDARY_TYPE == 'circle':
        pygame.draw.circle(screen, (255, 255, 255), (CENTER_X, CENTER_Y), CIRCLE_RADIUS, 5)

def main():
    global BOUNDARY_TYPE, BACKGROUND_MODE
    clock = pygame.time.Clock()
    balls = [Ball()]  # Start with one ball
    
    running = True
    while running:
        clock.tick(60)
        # screen.fill(BACKGROUND_COLOR)
        draw_background()
        draw_boundary()
        # After draw_background()
        pygame.draw.circle(screen, (255, 255, 255), (CENTER_X, CENTER_Y), 5)  # White center dot

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Key controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    BOUNDARY_TYPE = 'circle'
                elif event.key == pygame.K_s:
                    BOUNDARY_TYPE = 'square'
                elif event.key == pygame.K_b:
                    BACKGROUND_MODE = 'black'
                elif event.key == pygame.K_o:
                    BACKGROUND_MODE = 'orange'
                elif event.key == pygame.K_l:
                    BACKGROUND_MODE = 'blue' 
                elif event.key == pygame.K_r:
                    balls.clear()  # Remove all balls
                    balls.append(Ball())  # Add one new ball
        

        
        # Move and draw balls
        new_balls = []
        for ball in balls:
            ball.move()
            ball.draw()

            # Check if ball is ready to duplicate
            if ball.has_hit_boundary and ball.is_ready_to_split():
                # Create a new ball at same location with random velocity/color
                new_ball = Ball(x=ball.x, y=ball.y)

                # Apply a small random push to both balls
                angle = random.uniform(0, 2 * math.pi)
                push_strength = 2

                ball.vx += push_strength * math.cos(angle)
                ball.vy += push_strength * math.sin(angle)

                new_ball.vx += push_strength * math.cos(angle + math.pi/2)
                new_ball.vy += push_strength * math.sin(angle + math.pi/2)

                new_balls.append(new_ball)
                ball.last_split_time = time.time()



        balls.extend(new_balls)  # Add newly created balls

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
