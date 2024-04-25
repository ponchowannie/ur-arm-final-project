import socket
import time
import math

def gripper_open():
    # OPEN GRIPPER
    g.send(b'SET POS 0\n')
    time.sleep(0.5)

def gripper_close():
    # CLOSE GRIPPER 
    g.send(b'SET POS 255\n')
    time.sleep(0.5)

def move_to_home():
    s.send(b'movel(p[ .125, -.315, .0, 2.2, 2.2 , 0],0.2,0.2,2,0)\n')
    print('Moved to Home')
    time.sleep(1)

def movel(
    x: float = 0,
    y: float = 0,
    z: float = 0,
    rx: float = 0,
    ry: float = 0,
    rz: float = 0,
    acceleration: float = 1,
    velocity: float = 0.1,
    etime: float = 1.5,
    blend_radius: float = 0
):
    movel_cmd = f'movel(pose_add(get_actual_tcp_pose(),p[{x},{y},{z},{rx},{ry},{rz}]),{acceleration},{velocity},{etime},{blend_radius})\n'
    s.send(movel_cmd.encode(encoding='utf-8', errors='ignore'))
    time.sleep(etime)


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

# camera
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
c.connect((CAM_IP, CAM_PORT))

ti = 1
object_pos = c.recv(255).decode('utf-8')
print(object_pos)
dx, dy, dradian = 0, 0, 0
while [dx,dy,dradian] == [0,0,0]: # implement new logic here
    # recieve coordinates
    object_pos = c.recv(255).decode('utf-8')
    print(object_pos)
    if '[,,,,]' not in object_pos:
        pos_list = [x for x in object_pos[1:-1].split(',')]
        xm = float(pos_list[0])
        ym = float(pos_list[1])
        theta = float(pos_list[2])

        # in millimeters and radians
        # object_pos from cam - x is robot y
        # object_pos from cam - y is robot x
        dy = xm/1000
        dx = ym/1000 

        # gripper x offset = 0.175
        # gripper z offset = -0.225
        dx += 0.175

        # z to box
        dz= -0.225

        # offset is for speed
        dx -= 0.04 * ti
        # x to box
        dx -= 0.023
        dradian = theta%180*math.pi/180

print([dx,dy,dradian])

movel(x=dx, y=-dy, z=dz, etime=ti)
gripper_close()
movel(z=0.225)