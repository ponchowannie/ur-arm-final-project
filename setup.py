import socket
import time

# initializing
HOST = '10.10.0.14'
PORT = 30003
GRIPPER_PORT = 63352
CAM_IP = '10.10.1.10'
CAM_PORT = 2024

# socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) test if it works, might not be needed
s.connect((HOST, PORT))

# gripper
g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
g.connect((HOST, GRIPPER_PORT))

def move_to_home():
    s.send(b'movel(p[ .125, -.315, .0, 2.2, 2.2 , 0],0.2,0.2,2,0)\n')
    print('Moved to Home')
    time.sleep(1)

# gripper
def gripper_connection() :
   #Socket communication
   g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   g.connect((HOST, GRIPPER_PORT))
   g.sendall(b'GET POS\n')
   g_recv = str(g.recv(10), 'UTF-8')
   if g_recv :
      g.send(b'SET ACT 1\n')
      g_recv = str(g.recv(10), 'UTF-8')
      print (g_recv)
      time.sleep(3)
      g.send(b'SET GTO 1\n')
      g.send(b'SET SPE 255\n')
      g.send(b'SET FOR 255\n')
      print ('Gripper Activated')

def gripper_open():
    # OPEN GRIPPER
    g.send(b'SET POS 0\n')
    time.sleep(0.5)

gripper_connection()
gripper_open()
move_to_home()
time.sleep(1)