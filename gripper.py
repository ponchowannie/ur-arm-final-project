# import socket
# import time

# class Gripper:

#     # gripper
#     def __init__(self):
#         self.HOST = '10.10.0.14'
#         self.GRIPPER_PORT = 63352

#     def gripper_connect(self):
#         #Socket communication
#         g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         g.connect((self.HOST, self.GRIPPER_PORT))
#         g.sendall(b'GET POS\n')
#         g_recv = str(g.recv(10), 'UTF-8')
#         if g_recv :
#             g.send(b'SET ACT 1\n')
#             g_recv = str(g.recv(10), 'UTF-8')
#             print (g_recv)
#             time.sleep(3)
#             g.send(b'SET GTO 1\n')
#             g.send(b'SET SPE 255\n')
#             g.send(b'SET FOR 255\n')
#             print ('Gripper Activated')