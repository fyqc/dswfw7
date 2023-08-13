import os
import winreg
from PIL import Image

# 2023 年 8 月 12 日
# August 12, 2023

dual_monitor_folder = r"D:\My pictures"
vertical_image = "132.png"
horizontal_image = "wallhaven-3988e6.png"
output = "github.png"

os.chdir(dual_monitor_folder)

# レジストリを読み取り、ver_x、ver_y、offset_y の値を取得します。
# Read the registry to get the values of ver_x, ver_y and offset_y
key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                     r"SYSTEM\ControlSet001\Hardware Profiles\UnitedVideo\CONTROL\VIDEO\{690A5E6F-579C-473E-B419-F6A46A64D10B}\0001")
ver_x, _ = winreg.QueryValueEx(key, "DefaultSettings.XResolution")
ver_y, _ = winreg.QueryValueEx(key, "DefaultSettings.YResolution")
offset_y_hex, _ = winreg.QueryValueEx(key, "Attach.RelativeY")

# offset_y は 2 バイトの 16 進数で、正しい 10 進数値を取得するには、次の式に従って変換する必要があります。
# Where offset_y is a double-byte hexadecimal number, which needs to be converted according to the following formula to obtain the correct decimal value
os_y = offset_y_hex-2**32

# 図面を開き、プロパティ -> 幅 = (HX + ver_x)、高さ = ver_y、最終ファイルとして保存
# Open the drawing, properties -> width = (HX + ver_x), height = ver_y, save as final
output_length = 1080 + 1920
output_height = 1920
final = Image.new("RGB", (output_length, output_height), "#ffffff")

# 縦画面の壁紙を開き、(0,0,ver_x,os_y)をインターセプトしてver_crop1としてコピーし、残りの領域をver_crop2としてコピーします
# Open the vertical screen wallpaper, intercept (0,0,ver_x,os_y) and copy it as ver_crop1, and the remaining area as ver_crop2
vi = Image.open(vertical_image).copy()
ver_crop1 = vi.crop((0, 0, ver_x, abs(os_y)))
ver_crop2 = vi.crop((0, abs(os_y), ver_x, ver_y))

# 横画面の壁紙を最終の(0,0)座標にコピーします
# Copy the horizontal screen wallpaper to the final (0, 0) coordinates
hi = Image.open(horizontal_image).copy()
final.paste(hi, (0, 0), None)

# ver_crop2 を最終 (ver_y, 0) 座標に貼り付けます
# Paste ver_crop2 to the final (ver_y, 0) coordinates
final.paste(ver_crop2, (ver_y, 0), None)

# ver_crop1 を最終 (ver_y, ver_y-os_y) 座標に貼り付けます
# Paste ver_crop1 to the final (ver_y, ver_y-os_y) coordinates
final.paste(ver_crop1, (ver_y, ver_y-abs(os_y)), None)

# ファイナルを保存する
# save final
final.save(output)
