import pygame

class GameObject:
    def __init__(self, surface: pygame.Surface, rect: pygame.Rect, color: pygame.Color):
        """
            The GameObject class is used to draw and check collision with objects and entitys
            @parameters
                surface: the game screen to draw on
                rect: the x, y, width and height of the object
                color: the objects color
        """

        self.surface = surface
        self.rect = rect
        self.color = color

    def draw_object(self):
        """
            draw_object(): draws the object upon the screen
        """

        pygame.draw.rect(surface=self.surface, color=self.color, rect=self.rect)

    def check_collission(self, entity: pygame.Rect) -> bool:
        """
            check_collission() is a function used to check collission between the object & the entity
            @parameters
                entity: a pygame.Rect object which is the x, y, width and height of the entity.
        """
        
        return self.rect.colliderect(entity)