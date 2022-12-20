import pygame
import sys
import logging
import threading
from networking.network import Network
from networking.outgoing import OutgoingPacket
from networking.networkcrypt import NetworkEncryption
from misc.eventhandler import Eventhandler
from misc.gui_manager import GuiManager
from entity.player import Player
from settings import Settings

class Client:
    """Main file for the game.
    @Attributes
    clock: pygame.Clock
        Clock to set framerate with.
    connected: bool
        True/False based on if connection succeds..
    client_id: int
        Unique identifier for our client.
    -----------
    @Methods
    draw_others()
        Draws all other players connected.
    main()
        Main loop for client-side.
    """

    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Initialize the fps clock & our screen
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.window_size)
        pygame.display.set_caption(self.settings.game_title)

        # Initialize GUI manager
        self.gui_manager = GuiManager(surface=self.screen)

        # Initialize networking
        self.network = Network()
        self.connected = False
        self.client_id = None

        # Initialize encryption for RSA
        self.rsa = NetworkEncryption()
    
    def draw_others(self):
        '''Draws other players that are connected.'''

        # For key: client_id, value: other/online_player
        for client_id, o_player in self.network.players.items():
            # If the connected client has not received a screen to be drawn on
            if o_player.surface != self.screen:
                # Set new surface and log info
                logging.info(f"{client_id} does not have a surface.")
                o_player.surface = self.screen
            
            # Draw player now
            o_player.draw_player()
            
    def main(self):
        '''The main loop running the game client.'''
        
        # Initialize our player
        player = Player(surface=self.screen)

        # Initialize main_menu/startBtn UI element
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
                if not self.connected:
                    # Connect to server and change our boolean
                    self.connected = self.network.connect_server(host=self.settings.host,
                                                                 port=self.settings.port)

                    # Get our client id and change our client_id
                    self.client_id = self.network.get_clientid()

                    # Initialize OutgoingPacket class for sending packets
                    self.outgoing = OutgoingPacket(server=self.network.sock,
                                                   client_id=self.client_id,
                                                   rsa=self.rsa)
                    
                    # Start our thread to receive packets from the server
                    self.receive_thread = threading.Thread(target=self.network.receive_thread, args=(self.connected,))
                    self.receive_thread.start()
                
                # Fill the surface with black color so our player rect doesnt overlap
                self.screen.fill(color=(0, 0, 0))
                
                # Draw other players
                self.draw_others()

                # Draw & move our local player, also send new position to server
                player.draw_player()
                player.move_player()
                self.outgoing.send_playerpos(player=player)

            # Null check to be able to exit peacefully out of client
            if event is not None and event.type == pygame.WINDOWCLOSE:

                # If we are still connected
                if self.connected:
                    # End all network & thread related things.
                    self.network.close()
                    self.connected = False
                    self.receive_thread.join()

                # System exit
                sys.exit()
            
            # Update display
            pygame.display.update()
    

if __name__ == "__main__":
    Client().main()