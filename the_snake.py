import pygame
from random import randint, choice

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

class GameObject:
    """
    A base class for all game objects.
    """

    def __init__(self, position=None):
        """
        Initialize the game object.

        :param position: Tuple representing the position of the object.
        """
        self.position = position
        self.body_color = (0, 0, 0)

    def draw(self, screen):
        """
        Draw the game object on the screen.

        :param screen: Pygame screen object.
        """
        pass

class Apple(GameObject):
    """
    Class representing an apple that can be eaten by the snake.
    """

    def __init__(self):
        """
        Initialize the apple with a random position.
        """
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """
        Randomize the position of the apple within the grid.
        """
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self, screen):
        """
        Draw the apple on the screen.

        :param screen: Pygame screen object.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    """
    Class representing the snake.
    """

    def __init__(self):
        """
        Initialize the snake with default settings.
        """
        super().__init__()
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """
        Update the direction of the snake based on user input.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Move the snake in its current direction.
        """
        head_x, head_y = self.get_head_position()
        new_head_x = (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT

        if (new_head_x, new_head_y) in self.positions:
            self.reset()
        else:
            self.positions.insert(0, (new_head_x, new_head_y))
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, screen):
        """
        Draw the snake on the screen.

        :param screen: Pygame screen object.
        """
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """
        Get the position of the snake's head.

        :return: Tuple representing the position of the snake's head.
        """
        return self.positions[0]

    def reset(self):
        """
        Reset the snake to its initial state.
        """
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

def handle_keys(snake):
    """
    Handle keyboard input to control the snake.

    :param snake: Snake object to control.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT

def main():
    """
    Main function to run the game.
    """
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()

if __name__ == "__main__":
    main()
