import pygame

class Item:
    def __init__(self, item_id: int):
        """
            The Item class is used for declaring what item the player has
            @parameters
                item_id: an integer which determines what type of item they have
                         the item_id is checked against our MYSQL database
        """

        self.item_id = item_id
    
    def get_itemrect(self, player_pos: tuple, offset: int) -> pygame.Rect:
        """
            get_itemrect() returns a pygame.Rect object
            @parameters
                player_pos: the position of the player
                offset: the offset of the item
        """
        
        return pygame.Rect((player_pos[0] + offset * 2, player_pos[1] + offset), (20, 10))
