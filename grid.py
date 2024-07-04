
def init(screen):
    WIDTH, HEIGHT = screen.width, screen.height


def get_grid_square(pos):
    if not isinstance(pos, tuple) or len(pos) != 2:
        raise ValueError("Input must be a tuple with two elements (x, y).")
    x, y = pos
    grid_x, grid_y = x // 80, y // 80
    return grid_x, grid_y
