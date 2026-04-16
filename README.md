JPG to RGB565 Converter
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
