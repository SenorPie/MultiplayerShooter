import os
from dotenv import load_dotenv


class Settings:
    def __init__(self):
        load_dotenv()

        # Database related
        self.db_name = os.getenv("DB_NAME")

        # Game window related
        self.game_title = os.getenv("GAME_TITLE")
        self.window_size = (int(os.getenv("WIDTH")), int(os.getenv("HEIGHT")))