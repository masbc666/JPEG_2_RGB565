#!/usr/bin/env python3
"""
Convert JPG image to RGB565 format uint16_t array for embedded development.
"""

import argparse
import sys
import os
from PIL import Image
import numpy as np

def rgb_to_rgb565(r, g, b):
    """
    Convert 8-bit RGB values (0-255) to 16-bit RGB565 format.
    
    Args:
        r, g, b: Red, green, blue values (0-255)
    
    Returns:
        16-bit RGB565 value as uint16
    """
    # Clamp values to valid range
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    
    # Convert to 5-6-5 bits
    r5 = (r >> 3) & 0x1F  # 5 bits
    g6 = (g >> 2) & 0x3F  # 6 bits
    b5 = (b >> 3) & 0x1F  # 5 bits
    
    # Combine into 16-bit value
    return (r5 << 11) | (g6 << 5) | b5

def image_to_rgb565_array(image_path):
    """
    Load image and convert all pixels to RGB565 array.
    
    Args:
        image_path: Path to input image file
    
    Returns:
        tuple: (width, height, rgb565_array as list of uint16)
    """
    try:
        img = Image.open(image_path)
    except Exception as e:
        raise ValueError(f"Cannot open image file '{image_path}': {e}")
    
    # Convert to RGB mode if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    width, height = img.size
    
    # Get pixel data as bytes and convert to numpy array for efficient processing
    img_bytes = img.tobytes()  # Returns bytes in RGB order
    
    # Convert to numpy array of uint8, reshape to (height, width, 3)
    arr = np.frombuffer(img_bytes, dtype=np.uint8).reshape(height, width, 3)
    
    # Extract R, G, B channels
    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]
    
    # Convert to RGB565 using vectorized operations
    # Shift and mask to get 5-6-5 bits
    r5 = (r >> 3).astype(np.uint16) & 0x1F
    g6 = (g >> 2).astype(np.uint16) & 0x3F
    b5 = (b >> 3).astype(np.uint16) & 0x1F
    
    # Combine into 16-bit values
    rgb565 = (r5 << 11) | (g6 << 5) | b5
    
    # Flatten to 1D array and convert to Python list
    rgb565_array = rgb565.flatten().tolist()
    
    return width, height, rgb565_array

def byteswap_uint16(val):
    """
    Swap bytes in a 16-bit value (little-endian conversion).
    
    Args:
        val: 16-bit value
    
    Returns:
        Value with bytes swapped
    """
    return ((val & 0xFF) << 8) | ((val >> 8) & 0xFF)


def apply_little_endian(array_data):
    """
    Convert array of uint16 values to little-endian format.
    
    Args:
        array_data: List of uint16 values
    
    Returns:
        List of byte-swapped values
    """
    return [byteswap_uint16(val) for val in array_data]


def generate_c_array(width, height, array_data, array_name="image_data", little_endian=False):
    """
    Generate C language array declaration.
    
    Args:
        width: Image width
        height: Image height
        array_data: List of uint16 values
        array_name: Name for the array variable
        little_endian: If True, values are byte-swapped for little-endian systems
    
    Returns:
        String with C array declaration
    """
    endian_note = " (little-endian)" if little_endian else ""
    c_code = f"// Generated from image {width}x{height}{endian_note}\n"
    c_code += f"const uint16_t {array_name}[{len(array_data)}] = {{\n"
    
    # Format array with 8 values per line for readability
    for i in range(0, len(array_data), 8):
        line_values = array_data[i:i+8]
        line = ", ".join(f"0x{val:04X}" for val in line_values)
        c_code += f"    {line}"
        if i + 8 < len(array_data):
            c_code += ","
        c_code += "\n"
    
    c_code += "};\n"
    
    # Add width and height defines
    c_code += f"\n#define {array_name.upper()}_WIDTH {width}\n"
    c_code += f"#define {array_name.upper()}_HEIGHT {height}\n"
    
    return c_code

def save_to_file(output_path, content):
    """
    Save content to file.
    
    Args:
        output_path: Path to output file
        content: String content to write
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully saved to: {output_path}")
    except Exception as e:
        raise IOError(f"Cannot write to file '{output_path}': {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Convert JPG image to RGB565 format uint16_t array for embedded development.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.jpg -o output.c
  %(prog)s input.jpg -o image_data.h --array-name my_image
  %(prog)s input.jpg -o output.txt --raw
  %(prog)s input.jpg -o output_le.c --little-endian
  %(prog)s input.jpg -o output_le.txt --raw --little-endian
        """
    )
    
    parser.add_argument('input', help='Input JPG image file')
    parser.add_argument('-o', '--output', default='output.c',
                       help='Output file path (default: output.c)')
    parser.add_argument('--array-name', default='image_data',
                       help='Name for the C array variable (default: image_data)')
    parser.add_argument('--raw', action='store_true',
                       help='Output raw hex values (one per line) instead of C array')
    parser.add_argument('--no-header', action='store_true',
                       help='Do not include width/height defines in C output')
    parser.add_argument('--little-endian', '--le', action='store_true',
                       help='Generate little-endian byte order (swap bytes)')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)
    
    # Check file extension (warn if not jpg/jpeg)
    if not args.input.lower().endswith(('.jpg', '.jpeg')):
        print(f"Warning: Input file '{args.input}' may not be a JPG image.", file=sys.stderr)
    
    try:
        # Convert image to RGB565 array
        print(f"Processing image: {args.input}")
        width, height, rgb565_array = image_to_rgb565_array(args.input)
        print(f"Image size: {width}x{height} pixels")
        print(f"Total pixels: {len(rgb565_array)}")
        
        # Apply little-endian conversion if requested
        if args.little_endian:
            rgb565_array = apply_little_endian(rgb565_array)
            print(f"Byte order: Little-endian (bytes swapped)")
        else:
            print(f"Byte order: Big-endian (native)")
        
        # Generate output content
        if args.raw:
            # Raw hex values, one per line
            content = "\n".join(f"0x{val:04X}" for val in rgb565_array)
        else:
            # C array format
            content = generate_c_array(width, height, rgb565_array, 
                                      args.array_name, args.little_endian)
            if args.no_header:
                # Remove the width/height defines
                lines = content.split('\n')
                # Keep only lines before the defines
                content_lines = []
                for line in lines:
                    if line.startswith('#define'):
                        break
                    content_lines.append(line)
                content = '\n'.join(content_lines).strip() + '\n'
        
        # Save to file
        save_to_file(args.output, content)
        
        # Print summary
        print(f"Conversion complete:")
        print(f"  Input:  {args.input}")
        print(f"  Output: {args.output}")
        print(f"  Format: {'Raw hex' if args.raw else 'C array'}")
        if args.little_endian:
            print(f"  Byte order: Little-endian")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()