from .game_object import GameObject
import pygame

class Player:
    def __init__(self, surface=None):
        """Init for class Player.
        @Parameters
            surface: pygame.Surface
                Parameter surface gives us control over drawing the player onto the screen.
        """

        # TODO ADD CAMERA
        self.surface = surface

        # Set the X and Y pos in the first tuple, and then the Width and height
        self.player_rect = pygame.Rect((100, 100), (50, 50))

        # Health of player
        self.health = 100

        # Red color
        self.color = (255, 0, 0)
        
        # Speed that the player is moving at
        self.speed = 5
    
    def draw_player(self):
        '''Draws the player from the given values given in the init.'''

        # Draw the player
        pygame.draw.rect(surface=self.surface, color=self.color,
                         rect=self.player_rect)
        
    def move_player(self):
        '''Moves player using arrow keys and editing the player rectangle position.'''

        # Get key pressed
        keys = pygame.key.get_pressed()

        # Change position based on the movement direction * speed
        self.player_rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        self.player_rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed
