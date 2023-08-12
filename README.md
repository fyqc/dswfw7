# Different wallpaper settings for horizontal and vertical dual screens under Win7

> This article refers to and draws on the tutorials on Baidu Jingyan：[Link (Simplified Chinese)](https://jingyan.baidu.com/article/76a7e409e5d575fc3b6e15fc.html)  
> However, there are many mistakes in the original tutorial, and this article has made some necessary corrections and corrections during the verification process.

This code is tested under Windows 7 and Python 3.8.10.  

English | [中文](https://github.com/fyqc/dswfw7/blob/main/README-zh.md)

---

## Features

This code simplifies the operation of setting wallpapers for horizontal and vertical dual screens with different monitors in Windows 7 system.

The effect is as follows:  

![display-on-monitor](https://raw.githubusercontent.com/fyqc/dswfw7/main/IMG/display-on-monitor.jpg)

---

On Windows systems prior to Windows 8, it was very difficult to set separate wallpapers for two monitors if they were oriented in different directions, especially if their bottom or top heights were not at the same level.  

![screen-resolution-setting](https://raw.githubusercontent.com/fyqc/dswfw7/main/IMG/screen-resolution-setting.jpg)


Because the system will use a large image by default to cut it at a specific pixel position and present it on the display, as shown in the following figure:  

![result](https://raw.githubusercontent.com/fyqc/dswfw7/main/IMG/result.jpg)


## Preparation

You need to place two pre-prepared pictures in the specified directory `dual_monitor_folder`, here they are named `vertical_image` and `horizontal_image`, you can change them to the name you want, and the image resolution is pre-cut , respectively corresponding to the resolution of the display.  

Both of my monitors are 1920×1080 pixels, so the resolution of `vertical_image` is 1080*1920, and the resolution of `horizontal_image` is 1920*1080.

---

## codes and explanations

Introduce Python's built-in `os` library and `winreg` library for changing folders and calling registry information.  

Introduce a third-party image library [`Pillow`](https://pypi.org/project/Pillow/) for image reading, cropping and pasting.

```python
import os
import winreg
from PIL import Image
```

Specify each input file and its folder, and specify the file name of the file to be generated.
Change Python's working directory into the target folder.

```python
dual_monitor_folder = r"D:\Wallpaper"
vertical_image = "132.png"  # 1080*1920
horizontal_image = "wallhaven-3988e6.png"  # 1920*1080
output = "github.png"
os.chdir(dual_monitor_folder)
```

Use the `winreg` library to read the registry, find the screen resolution of the vertical screen, recorded as `ver_x` and `ver_y`, and the relative screen offset `os_y` between the two monitors.

![regedit](https://raw.githubusercontent.com/fyqc/dswfw7/main/IMG/regedit.jpg)  

**Notice**:  

*The location of the your registry here is most likely to be different from my parameters behind `UnitedVideo`, please enter the registry of your computer to find and replace*

** where offset_y is a double-byte hexadecimal number, which needs to be converted according to the following formula to obtain the correct decimal value**

```python
key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\ControlSet001\Hardware Profiles\UnitedVideo\CONTROL\VIDEO\{690A5E6F-579C-473E-B419-F6A46A64D10B}\0001")

ver_x, _ = winreg.QueryValueEx(key, "DefaultSettings.XResolution")  # 1080
ver_y, _ = winreg.QueryValueEx(key, "DefaultSettings.YResolution")  # 1920
offset_y_hex, _ = winreg.QueryValueEx(key, "Attach.RelativeY")  # 4294966807
os_y = offset_y_hex-2**32  # -489
```

> For those who are interested, can go to the following stackoverflow address to read advanced knowledge of hexadecimal conversion:  
> https://stackoverflow.com/questions/26219414/how-to-convert-hex-number-to-decimal-stored-in-a-dword-instead-qword  


---

Use PIL's Image library to create a new image `final`, the width is the sum of the total width of the horizontal and vertical images (hor_x + ver_x), and the height is the height of the vertical image (ver_y)

```python3
output_length = 1080 + 1920
output_height = 1920
final = Image.new("RGB", (output_length, output_height), "#ffffff")
```

The label on the original illustration in the article on Baidu is wrong!  
I modify it to the correct value as below:

![vertical](https://raw.githubusercontent.com/fyqc/dswfw7/main/IMG/vertical.jpg)    

![paste-position](https://raw.githubusercontent.com/fyqc/dswfw7/main/IMG/paste-position.jpg)  

```python
# Copy the (0,0,ver_x,os_y) area of the vertical screen wallpaper as ver_crop1, and copy the remaining area as ver_crop2
vi = Image.open(vertical_image).copy()
ver_crop1 = vi.crop((0, 0, ver_x, abs(os_y)))
ver_crop2 = vi.crop((0, abs(os_y), ver_x, ver_y))

# Copy the horizontal screen wallpaper to the final (0, 0) coordinates
hi = Image.open(horizontal_image).copy()
final.paste(hi, (0, 0), None)

# Paste ver_crop2 to the final (ver_y, 0) coordinates
final.paste(ver_crop2, (ver_y, 0), None)

# Paste ver_crop1 to the final (ver_y, ver_y-os_y) coordinates
final.paste(ver_crop1, (ver_y, ver_y-abs(os_y)), None)

# save final
final.save(output)
```
