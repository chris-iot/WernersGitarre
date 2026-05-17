# Werner Pattern – Bring-up & Extension Reference

This file summarizes the key architecture and implementation decisions (as of: simulator → firmware port + immediate pattern switching). For follow-up work, simply point to this file.

---

## Hardware Display

| Property | Value |
|----------|-------|
| Strips | 6 × WS2812B, 128 LEDs each |
| Layout | 6 pixels tall × 128 pixels wide |
| X axis | 0 = left, 127 = right (strip end) |
| Y axis / strips | `leds[0]` = **D1 bottom** … `leds[5]` = **D7 top** |
| DATA_PINS | D1, D2, D4, D5, D6, D7 (see `src/main.cpp`) |
| Brightness | `BRIGHTNESS 120` |
| Frame rate | ~50 FPS (`delay(20)` in `loop()`) |

**Verify orientation (without hardware):** The letter **W** is asymmetric – outer legs in the lower bitmap rows. Font row 0 = bottom strip (D1). Canonical W bitmap: `{0x11, 0x11, 0x15, 0x15, 0x1b, 0x11}`.

**GIF preview:** In `tools/werner_simulator.py` → `render_frame_image()`, strip 0 is drawn at the **top**. The GIF is **vertically flipped** relative to real hardware.

---

## Files & Responsibilities

```
src/
  main.cpp              # Potentiometer, pattern selection, loop(), immediate pattern switch
  werner_pattern.cpp/h  # 9-scene animation, text rendering
  werner_fonts.h        # Font declarations + scene timing constants (generated)
  werner_fonts.cpp      # fontBitmaps[256] in PROGMEM, fontBitmapRow()

tools/
  font_generator.py       # Canonical 6×5 bitmaps (source of truth)
  export_fonts_to_cpp.py  # Generates src/werner_fonts.h + .cpp
  werner_simulator.py     # Reference implementation + GIF (werner_pattern.gif)
```

**Recommended order when making changes:**
1. Adjust logic/colors/timing in `werner_simulator.py` and check the GIF
2. Port the same logic to `werner_pattern.cpp`
3. Add new characters in `font_generator.py`, then re-export fonts

**Regenerate fonts:**
```bash
cd tools
python export_fonts_to_cpp.py
```

**Build:**
```bash
pio run
```

---

## Potentiometer → Pattern

| Pot range | Pattern |
|-----------|---------|
| 0–139 | 0 = Werner (9-scene sequence) |
| 140–1023 | 1–10 = Rainbow, Theater, Wave, … |

Implementation: `updatePatternFromPot()` in `src/main.cpp`.

---

## Immediate Pattern Switch (User Feedback)

On **every** pot change (`patternChanged == true`) in `loop()`, **before** the new pattern runs:

1. `fillAll(CRGB::Black)`
2. `gHue = 0` (reset animation phase for all other patterns)
3. `FastLED.show()` (clear the last frame of the old pattern immediately)
4. If new pattern = 0: `wernerPatternOnEnter()` (restart sequence from the beginning)

Werner runs **only** while pattern 0 is active. Leaving pattern 0 stops the sequence; selecting it again starts at “BOOTING”.

Maximum response latency ≈ one `loop()` iteration (~20 ms + pot read).

---

## Werner Sequence (37 s, then loop)

Time base: `millis() - wernerSequenceStartMs`, constants in `src/werner_fonts.h`.

| Scene | Start (ms) | End (ms) | Content |
|-------|------------|----------|---------|
| Booting | 0 | 2000 | `BOOTING` centered, cyan; yellow dots (all strips), 0–3 every 500 ms |
| Jahre | 2000 | 10000 | Scroll: `41+ JAHRE WERNER BEI ROHDE UND SCHWARZ` (8 s, white) |
| Highway | 10000 | 22000 | Scroll: `GET READY FOR THE HIGHWAY TO HELL` (12 s, white→red via saturation) |
| Frequency | 22000 | 24000 | Centered: `FREQUENCY UNLOCKED`, orange, fade from 1 s |
| Black | 24000 | 25000 | Pause |
| Missing | 25000 | 30000 | `MISSING K666`: 3 s from right, row-by-row reveal |
| Firmware | 30000 | 32000 | `FIRMWARE ERROR` centered, red, flicker |
| Flames | 32000 | 34000 | Same text, flames moving upward (HSV, strip offset) |
| Pause | 34000 | 37000 | Black |

Dispatcher: `wernerPatternUpdate()` in `src/werner_pattern.cpp` (1:1 with `WernerSimulator.update()`).

---

## Font Format

- 6 rows × 5 bits per character
- `rows[0]` = bottom strip, `rows[5]` = top strip
- Bit 4 = left pixel, bit 0 = right pixel
- Character spacing: 5 + 1 = **6** pixels per glyph (`CHAR_STRIDE`)
- Access: `fontBitmapRow(c, row)` via `pgm_read_byte` (ESP8266 PROGMEM)

Booting dots (`•`) are **not** a font – single yellow pixels on **all** 6 strips at `center + charIdx*6 + 2`.

---

## Rendering Helpers (`werner_pattern.cpp`)

| Function | Purpose |
|----------|---------|
| `drawGlyph` | Single character at x |
| `drawTextAt` | String at fixed x position |
| `drawScrollingText` | Scroll right to left |
| `drawPixelAllStrips` | One x, all strips (booting dots) |
| `drawGlyphRowLimited` | Missing: only bottom N rows |
| `drawGlyphStripOffset` | Flames: vertical offset |

Colors follow `werner_simulator.py` (HSV/RGB as there).

---

## Known Pitfalls / History

1. **Old `letterBitmaps[]` in main.cpp** was outdated (wrong W) – removed; use `werner_fonts` only.
2. **`export_fonts_to_cpp.py` comment** must say “row 0 = bottom (D1)”, not “top to bottom”.
3. **`tools/werner_fonts.h`** (if still present) may be stale – authoritative files are **`src/werner_fonts.*`**.
4. **Guitar Hero scene** was removed from the sequence (may still appear in old docs/GIF descriptions).
5. **RAM:** `fontBitmaps` must stay in PROGMEM (~1.5 KB flash instead of RAM).
6. **Reference build stats:** RAM ~37.8%, Flash ~26.7% (NodeMCU v2).

---

## Typical Extensions

| Task | Where to change |
|------|-----------------|
| New scene / timing | `werner_simulator.py` + `werner_pattern.cpp` + `export_fonts_to_cpp.py` (constants) |
| New character | `font_generator.py` → `export_fonts_to_cpp.py` |
| Scroll speed | `drawScrollingText`, `durationMs` per scene |
| Pot thresholds | `updatePatternFromPot()` |
| Faster pattern stop | already in `loop()` on `patternChanged`; optionally reduce `delay(20)` for faster pot response |
| Serial debug | `logStatus()` in `main.cpp` (115200 baud) |

---

## Verification Without Hardware

1. `pio run` – must compile
2. Scene boundaries and formulas: `werner_pattern.cpp` ↔ `werner_simulator.py` line by line
3. Optional: `cd tools && python werner_simulator.py` → `werner_pattern.gif`
4. W bitmap: ASCII 87 = `{0x11, 0x11, 0x15, 0x15, 0x1b, 0x11}`

---

## Short Prompt for the Assistant

> Read `WERNER_BRINGUP.md` in the project root. Display: 6×128, strip 0 = D1 bottom. Werner pattern in `src/werner_pattern.cpp`, reference `tools/werner_simulator.py`, fonts via `font_generator.py` / `export_fonts_to_cpp.py`. Pattern switch: immediate black + show in `main.cpp` loop.
