import threading
import socket
import logging
import pickle
from settings import Settings
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Create a threading lock to synchronize access to shared resources
lock = threading.Lock()

class ThreadedServer(object):
    """ThreadedServer is as the name suggests, a threaded server.
    @Attributes
    sock: socket
        TCP/IP socket to accept connections from.
    clients: list
        List of clients connected to socket.
    client_id: int
        Number sent to client on-join, increments with 1 after each client.
    -----------
    @Methods
    listen()
        Listens for new connections, starts thread on new connection.
    client_handler(client, address)
        Takes care of data coming in from clients as well as data going back out.
    """

    def __init__(self):
        # Load our settings and RSA encryption
        settings = Settings()

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the host and port
        self.sock.bind((settings.host, settings.port))

        # Create a list to store the connected clients
        self.clients = []

        # A integer that increments after client connection, this is so our clients each get a unique key
        self.client_id = 1

        # Load private key
        self.private_key = self.load_privkey()

    def listen(self):
        '''Listen for new connections, sends client_id to server and then starts a new thread.'''
       
        # Start listening for incoming connections
        self.sock.listen()
        logging.info("Server has started")

        while True:
            # Accept an incoming connection
            client, address = self.sock.accept()
            logging.info("New connection to server")

            # Send the 'client_id' to our connected client and increment self.client_id
            client.send(self.client_id.to_bytes(5, "little"))
            self.client_id += 1

            # Add the client to the list of connected clients
            self.clients.append(client)

            # Create a new thread to handle the connection
            client_thread = threading.Thread(target=self.client_handler, args=(client, address))

            # Start the new thread
            client_thread.start()
            logging.info("Thread has been started on server for new connection")

    def client_handler(self, client: socket.socket, address):
        """Receives data from client and send data to client(s)
        @Parameters
            client : socket
                The socket connection provided when a user connects
            
            address : _RetAddress
                The address provided when a user connects
        """

        while True:
            try:
                # Receive data from the client
                data = client.recv(4096)

                # If the client has disconnected, remove it from the list of connected clients
                if not data:
                    logging.info("Client has disconnected, removing them from server.")
                    self.clients.remove(client)
                    client.close()
                    break

                # Forward the message to all other connected clients
                for c in self.clients:
                    if c != client:
                        # Decrypt data with our RSA private key
                        decrypted_data = self.decrypt_data(data)
                        print(decrypted_data)
                        c.send(decrypted_data)

            # If a client is abruptetly disconnected do the following to ensure the server's stability
            except ConnectionResetError:
                logging.info("Client has disconnected, removing them from server.")
                self.clients.remove(client)
                client.close()
                break

    def load_privkey(self):
        '''Load private key from file saved in folder /keys'''
        with open("keys/private_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(),
                                                             password=b'8hPr2q2ntPMXQ2dPAfqJxGyyrH2U*XI(hIEnaHNHC&vTwWJNVX9KqYRwrem2WmPZ')
            return private_key

    def decrypt_data(self, encrypted_data) -> str:
        """Decrypts the encrypted_data signed by the RSA public_key
        @Parameters
            encrypted_data: bytes
                Contains the encrypted data that needs to be decrypted server sided by the private key
        """
        
        plaintext = self.private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None))
    
        return plaintext

if __name__ == "__main__":
    # Create a ThreadedServer instance
    server = ThreadedServer()
    
    # Start the server
    server.listen()