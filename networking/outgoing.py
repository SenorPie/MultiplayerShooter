import socket
import pickle
from cryptography.fernet import Fernet
from entity.player import Player

class OutgoingPacket:
    """Outgoing network traffic for data sent from client to server.
    @Methods
    send_playerpos(player)
        Sends a pickled object of the players client_id and position on map.
    """
    def __init__(self, server: socket.socket, client_id, rsa: Fernet):
        self.server = server
        self.client_id = client_id
        self.rsa = rsa

    # TODO: IMPLEMENT ENCRYPTION IN THE NETWORK, IMPLEMENT BORDERS, MAKE GAME WINDOW LARGER, IMPLEMENT SHOOTING
    # https://stackoverflow.com/questions/65042712/rsa-encryption-of-python-list
    # Encryption done with public/private key.
    def send_playerpos(self, player: Player):
        """Sends a position of the player to the server, client-server communication.
        @Parameters
            player: Player
                Create dictionary with player.player_rect and send the data pickled.
        """

        # Dictionary with our client & position
        data = [self.client_id, player.player_rect]

        # Send pickled data to
        self.server.send(pickle.dumps(data))