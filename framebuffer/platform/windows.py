import ctypes
import os
from ctypes import c_int
from ctypes import wintypes
from typing import Literal

import numpy
from framebuffer.math.linalg import Vector

type RegisteredKey = Literal["w", "a", "s", "d", "space", "shift"]


class POINT(ctypes.Structure):
    _fields_ = [("x", c_int), ("y", c_int)]


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", ctypes.c_long),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", ctypes.c_char * 260),
    ]


class WindowsInterface:
    @staticmethod
    def get_window_size() -> tuple[int, int]:
        width: int = ctypes.windll.user32.GetSystemMetrics(0)
        height: int = ctypes.windll.user32.GetSystemMetrics(1)

        return width, height

    @staticmethod
    # TODO [severity 4/5, effort 1/5]: Handle zero mouse displacement before normalization.
    def get_mouse_update() -> Vector[numpy.float64]:
        width, height = WindowsInterface.get_window_size()
        pt: POINT = POINT()

        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        ctypes.windll.user32.SetCursorPos(width // 2, height // 2)
        mouse_position: Vector[numpy.float64] = numpy.array(
            [pt.x - width // 2, pt.y - height // 2], dtype=numpy.float64
        )

        return mouse_position / numpy.linalg.norm(mouse_position)

    @staticmethod
    # TODO [severity 3/5, effort 1/5]: Report all declared keys, including space and shift.
    def get_key_update() -> dict[RegisteredKey, bool]:
        return {
            "w": ctypes.windll.user32.GetKeyState(87) < 0,
            "a": ctypes.windll.user32.GetKeyState(65) < 0,
            "s": ctypes.windll.user32.GetKeyState(83) < 0,
            "d": ctypes.windll.user32.GetKeyState(68) < 0,
        }

    @staticmethod
    # TODO [severity 3/5, effort 2/5]: Cache process ancestry instead of snapshotting per component.
    # TODO [severity 4/5, effort 2/5]: Declare Win32 argument/result types and close handles in finally.
    def get_game_is_active_window() -> bool:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        foreground_pid = wintypes.DWORD()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(foreground_pid))
        snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot(0x00000002, 0)
        entry: PROCESSENTRY32 = PROCESSENTRY32()
        entry.dwSize = ctypes.sizeof(PROCESSENTRY32)
        parent_map: dict[int, int] = {}

        if ctypes.windll.kernel32.Process32First(snapshot, ctypes.byref(entry)):
            while True:
                parent_map[entry.th32ProcessID] = entry.th32ParentProcessID

                if not ctypes.windll.kernel32.Process32Next(snapshot, ctypes.byref(entry)):
                    break

        ctypes.windll.kernel32.CloseHandle(snapshot)

        pid: int = os.getpid()
        visited: set[int] = set()

        while pid and pid not in visited:
            if pid == foreground_pid.value:
                return True

            visited.add(pid)

            if pid not in parent_map:
                break

            pid = parent_map[pid]

        return False
