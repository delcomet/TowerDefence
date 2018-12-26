from math import sqrt
from math import acos
from math import degrees


def plus(list1, list2):
    a = [list1[0] + list2[0], list1[1] + list2[1]]
    return a


def dotp(list1, list2):
    a = list1[0] * list2[0] + list1[1] * list2[1]
    return a




def times(scalar, list1):
    a = [x * scalar for x in list1]
    return a




def reverse(list1):
    a = [-list1[0], -list1[1]]
    return a


def mag(list1):
    a = sqrt(dotp(list1, list1))
    return a


def proj(list1, list2):
    scalar = dotp(list1, list2) / dotp(list2, list2)
    a = times(scalar, list2)
    return a


def comp(list1, list2):
    a = dotp(list1, list2) / mag(list2)
    return a


def distance(end_pos, start_pos):
    distance_vector = [end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]]
    return distance_vector


def angle(vector1, vector2):
    dot_product = dotp(vector1, vector2)
    mag1 = mag(vector1)
    mag2 = mag(vector2)
    a = dot_product / (mag1*mag2)
    angle_radians = acos(a)
    angle_degrees = degrees(angle_radians)
    return angle_degrees

def unit(vector):
    return times(1/mag(vector), vector)

def perpendicular(list1):
    x, y = list1
    list2 = [-y, x]
    assert dotp(list1, list2) == 0
    return unit(list2)
