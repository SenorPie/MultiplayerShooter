import pygame

class Eventhandler:
    @staticmethod
    def get_events() -> pygame.event:
        for event in pygame.event.get():
            return event