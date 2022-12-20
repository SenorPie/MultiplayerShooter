import pygame

class GameObject:
    def __init__(self, surface: pygame.Surface, rect: pygame.Rect, color: pygame.Color):
        """The GameObject class is used to draw and check collision with objects and entitys.
        @Parameters
            surface: pygame.Surface
                The game screen to draw on.
            rect: pygame.Rect
                The x, y, width and height of the object.
            color: pygame.Color
                The object's color.
        """

        self.surface = surface
        self.rect = rect
        self.color = color

    def draw_object(self):
        '''Draws the object upon the screen.'''
        pygame.draw.rect(surface=self.surface, color=self.color, rect=self.rect)

    def check_collission(self, entity: pygame.Rect) -> bool:
        """Function is used to check collission between the object & the entity.
        @Parameters
            entity: pygame.Rect
                Object which is the x, y, width and height of the entity.
        @Returns
            Entity collided with Object -> True
            Entity did not collide with object -> False
        """
        
        return self.rect.colliderect(entity)