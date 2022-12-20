import pygame

class Eventhandler:
    """Eventhandler is used in our game loop to seperate code and have a structure for events.
    @Methods
        @staticmethod
        get_events() -> pygame.event 
            returns all events in pygame.event.get().
    """
    @staticmethod
    def get_events() -> pygame.event:
        for event in pygame.event.get():
            return event