# import socket
# import time

# class Camera:

#     # gripper
#     def __init__(self):
#         self.CAM_IP = '10.10.1.10'
#         self.CAM_PORT = 2024

#     def camera_connect(self):
#         # camera
#         c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         # c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         c.connect((self.CAM_IP, self.CAM_PORT))
