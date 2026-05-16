#pragma once

#include <Arduino.h>

// Auto-generated font bitmaps for Werner pattern
// 6 pixels tall, 5 pixels wide per character
// Generated from font_generator.py

// Font bitmap: rows[0]=bottom strip (D1), rows[5]=top strip (D7)
// Each byte: 0bXXXXX where bit 4=left, bit 0=right
struct FontBitmap {
  uint8_t rows[6];
};

extern const FontBitmap fontBitmaps[256] PROGMEM;

uint8_t fontBitmapRow(char c, uint8_t row);

// Scene timing (ms), matches werner_simulator.py
constexpr unsigned long SCENE_BOOTING_END = 2000;
constexpr unsigned long SCENE_JAHRE_END = 10000;
constexpr unsigned long SCENE_HIGHWAY_END = 22000;
constexpr unsigned long SCENE_FREQUENCY_END = 24000;
constexpr unsigned long SCENE_BLACK_END = 25000;
constexpr unsigned long SCENE_MISSING_END = 30000;
constexpr unsigned long SCENE_FIRMWARE_END = 32000;
constexpr unsigned long SCENE_FLAMES_END = 34000;
constexpr unsigned long WERNER_PATTERN_DURATION = 37000;