#include <Arduino.h>
#include <FastLED.h>

// Constants
#define NUM_STRIPS 4
#define NUM_LEDS_PER_STRIP 128
#define LED_TYPE WS2812B
#define COLOR_ORDER GRB
#define BRIGHTNESS 120

const uint8_t DATA_PINS[NUM_STRIPS] = {2, 3, 4, 5};
const uint8_t POT_PIN = A0;

CRGB leds[NUM_STRIPS][NUM_LEDS_PER_STRIP];

uint8_t currentPattern = 0;
uint8_t gHue = 0;

void fillAll(CRGB color) {
  for (uint8_t strip = 0; strip < NUM_STRIPS; strip++) {
    fill_solid(leds[strip], NUM_LEDS_PER_STRIP, color);
  }
}

void patternRainbow() {
  for (uint8_t strip = 0; strip < NUM_STRIPS; strip++) {
    for (uint16_t i = 0; i < NUM_LEDS_PER_STRIP; i++) {
      leds[strip][i] = CHSV((gHue + i * 2 + strip * 32) & 0xFF, 255, 255);
    }
  }
}

void patternTheaterChase() {
  for (uint8_t strip = 0; strip < NUM_STRIPS; strip++) {
    for (uint16_t i = 0; i < NUM_LEDS_PER_STRIP; i++) {
      if ((i + gHue / 16 + strip) % 3 == 0) {
        leds[strip][i] = CHSV((gHue + strip * 40) & 0xFF, 255, 255);
      } else {
        leds[strip][i] = CRGB::Black;
      }
    }
  }
}

void patternWave() {
  for (uint8_t strip = 0; strip < NUM_STRIPS; strip++) {
    for (uint16_t i = 0; i < NUM_LEDS_PER_STRIP; i++) {
      uint8_t position = (i * 8 + strip * 64 + gHue * 2) & 0xFF;
      leds[strip][i] = CHSV(position, 200, beatsin8(30 + strip * 10, 120, 255));
    }
  }
}

void patternScanner() {
  fillAll(CRGB::Black);
  uint16_t pos = beat16(12) >> 8;
  for (uint8_t strip = 0; strip < NUM_STRIPS; strip++) {
    uint16_t index = (pos + strip * 32) % NUM_LEDS_PER_STRIP;
    leds[strip][index] = CHSV((gHue + strip * 50) & 0xFF, 255, 255);
    if (index > 0) leds[strip][index - 1] = CRGB::Black;
  }
}

void patternSparkle() {
  fillAll(CHSV(gHue, 255, 30));
  for (uint8_t strip = 0; strip < NUM_STRIPS; strip++) {
    if (random8() < 64) {
      leds[strip][random16(NUM_LEDS_PER_STRIP)] = CHSV((gHue + strip * 50) & 0xFF, 255, 255);
    }
  }
}

void patternMirrorGradient() {
  for (uint8_t strip = 0; strip < NUM_STRIPS; strip++) {
    uint8_t hue = gHue + strip * 64;
    for (uint16_t i = 0; i < NUM_LEDS_PER_STRIP; i++) {
      leds[strip][i] = CHSV(hue, 255, 255);
    }
  }
}

void patternDiagonalChase() {
  fillAll(CRGB::Black);
  for (uint8_t strip = 0; strip < NUM_STRIPS; strip++) {
    uint16_t index = (gHue * 2 + strip * 32) % NUM_LEDS_PER_STRIP;
    leds[strip][index] = CHSV((gHue * 2 + strip * 60) & 0xFF, 255, 255);
    if (index > 0) leds[strip][index - 1] = CHSV((gHue * 2 + strip * 60) & 0xFF, 255, 128);
  }
}

void patternEqualizer() {
  fillAll(CRGB::Black);
  for (uint8_t strip = 0; strip < NUM_STRIPS; strip++) {
    uint8_t height = beatsin8(20 + strip * 5, 10, NUM_LEDS_PER_STRIP - 1);
    for (uint16_t i = 0; i < height; i++) {
      leds[strip][i] = CHSV((gHue + strip * 50) & 0xFF, 255, 255);
    }
  }
}

void patternStripPulse() {
  fillAll(CRGB::Black);
  uint8_t centerStrip = 1;
  uint16_t pos = beat16(12) >> 8;
  for (uint8_t strip = 0; strip < NUM_STRIPS; strip++) {
    uint8_t brightness = beatsin8(10 + (abs(strip - centerStrip) * 5), 50, 255);
    for (uint16_t i = 0; i < NUM_LEDS_PER_STRIP; i++) {
      leds[strip][i] = CHSV((gHue + strip * 40 + i / 2) & 0xFF, 200, brightness);
    }
  }
}

void patternStackedWaves() {
  for (uint8_t strip = 0; strip < NUM_STRIPS; strip++) {
    for (uint16_t i = 0; i < NUM_LEDS_PER_STRIP; i++) {
      uint8_t wave = beatsin8(20 - strip * 3, 0, 255, 0, (i * 2) & 0xFF);
      leds[strip][i] = CHSV((gHue + strip * 40) & 0xFF, 200, wave);
    }
  }
}

void updatePatternFromPot() {
  int potValue = analogRead(POT_PIN);
  currentPattern = map(potValue, 0, 1023, 0, 9);
}

void setup() {
  delay(1000);
  FastLED.addLeds<LED_TYPE, 2, COLOR_ORDER>(leds[0], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, 3, COLOR_ORDER>(leds[1], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, 4, COLOR_ORDER>(leds[2], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, 5, COLOR_ORDER>(leds[3], NUM_LEDS_PER_STRIP);
  FastLED.setBrightness(BRIGHTNESS);
  pinMode(POT_PIN, INPUT);
}

void loop() {
  updatePatternFromPot();

  switch (currentPattern) {
    case 0:
      patternRainbow();
      break;
    case 1:
      patternTheaterChase();
      break;
    case 2:
      patternWave();
      break;
    case 3:
      patternScanner();
      break;
    case 4:
      patternSparkle();
      break;
    case 5:
      patternMirrorGradient();
      break;
    case 6:
      patternDiagonalChase();
      break;
    case 7:
      patternEqualizer();
      break;
    case 8:
      patternStripPulse();
      break;
    case 9:
      patternStackedWaves();
      break;
  }

  FastLED.show();
  gHue++;
  delay(20);
}
