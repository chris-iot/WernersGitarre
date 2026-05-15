#!/usr/bin/env python3
"""
Export font bitmaps as C++ header code.
Run: python export_fonts_to_cpp.py > fonts.h
"""

from font_generator import create_font_bitmaps

def export_bitmaps_for_firmware():
    """Export bitmaps needed specifically for Werner pattern scenes."""
    
    fonts = create_font_bitmaps()
    
    # Required for Werner scenes
    scene_texts = {
        'booting': 'Booting',
        'jahre': '41+ Jahre Werner @R&S',
        'highway': 'Get Ready for the Highway to Hell',
        'frequency': 'Frequency unlocked',
        'missing': 'Missing K666',
        'firmware': 'Firmware error',
    }
    
    # Collect all unique characters
    unique_chars = set()
    for text in scene_texts.values():
        unique_chars.update(text.lower())
        unique_chars.update(text.upper())
    
    unique_chars = sorted(list(unique_chars))
    
    # Generate C++ code
    cpp_lines = [
        "// Auto-generated font bitmaps for Werner pattern",
        "// 6 pixels tall, 5 pixels wide per character",
        "// Generated from font_generator.py",
        "",
        "// Font bitmap structure: 6 bytes per character (rows 0-5, top to bottom)",
        "// Each byte: 0bXXXXX where bit 4=left, bit 0=right",
        "typedef struct {",
        "  uint8_t rows[6];",
        "} FontBitmap;",
        "",
        "// Character-to-bitmap lookup",
        "const FontBitmap fontBitmaps[256] = {",
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
                f"  [{ascii_val:3d}] = {{{rows_str}}}, // '{char_display}' ASCII {ascii_val}"
            )
        else:
            # Empty bitmap for undefined
            cpp_lines.append(
                f"  [{ascii_val:3d}] = {{0x00, 0x00, 0x00, 0x00, 0x00, 0x00}}, // (undefined)"
            )
    
    cpp_lines.append("};")
    cpp_lines.append("")
    cpp_lines.append("// Helper function to get bitmap for character")
    cpp_lines.append("const FontBitmap* getFontBitmap(char c) {")
    cpp_lines.append("  return &fontBitmaps[(unsigned char)c];")
    cpp_lines.append("}")
    cpp_lines.append("")
    
    cpp_lines.append("// Guitar Hero section removed from the animation sequence")
    cpp_lines.append("// No note timing data is generated for the firmware preview.")
    cpp_lines.append("")
    
    # Add scene constants
    cpp_lines.append("// Scene timing constants")
    cpp_lines.append("const unsigned long SCENE_BOOTING_START = 0;")
    cpp_lines.append("const unsigned long SCENE_BOOTING_END = 2000;")
    cpp_lines.append("const unsigned long SCENE_JAHRE_START = 2000;")
    cpp_lines.append("const unsigned long SCENE_JAHRE_END = 10000;")
    cpp_lines.append("const unsigned long SCENE_HIGHWAY_START = 10000;")
    cpp_lines.append("const unsigned long SCENE_HIGHWAY_END = 22000;")
    cpp_lines.append("const unsigned long SCENE_PAUSE_START = 22000;")
    cpp_lines.append("const unsigned long SCENE_PAUSE_END = 37000;")
    cpp_lines.append("")
    cpp_lines.append("// Total Werner pattern duration: 37 seconds")
    cpp_lines.append("const unsigned long WERNER_PATTERN_DURATION = 37000;")
    
    return "\n".join(cpp_lines)


def export_text_bitmaps(text):
    """Generate bitmap data for a specific text string."""
    fonts = create_font_bitmaps()
    
    cpp_lines = [
        f"// Bitmap data for text: \"{text}\"",
        f"const uint8_t text_{text.lower().replace(' ', '_')}[] = {{",
    ]
    
    for i, char in enumerate(text):
        if char in fonts:
            bitmap = fonts[char]
            rows_hex = ", ".join(f"0x{b:02x}" for b in bitmap)
            cpp_lines.append(f"  // Character {i}: '{char}'")
            cpp_lines.append(f"  {rows_hex},")
    
    cpp_lines.append("};")
    cpp_lines.append(f"const size_t text_{text.lower().replace(' ', '_')}_len = {len(text)};")
    
    return "\n".join(cpp_lines)


if __name__ == "__main__":
    print(export_bitmaps_for_firmware())
