import pygame_gui
import pygame

class GuiManager:
    def __init__(self, surface: pygame.Surface):
        """The GUIManager class initializes the GUI and loads the menus needed to load.
        @Parameters
            surface : pygame.Surface
                The game window / client.screen
        """

        # Set self.surface
        self.surface = surface

        # Initialize GUI_manager and startBtn
        self.manager = pygame_gui.UIManager(window_resolution=surface.get_size())        
        self.startbtn = pygame_gui.elements.UIButton

        self.game_started = False

    def gui_loop(self, clock_tick: int, event: pygame.event, mapeditor: bool = False):
        """This loop is run within the client's main loop.
        @Parameters
            clock_tick: int
                No explaniation, check docs.
            event: pygame.event
                Pygame event object.
            mapeditor: bool
                If we want to run the mapeditor.
        """

        # 60 fps / 1000.0
        time_delta = clock_tick/1000.0

        self.manager.process_events(event=event)
        self.manager.update(time_delta=time_delta)

        # Draw our UI
        self.manager.draw_ui(window_surface=self.surface)
    
        if not mapeditor:
            # If check incase start_btn is pressed.
            if not self.game_started:
                self.game_started = self.startbtn.check_pressed()

    def main_menu(self):
        '''This function loads the start menu.'''
        startbtn_Rect = pygame.Rect((180, 200), (150, 50))
        self.startbtn = pygame_gui.elements.UIButton(relative_rect=startbtn_Rect, text="Start game",
                                                     manager=self.manager)
    
    def map_editor_text(self):
        '''This function loads the map editor menu.'''
        text_rect = pygame.Rect((175, 25), (180, 50))
        pygame_gui.elements.UILabel(relative_rect=text_rect, text="Press S to save map", manager=self.manager)
        
        text_rect = pygame.Rect((175, 50), (180, 50))
        pygame_gui.elements.UILabel(relative_rect=text_rect, text="Press A for +brushsize", manager=self.manager)
        
        text_rect = pygame.Rect((175, 75), (180, 50))
        pygame_gui.elements.UILabel(relative_rect=text_rect, text="Press N for -brushsize", manager=self.manager)
        
        text_rect = pygame.Rect((175, 100), (180, 50))
        pygame_gui.elements.UILabel(relative_rect=text_rect, text="Press R to reset", manager=self.manager)
