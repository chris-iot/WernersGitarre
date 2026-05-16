#include "werner_pattern.h"
#include "werner_fonts.h"
#include <FastLED.h>

#define NUM_STRIPS 6
#define NUM_LEDS_PER_STRIP 128
#define CHAR_WIDTH 5
#define CHAR_SPACING 1
#define CHAR_STRIDE (CHAR_WIDTH + CHAR_SPACING)

extern CRGB leds[NUM_STRIPS][NUM_LEDS_PER_STRIP];

static unsigned long wernerSequenceStartMs = 0;

static void fillAll(CRGB color) {
  for (uint8_t strip = 0; strip < NUM_STRIPS; strip++) {
    fill_solid(leds[strip], NUM_LEDS_PER_STRIP, color);
  }
}

static uint8_t textWidth(const char* text) {
  uint8_t len = 0;
  while (text[len] != '\0') len++;
  if (len == 0) return 0;
  return len * CHAR_STRIDE - CHAR_SPACING;
}

static void setPixel(uint8_t strip, int16_t x, CRGB color) {
  if (strip >= NUM_STRIPS || x < 0 || x >= NUM_LEDS_PER_STRIP) return;
  leds[strip][x] = color;
}

static void drawPixelAllStrips(int16_t x, CRGB color) {
  for (uint8_t strip = 0; strip < NUM_STRIPS; strip++) {
    setPixel(strip, x, color);
  }
}

static void drawGlyph(char c, int16_t x, CRGB color) {
  for (uint8_t row = 0; row < NUM_STRIPS; row++) {
    uint8_t rowBits = fontBitmapRow(c, row);
    for (uint8_t col = 0; col < CHAR_WIDTH; col++) {
      if (rowBits & (1 << (CHAR_WIDTH - 1 - col))) {
        setPixel(row, x + col, color);
      }
    }
  }
}

static void drawGlyphRowLimited(char c, int16_t x, CRGB color, uint8_t maxRowExclusive) {
  for (uint8_t row = 0; row < maxRowExclusive && row < NUM_STRIPS; row++) {
    uint8_t rowBits = fontBitmapRow(c, row);
    for (uint8_t col = 0; col < CHAR_WIDTH; col++) {
      if (rowBits & (1 << (CHAR_WIDTH - 1 - col))) {
        setPixel(row, x + col, color);
      }
    }
  }
}

static void drawGlyphStripOffset(char c, int16_t x, uint8_t stripOffset, CHSV color) {
  for (uint8_t row = 0; row < NUM_STRIPS; row++) {
    uint8_t rowBits = fontBitmapRow(c, row);
    uint8_t targetStrip = row + stripOffset;
    for (uint8_t col = 0; col < CHAR_WIDTH; col++) {
      if (rowBits & (1 << (CHAR_WIDTH - 1 - col))) {
        if (targetStrip < NUM_STRIPS) {
          leds[targetStrip][x + col] = color;
        }
      }
    }
  }
}

static void drawTextAt(const char* text, int16_t startX, CRGB color) {
  for (uint8_t charIdx = 0; text[charIdx] != '\0'; charIdx++) {
    drawGlyph(text[charIdx], startX + charIdx * CHAR_STRIDE, color);
  }
}

static void drawScrollingText(const char* text, unsigned long elapsedMs, unsigned long durationMs, CHSV color) {
  uint8_t totalW = textWidth(text);
  if (durationMs == 0) durationMs = 1;
  float scrollSpeed = (float)(NUM_LEDS_PER_STRIP + totalW) / (float)durationMs;
  int16_t scrollPos = (int16_t)(scrollSpeed * elapsedMs);
  int16_t startX = NUM_LEDS_PER_STRIP;

  for (uint8_t charIdx = 0; text[charIdx] != '\0'; charIdx++) {
    int16_t charX = startX + charIdx * CHAR_STRIDE - scrollPos;
    if (charX + CHAR_WIDTH < 0 || charX > NUM_LEDS_PER_STRIP) continue;

    char c = text[charIdx];
    for (uint8_t row = 0; row < NUM_STRIPS; row++) {
      uint8_t rowBits = fontBitmapRow(c, row);
      for (uint8_t col = 0; col < CHAR_WIDTH; col++) {
        if (rowBits & (1 << (CHAR_WIDTH - 1 - col))) {
          int16_t ledIdx = charX + col;
          if (ledIdx >= 0 && ledIdx < NUM_LEDS_PER_STRIP) {
            leds[row][ledIdx] = color;
          }
        }
      }
    }
  }
}

static void sceneBooting(unsigned long elapsedMs) {
  const char text[] = "BOOTING";
  uint8_t dotCount = (elapsedMs / 500) % 4;

  uint8_t animLen = dotCount + 7 + dotCount;
  uint8_t totalWidth = animLen * CHAR_STRIDE;
  int16_t center = (NUM_LEDS_PER_STRIP - totalWidth) / 2;

  CRGB cyan(0, 255, 255);
  CRGB yellow(255, 200, 0);

  uint8_t charIdx = 0;
  for (uint8_t d = 0; d < dotCount; d++, charIdx++) {
    int16_t x = center + charIdx * CHAR_STRIDE + 2;
    drawPixelAllStrips(x, yellow);
  }
  for (uint8_t i = 0; text[i] != '\0'; i++, charIdx++) {
    drawGlyph(text[i], center + charIdx * CHAR_STRIDE, cyan);
  }
  for (uint8_t d = 0; d < dotCount; d++, charIdx++) {
    int16_t x = center + charIdx * CHAR_STRIDE + 2;
    drawPixelAllStrips(x, yellow);
  }
}

static void sceneJahre(unsigned long elapsedMs) {
  const char text[] = "41+ JAHRE WERNER BEI ROHDE UND SCHWARZ";
  drawScrollingText(text, elapsedMs, 8000, CHSV(0, 0, 255));
}

static void sceneHighway(unsigned long elapsedMs) {
  const char text[] = "GET READY FOR THE HIGHWAY TO HELL";
  uint8_t saturation = (uint8_t)((elapsedMs * 255UL) / 12000UL);
  if (saturation > 255) saturation = 255;
  drawScrollingText(text, elapsedMs, 12000, CHSV(0, saturation, 255));
}

static void sceneFrequency(unsigned long elapsedMs) {
  const char text[] = "FREQUENCY UNLOCKED";
  uint8_t totalW = textWidth(text);
  int16_t center = (NUM_LEDS_PER_STRIP - totalW) / 2;

  float fadeFactor = 1.0f;
  if (elapsedMs > 1000) {
    fadeFactor = 1.0f - (float)(elapsedMs - 1000) / 1000.0f;
    if (fadeFactor < 0.0f) fadeFactor = 0.0f;
  }
  uint8_t brightness = (uint8_t)(255.0f * fadeFactor);

  for (uint8_t charIdx = 0; text[charIdx] != '\0'; charIdx++) {
    int16_t x = center + charIdx * CHAR_STRIDE;
    char c = text[charIdx];
    for (uint8_t row = 0; row < NUM_STRIPS; row++) {
      uint8_t rowBits = fontBitmapRow(c, row);
      for (uint8_t col = 0; col < CHAR_WIDTH; col++) {
        if (rowBits & (1 << (CHAR_WIDTH - 1 - col))) {
          int16_t ledIdx = x + col;
          if (ledIdx >= 0 && ledIdx < NUM_LEDS_PER_STRIP) {
            leds[row][ledIdx] = CRGB(brightness, brightness / 2, 0);
          }
        }
      }
    }
  }
}

static void sceneMissing(unsigned long elapsedMs) {
  const char text[] = "MISSING K666";
  uint8_t totalW = textWidth(text);
  int16_t targetX = (NUM_LEDS_PER_STRIP - totalW) / 2;
  const unsigned long entranceDurationMs = 3000;

  int16_t xOffset;
  if (elapsedMs < entranceDurationMs) {
    float scrollSpeed = (float)(NUM_LEDS_PER_STRIP - targetX) / (float)entranceDurationMs;
    xOffset = NUM_LEDS_PER_STRIP - (int16_t)(scrollSpeed * elapsedMs);
  } else {
    xOffset = targetX;
  }

  float revealTime = (float)elapsedMs / (float)entranceDurationMs * 6.0f;
  if (revealTime > 6.0f) revealTime = 6.0f;
  uint8_t stripsToShow = (uint8_t)revealTime;

  CRGB orange(255, 128, 0);
  for (uint8_t charIdx = 0; text[charIdx] != '\0'; charIdx++) {
    drawGlyphRowLimited(text[charIdx], xOffset + charIdx * CHAR_STRIDE, orange, stripsToShow);
  }
}

static void sceneFirmware(unsigned long elapsedMs) {
  const char text[] = "FIRMWARE ERROR";
  uint8_t totalW = textWidth(text);
  int16_t center = (NUM_LEDS_PER_STRIP - totalW) / 2;

  uint8_t brightness = ((elapsedMs * 10) / 1000) % 2 ? 255 : 100;
  CRGB red(brightness, 0, 0);
  drawTextAt(text, center, red);
}

static void sceneFlames(unsigned long elapsedMs) {
  const char text[] = "FIRMWARE ERROR";
  uint8_t totalW = textWidth(text);
  int16_t center = (NUM_LEDS_PER_STRIP - totalW) / 2;

  uint8_t verticalOffset = (uint8_t)((elapsedMs * (NUM_STRIPS + 2)) / 2000UL);
  float flameT = (float)elapsedMs / 2000.0f;
  if (flameT > 1.0f) flameT = 1.0f;
  uint8_t hue = 32 + (uint8_t)(64 * flameT);

  for (uint8_t charIdx = 0; text[charIdx] != '\0'; charIdx++) {
    drawGlyphStripOffset(text[charIdx], center + charIdx * CHAR_STRIDE, verticalOffset, CHSV(hue, 255, 255));
  }
}

void wernerPatternOnEnter() {
  wernerSequenceStartMs = millis();
}

void wernerPatternUpdate() {
  fillAll(CRGB::Black);

  unsigned long elapsed = millis() - wernerSequenceStartMs;
  if (elapsed >= WERNER_PATTERN_DURATION) {
    wernerSequenceStartMs = millis();
    elapsed = 0;
  }

  if (elapsed < SCENE_BOOTING_END) {
    sceneBooting(elapsed);
  } else if (elapsed < SCENE_JAHRE_END) {
    sceneJahre(elapsed - SCENE_BOOTING_END);
  } else if (elapsed < SCENE_HIGHWAY_END) {
    sceneHighway(elapsed - SCENE_JAHRE_END);
  } else if (elapsed < SCENE_FREQUENCY_END) {
    sceneFrequency(elapsed - SCENE_HIGHWAY_END);
  } else if (elapsed < SCENE_BLACK_END) {
    // black
  } else if (elapsed < SCENE_MISSING_END) {
    sceneMissing(elapsed - SCENE_BLACK_END);
  } else if (elapsed < SCENE_FIRMWARE_END) {
    sceneFirmware(elapsed - SCENE_MISSING_END);
  } else if (elapsed < SCENE_FLAMES_END) {
    sceneFlames(elapsed - SCENE_FIRMWARE_END);
  }
  // SCENE_FLAMES_END .. WERNER_PATTERN_DURATION: pause (black)
}
