import numpy as np
from pyquaternion import Quaternion

# ----------------------------------- given once in the beginning - position of lighthouse base station as a vector
L_station_x = float(input("L_station_x: "))
L_station_y = float(input("L_station_y: "))
L_station_z = float(input("L_station_z: "))
# -----------------------------------
R_station_x = float(input("R_station_x: "))
R_station_y = float(input("R_station_y: "))
R_station_z = float(input("R_station_z: "))
# -----------------------------------
stations = {"L": (L_station_x, L_station_y, L_station_z),
            "R": (R_station_x, R_station_y, R_station_z)}
vert_axis = []
hrzn_axis = []
res = []
last_pose = None

def rotate(alpha, axis, x):
    """
    Takes in an angle in radians, an axis, and a vector
    Returns a rotated vector
    """
    rotated_x = Quaternion(axis=axis, angle=alpha).rotate(x)
    return rotated_x

def planeprojection(x, LH_update):
    """
    Takes in a datapoint from the IMU and an update from a lighthouse base station
    Returns the datapoint projected on the plane defined by the LH update
    """

    phi = LH_update[0]
    theta = LH_update[1]
    station = LH_update[2]
    p = stations[station]
    lighthouse_normal = station[1] # vector representing the lighthouse station orientation
    axis = vert_axis
    lighthouse_normal = rotate(phi, axis, lighthouse_normal)
    axis = hrzn_axis
    lighthouse_normal = rotate(theta, axis, lighthouse_normal)
    #dot product of position vector to the vertex from plane and normal vector
    dotscalar = np.dot(np.subtract(x, p), lighthouse_normal)
    #now returning the position vector of the projection onto the plane
    return np.subtract(x, dotscalar * lighthouse_normal)


def get_pose(last_pose, acc_update = None, gyro_update = None, LH_update = None):
    """
    Takes in datapoints from accelerometer, gyroscope and lighthouse basestation 
    Assumes that acc and gyro updates are synchronized and will be called every time we receive a pair (acc,gyro)
    Applies filtering on the IMU data and afterwards, if an update from a LH base station is available, 
    will project the result on the corresponding plane
    Returns a predicted pose
    """
    # get pose x from acc_update and gyro_update

    # TODO
    # https://github.com/KalebKE/AccelerationExplorer
    # assume we get a tuple of position and orientation (x,o)
    x = [1,1,1]
    if LH_update:
        x = planeprojection(x, LH_update)
        #project pose x to the plane
    return pose



while True:
    #get stream of sensor data
    # ----------------------------------- read from sensor output, either from file or online
    ddx = float(input("ddx: "))
    ddy = float(input("ddy: "))
    ddz = float(input("ddz: "))
    ACC_UPDATE = (ddx,ddy,ddz)
    
    pitch = float(input("pitch: "))
    roll = float(input("roll: "))
    yaw = float(input("yaw: "))
    GYRO_UPDATE = (pitch, roll, yaw)

    gamma = float(input("gamma: "))
    phi = float(input("phi: "))
    station = input("station: ")
    LH_UPDATE = (gamma, phi, station)
    # ----------------------------------- 

    acc_update = ACC_UPDATE
    gyro_update = GYRO_UPDATE
    LH_update = LH_UPDATE
    pose = get_pose(last_pose, acc_update, gyro_update, LH_update)
    res.append(pose)
    last_pose = pose.copy(deep = True)
    print(res)
    # plot coords
