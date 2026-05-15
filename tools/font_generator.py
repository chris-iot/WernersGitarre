"""
Font bitmap generator for Werner pattern.
Generates 6-pixel-tall fonts for text display on LED strips.
"""

def create_font_bitmaps():
    """
    Create 6-pixel tall font bitmaps for Werner pattern.
    Each character is represented as 6 rows of 5-bit width.
    Format: 0bXXXXX where bit 4 = leftmost pixel, bit 0 = rightmost pixel.
    Rows are indexed from bottom to top (row 0 = bottom strip D1, row 5 = top).
    """
    
    fonts = {}
    
    # W
    fonts['W'] = [
        0b10001,  # row 0 (bottom)
        0b10001,
        0b10101,
        0b10101,
        0b11011,
        0b10001   # row 5 (top)
    ]
    
    # T
    fonts['T'] = [
        0b11111,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b00100
    ]
    
    # A
    fonts['A'] = [
        0b01110,
        0b10001,
        0b10001,
        0b11111,
        0b10001,
        0b10001
    ]
    
    # E
    fonts['E'] = [
        0b11111,
        0b10000,
        0b11110,
        0b10000,
        0b10000,
        0b11111
    ]
    
    # R
    fonts['R'] = [
        0b11110,
        0b10001,
        0b11110,
        0b10100,
        0b10010,
        0b10001
    ]
    
    # N
    fonts['N'] = [
        0b10001,
        0b11001,
        0b10101,
        0b10011,
        0b10001,
        0b10001
    ]
    
    # B (for "Booting")
    fonts['B'] = [
        0b11110,
        0b10001,
        0b11110,
        0b10001,
        0b10001,
        0b11110
    ]

    # C
    fonts['C'] = [
        0b01110,
        0b10001,
        0b10000,
        0b10000,
        0b10001,
        0b01110
    ]

    # D
    fonts['D'] = [
        0b11110,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b11110
    ]

    # H
    fonts['H'] = [
        0b10001,
        0b10001,
        0b11111,
        0b10001,
        0b10001,
        0b10001
    ]

    # I
    fonts['I'] = [
        0b11111,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b11111
    ]

    # K
    fonts['K'] = [
        0b10001,
        0b10010,
        0b11100,
        0b10010,
        0b10001,
        0b10001
    ]

    # L
    fonts['L'] = [
        0b10000,
        0b10000,
        0b10000,
        0b10000,
        0b10000,
        0b11111
    ]

    # M
    fonts['M'] = [
        0b10001,
        0b11011,
        0b10101,
        0b10001,
        0b10001,
        0b10001
    ]

    # O
    fonts['O'] = [
        0b01110,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b01110
    ]

    # Q
    fonts['Q'] = [
        0b01110,
        0b10001,
        0b10001,
        0b10001,
        0b10011,
        0b01111
    ]

    # S
    fonts['S'] = [
        0b01110,
        0b10000,
        0b01110,
        0b00001,
        0b10001,
        0b01110
    ]

    # U
    fonts['U'] = [
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b01110
    ]

    # V
    fonts['V'] = [
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b01010,
        0b00100
    ]

    # X
    fonts['X'] = [
        0b10001,
        0b01010,
        0b00100,
        0b01010,
        0b10001,
        0b10001
    ]

    # Y
    fonts['Y'] = [
        0b10001,
        0b10001,
        0b01010,
        0b00100,
        0b00100,
        0b00100
    ]

    # Z
    fonts['Z'] = [
        0b11111,
        0b00010,
        0b00100,
        0b01000,
        0b10000,
        0b11111
    ]

    # o
    fonts['o'] = [
        0b00000,
        0b01110,
        0b10001,
        0b10001,
        0b10001,
        0b01110
    ]
    
    # t
    fonts['t'] = [
        0b00100,
        0b01110,
        0b00100,
        0b00100,
        0b00100,
        0b01110
    ]
    
    # i
    fonts['i'] = [
        0b00100,
        0b00000,
        0b00100,
        0b00100,
        0b00100,
        0b00100
    ]
    
    # n
    fonts['n'] = [
        0b00000,
        0b01110,
        0b10001,
        0b10001,
        0b10001,
        0b10001
    ]
    
    # g
    fonts['g'] = [
        0b00000,
        0b01110,
        0b10001,
        0b10001,
        0b01111,
        0b00001
    ]
    
    # 4
    fonts['4'] = [
        0b10001,
        0b10001,
        0b01111,
        0b00001,
        0b00001,
        0b00001
    ]
    
    # 1
    fonts['1'] = [
        0b00010,
        0b00110,
        0b00010,
        0b00010,
        0b00010,
        0b00111
    ]
    
    # +
    fonts['+'] = [
        0b00000,
        0b00100,
        0b01110,
        0b00100,
        0b00000,
        0b00000
    ]
    
    # J (for Jahren)
    fonts['J'] = [
        0b11111,
        0b00001,
        0b00001,
        0b00001,
        0b10001,
        0b01110
    ]
    
    # a
    fonts['a'] = [
        0b00000,
        0b01110,
        0b10001,
        0b01111,
        0b10001,
        0b01111
    ]
    
    # h
    fonts['h'] = [
        0b10000,
        0b10000,
        0b11110,
        0b10001,
        0b10001,
        0b10001
    ]
    
    # r
    fonts['r'] = [
        0b00000,
        0b01110,
        0b10000,
        0b10000,
        0b10000,
        0b10000
    ]
    
    # e
    fonts['e'] = [
        0b00000,
        0b01110,
        0b10001,
        0b11111,
        0b10000,
        0b01110
    ]
    
    # space
    fonts[' '] = [
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000
    ]
    
    # @
    fonts['@'] = [
        0b01110,
        0b10001,
        0b01011,
        0b01011,
        0b01011,
        0b01110
    ]
    
    # lowercase letters needed for descriptions
    fonts['G'] = [
        0b01110,
        0b10001,
        0b10000,
        0b10111,
        0b10001,
        0b01110
    ]
    
    fonts['d'] = [
        0b00001,
        0b00001,
        0b01111,
        0b10001,
        0b10001,
        0b01111
    ]
    
    fonts['y'] = [
        0b00000,
        0b10001,
        0b10001,
        0b01111,
        0b00001,
        0b01110
    ]
    
    fonts['F'] = [
        0b11111,
        0b10000,
        0b11110,
        0b10000,
        0b10000,
        0b10000
    ]
    
    fonts['c'] = [
        0b00000,
        0b01110,
        0b10000,
        0b10000,
        0b10000,
        0b01110
    ]
    
    fonts['u'] = [
        0b00000,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b01111
    ]
    
    fonts['m'] = [
        0b00000,
        0b11011,
        0b10101,
        0b10101,
        0b10101,
        0b10101
    ]
    
    fonts['s'] = [
        0b00000,
        0b01110,
        0b10000,
        0b01110,
        0b00001,
        0b01110
    ]
    
    fonts['l'] = [
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b00100
    ]
    
    fonts['k'] = [
        0b10000,
        0b10001,
        0b10010,
        0b11100,
        0b10010,
        0b10001
    ]
    
    fonts['.'] = [
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        0b00100
    ]
    
    fonts['-'] = [
        0b00000,
        0b00000,
        0b11111,
        0b00000,
        0b00000,
        0b00000
    ]
    
    fonts['p'] = [
        0b00000,
        0b11110,
        0b10001,
        0b11110,
        0b10000,
        0b10000
    ]
    
    fonts['f'] = [
        0b00110,
        0b01000,
        0b11110,
        0b01000,
        0b01000,
        0b01000
    ]
    
    fonts['v'] = [
        0b00000,
        0b10001,
        0b10001,
        0b10001,
        0b01010,
        0b00100
    ]
    
    fonts['w'] = [
        0b00000,
        0b10001,
        0b10101,
        0b10101,
        0b10101,
        0b01010
    ]
    
    fonts['2'] = [
        0b01110,
        0b10001,
        0b00001,
        0b01110,
        0b10000,
        0b11111
    ]
    
    fonts['3'] = [
        0b01110,
        0b10001,
        0b00110,
        0b10001,
        0b10001,
        0b01110
    ]
    
    fonts['6'] = [
        0b01110,
        0b10000,
        0b11110,
        0b10001,
        0b10001,
        0b01110
    ]
    
    fonts['7'] = [
        0b11111,
        0b00001,
        0b00010,
        0b00100,
        0b01000,
        0b10000
    ]
    
    fonts['8'] = [
        0b01110,
        0b10001,
        0b01110,
        0b10001,
        0b10001,
        0b01110
    ]
    
    fonts['9'] = [
        0b01110,
        0b10001,
        0b10001,
        0b01111,
        0b00001,
        0b01110
    ]
    
    fonts['0'] = [
        0b01110,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b01110
    ]
    
    fonts['5'] = [
        0b11111,
        0b10000,
        0b11110,
        0b00001,
        0b10001,
        0b01110
    ]
    
    fonts['q'] = [
        0b00000,
        0b01111,
        0b10001,
        0b10001,
        0b01111,
        0b00001
    ]
    
    return fonts


def export_bitmaps_as_cpp():
    """Export all bitmaps as C++ arrays for firmware."""
    fonts = create_font_bitmaps()
    cpp_code = []
    
    cpp_code.append("// Auto-generated font bitmaps (6 pixels tall)")
    cpp_code.append("const uint8_t fontBitmaps[256][6] = {")
    
    for ascii_val in range(256):
        char = chr(ascii_val)
        if char in fonts:
            bitmap = fonts[char]
            cpp_code.append(f"  // {repr(char)}")
            cpp_code.append(f"  {{{', '.join(f'0b{b:05b}' for b in bitmap)}}},")
        else:
            # Empty bitmap for undefined characters
            cpp_code.append(f"  {{{', '.join('0b00000' for _ in range(6))}}},")
    
    cpp_code.append("};")
    
    return "\n".join(cpp_code)


if __name__ == "__main__":
    fonts = create_font_bitmaps()
    print(f"Generated {len(fonts)} font bitmaps")
    print("\nExample: 'W' bitmap:")
    for row in fonts['W']:
        print(f"  {row:08b} → {row}")
