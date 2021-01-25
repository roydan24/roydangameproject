
import random
import pygame

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 800
HEIGHT = 600
TITLE = "gameproject"
NUM_COINS = 10

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./images/link copy.png")
        # scaling the image down .5x
        self.image = pygame.transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect()

        self.vel_x = 0
        self.vel_y = 0

        # Move left/right
        self.rect.x += self.vel_x

        # List of sprites we can bump against
        self.level = None

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.vel_x

        # Move up/down
        self.rect.y += self.vel_y

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.vel_y == 0:
            self.vel_y = 1
        else:
            self.vel_y += .35

        # See if we are on the ground.
        if self.rect.y >= HEIGHT - self.rect.height and self.vel_y >= 0:
            self.vel_y = 0
            self.rect.y = HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= HEIGHT:
            self.vel_y = -10

            # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.vel_x > 0:
                self.rect.right = block.rect.left
            elif self.vel_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

    # Player movement
    def go_left(self):
        self.vel_x = -4
    def go_right(self):
        self.vel_x = 4
    def stop(self):
        self.vel_x = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self, y_coord):
        """
        Arguments:
            y_coord - initial y-coordinate
        """
        super().__init__()

        self.image = pygame.image.load("./images/goomba copy.png")

        self.rect = self.image.get_rect()

        # initial location middle of the screen at y_coord
        self.rect.centerx = WIDTH / 2
        self.rect.centery = y_coord

        self.x_vel = 3

    def update(self):
        """Move the enemy side-to-side"""
        self.rect.x += self.x_vel

        # Keep enemy in the screen
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.x_vel *= -1

class Coin(pygame.sprite.Sprite):
    def __init__(self, radius=6):
        self.radius = radius

        self.colour = YELLOW

        self.x, self.y = (
            random.randrange(0, WIDTH),
            random.randrange(0, HEIGHT)
        )

        self.vel_y = random.choice([1, 2])

    def draw(self, screen):
        """Draws the coins on the screen."""

        pygame.draw.circle(
            screen,
            self.colour,
            (self.x, self.y),
            self.radius
        )

    def update(self):
        """Update location of coin."""
        self.y += self.vel_y

        # reset location if it reaches the bottom
        if self.y > HEIGHT:
            self.x = random.randrange(0, WIDTH)
            self.y = random.randrange(-15, 0)


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    score = 0


    # Sprite groups
    all_sprites = pygame.sprite.RenderUpdates()
    enemy_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()

    # Create player
    player = Player()
    all_sprites.add(player)

    # create coins
    coin_list = []
    for i in range(NUM_COINS):
        coin = Coin()
        coin_list.append(coin)
        coin.vel_y = random.choice([3, 4])

    # ----- MAIN LOOP
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.vel_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.vel_x > 0:
                    player.stop()

                # If the player gets near the right side, shift the world left (-x)
                if player.rect.right > WIDTH:
                    player.rect.right = WIDTH

                # If the player gets near the left side, shift the world right (+x)
                if player.rect.left < 0:
                    player.rect.left = 0

        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # ----- LOGIC
        all_sprites.update()

        for coin in coin_list:
            coin.update()

        # Player collides with coin
        coins_collected = pygame.sprite.spritecollide(player, coin_group, True)
        for coin in coins_collected:
            score += 1
            print(score)

        # ----- DRAW
        screen.fill(SKY_BLUE)
        for coin in coin_list:
            coin.draw(screen)

        dirty_rectangles = all_sprites.draw(screen)

        # ----- UPDATE
        pygame.display.flip()
        pygame.display.update(dirty_rectangles)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()