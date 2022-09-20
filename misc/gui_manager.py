import imp


import pygame_gui
import pygame

class GuiManager:
    def __init__(self, surface: pygame.Surface):
        """
            The GUIManager class initializes the GUI and loads the menus needed to load
            @parameters
                surface: a pygame.Surface object meaning the surface / game window
        """
    
        self.surface = surface
        self.manager = pygame_gui.UIManager(window_resolution=surface.get_size())
        self.game_started = False
        self.startbtn = pygame_gui.elements.UIButton

    def gui_loop(self, clock_tick, event: pygame.event, mapeditor: bool = False):
        """
            The GUI loop is run in the main gameloop
            @parameters
                clock_tick: the current clock tick
                event: pygame.event, the pygame event
                mapeditor: bool if it should run the map editor gui or not
        """

        # 60 fps / 1000.0
        time_delta = clock_tick/1000.0

        self.manager.process_events(event=event)
        self.manager.update(time_delta=time_delta)
        self.manager.draw_ui(window_surface=self.surface)
    
        if not mapeditor:
            if not self.game_started:
                self.game_started = self.startbtn.check_pressed()

    def main_menu(self):
        """  main_menu() loads the start menu """
        startbtn_Rect = pygame.Rect((180, 200), (150, 50))
        self.startbtn = pygame_gui.elements.UIButton(relative_rect=startbtn_Rect, text="Start game",
                                                     manager=self.manager)
    
    def map_editor_text(self):
        text_rect = pygame.Rect((175, 25), (180, 50))
        pygame_gui.elements.UILabel(relative_rect=text_rect, text="Press S to save map", manager=self.manager)
        
        text_rect = pygame.Rect((175, 50), (180, 50))
        pygame_gui.elements.UILabel(relative_rect=text_rect, text="Press A for +brushsize", manager=self.manager)
        
        text_rect = pygame.Rect((175, 75), (180, 50))
        pygame_gui.elements.UILabel(relative_rect=text_rect, text="Press N for -brushsize", manager=self.manager)
        
        text_rect = pygame.Rect((175, 100), (180, 50))
        pygame_gui.elements.UILabel(relative_rect=text_rect, text="Press C for new shape", manager=self.manager)

