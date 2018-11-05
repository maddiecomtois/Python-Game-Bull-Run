"""
Game where the player must run through the Streets of Spain jumping over obstacles
while escaping a bull chasing form behind.

@author Maddie Comtois
@version August 1, 2016
"""

import pygame, sys, random, time

# Start Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Frames per second
FPS = 60

# Set up the different types of fonts
font = pygame.font.SysFont('Courier New', 50, True, False)
font2 = pygame.font.SysFont('Georgia', 29, True, False)
fontScore = pygame.font.SysFont(None, 50, True, False)

# Set up the sound effects/music
bullSoundEffect = pygame.mixer.Sound('bullSoundEffect.wav')
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('bullfightingMusic.wav')


class Player(pygame.sprite.Sprite):
    """ This class sets up the torero character and the gravity, sprite collisions,
    jumps, and movement that go with it. """

    # Method that constructs the character
    def __init__(self):

        # This calls the parent class' constructor
        super().__init__()

        # Loads the torero image of the player and creates a rectangle reference for it
        self.image = pygame.image.load('torero.png')
        self.rect = self.image.get_rect()

        # Sets the torero's speed
        self.changeX = 0
        self.changeY = 0

        # List of sprites we can bump against
        self.level = None

    def gravity(self):
        """ This function calls the effect of gravity on the player. """
        if self.changeY == 0:
            self.changeY = 10
        else:
            # Affects how high the player jumps
            self.changeY += .5

        # Checks if the player is on the ground and not jumping
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.changeY >= 0:
            self.changeY = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def update(self):
        """ This functions updates the player to see if it is moving,
        colliding with sprites, and being affected by gravity. """

        # Checks for gravity
        self.gravity()

        # Moves the character left or right
        self.rect.x += self.changeX

        # Checks to see if the player ran into a platform in the x-direction
        platformHitList = pygame.sprite.spritecollide(self, self.level.platform_list, False)

        for item in platformHitList:
            # Lets the player jump if it has collided with a platform
            for event in pygame.event.get():
                if event.key == pygame.K_UP:
                    self.jump()
            # If the player moves right, it will touch the left side of the platform
            if self.changeX > 0:
                self.rect.right = item.rect.left
            elif self.changeX < 0:
                # If the player moves left, it will touch the right side of the platform
                self.rect.left = item.rect.right

        # Moves the player up (back down)
        self.rect.y += self.changeY

        # Checks to see if the player ran into a platform in the y-direction
        platformHitList = pygame.sprite.spritecollide(self, self.level.platform_list, False)

        for item in platformHitList:

            for event in pygame.event.get():
                if event.key == pygame.K_UP:
                    self.jump()

            if self.changeY > 0:
                self.rect.bottom = item.rect.top
            elif self.changeY < 0:
                self.rect.top = item.rect.bottom

            # Stops the player from moving vertically
            self.changeY = 0


    def jump(self):
        """ This function makes the player jump """

        # Moves the player down to see if there is a platform
        self.rect.y += 2
        touchedPlatformList = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        # Lands the player onto a platform
        self.rect.y -= 2

        # Sets the speed of the jump if there is a platform to jump onto
        if len(touchedPlatformList) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.changeY = -10

    def moveLeft(self):
        """ Called to move the player left when the left arrow key is pressed """
        self.changeX = -8

    def moveRight(self):
        """ Called to move the player right when the right arrow key is pressed """
        self.changeX = 8

    def standStill(self):
        """ Called to keep the player still when no arrow keys are pressed """
        self.changeX = 0

class Bull(pygame.sprite.Sprite):
    """ This class sets up the Bull character """
    def __init__(self):

        super().__init__()

        # Loads the bull image
        self.image = pygame.image.load('bull2.jpg').convert()
        # Gets rid of the white background around the image
        self.image.set_colorkey(WHITE)
        # Scales the bull to the right size
        self.image = pygame.transform.scale(self.image, (200, 200))
        # Flips the image across the y-axis (180 degrees)
        self.image = pygame.transform.flip(self.image, 180, 0)
        # Creates a rectangle reference for the bull.
        self.rect = self.image.get_rect()

class Platform(pygame.sprite.Sprite):
    """ This class sets up the platforms that the player can jump onto """

    def __init__(self, width, height):

        super().__init__()

        # Loads the image of the platforms
        self.image = pygame.image.load('stoneplatform.png').convert()
        # Scales the paltform image to the right size
        self.image = pygame.transform.scale(self.image, (100, 50))
        # Creates a rectangle reference for the platforms
        self.rect = self.image.get_rect()


class Backgroundsetup(object):
    """ This is a parent class for setting up all of the different
     backgrounds used throughout the game"""

    def __init__(self, player, bull):
        """ Constructor that takes the player and bull into account when setting up the backgrounds. """
        # Groups the platform sprites into a list
        self.platform_list = pygame.sprite.Group()
        # Sets up a reference for the player
        self.player = player
        # Sets the background shift to 0
        self.background_shift = 0

    def update(self):
        """ This function updates everything on the current background."""
        self.platform_list.update()

    def draw(self, screen):
        """ This function draws everything that is on the current background """

        screen.blit(self.background, [0, 0])

        # This draws the platforms that are in the platform list
        self.platform_list.draw(screen)

    def shift_background(self, shiftX):
        """ This function moves the objects on the screen when the background shifts"""
        self.background_shift += shiftX

        for platform in self.platform_list:
            platform.rect.x += shiftX

class Background1(Backgroundsetup):
    """ This class sets up the first background """

    def __init__(self, player, bull):
        # Passes the specific background information to the parent background set up class
        Backgroundsetup.__init__(self, player, bull)

        # Load and scale the first background image
        self.background = pygame.image.load('backgroundstreet1.jpg').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Sets the background limit the length of the current background
        self.background_limit = -2000

        # Sets the width, height, x position and y position of the first level of platforms
        level = [[10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620]
                 ]

        # Sets the width, height, x position and y position of the second level of platforms
        level2 = [[10, 10, random.randint(level[0][2] + 10, level[0][2] + 300), level[0][3] - 100],
                 [10, 10, random.randint(level[1][2] + 10, level[1][2] + 300), level[1][3] - 100],
                 [10, 10, random.randint(level[2][2] + 10, level[2][2] + 300), level[2][3] - 100],
                 [10, 10, random.randint(level[3][2] + 10, level[3][2] + 300), level[3][3] - 100],
                 [10, 10, random.randint(level[4][2] + 10, level[4][2] + 300), level[4][3] - 100]
                 ]

        # Sets the width, height, x position and y position of the third level of platforms
        level3 = [[10, 10, random.randint(level2[0][2] + 10, level2[0][2] + 300), level2[0][3] - 100],
                  [10, 10, random.randint(level2[1][2] + 10, level2[1][2] + 300), level2[1][3] - 100],
                  ]

        # This adds the first level of platforms to the platform list
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # This adds the second level of platforms to the platform list
        for platform in level2:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # This adds the third level of platforms to the platform list
        for platform in level3:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class Background2(Backgroundsetup):
    """ This class sets up the second background """

    def __init__(self, player, bull):
        # Passes the specific background information to the parent background set up class
        Backgroundsetup.__init__(self, player, bull)

        # Load and scale the first background image
        self.background = pygame.image.load('backgroundstreet2.jpg').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Sets the background limit the length of the current background
        self.background_limit = -2000

        # Sets the width, height, x position and y position of the first level of platforms
        level = [[10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 310, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620]
                 ]

        # Sets the width, height, x position and y position of the second level of platforms
        level2 = [[10, 10, random.randint(level[0][2] + 10, level[0][2] + 300), level[0][3] - 100],
                  [10, 10, random.randint(level[1][2] + 10, level[1][2] + 300), level[1][3] - 100],
                  [10, 10, random.randint(level[2][2] + 10, level[2][2] + 300), level[2][3] - 100],
                  [10, 10, random.randint(level[3][2] + 10, level[3][2] + 300), level[3][3] - 100],
                  [10, 10, random.randint(level[4][2] + 10, level[4][2] + 300), level[4][3] - 100]
                  ]

        # Sets the width, height, x position and y position of the third level of platforms
        level3 = [[10, 10, random.randint(level2[0][2] + 10, level2[0][2] + 300), level2[0][3] - 100],
                  [10, 10, random.randint(level2[1][2] + 10, level2[1][2] + 300), level2[1][3] - 100],
                  ]

        # This adds the first level of platforms to the platform list
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # This adds the second level of platforms to the platform list
        for platform in level2:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # This adds the third level of platforms to the platform list
        for platform in level3:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class Background3(Backgroundsetup):
    """ This class sets up the third background """

    def __init__(self, player, bull):
        # Passes the specific background information to the parent background set up class
        Backgroundsetup.__init__(self, player, bull)

        # Load and scale the first background image
        self.background = pygame.image.load('backgroundstreet3.jpg').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Sets the background limit the length of the current background
        self.background_limit = -2000


        # Sets the width, height, x position and y position of the first level of platforms
        level = [[10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 310, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620]
                 ]

        # Sets the width, height, x position and y position of the second level of platforms
        level2 = [[10, 10, random.randint(level[0][2] + 10, level[0][2] + 300), level[0][3] - 100],
                  [10, 10, random.randint(level[1][2] + 10, level[1][2] + 300), level[1][3] - 100],
                  [10, 10, random.randint(level[2][2] + 10, level[2][2] + 300), level[2][3] - 100],
                  [10, 10, random.randint(level[3][2] + 10, level[3][2] + 300), level[3][3] - 100],
                  [10, 10, random.randint(level[4][2] + 10, level[4][2] + 300), level[4][3] - 100]
                  ]

        # Sets the width, height, x position and y position of the third level of platforms
        level3 = [[10, 10, random.randint(level2[0][2] + 10, level2[0][2] + 300), level2[0][3] - 100],
                  [10, 10, random.randint(level2[1][2] + 10, level2[1][2] + 300), level2[1][3] - 100],
                  ]

        # This adds the first level of platforms to the platform list
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # This adds the second level of platforms to the platform list
        for platform in level2:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # This adds the third level of platforms to the platform list
        for platform in level3:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class Background4(Backgroundsetup):
    """ This class sets up the fourth background """

    def __init__(self, player, bull):
        # Passes the specific background information to the parent background set up class
        Backgroundsetup.__init__(self, player, bull)

        # Load and scale the first background image
        self.background = pygame.image.load('backgroundstreet4.jpg').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Sets the background limit the length of the current background
        self.background_limit = -2000

        # Sets the width, height, x position and y position of the first level of platforms
        level = [[10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620]
                 ]

        # Sets the width, height, x position and y position of the second level of platforms
        level2 = [[10, 10, random.randint(level[0][2] + 10, level[0][2] + 300), level[0][3] - 100],
                  [10, 10, random.randint(level[1][2] + 10, level[1][2] + 300), level[1][3] - 100],
                  [10, 10, random.randint(level[2][2] + 10, level[2][2] + 300), level[2][3] - 100],
                  [10, 10, random.randint(level[3][2] + 10, level[3][2] + 300), level[3][3] - 100],
                  [10, 10, random.randint(level[4][2] + 10, level[4][2] + 300), level[4][3] - 100]
                  ]

        # Sets the width, height, x position and y position of the third level of platforms
        level3 = [[10, 10, random.randint(level2[0][2] + 10, level2[0][2] + 300), level2[0][3] - 100],
                  [10, 10, random.randint(level2[1][2] + 10, level2[1][2] + 300), level2[1][3] - 100],
                  ]

        # This adds the first level of platforms to the platform list
        for platform in level:
            block  = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # This adds the second level of platforms to the platform list
        for platform in level2:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # This adds the third level of platforms to the platform list
        for platform in level3:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class Background5(Backgroundsetup):
    """ This class sets up the fifth background """

    def __init__(self, player, bull):
        # Passes the specific background information to the parent background set up class
        Backgroundsetup.__init__(self, player, bull)

        # Load and scale the first background image
        self.background = pygame.image.load('backgroundstreet5.jpg').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Sets the background limit the length of the current background
        self.background_limit = -2000

        # Sets the width, height, x position and y position of the first level of platforms
        level = [[10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620]
                 ]

        # Sets the width, height, x position and y position of the second level of platforms
        level2 = [[10, 10, random.randint(level[0][2] + 10, level[0][2] + 300), level[0][3] - 100],
                  [10, 10, random.randint(level[1][2] + 10, level[1][2] + 300), level[1][3] - 100],
                  [10, 10, random.randint(level[2][2] + 10, level[2][2] + 300), level[2][3] - 100],
                  [10, 10, random.randint(level[3][2] + 10, level[3][2] + 300), level[3][3] - 100],
                  [10, 10, random.randint(level[4][2] + 10, level[4][2] + 300), level[4][3] - 100]
                  ]

        # Sets the width, height, x position and y position of the third level of platforms
        level3 = [[10, 10, random.randint(level2[0][2] + 10, level2[0][2] + 300), level2[0][3] - 100],
                  [10, 10, random.randint(level2[1][2] + 10, level2[1][2] + 300), level2[1][3] - 100],
                  ]

        # This adds the first level of platforms to the platform list
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # This adds the second level of platforms to the platform list
        for platform in level2:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # This adds the third level of platforms to the platform list
        for platform in level3:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class Background6(Backgroundsetup):
    """ This class sets up the sixth background """

    def __init__(self, player, bull):
        # Passes the specific background information to the parent background set up class
        Backgroundsetup.__init__(self, player, bull)

        # Load and scale the first background image
        self.background = pygame.image.load('backgroundstreet6.jpg').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Sets the background limit the length of the current background
        self.background_limit = -2000

        # Sets the width, height, x position and y position of the first level of platforms
        level = [[10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620]
                 ]

        # Sets the width, height, x position and y position of the second level of platforms
        level2 = [[10, 10, random.randint(level[0][2] + 10, level[0][2] + 300), level[0][3] - 100],
                  [10, 10, random.randint(level[1][2] + 10, level[1][2] + 300), level[1][3] - 100],
                  [10, 10, random.randint(level[2][2] + 10, level[2][2] + 300), level[2][3] - 100],
                  [10, 10, random.randint(level[3][2] + 10, level[3][2] + 300), level[3][3] - 100],
                  [10, 10, random.randint(level[4][2] + 10, level[4][2] + 300), level[4][3] - 100]
                  ]

        # Sets the width, height, x position and y position of the third level of platforms
        level3 = [[10, 10, random.randint(level2[0][2] + 10, level2[0][2] + 300), level2[0][3] - 100],
                  [10, 10, random.randint(level2[1][2] + 10, level2[1][2] + 300), level2[1][3] - 100],
                  ]

        # This adds the first level of platforms to the platform list
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # This adds the second level of platforms to the platform list
        for platform in level2:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # This adds the third level of platforms to the platform list
        for platform in level3:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class Background7(Backgroundsetup):
    """ This class sets up the seventh background """

    def __init__(self, player, bull):
        # Passes the specific background information to the parent background set up class
        Backgroundsetup.__init__(self, player, bull)

        # Load and scale the first background image
        self.background = pygame.image.load('backgroundstreet7.jpg').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Sets the background limit the length of the current background
        self.background_limit = -2000

        # Sets the width, height, x position and y position of the first level of platforms
        level = [[10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620],
                 [10, 10, random.randint(player.rect.x + 200, 2500), 620]
                 ]

        # Sets the width, height, x position and y position of the second level of platforms
        level2 = [[10, 10, random.randint(level[0][2] + 10, level[0][2] + 300), level[0][3] - 100],
                  [10, 10, random.randint(level[1][2] + 10, level[1][2] + 300), level[1][3] - 100],
                  [10, 10, random.randint(level[2][2] + 10, level[2][2] + 300), level[2][3] - 100],
                  [10, 10, random.randint(level[3][2] + 10, level[3][2] + 300), level[3][3] - 100],
                  [10, 10, random.randint(level[4][2] + 10, level[4][2] + 300), level[4][3] - 100]
                  ]

        # Sets the width, height, x position and y position of the third level of platforms
        level3 = [[10, 10, random.randint(level2[0][2] + 10, level2[0][2] + 300), level2[0][3] - 100],
                  [10, 10, random.randint(level2[1][2] + 10, level2[1][2] + 300), level2[1][3] - 100],
                  ]

        # This adds the first level of platforms to the platform list
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # This adds the second level of platforms to the platform list
        for platform in level2:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # This adds the third level of platforms to the platform list
        for platform in level3:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class Background7Copy(Backgroundsetup):
    """ This class creates a semi-copy of the last background class to pass into the background list
    as the final background for the player to pass through before winning the game"""
    def __init__(self, player, bull):
        # Passes the specific background information to the parent background set up class

        Backgroundsetup.__init__(self, player, bull)
        # Load and scale the first background image
        self.background = pygame.image.load('backgroundstreet7.jpg').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Sets the background limit the length of the current background
        self.background_limit = -2000

class BackgroundFinal(Backgroundsetup):
    """ This class creates the background for a winning game """

    def __init__(self, player):
        # Passes the specific background information to the parent background set up class
        Backgroundsetup.__init__(self, player)

        # Load and scale the first background image
        self.background = pygame.image.load('backgroundfinal.jpg').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))


def waitForPlayerToPressKey():
    """ This function waits for a player to press any key before continuing
    with the game """

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                return

def beginningInstructions():
    """ This function sets up the beginning game instructions
    before the main game loop """

    # Sets the screen size
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    # Hides the mouse
    pygame.mouse.set_visible(False)
    # Creates a surface to display the instructions
    windowSurface = pygame.display.set_mode(size, pygame.FULLSCREEN)

    # Loads and scales the background image of the instruction screen
    startScreen = pygame.image.load('bullring.jpg').convert()
    startScreen = pygame.transform.scale(startScreen, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Blits the background image onto the screen
    windowSurface.blit(startScreen, [0, 0])

    # Creates the game instructions
    gameTitle = font.render('Bull Run', 1, BLACK, None)
    gameInstructions1 = font2.render('Today is the annual Running of the Bulls in Pamplona, Spain.', 1, BLACK, None)
    gameInstructions2 = font2.render('You are Fermín, an aspiring matador who hopes to reach the', 1, BLACK, None)
    gameInstructions3 = font2.render('bull ring before he is run down by a large, angry bull.', 1, BLACK, None)
    gameInstructions4 = font2.render('Use your left and right arrow keys to move Fermín, and press ', 1, BLACK, None)
    gameInstructions5 = font2.render('the up arrow or space bar to jump. Try to run through the', 1, BLACK, None)
    gameInstructions6 = font2.render('course as fast as you can, and of course, watch out for the bull!', 1, BLACK, None)
    gameInstructions7 = font2.render('Press any key to start.', 1, BLACK, None)

    # Draws the game instructions and background rectangle onto the screen
    pygame.draw.rect(windowSurface, WHITE, [40, 70, 930, 550])
    windowSurface.blit(gameTitle, (380, 100))
    windowSurface.blit(gameInstructions1, (45, 200))
    windowSurface.blit(gameInstructions2, (45, 250))
    windowSurface.blit(gameInstructions3, (45, 300))
    windowSurface.blit(gameInstructions4, (45, 350))
    windowSurface.blit(gameInstructions5, (45, 400))
    windowSurface.blit(gameInstructions6, (45, 450))
    windowSurface.blit(gameInstructions7, (350, 550))

    # Updates the screen and waits for a player to press a key to continue
    pygame.display.update()
    waitForPlayerToPressKey()

def main():
    """ This function runs the main program """

    # Sets the top score to zero
    topScore = 0
    loseGame = False

    while True:

        # Starts the music
        pygame.mixer.music.play(-1, 0.0)

        # Sets the values of the score and max lives
        score = 0
        maxLives = 3

        # Sets the screen dimensions
        size = [SCREEN_WIDTH, SCREEN_HEIGHT]
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

        # Sets the game captions
        pygame.display.set_caption("Bull Run")

        # Sets the speed of the bull
        bullchangeX = 1

        # Create the player and the bull
        player = Player()
        bull = Bull()

        # Create all the backgrounds
        backgroundList = []
        backgroundList.append(Background1(player, bull))
        backgroundList.append(Background2(player, bull))
        backgroundList.append(Background3(player, bull))
        backgroundList.append(Background4(player, bull))
        backgroundList.append(Background5(player, bull))
        backgroundList.append(Background6(player, bull))
        backgroundList.append(Background7(player, bull))
        backgroundList.append(Background7Copy(player, bull))

        # Sets the current background to the first one in the background list
        currentBackgroundNo = 0
        currentBackground = backgroundList[currentBackgroundNo]

        # Adds the active sprites to a list and sets the player to the current background
        currentSprites = pygame.sprite.Group()
        player.level = currentBackground

        # Sets the x and y direction of the player
        player.rect.x = 100
        player.rect.y = SCREEN_HEIGHT - player.rect.height

        # Adds the player to the sprite list
        currentSprites.add(player)

        # Sets the x and y direction of the bull
        bull.rect.x = -200
        bull.rect.y = SCREEN_HEIGHT - bull.rect.height + 25

        # Adds the bull to the sprite list
        currentSprites.add(bull)

        # Sets the game to loop until the player exits the game.
        done = False

        # Manages how fast the screen updates
        clock = pygame.time.Clock()

        # Main program loop
        while not done:

            # Increases the score with each loop
            score += 1

            # Quits the game if the user closes out the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Moves the player based on the key pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        player.moveLeft()
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        player.moveRight()
                    if event.key == pygame.K_UP or pygame.K_SPACE or event.key == ord('w'):
                        player.jump()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                # Keeps the player from moving when no key is pressed
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player.changeX < 0:
                        player.standStill()
                    if event.key == pygame.K_RIGHT and player.changeX > 0:
                        player.standStill()
                    if event.key == ord('a') and player.changeX > 0:
                        player.standStill()
                    if event.key == ord('d') and player.changeX > 0:
                        player.standStill()

            # Moves the bull
            bull.rect.x += bullchangeX
            # Moves the bull back to the left side of the screen after it runs off the right
            if bull.rect.x >= SCREEN_WIDTH:
                bull.rect.x = -200

            # If the player runs into the bull
            if player.rect.colliderect(bull):
                # Moves the bull backwards 200 pixels
                bull.rect.x = -200
                # Plays the angry bull sound effect
                bullSoundEffect.play()
                # Takes away a life
                maxLives -= 1

            # Exits the main game loop if the player runs out of lives
            if maxLives == 0:
                pygame.mixer.music.stop()
                gameOverSound.play()
                time.sleep(1)
                loseGame = True
                break

            # Updates the sprites
            currentSprites.update()

            # Updates the platforms for the current background
            currentBackground.update()

            # Scrolls the background right to keep the player on the screen
            if player.rect.right >= 500:
                diff = player.rect.right - 500
                player.rect.right = 500
                currentBackground.shift_background(-diff)
            # Scrolls the background left to keep the player on the screen
            if player.rect.left <= 100:
                diff = 100 - player.rect.left
                player.rect.left = 100
                currentBackground.shift_background(diff)

            # Pin points the character position based on its x location and the background shift
            playerPosition = player.rect.x + currentBackground.background_shift

            # Changes to the next background in the background list
            if playerPosition < currentBackground.background_limit:
                player.rect.x = 120
                if currentBackgroundNo < len(backgroundList):
                    currentBackgroundNo += 1
                    currentBackground = backgroundList[currentBackgroundNo]
                    player.level = currentBackground

                # Exits the game if the player has made it through all the backgrounds
                if currentBackgroundNo == len(backgroundList) - 1:
                    # Checks to make sure the player does not run into the bull at the same time as it wins
                    if maxLives > 0:
                        loseGame = False
                        break
                    if maxLives == 0:
                        loseGame = True
                        break

            # Creates text for the score, fastest score, and max lives displayed on the screen during the game
            textScore = fontScore.render('Speed Score: %s' % (score), 1, RED, None)
            textTopScore = fontScore.render('Fastest Successful Run: %s' % (topScore), 1, RED, None)
            textMaxLives = fontScore.render('Lives: %s' % (maxLives), 1, RED, None)

            # Draws the background, sprites, and text onto the screen
            currentBackground.draw(screen)
            currentSprites.draw(screen)
            screen.blit(textScore, (25, 25))
            screen.blit(textTopScore, (25, 60))
            screen.blit(textMaxLives, (25, 95))

            clock.tick(FPS)

            # Updates the screen with everything that was drawn
            pygame.display.flip()

        # Brings up the game over screen if the player loses the game
        if loseGame == True:

            # Sets up and scales the game over screen
            loserScreenSurface = pygame.display.set_mode(size, pygame.FULLSCREEN)
            loserScreen = pygame.image.load('bullgameover.jpg').convert()
            loserScreen = pygame.transform.scale(loserScreen, (SCREEN_WIDTH, SCREEN_HEIGHT))
            loserScreenSurface.blit(loserScreen, [0, 0])

            # Sets up the text for the game over screen
            gameOver = font.render('Game Over!', 1, RED, None)
            finalScore = font2.render('Your speed score is: %s' % (score), 1, RED, None)
            finalInstructions = font2.render('Press any key to play again,', 1, RED, None)
            finalInstructions2 = font2.render('or press the esc key to quit.', 1, RED, None)

            # Draws everything onto the screen surface
            screen.blit(gameOver, (320, 180))
            screen.blit(finalScore, (320, 400))
            screen.blit(finalInstructions, (300, 450))
            screen.blit(finalInstructions2, (300, 500))

            # Updates the screen and resets the score to 0
            pygame.display.update()
            score = 0

            # Waits for player to press a key to play again and restarts the music
            waitForPlayerToPressKey()
            pygame.mixer.music.play(-1, 0.0)

        # Brings up the winning screen if the player wins the game
        if loseGame == False:

            # If the player beat their fastest time, this resets their fastest score
            if topScore > score or topScore == 0:
                topScore = score

            # Sets up and scales the winning screen
            finalScreenSurface = pygame.display.set_mode(size, pygame.FULLSCREEN)
            finalScreen = pygame.image.load('backgroundfinal.jpg').convert()
            finalScreen = pygame.transform.scale(finalScreen, (SCREEN_WIDTH, SCREEN_HEIGHT))

            # Sets up the torero and confetti images
            toreroImage = pygame.image.load('torero.png')
            confetti = pygame.image.load('confetti.png')

            # Draws the background onto the screen surface
            finalScreenSurface.blit(finalScreen, [0, 0])

            # Sets up the text for the winning screen
            congratulations = font.render('Congratulations!', 1, RED, None)
            endOfGame = font2.render('You have made it to the bull ring safe and sound!', 1, RED, None)
            endOfGame2 = font2.render('Your speed score is: %s' % (score), 1, RED, None)
            endOfGame3 = font2.render('Press any key to play again, or press the esc key to quit', 1, RED, None)

            # Draws everything onto the screen surface
            pygame.draw.rect(screen, WHITE, [40, 30, 900, 300])
            screen.blit(confetti, [0, 300])
            screen.blit(congratulations, (235, 70))
            screen.blit(endOfGame, (100, 150))
            screen.blit(endOfGame2, (100, 200))
            screen.blit(endOfGame3, (100, 250))
            screen.blit(toreroImage, (300, 550))

            # Updates the screen when for player to press a key to play again
            pygame.display.update()
            waitForPlayerToPressKey()

beginningInstructions()
main()
