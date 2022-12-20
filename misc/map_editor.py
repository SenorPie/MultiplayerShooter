from eventhandler import Eventhandler
from gui_manager import GuiManager
import sys
import json
import pygame

class MapEditor:
    def __init__(self):
        '''MapEditor is a universal class used for drawing & showing the brush cursor.'''
        # Radius is to dictate the size of the circle
        self.radius = 30

        # Position is to dictate the starting position (center) of the circle
        self.position = (255, 255)

        # Color is for showing the player the cursor of the circle they are moving
        self.color = (255, 0, 0)

        # Array to keep what the player has drawn
        self.drawn_area = []

    def mouse_motion(self, event: pygame.event):
        """This function displays where the user is hovering their cursor.
        @Parameters
            event : pygame.event.
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
        '''Draw where the cursor is hovered and append to array "drawn_area"'''

        for drawn in self.drawn_area:
            pygame.draw.circle(surface=self.surface, color=drawn[0],
                               center=drawn[1], radius=drawn[2])
    
    def save_map(self, color, position, radius):
        with open(file="objects.json") as fp:
            list_obj = json.load(fp)

        object_dict = {"color": color, "position": position, "radius": radius}        
        list_obj.append(object_dict)
        new_list_obj = json.dumps(list_obj, indent=4, sort_keys=True)

        with open(file="objects.json", mode="w") as f:
            f.write(new_list_obj)
    
    def load_map(self):
        with open("objects.json") as f:
            list_obj = json.load(f)
            
            for object in list_obj:
                self.drawn_area.append((object.get("color"), object.get("position"), object.get("radius")))
        
        self.draw()

    def keybinds(self, event: pygame.event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                for object in self.drawn_area:
                    self.save_map(color=object[0], position=object[1], radius=object[2])
            elif event.key == pygame.K_a:
                self.radius += 5
            elif event.key == pygame.K_n:
                self.radius -= 5
            elif event.key == pygame.K_r:
                self.drawn_area.clear()

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
        self.load_map()

        # The main client loop
        while True:
            # Set framerate to tick at 60 fps
            fps_tick = self.clock.tick(60)

            # Eventhandler to get events
            event = Eventhandler.get_events()
            self.mouse_motion(event=event)
        
            # Null check to be able to exit peacefully out of client
            if event is not None and event.type == pygame.WINDOWCLOSE:
                sys.exit()
            
            # Start the GUI loop
            if event is not None:
                self.keybinds(event=event)
                self.gui_manager.gui_loop(clock_tick=fps_tick, event=event, mapeditor=True)

            # Update display
            pygame.display.update()

if __name__ == "__main__":
    MapEditor().main()