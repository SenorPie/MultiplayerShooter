import socket
import pickle
import logging
from entity.player import Player

class Network:
    def __init__(self):
        '''Initialize network class.'''
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players = {}

    def close(self):
        '''Close socket connectiton.'''
        self.sock.close()

    def connect_server(self, host: str, port: int) -> bool:
        """Connects to our TCP server.
        @Parameters
            host: str
                Ip of our host
            port: int
                Port of our host
        -----------
        @Returns
            Client connection succesful -> True
            Client connection failed -> False
        """

        try:
            # Connect to the server
            self.sock.connect((host, port))
            
            # Log that we connected to the server.
            logging.info("Succesfully connected to server.")

            # Return true as we completed connection
            return True
        except ConnectionError as e:
            # Log error
            logging.error(e)

            # Return false if we fail to connect to the server.
            return False
    
    def get_clientid(self) -> int:
        '''Decodes the integer provided by the server, this is our unique identifier that other clients recognize.'''
        # Receive data from server
        data = self.sock.recv(4096)

        # Convert data from bytes to integer
        client_id = int.from_bytes(data, "little")

        # Check if it is an instance of an integer, if so, return client_id
        if isinstance(client_id, int):
            logging.info(f"Received client_id from server: {client_id}")
            return client_id
        else:
            logging.error(f"Received client_id in other format than int: {client_id}")

    def receive_thread(self, connected: bool):
        """Function started after connection and client_id assignment, takes care of incoming data.
        @Parameters
            connected: bool
                True/False value passed on from the client to know if we have connected.
        """

        # After we got the clientid, we start this thread.
        while connected:
            try:
                # Receive our data
                data = self.sock.recv(4096)
            except ConnectionError:
                logging.info("Connection error to server, did you disconnect?")
                break

            # If the connection has been closed, break out of the loop
            if not data:
                break
            
            try:
                server_data, data_type = self.msg_or_data(data=data)
                if data_type == "pickle":
                    client_id, rect = server_data
                    player = self.players.get(client_id)

                    if player:
                        player.player_rect = rect
                        self.players.update({client_id: player})
                    else:
                        new_player = Player()
                        new_player.player_rect = rect
                        self.players[client_id] = new_player
            except:
                logging.warning("Error decoding data...")
            
    def msg_or_data(self, data: bytes):
        """Decodes what our receive_thread gets, decoding a text differniates a lot to decoding a pickle object.
        @Parameters
            data: bytes 
                Data received from the server.
        -----------
        @Returns
            Decode message -> data: str, data_type="msg"
            Decode pickle -> data: bytes, data_type="pickle"
        """

        data_type = None
        
        try:
            data = data.decode("utf-8")
            data_type = "msg"
            return data, data_type
        except UnicodeDecodeError:
            logging.warning("Data received to client is not a message, decoding as pickle")
        
        try:
            data = pickle.loads(data)
            data_type = "pickle"
            return data, data_type
        except Exception:
            logging.warning("Data received to client is not a pickle object, ERROR!")