import pygame
import sys
from misc.eventhandler import Eventhandler
from misc.gui_manager import GuiManager
from entity.player import Player
from settings import Settings

class Client:
    def __init__(self):
        """
            Client is the class used for handling the main loop and also initializing the @screen
            @parameters
                window_size:
                    type: tuple (width, height)
                    description: Size of the window
        """

        # Initialize pygame
        pygame.init()

        # Initialize the fps clock & our screen
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.window_size)
        pygame.display.set_caption(self.settings.game_title)

        # Initialize GUI manager
        self.gui_manager = GuiManager(surface=self.screen)

    def main(self):
        """ The main loop running the game client """
        
        player = Player(surface=self.screen)
        self.gui_manager.main_menu()

        # The main client loop
        while True:
            # Set framerate to tick at 60 fps
            fps_tick = self.clock.tick(60)

            # Eventhandler to get events
            event = Eventhandler.get_events()

            # Start the GUI loop
            if event is not None:
                self.gui_manager.gui_loop(clock_tick=fps_tick, event=event)

            # If the start_button has been pressed, start the game
            if self.gui_manager.game_started:
                player.draw_player()
                player.move_player()
        
            # Null check to be able to exit peacefully out of client
            if event is not None and event.type == pygame.WINDOWCLOSE:
                sys.exit()
            
            # Update display
            pygame.display.update()
    

if __name__ == "__main__":
    Client().main()