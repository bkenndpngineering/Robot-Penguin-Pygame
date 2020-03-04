import math
from constants import *

def rotate_point_to_yz_plane(x0, y0, z0, phi):
    # do rotation matrix
    x = x0 * math.cos(phi) + y0 * math.sin(phi)
    y = -x0 * math.sin(phi) + y0 * math.cos(phi)

    # z is the same
    z = z0
    return (x, y, z)

def compute_triple_inverse_kinematics(x, y, z):
    thetas = []
    for phi in phi_vals:
        (x0, y0, z0) = rotate_point_to_yz_plane(x, y, z, phi)
        theta = inverse_kinematics_in_yz_plane(x0, y0, z0)
        if theta == -1:
            raise ValueError('that point is impossible!')
        thetas.append(theta)
    return (thetas[0], thetas[1], thetas[2])


def forward_kinematics(theta1, theta2, theta3):

    # Finding J' points (centers of intersecting spheres)
    x1 = 0
    y1 = (f - e) / (2 * math.sqrt(3)) + rf * math.cos(math.radians(theta1))
    z1 = -rf * math.sin(math.radians(theta1))
    (x1, y1, z1) = rotate_point_to_yz_plane(x1, y1, z1, phi_vals[0])

    x2 = 0
    y2 = (f - e) / (2 * math.sqrt(3)) + rf * math.cos(math.radians(theta2))
    z2 = -rf * math.sin(math.radians(theta2))
    (x2, y2, z2) = rotate_point_to_yz_plane(x2, y2, z2, phi_vals[1])

    x3 = 0
    y3 = (f - e) / (2 * math.sqrt(3)) + rf * math.cos(math.radians(theta3))
    z3 = -rf * math.sin(math.radians(theta3))
    (x3, y3, z3) = rotate_point_to_yz_plane(x3, y3, z3, phi_vals[2])

    # Find intersection of 3 spheres
    w1 = x1 ** 2 + y1 ** 2 + z1 ** 2
    w2 = x2 ** 2 + y2 ** 2 + z2 ** 2
    w3 = x3 ** 2 + y3 ** 2 + z3 ** 2

    # Coefficients in EQN x = a1*z + b1
    dnm = (x3 - x1) * (y2 - y1) - (x2 - x1) * (y3 - y1)

    a1 = ((z2 - z1) * (y3 - y1) - (z3 - z1) * (y2 - y1))
    b1 = -((w2 - w1) * (y3 - y1) - (w3 - w1) * (y2 - y1)) / 2

    a2 = -((z2 - z1) * (x3 - x1) - (z3 - z1) * (x2 - x1))
    b2 = ((w1 - w2) * (x1 - x3) - (w1 - w3) * (x1 - x2)) / 2

    # Coefficients in Quadratic
    A = dnm ** 2 + a1 ** 2 + a2 ** 2
    B = 2 * (a1 * (b1 - x1 * dnm) + a2 * (b2 - y1 * dnm) - z1 * dnm ** 2)
    C = (b1 - x1 * dnm) ** 2 + (b2 - y1 * dnm) ** 2 + (z1 ** 2 - re ** 2) * dnm ** 2

    # Quadratic EQN
    disc = B ** 2 - 4 * A * C
    # discriminant < 0 -> no solution
    if disc < 0:
        return (-99, -99, -99)
    z = (-B - math.sqrt(disc)) / (2 * A)

    # Solve for x and y from z
    x = (a1 * z + b1) / dnm
    y = -(a2 * z + b2) / dnm

    # Fudge z for end effector height
    z = z - z0

    # GG EZ
    return (x, y, z)

def wrap_angle_rad(theta):
    while abs(theta) > math.pi:
        if theta < math.pi:
            theta += 2*math.pi
        if theta > math.pi:
            theta -= 2*math.pi
    return theta

def inverse_kinematics_in_yz_plane(x0,y0,z0):

    #linear coefficients of EQN z = b*y + a

    a = (x0**2 + (y0-e/(2*math.sqrt(3)))**2 + z0**2 + rf**2 - re**2 - f**2/12)/(2*z0)
    b = (-f/(2*math.sqrt(3)) - y0 + e/(2*math.sqrt(3)))/z0

    #plug line (z = b*y + a) into circle in yz w/ center (-f/2sqrt(3),0)

    disc = (f/math.sqrt(3) + 2*a*b) - 4*(b**2+1)*(f**2/12 + a**2 - rf**2)
    if disc < 0:
        #disciminate < 0 -> no solution
        return -1

    #compute solution w/ lower y value
    y = (-(f/math.sqrt(3) + 2*a*b) - math.sqrt(disc))/(2*(b**2+1))
    z = b*y + a

    theta = wrap_angle_rad(math.atan(z/(y + f/(2*math.sqrt(3)))))
    return math.degrees(theta)
