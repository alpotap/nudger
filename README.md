# Nudger

Nudger is a tiny Windows utility that prevents the mouse cursor from staying fully idle by moving it a single pixel to the right every 3 minutes.

## What it does

- Runs continuously in a loop.
- Reads the current mouse cursor position.
- Moves the cursor by +1 on the X axis (right) while keeping Y unchanged.
- Waits 180 seconds (3 minutes).
- Repeats.

## Files

- `mouse_nudge.py`: Python script that performs the mouse movement using the Windows User32 API via `ctypes`.
- `start_mouse_nudge.bat`: Batch launcher that starts the Python script from the script directory.

## Requirements

- Windows
- Python 3 available as either `py -3` or `python`

## Run

From this folder, run:

```bat
start_mouse_nudge.bat
```

Or double-click `start_mouse_nudge.bat` in File Explorer.

## Stop

- If running in a terminal: press `Ctrl+C`.
- If launched from a command window: close the window.

## Notes

- Movement is intentionally minimal (1 pixel right only).
- The script does not move back left.
- It uses no external Python packages.
