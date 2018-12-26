from pygame.constants import MOUSEBUTTONDOWN

def left_click(event):
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
            return True
    return False


def right_click(event):
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 3:
            return True
    return False

        