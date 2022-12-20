import socket
import pickle
import random
import pygame
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 10000))

data = sock.recv(4096)
client_id = int.from_bytes(data, "little")
count = 0
while count < 300:
    rect = pygame.Rect((random.randrange(0, 500), random.randrange(0, 500)), (80, 80))
    data = [random.randrange(20, 50), rect]
    time.sleep(0.1)
    count += 1
    sock.send(pickle.dumps(data))