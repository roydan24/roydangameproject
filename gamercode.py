
import random
import pygame

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
GREEN = (34, 139, 34)
WIDTH = 800
HEIGHT = 600
TITLE = "Link's Coin Fall"
NUM_COINS = 30

# Create player class
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

        # Move up/down
        self.rect.y += self.vel_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.vel_y > 0:
                self.rect.bottom = block.rect.top
            elif self.vel_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.vel_y = 0

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
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
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

# Create enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, y_coord):
        """
        Arguments:
            y_coord - initial y-coordinate
        """
        super().__init__()

        self.image = pygame.image.load("./images/goomba.png")
        self.image = pygame.transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect()

        # initial location middle of the screen at y_coord
        self.rect.centerx = WIDTH / 2
        self.rect.centery = 570

        self.x_vel = 5

    def update(self):
        """Move the enemy side-to-side"""
        self.rect.x += self.x_vel

        # Keep enemy in the screen
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.x_vel *= -1

# Create coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./images/coin.png")
        self.image = pygame.transform.scale(self.image, (32, 32))

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = (
            random.randrange(0, WIDTH),
            random.randrange(0, HEIGHT)
        )

        self.vel_y = random.choice([1, 2])

    def update(self):
        """Update location of coin."""
        self.rect.y += self.vel_y

        # reset location if it reaches the bottom
        if self.rect.y > HEIGHT:
            self.rect.x = random.randrange(0, WIDTH)
            self.rect.y = random.randrange(-15, 0)

# May add platforms later on
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()


class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = None

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """


        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform
        level = [
            [210, 70, 600, 800],
        ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


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
    enemy_sprites = pygame.sprite.Group()
    coin_sprites = pygame.sprite.Group()

    # enemies
    enemy = Enemy(1)
    all_sprites.add(enemy)
    enemy_sprites.add(enemy)

    # Create player
    player = Player()
    all_sprites.add(player)

    # create coins
    coin_list = []
    for i in range(NUM_COINS):
        coin = Coin()
        coin_list.append(coin)
        coin.rect.x = random.randrange(WIDTH - coin.rect.width)
        coin.rect.y = random.randrange(HEIGHT - coin.rect.height)
        all_sprites.add(coin)
        coin_sprites.add(coin)

    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

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

                # If the player and enemy gets near the right side, shift the world left (-x)
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

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > WIDTH:
            player.rect.right = WIDTH

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0

        # Update coin
        for coin in coin_sprites:
             coin.update()

        # Player collides with coin
        coins_collected = pygame.sprite.spritecollide(player, coin_sprites, True)
        for coin in coins_collected:
            score += 1
            print(f"Score = {score}")

        # Enemy collides with player
        enemy_collide = pygame.sprite.spritecollide(player, enemy_sprites, False)
        for enemy in enemy_collide:
            print("Game Over")
            done = True

        # ----- DRAW
        screen.fill(GREEN)

        current_level.draw(screen)
        dirty_rectangles = all_sprites.draw(screen)


        # ----- UPDATE
        pygame.display.flip()
        pygame.display.update(dirty_rectangles)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()