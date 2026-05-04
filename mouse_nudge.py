import ctypes
import time

INTERVAL_SECONDS = 180
PIXELS_RIGHT = 1


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def get_cursor_pos() -> tuple[int, int]:
    point = POINT()
    if not ctypes.windll.user32.GetCursorPos(ctypes.byref(point)):
        raise OSError("GetCursorPos failed")
    return point.x, point.y


def set_cursor_pos(x: int, y: int) -> None:
    if not ctypes.windll.user32.SetCursorPos(x, y):
        raise OSError("SetCursorPos failed")


def main() -> None:
    while True:
        x, y = get_cursor_pos()
        set_cursor_pos(x + PIXELS_RIGHT, y)
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
