#include <Arduino.h>
#include <FastLED.h>

// NodeMCU V3 Pin Mapping (D-pins to GPIO)
#define D0 16
#define D1 5
#define D2 4
#define D3 0
#define D4 2
#define D5 14
#define D6 12
#define D7 13
#define D8 15

// Constants
#define NUM_STRIPS 6
#define NUM_LEDS_PER_STRIP 128
#define LED_TYPE WS2812B
#define COLOR_ORDER GRB
#define BRIGHTNESS 120

const uint8_t DATA_PINS[NUM_STRIPS] = {D1, D2, D4, D5, D6, D7};
const uint8_t POT_PIN = A0;

CRGB leds[NUM_STRIPS][NUM_LEDS_PER_STRIP];

uint8_t currentPattern = 0;
uint8_t lastPatternIndex = 255;
bool patternChanged = false;
uint8_t gHue = 0;
uint8_t lastPattern = 255;
unsigned long lastLogTime = 0;

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

const char scrollText[] = "WERNER";
const uint8_t letterHeight = 6;
const uint8_t letterWidth = 5;
const uint8_t letterSpacing = 1;

const uint8_t letterBitmaps[][6] = {
  // W (bottom-to-top rows)
  {0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b10001},
  // E
  {0b11111, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111},
  // R
  {0b11110, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001},
  // N
  {0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001}
};

const uint8_t getLetterIndex(char c) {
  switch (c) {
    case 'W': return 0;
    case 'E': return 1;
    case 'R': return 2;
    case 'N': return 3;
    default: return 0;
  }
}

void patternWerner() {
  fillAll(CRGB::Black);
  const uint8_t textLength = sizeof(scrollText) - 1;
  const uint8_t wordWidth = textLength * (letterWidth + letterSpacing) - letterSpacing;
  const uint8_t copySpacing = 2;
  const uint8_t blockWidth = wordWidth + copySpacing;
  uint8_t repeats = NUM_LEDS_PER_STRIP / blockWidth;
  if (repeats == 0) {
    repeats = 1;
  }
  const int totalWidth = repeats * blockWidth - copySpacing;
  const int visibleWidth = NUM_LEDS_PER_STRIP;
  const int scrollPeriod = visibleWidth + totalWidth;
  const int startX = visibleWidth - (gHue % scrollPeriod);

  for (uint8_t copyIndex = 0; copyIndex < repeats; copyIndex++) {
    int wordX = startX + copyIndex * blockWidth;
    for (uint8_t charIndex = 0; scrollText[charIndex] != '\0'; charIndex++) {
      uint8_t letterIndex = getLetterIndex(scrollText[charIndex]);
      int charX = wordX + charIndex * (letterWidth + letterSpacing);
      CRGB color = CRGB::White;
      for (uint8_t row = 0; row < letterHeight; row++) {
        int stripIndex = row; // 0 = D1 bottom, 5 = top
        for (uint8_t col = 0; col < letterWidth; col++) {
          int displayCol = charX + col;
          if (displayCol < 0 || displayCol >= NUM_LEDS_PER_STRIP) {
            continue;
          }
          if (letterBitmaps[letterIndex][row] & (1 << (letterWidth - 1 - col))) {
            leds[stripIndex][displayCol] = color;
          }
        }
      }
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

void logStatus() {
  unsigned long now = millis();
  if (now - lastLogTime < 1000) {
    return;
  }
  lastLogTime = now;
  if (currentPattern != lastPattern) {
    Serial.print("Pattern selected: ");
    Serial.println(currentPattern);
    lastPattern = currentPattern;
  } else {
    Serial.print("Running pattern ");
    Serial.print(currentPattern);
    Serial.print("  Hue= ");
    Serial.println(gHue);
  }
}

void updatePatternFromPot() {
  int potValue = analogRead(POT_PIN);
  potValue = constrain(potValue, 0, 1023);
  
  uint8_t newPattern;
  if (potValue < 140) {
    newPattern = 0;  // Pattern 0 (Werner) spans 0-140
  } else {
    newPattern = map(potValue, 140, 1023, 1, 10);
    newPattern = constrain(newPattern, 1, 10);
  }
  
  if (newPattern != lastPatternIndex) {
    patternChanged = true;
    lastPatternIndex = newPattern;
  }
  currentPattern = newPattern;
}

void setup() {
  delay(1000);
  Serial.begin(115200);
  Serial.println("Starting FastLED NodeMCU controller");
  Serial.print("Data pins: ");
  for (uint8_t i = 0; i < NUM_STRIPS; i++) {
    Serial.print(DATA_PINS[i]);
    if (i + 1 < NUM_STRIPS) {
      Serial.print(", ");
    }
  }
  Serial.println();
  currentPattern = 0;
  lastPatternIndex = 0;
  lastPattern = 255;
  patternChanged = false;

  FastLED.addLeds<LED_TYPE, D1, COLOR_ORDER>(leds[0], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, D2, COLOR_ORDER>(leds[1], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, D4, COLOR_ORDER>(leds[2], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, D5, COLOR_ORDER>(leds[3], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, D6, COLOR_ORDER>(leds[4], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, D7, COLOR_ORDER>(leds[5], NUM_LEDS_PER_STRIP);
  FastLED.setBrightness(BRIGHTNESS);
  pinMode(POT_PIN, INPUT);
}

void loop() {
  updatePatternFromPot();
  patternChanged = false;  // Clear flag after checking patterns

  switch (currentPattern) {
    case 0:
      patternWerner();
      break;
    case 1:
      patternRainbow();
      break;
    case 2:
      patternTheaterChase();
      break;
    case 3:
      patternWave();
      break;
    case 4:
      patternScanner();
      break;
    case 5:
      patternSparkle();
      break;
    case 6:
      patternMirrorGradient();
      break;
    case 7:
      patternDiagonalChase();
      break;
    case 8:
      patternEqualizer();
      break;
    case 9:
      patternStripPulse();
      break;
    case 10:
      patternStackedWaves();
      break;
  }

  FastLED.show();
  logStatus();
  gHue++;
  delay(20);
}
