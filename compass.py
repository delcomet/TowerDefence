# [x, y]

UP = [0, -1]
DOWN = [0, 1]
LEFT = [-1, 0]
RIGHT = [1, 0]

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

def get_direction(speed_vector=[0, 0]):
    if speed_vector == [0, 0]:
        return speed_vector
    elif speed_vector[0] == 0 and speed_vector[1] > 0:
        return DOWN
    elif speed_vector[0] == 0 and speed_vector[1] < 0:
        return UP
    elif speed_vector[0] < 0 and speed_vector[1] == 0:
        return LEFT
    elif speed_vector[0] > 0 and speed_vector[1] == 0:
        return RIGHT
        