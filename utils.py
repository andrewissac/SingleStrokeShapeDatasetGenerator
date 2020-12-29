
def mkdir(path):
    import os
    if not os.path.exists(path):
        os.mkdir(path)


def mouseInRect(mx, my, rect):
    x, y, w, h = rect
    if (mx > x) & (mx < x + w):
        if (my > y) & (my < y + h):
            return True
    return False
