# Win7下横竖双屏不同壁纸设置

> 本文参考引用并借鉴了百度经验上的教程：[链接](https://jingyan.baidu.com/article/76a7e409e5d575fc3b6e15fc.html)  
> 然而原教程中存在许多错误，本文在验证的过程进行了一些必要的勘误与纠正。

本代码在Windows 7与Python 3.8.10下测试通过。  

[English](https://github.com/fyqc/dswfw7/blob/main/README.md) | 中文

---

## 功能介绍

本代码简化了在Windows 7系统中为横竖双屏不同的显示器设置壁纸的操作。  

成品效果图如下：  

![display-on-monitor](https://raw.githubusercontent.com/fyqc/dswfw7/main/IMG/display-on-monitor.jpg)

---

在Windows 8之前的Windows系统中，如果两台显示器的摆放方向不同，尤其是在它们的底部或顶部的高度不齐平的时候，为它们设置单独的壁纸是十分困难的。  

![screen-resolution-setting](https://raw.githubusercontent.com/fyqc/dswfw7/main/IMG/screen-resolution-setting.jpg)


因为系统默认会用一张大图在特定的像素位置进行切割后呈现在显示器上，如下图所示：  

![result](https://raw.githubusercontent.com/fyqc/dswfw7/main/IMG/result.jpg)


## 准备工作

需要在指定的目录`dual_monitor_folder`中放置两张提前准备好的图片，这里以`vertical_image`和`horizontal_image`为名称，你可以随意将其改为自己想要的名称，其中图片分辨率事先裁剪好，分别对应显示器的分辨率。

我的两台显示器都是1920×1080像素，所以`vertical_image`的分辨率为1080*1920,`horizontal_image`分辨率为1920*1080.

---

## 代码与释义

引入Python自带的`os`库和`winreg`库，用于更改文件夹和调取注册表的信息。  
引入第三方的图片库[`Pillow`](https://pypi.org/project/Pillow/)用于图片的读取、裁剪和粘贴。

```python
import os
import winreg
from PIL import Image
```

指定各输入的文件和其所在的文件夹，并指定需要生成的文件的文件名。  
将Python的工作目录更改到目标文件夹中。

```python
dual_monitor_folder = r"D:\Wallpaper"
vertical_image = "132.png"  # 1080*1920
horizontal_image = "wallhaven-3988e6.png"  # 1920*1080
output = "github.png"
os.chdir(dual_monitor_folder)
```

用winreg库来读取注册表，查找竖屏的屏幕分辨率，记为`ver_x`和`ver_y`，以及两个显示器之间相对的屏幕偏移量`os_y`.  

![regedit](https://raw.githubusercontent.com/fyqc/dswfw7/main/IMG/regedit.jpg)  

**注意**：  
*此处注册表的位置在`UnitedVideo`后面的参数大概率与你的并不相同，请自行进入你的计算机的注册表中进行查找与替换*

**其中offset_y是双字节十六进制数，需要按照以下公式进行转换，以获得正确的十进制的数值**

```python
key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\ControlSet001\Hardware Profiles\UnitedVideo\CONTROL\VIDEO\{690A5E6F-579C-473E-B419-F6A46A64D10B}\0001")

ver_x, _ = winreg.QueryValueEx(key, "DefaultSettings.XResolution")  # 1080
ver_y, _ = winreg.QueryValueEx(key, "DefaultSettings.YResolution")  # 1920
offset_y_hex, _ = winreg.QueryValueEx(key, "Attach.RelativeY")  # 4294966807
os_y = offset_y_hex-2**32  # -489
```

> 有兴趣的朋友可以前往以下stackoverflow地址阅读16进制转换的进阶知识：  
> https://stackoverflow.com/questions/26219414/how-to-convert-hex-number-to-decimal-stored-in-a-dword-instead-qword  


---

用PIL的Image库来创建新图片`final`，宽度为横竖两张图片的总宽之和(hor_x + ver_x)，高度是竖图的高(ver_y)

```python3
output_length = 1080 + 1920
output_height = 1920
final = Image.new("RGB", (output_length, output_height), "#ffffff")
```

以下的部分，百度上文章里面插图上的标注是错的！  
这里修改成正确的值：

![vertical](https://raw.githubusercontent.com/fyqc/dswfw7/main/IMG/vertical.jpg)    

![paste-position](https://raw.githubusercontent.com/fyqc/dswfw7/main/IMG/paste-position.jpg)  

```python
# 截取竖屏壁纸的(0,0,ver_x,os_y)区域复制为ver_crop1，剩余区域复制为ver_crop2
vi = Image.open(vertical_image).copy()
ver_crop1 = vi.crop((0, 0, ver_x, abs(os_y)))
ver_crop2 = vi.crop((0, abs(os_y), ver_x, ver_y))

# 将横屏壁纸复制到final的（0，0）坐标
hi = Image.open(horizontal_image).copy()
final.paste(hi, (0, 0), None)

# 把ver_crop2粘贴到final的（ver_y，0）坐标
final.paste(ver_crop2, (ver_y, 0), None)

# 把ver_crop1粘贴到final的（ver_y，ver_y-os_y）坐标
final.paste(ver_crop1, (ver_y, ver_y-abs(os_y)), None)

# 保存final
final.save(output)
```
