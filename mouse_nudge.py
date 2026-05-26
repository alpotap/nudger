import ctypes
import time
from datetime import datetime, time as dt_time, timedelta

INTERVAL_SECONDS = 60  # Move mouse every 60 seconds
PIXELS_RIGHT = 2
AUTO_STOP_TIME = dt_time(hour=18, minute=0)

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


def get_session_stop_time(started_at: datetime | None = None) -> datetime:
    """Return the stop time for this launch.

    - If started before 18:00, stop at 18:00 today.
    - If started at/after 18:00, run until midnight (00:00 next day).
    """
    start_time = started_at or datetime.now()
    stop_today = datetime.combine(start_time.date(), AUTO_STOP_TIME)
    if start_time < stop_today:
        return stop_today
    return datetime.combine(start_time.date(), dt_time.min) + timedelta(days=1)


def seconds_until_stop(stop_at: datetime, now: datetime | None = None) -> float:
    """Return remaining seconds until the given stop time."""
    current = now or datetime.now()
    return max(0.0, (stop_at - current).total_seconds())


def main() -> None:
    started_at = datetime.now()
    stop_at = get_session_stop_time(started_at)
    print("Mouse nudge started")
    
    while True:
        if datetime.now() >= stop_at:
            print("Stopped")
            break

        try:
            trigger_input_activity()
            sleep_seconds = min(float(INTERVAL_SECONDS), seconds_until_stop(stop_at))
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)
        except Exception as e:
            print(f"Error: {e}")
            sleep_seconds = min(5.0, seconds_until_stop(stop_at))
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)


if __name__ == "__main__":
    main()
