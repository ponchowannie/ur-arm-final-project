import socket
import time
import numpy as np
import math

def gripper_open():
    # OPEN GRIPPER
    g.send(b'SET POS 0\n')
    time.sleep(2)

def gripper_close():
    # CLOSE GRIPPER 
    g.send(b'SET POS 255\n')
    time.sleep(2)

def move_to_home():
    s.send(b'movel(p[.116,-.3,.2,0,-3.143,0],0.2,0.2,2,0)\n')
    time.sleep(1)

def move_to_starting_pos():
    # self.movej(x,y,z,rx,ry,rz,relative)
    pass

def movej(
    x: float = 0,
    y: float = 0,
    z: float = 0,
    rx: float = 0,
    ry: float = 0,
    rz: float = 0,
    acceleration: float = 1,
    velocity: float = 0.5,
    blend_radius: float = 0 
):
    movej_cmd = f'movej(pose_add(get_actual_tcp_pose(),p[{x},{y},{z},{rx},{ry},{rz}]),{acceleration},{velocity},{time},{blend_radius})'
    s.send(movej_cmd)
    time.sleep(1)

def movel(
    x: float = 0,
    y: float = 0,
    z: float = 0,
    rx: float = 0,
    ry: float = 0,
    rz: float = 0,
    acceleration: float = 1,
    velocity: float = 0.5,
    blend_radius: float = 0
):
    movel_cmd = f'movel(pose_add(get_actual_tcp_pose(),p[{x},{y},{z},{rx},{ry},{rz}]),{acceleration},{velocity},{time},{blend_radius})\n'
    s.send(movel_cmd)
    time.sleep(1)


# initializing
HOST = '10.10.0.14'
PORT = int
GRIPPER_PORT = int
CAM_PORT = int

# socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) test if it works, might not be needed
s.connect((HOST, PORT))

# gripper
g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
g.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
g.connect((HOST, GRIPPER_PORT))

# camera
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
c.connect((HOST, CAM_PORT))

dx, dy, dradian = 0, 0, 0
while [dx,dy,dradian] == [0,0,0]: # implement new logic here
    # recieve coordinates
    object_pos = c.recv(255).decode('utf-8')
    pos_list = [x for x in object_pos.split(',')]
    xm = pos_list[0]
    ym = pos_list[1]
    theta = pos_list[2]

    # in millimeters and radians
    dx = xm/1000
    dy = ym/1000 
    dradian = theta%180*math.pi/180

# set starting position for ur-arm
move_to_home()

# move ur-arm relatively
movej(x=dx, y=dy, rz=dradian)
movel(y=0.01,z=-0.32) # measure offset of conveyor movement