JPG 2 RGB565 Converter
========================

A Python program to convert JPG images to RGB565 format uint16_t arrays for embedded development.

Requirements
------------
- Python 3.6+
- Pillow (PIL) library
- NumPy library

Install dependencies:
```
pip install Pillow numpy
```

Usage
-----
Basic usage:
```
python jpg_to_rgb565.py input.jpg -o output.c
```

Command line options:
```
usage: jpg_to_rgb565.py [-h] [-o OUTPUT] [--array-name ARRAY_NAME] [--raw] [--no-header] [--little-endian] input

Convert JPG image to RGB565 format uint16_t array for embedded development.

positional arguments:
  input                 Input JPG image file

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file path (default: output.c)
  --array-name ARRAY_NAME
                        Name for the C array variable (default: image_data)
  --raw                 Output raw hex values (one per line) instead of C array
  --no-header           Do not include width/height defines in C output
  --little-endian, --le
                        Generate little-endian byte order (swap bytes)

Examples:
  jpg_to_rgb565.py input.jpg -o output.c
  jpg_to_rgb565.py input.jpg -o image_data.h --array-name my_image
  jpg_to_rgb565.py input.jpg -o output.txt --raw
  jpg_to_rgb565.py input.jpg -o output_le.c --little-endian
  jpg_to_rgb565.py input.jpg -o output_le.txt --raw --little-endian
```

Output Format
-------------
Default C array output (big-endian):
```c
// Generated from image 4x4
const uint16_t image_data[16] = {
    0x89C3, 0xD42D, 0x10A0, 0xDEF7, 0xFF39, 0x3800, 0x948D, 0x6B69,
    0xBDD7, 0x2104, 0x030C, 0x01A6, 0x9493, 0x39C8, 0x138E, 0x02AA
};

#define IMAGE_DATA_WIDTH 4
#define IMAGE_DATA_HEIGHT 4
```

Little-endian output (with `--little-endian` option):
```c
// Generated from image 4x4 (little-endian)
const uint16_t image_data[16] = {
    0xC389, 0x2DD4, 0xA010, 0xF7DE, 0x39FF, 0x0038, 0x8D94, 0x696B,
    0xD7BD, 0x0421, 0x0C03, 0xA601, 0x9394, 0xC839, 0x8E13, 0xAA02
};

#define IMAGE_DATA_WIDTH 4
#define IMAGE_DATA_HEIGHT 4
```

Byte Order Explanation
----------------------
- **Big-endian (default)**: 16-bit values are stored in memory as they appear (high byte first).
  Example: 0x89C3 is stored as bytes `0x89` followed by `0xC3`.
- **Little-endian (with `--little-endian` option)**: Bytes are swapped for little-endian systems.
  Example: 0x89C3 becomes 0xC389, stored as bytes `0xC3` followed by `0x89`.

Use `--little-endian` for ARM Cortex-M, x86, and other little-endian architectures.

RGB565 Format
-------------
RGB565 is a 16-bit color format:
- Red: 5 bits (0-31)
- Green: 6 bits (0-63)
- Blue: 5 bits (0-31)

Conversion formula:
```
r5 = (r >> 3) & 0x1F
g6 = (g >> 2) & 0x3F
b5 = (b >> 3) & 0x1F
rgb565 = (r5 << 11) | (g6 << 5) | b5
```

Where r, g, b are 8-bit values (0-255).

Error Handling
--------------
- Checks if input file exists
- Validates image format
- Handles corrupted image files
- Provides clear error messages

Examples
--------
Test images can be created using create_test_image.py:
```
python create_test_image.py
```

This creates two test images: test_image.jpg (4x4) and test_image2.jpg (16x16).

License
-------
Free to use and modify for any purpose.

JPG RGB565数组转换器
======================

一个将 JPG 图像转换为 RGB565 格式 uint16_t 数组的 Python 程序，适用于嵌入式开发。

要求
----
- Python 3.6+
- Pillow (PIL) 库
- NumPy 库

安装依赖：
```
pip install Pillow numpy
```

使用方法
--------
基本用法：
```
python jpg_to_rgb565.py input.jpg -o output.c
```

命令行选项：
```
usage: jpg_to_rgb565.py [-h] [-o OUTPUT] [--array-name ARRAY_NAME] [--raw] [--no-header] [--little-endian] input

将 JPG 图像转换为 RGB565 格式 uint16_t 数组，用于嵌入式开发。

位置参数：
  input                 输入的 JPG 图像文件

选项：
  -h, --help            显示帮助信息并退出
  -o OUTPUT, --output OUTPUT
                        输出文件路径（默认：output.c）
  --array-name ARRAY_NAME
                        C 数组变量名（默认：image_data）
  --raw                 输出原始十六进制值（每行一个）而非 C 数组
  --no-header           不在 C 输出中包含宽度/高度定义
  --little-endian, --le 生成小端字节序（交换字节）

示例：
  jpg_to_rgb565.py input.jpg -o output.c
  jpg_to_rgb565.py input.jpg -o image_data.h --array-name my_image
  jpg_to_rgb565.py input.jpg -o output.txt --raw
  jpg_to_rgb565.py input.jpg -o output_le.c --little-endian
  jpg_to_rgb565.py input.jpg -o output_le.txt --raw --little-endian
```

输出格式
--------
默认 C 数组输出（大端序）：
```c
// 从图像 4x4 生成
const uint16_t image_data[16] = {
    0x89C3, 0xD42D, 0x10A0, 0xDEF7, 0xFF39, 0x3800, 0x948D, 0x6B69,
    0xBDD7, 0x2104, 0x030C, 0x01A6, 0x9493, 0x39C8, 0x138E, 0x02AA
};

#define IMAGE_DATA_WIDTH 4
#define IMAGE_DATA_HEIGHT 4
```

小端序输出（使用 `--little-endian` 选项）：
```c
// 从图像 4x4 生成（小端序）
const uint16_t image_data[16] = {
    0xC389, 0x2DD4, 0xA010, 0xF7DE, 0x39FF, 0x0038, 0x8D94, 0x696B,
    0xD7BD, 0x0421, 0x0C03, 0xA601, 0x9394, 0xC839, 0x8E13, 0xAA02
};

#define IMAGE_DATA_WIDTH 4
#define IMAGE_DATA_HEIGHT 4
```

字节序说明
----------
- **大端序（默认）**：16 位值按原样存储在内存中（高位字节在前）。
  例如：0x89C3 存储为字节 `0x89` 后跟 `0xC3`。
- **小端序（使用 `--little-endian` 选项）**：为小端序系统交换字节。
  例如：0x89C3 变为 0xC389，存储为字节 `0xC3` 后跟 `0x89`。

对于 ARM Cortex-M、x86 及其他小端序架构，请使用 `--little-endian`。

RGB565 格式
-----------
RGB565 是一种 16 位颜色格式：
- 红色：5 位（0-31）
- 绿色：6 位（0-63）
- 蓝色：5 位（0-31）

转换公式：
```
r5 = (r >> 3) & 0x1F
g6 = (g >> 2) & 0x3F
b5 = (b >> 3) & 0x1F
rgb565 = (r5 << 11) | (g6 << 5) | b5
```

其中 r、g、b 为 8 位值（0-255）。

错误处理
--------
- 检查输入文件是否存在
- 验证图像格式
- 处理损坏的图像文件
- 提供清晰的错误信息

示例
----
测试图像可以使用 create_test_image.py 创建：
```
python create_test_image.py
```

这将创建两个测试图像：test_image.jpg（4x4）和 test_image2.jpg（16x16）。

许可证
------
可自由使用和修改，用于任何目的.
