from eventhandler import Eventhandler
from gui_manager import GuiManager
import sys
import pygame

class MapEditor:
    def __init__(self):
        """
            MapEditor is a universal class used for drawing & showing the brush cursor.
            This is used to design the maps which are added onto the MYSQL Database containing the drawn objects

            @parameters
                surface:
                    type: pygame.Surface            
        """

        # Radius is to dictate the size of the circle
        self.radius = 30

        # Position is to dictate the starting position (center) of the circle
        self.position = (255, 255)

        # Color is for showing the player the cursor of the circle they are moving
        self.color = (255, 0, 0)

        # Array to keep what the player has drawn
        self.drawn_area = []

    def mouse_motion(self, event: pygame.event):
        """ mouse_motion is a to show the player their current position for them to draw with
            @parameters
                event: 
                    type: pygame.Event
        """

        if event is None: return
        
        if event.type == pygame.MOUSEMOTION:
            # Set circle pos = mouse cursor pos
            self.position = event.pos

            # Reset the screen so the circle doesn't skribble the entire page without them wanting to draw
            self.surface.fill((0, 0, 0))

            # Redraw the drawn areas
            self.draw()
        
            # Draw our circle with respective values
            pygame.draw.circle(surface=self.surface, color=self.color,
                               center=self.position, radius=self.radius)
        
        # Get left click button press
        left_mousebtn = pygame.mouse.get_pressed()[0]
        if left_mousebtn:
            # Append an object with the color, position and size of the drawn object
            self.drawn_area.append((self.color, self.position, self.radius))

    def draw(self):
        """
            draw(): draws the user drawn circles that are appended into the array @drawn_area
            whenever a user holds down mouse_btn left
        """

        for drawn in self.drawn_area:
            pygame.draw.circle(surface=self.surface, color=drawn[0],
                               center=drawn[1], radius=drawn[2])
    

    def main(self):
        """ The client loop for the pygame. """
        pygame.init()
        
        # Initialize the fps clock & our screen
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Map editor")

        # Initialize GUI manager
        self.gui_manager = GuiManager(surface=self.surface)
        self.gui_manager.map_editor_text()

        # The main client loop
        while True:
            # Set framerate to tick at 60 fps
            fps_tick = self.clock.tick(60)

            # Get the key press and append or remove to the radius.
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.radius += 5
            elif keys[pygame.K_n]:
                self.radius -= 5
            elif keys[pygame.K_r]:
                self.drawn_area.clear()

            # Eventhandler to get events
            event = Eventhandler.get_events()
            self.mouse_motion(event=event)
        
            # Null check to be able to exit peacefully out of client
            if event is not None and event.type == pygame.WINDOWCLOSE:
                sys.exit()
            
            # Start the GUI loop
            if event is not None:
                self.gui_manager.gui_loop(clock_tick=fps_tick, event=event, mapeditor=True)

            # Update display
            pygame.display.update()

if __name__ == "__main__":
    MapEditor().main()