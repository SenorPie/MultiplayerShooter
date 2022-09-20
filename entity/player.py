from items.item import Item
from .game_object import GameObject
import pygame

class Player:
    def __init__(self, surface: pygame.Surface):
        """
            The Player class is the class which we use to control and draw the player
            @parameters
                surface:
                    type: pygame.Surface
                    description: Parameter surface gives us control over drawing the player onto the screen
        """

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
        """
            draw_player is a function that draws the player from the given values given in the init
            the draw_player gets called in the main loop.
        """

        # Fill the surface with black color so our player rect doesnt overlap
        self.surface.fill(color=(0, 0, 0))

        # Draw the player
        pygame.draw.rect(surface=self.surface, color=self.color,
                         rect=self.player_rect)
        
        # Call the equip_item() function
        self.equip_item()
    
    def move_player(self):
        """
            move_player is a function that utilizes the get_pressed() function from pygame.key
            in order to determine which key they have pressed and change the x/y pos based on that
        """

        # Get key pressed
        keys = pygame.key.get_pressed()

        # Change position based on the movement direction * speed
        self.player_rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        self.player_rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed
    
    def equip_item(self):
        """
            equip_item is a function utilizing our item class to get the rect for our item
            in order to equip it at the correct spot
        """

        # Initialize our item with an item_id and the damage it does
        item = Item(item_id=1)

        # Get the rect from the get_itemrect function
        item_rect = item.get_itemrect(player_pos=(self.player_rect.x, self.player_rect.y), offset=20)

        # Draw the rect
        pygame.draw.rect(surface=self.surface, color=(0, 255, 0), rect=item_rect)