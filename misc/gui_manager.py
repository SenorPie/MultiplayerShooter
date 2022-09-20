import imp


import pygame_gui
import pygame

class GuiManager:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.manager = pygame_gui.UIManager(window_resolution=surface.get_size())
        self.main_menu()
        self.game_started = False

    def gui_loop(self, clock_tick, event: pygame.event):
        # 60 fps / 1000.0
        time_delta = clock_tick/1000.0

        self.manager.process_events(event=event)
        self.manager.update(time_delta=time_delta)

        if not self.game_started:
            self.game_started = self.startbtn.check_pressed()


        self.manager.draw_ui(window_surface=self.surface)
    
    def main_menu(self):
        startbtn_Rect = pygame.Rect((180, 200), (150, 50))
        self.startbtn = pygame_gui.elements.UIButton(relative_rect=startbtn_Rect, text="Start game",
                                                     manager=self.manager)