#!/usr/bin/env python3
"""
Export font bitmaps as C++ header code.
Run: python export_fonts_to_cpp.py > ../src/werner_fonts.h
"""

from font_generator import create_font_bitmaps

def export_bitmaps_for_firmware():
    """Export bitmaps needed specifically for Werner pattern scenes."""

    fonts = create_font_bitmaps()

    # Simulator strings (character coverage)
    scene_texts = [
        "BOOTING",
        "41+ JAHRE WERNER BEI ROHDE UND SCHWARZ",
        "GET READY FOR THE HIGHWAY TO HELL",
        "FREQUENCY UNLOCKED",
        "MISSING K666",
        "FIRMWARE ERROR",
    ]

    unique_chars = set()
    for text in scene_texts:
        unique_chars.update(text)

    # Generate C++ code
    cpp_lines = [
        "#pragma once",
        "",
        "#include <Arduino.h>",
        "",
        "// Auto-generated font bitmaps for Werner pattern",
        "// 6 pixels tall, 5 pixels wide per character",
        "// Generated from font_generator.py",
        "",
        "// Font bitmap: rows[0]=bottom strip (D1), rows[5]=top strip (D7)",
        "// Each byte: 0bXXXXX where bit 4=left, bit 0=right",
        "struct FontBitmap {",
        "  uint8_t rows[6];",
        "};",
        "",
        "extern const FontBitmap fontBitmaps[256] PROGMEM;",
        "",
        "uint8_t fontBitmapRow(char c, uint8_t row);",
        "",
        "// Scene timing (ms), matches werner_simulator.py",
        "constexpr unsigned long SCENE_BOOTING_END = 2000;",
        "constexpr unsigned long SCENE_JAHRE_END = 10000;",
        "constexpr unsigned long SCENE_HIGHWAY_END = 22000;",
        "constexpr unsigned long SCENE_FREQUENCY_END = 24000;",
        "constexpr unsigned long SCENE_BLACK_END = 25000;",
        "constexpr unsigned long SCENE_MISSING_END = 30000;",
        "constexpr unsigned long SCENE_FIRMWARE_END = 32000;",
        "constexpr unsigned long SCENE_FLAMES_END = 34000;",
        "constexpr unsigned long WERNER_PATTERN_DURATION = 37000;",
    ]

    return "\n".join(cpp_lines)


def export_bitmaps_implementation():
    """Font table implementation for .cpp file."""
    fonts = create_font_bitmaps()

    cpp_lines = [
        '#include "werner_fonts.h"',
        "",
        "const FontBitmap fontBitmaps[256] PROGMEM = {",
    ]

    for ascii_val in range(256):
        char = chr(ascii_val)
        if char in fonts:
            bitmap = fonts[char]
            rows_str = ", ".join(f"0x{b:02x}" for b in bitmap)
            if char == '"':
                char_display = '\\\\\\"'
            elif char == '\\':
                char_display = '\\\\\\\\'
            else:
                char_display = char if 32 <= ascii_val < 127 else '?'
            cpp_lines.append(
                f"  {{{rows_str}}}, // '{char_display}' ASCII {ascii_val}"
            )
        else:
            cpp_lines.append(
                "  {0x00, 0x00, 0x00, 0x00, 0x00, 0x00}, // (undefined)"
            )

    cpp_lines.append("};")
    cpp_lines.append("")
    cpp_lines.append("uint8_t fontBitmapRow(char c, uint8_t row) {")
    cpp_lines.append("  if (row > 5) return 0;")
    cpp_lines.append("  const FontBitmap* bm = &fontBitmaps[(unsigned char)c];")
    cpp_lines.append("  return pgm_read_byte(&bm->rows[row]);")
    cpp_lines.append("}")

    return "\n".join(cpp_lines)


if __name__ == "__main__":
    import os
    root = os.path.join(os.path.dirname(__file__), "..", "src")
    header_path = os.path.join(root, "werner_fonts.h")
    impl_path = os.path.join(root, "werner_fonts.cpp")
    with open(header_path, "w", encoding="utf-8") as f:
        f.write(export_bitmaps_for_firmware())
    with open(impl_path, "w", encoding="utf-8") as f:
        f.write(export_bitmaps_implementation())
    print(f"Wrote {header_path} and {impl_path}")
