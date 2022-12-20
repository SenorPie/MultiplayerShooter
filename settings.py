import os
import logging
from dotenv import load_dotenv


class Settings:
    '''Settings is used universally by both the Server and the Client to get env variables.'''
    def __init__(self):
        load_dotenv()

        # Server related
        self.host = os.getenv("HOST")
        self.port = int(os.getenv("PORT"))

        # Game window related
        self.game_title = os.getenv("GAME_TITLE")
        self.window_size = (int(os.getenv("WIDTH")), int(os.getenv("HEIGHT")))

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s',
                            handlers=[logging.FileHandler("game.log"), logging.StreamHandler()])
