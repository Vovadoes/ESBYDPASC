import ctypes
import win32api
from screeninfo import get_monitors

PROCESS_PER_MONITOR_DPI_AWARE = len(get_monitors())
MDT_EFFECTIVE_DPI = 0


def round_custom(num, step):
    return round(num / step) * step


class Monitor:
    def __init__(self, shcore, monitor):
        self.shcore = shcore
        self.monitor = monitor
        self.dpiX = ctypes.c_uint()
        self.dpiY = ctypes.c_uint()
        shcore.GetDpiForMonitor(
            monitor[0].handle,
            MDT_EFFECTIVE_DPI,
            ctypes.byref(self.dpiX),
            ctypes.byref(self.dpiY)
        )

    def get_max_dpi(self):
        return max([round_custom(self.dpiX.value, 25), round_custom(self.dpiY.value, 25)])


def getMonitors():
    dct = {}
    shcore = ctypes.windll.shcore
    monitors = win32api.EnumDisplayMonitors()
    shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    for i, monitor in enumerate(monitors):
        name = win32api.GetMonitorInfo(monitors[i][0])['Device']
        monitor_obj = Monitor(shcore, monitor)
        dct[name] = monitor_obj
        print(
            f"{name} dpiX: {round_custom(monitor_obj.dpiX.value, 25)}, dpiY: {round_custom(monitor_obj.dpiY.value, 25)}"
        )
    return dct
