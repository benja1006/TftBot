from window import Window


def trPoint(x: int, y: int, window: Window) -> tuple:
    """Take a point coded for 2560x1440 and returns the transformed value."""
    base_width = 2560
    base_height = 1440

    new_y = y/base_height * window.height + window.y
    new_x = x/base_width * window.width + window.x

    return (new_x, new_y)

def get_round(window: Window):
    
