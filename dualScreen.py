import ctypes
from ctypes import wintypes
import os
from PIL import Image

# 11/20/2026

dual_monitor_folder = (
    r"D:\Pictures"
)
vertical_image = "2 trimed.png"
horizontal_image = "1 trimed.png"
output = "github.png"

os.chdir(dual_monitor_folder)


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG),
    ]


monitors = []
MonitorEnumProc = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HMONITOR,
    wintypes.HDC,
    ctypes.POINTER(RECT),
    wintypes.LPARAM,
)


def _callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
    r = lprcMonitor.contents
    monitors.append({
        "left": r.left,
        "top": r.top,
        "right": r.right,
        "bottom": r.bottom,
        "width": r.right - r.left,
        "height": r.bottom - r.top,
    })
    return True


ctypes.windll.user32.EnumDisplayMonitors(
    None, None, MonitorEnumProc(_callback), 0
)

ver_mon = [m for m in monitors if m["height"] > m["width"]][0]
hor_mon = [m for m in monitors if m["width"] >= m["height"]][0]

total_w = max(m["right"] for m in monitors) - min(m["left"] for m in monitors)
total_h = max(m["bottom"] for m in monitors) - min(m["top"] for m in monitors)
final = Image.new("RGB", (total_w, total_h), "#ffffff")

hi = Image.open(horizontal_image)
vi = Image.open(vertical_image)

if hi.size != (hor_mon["width"], hor_mon["height"]):
    hi = hi.resize((hor_mon["width"], hor_mon["height"]), Image.LANCZOS)
if vi.size != (ver_mon["width"], ver_mon["height"]):
    vi = vi.resize((ver_mon["width"], ver_mon["height"]), Image.LANCZOS)


def paste_tiled(canvas, img, start_x, start_y):
    cw, ch = canvas.size
    iw, ih = img.size
    x0 = start_x % cw
    y0 = start_y % ch

    w1 = min(iw, cw - x0)
    h1 = min(ih, ch - y0)
    w2 = iw - w1
    h2 = ih - h1

    canvas.paste(img.crop((0, 0, w1, h1)), (x0, y0))
    if w2 > 0:
        canvas.paste(img.crop((w1, 0, iw, h1)), (0, y0))
    if h2 > 0:
        canvas.paste(img.crop((0, h1, w1, ih)), (x0, 0))
    if w2 > 0 and h2 > 0:
        canvas.paste(img.crop((w1, h1, iw, ih)), (0, 0))


paste_tiled(final, hi, hor_mon["left"], hor_mon["top"])
paste_tiled(final, vi, ver_mon["left"], ver_mon["top"])

final.save(output)
print(f"Total Size: {total_w}x{total_h} -> {output}")
