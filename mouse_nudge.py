import ctypes
import time

INTERVAL_SECONDS = 60  # Move mouse every 60 seconds
PIXELS_RIGHT = 2

# Windows API constants for mouse_event
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_KEYDOWN = 0x0002
MOUSEEVENTF_KEYUP = 0x0004

# Virtual key codes
VK_SHIFT = 0x10


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def get_cursor_pos() -> tuple[int, int]:
    point = POINT()
    if not ctypes.windll.user32.GetCursorPos(ctypes.byref(point)):
        raise OSError("GetCursorPos failed")
    return point.x, point.y


def mouse_event(flags: int, dx: int, dy: int, data: int = 0, extra: int = 0) -> None:
    """Generate a mouse event that Windows recognizes as user activity."""
    ctypes.windll.user32.mouse_event(flags, dx, dy, data, extra)


def keyboard_event(vk: int, flags: int = 0) -> None:
    """Generate a keyboard event that Windows recognizes as user activity."""
    ctypes.windll.user32.keybd_event(vk, 0, flags, 0)


def trigger_input_activity() -> None:
    """Generate input events to prevent sleep and Teams away status."""
    # Move mouse to generate input event (this is detected as real activity)
    mouse_event(MOUSEEVENTF_MOVE, PIXELS_RIGHT, 0)
    time.sleep(0.1)
    # Move back
    mouse_event(MOUSEEVENTF_MOVE, -PIXELS_RIGHT, 0)
    
    # Also send a harmless keyboard event (press and release Shift key)
    # This is less visible but helps ensure Teams and Windows detect activity
    keyboard_event(VK_SHIFT, 0)  # KEYDOWN
    time.sleep(0.05)
    keyboard_event(VK_SHIFT, 2)  # KEYUP (flag 2 = KEYEVENTF_KEYUP)


def main() -> None:
    print("Mouse nudge started - preventing Windows sleep and Teams away status")
    print(f"Activity will be triggered every {INTERVAL_SECONDS} seconds")
    
    while True:
        try:
            trigger_input_activity()
            time.sleep(INTERVAL_SECONDS)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()
