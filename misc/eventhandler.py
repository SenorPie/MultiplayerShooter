import pygame

class Eventhandler:
    """
        Eventhandler is used to get the pygame events with the static method
        @get_events() -> returns a pygame.Event
    """
    @staticmethod
    def get_events() -> pygame.event:
        for event in pygame.event.get():
            return event