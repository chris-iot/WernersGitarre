# Werner LED Pattern Tools

Python toolkit for simulating and visualizing the 9-scene Werner LED pattern without physical hardware.

## Files

- **font_generator.py** - Generates 6-pixel-tall bitmap fonts for text rendering
- **werner_simulator.py** - Main simulator with all 9 scenes (Booting, Jahren, Highway, Guitar Hero, Frequency, Missing, Firmware, Flames, Pause)
- **werner_pattern.gif** - Generated 35-second animation (1750 frames, 50 FPS)
- **requirements.txt** - Python dependencies (Pillow, numpy)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Generate Animation Preview

```python
from werner_simulator import generate_animation

# Generate 35-second animation as GIF
frames = generate_animation(duration_sec=35, fps=50, output_gif="werner_pattern.gif")
```

### Export Fonts to C++

```python
from font_generator import export_bitmaps_as_cpp

cpp_code = export_bitmaps_as_cpp()
print(cpp_code)
# Copy output to firmware if needed
```

### Test Simulator

```python
from werner_simulator import WernerSimulator

sim = WernerSimulator()
sim.update(elapsed_ms=5000)  # 5 seconds
frame = sim.get_frame_data()  # Returns (6, 128, 3) numpy array (6 strips × 128 LEDs × RGB)
```

## Scene Breakdown

| Scene | Duration | Description |
|-------|----------|-------------|
| Booting | 0-2s | "Booting" text with animated dots (•, ••, •••) |
| Jahren | 2-6s | "41+ Jahre Werner @R&S" scrolling white text |
| Highway | 6-12s | "Get Ready for the Highway to Hell" scrolling, white→red gradient |
| Guitar Hero | 12-20s | Simulated note drops on colored strips (AC/DC timing) |
| Frequency | 20-22s | "Frequency unlocked" centered, orange, fades out 22-23s |
| Missing | 23-28s | "Missing K666" drops down row-by-row (strips reveal progressively) |
| Firmware | 28-30s | "Firmware error" red text with flicker effect |
| Flames | 30-32s | "FLAMES" text moving upward with color shift (orange→red→yellow) |
| Pause | 32-35s | All black (rest) before loop repeats |

## LED Array Configuration

- **Strips:** 6 parallel WS2812B strips (D1, D2, D4, D5, D6, D7)
- **LEDs per strip:** 128
- **Total LEDs:** 768
- **Simulation resolution:** 1024×48 pixels (128 LEDs wide, 6 strips tall, 8px per LED)
- **Frame rate:** 50 FPS (20ms per frame) to match firmware

## Font System

Fonts are 6 pixels tall × 5 pixels wide per character. Each character is represented as 6 bytes, one per row.

Example (letter 'W'):
```python
'W': [
    0b10001,  # row 0 (bottom strip D1)
    0b10001,  # row 1
    0b10001,  # row 2
    0b10101,  # row 3
    0b10101,  # row 4
    0b10001   # row 5 (top)
]
```

Bit positions (LSB = right pixel):
```
Pixel: 4 3 2 1 0
Byte:  0bX X X X X
```

## Color System

Colors use HSV model in firmware but RGB for preview:
- **HSV:** (H: 0-255, S: 0-255, V: 0-255)
  - H=0: Red, H=85: Green, H=170: Blue
  - S=0: White, S=255: Full saturation
  - V=0: Off, V=255: Full brightness

- **RGB:** 8-bit per channel (0-255)
  - (255, 255, 255): White
  - (255, 0, 0): Red
  - (0, 255, 0): Green
  - (255, 255, 0): Yellow
  - (255, 128, 0): Orange

## Animation Output

The simulator generates frames as PIL images. Use the `render_frame_image()` method for PNG export or `get_frame_data()` for numpy arrays.

```python
sim.update(5000)  # 5 seconds

# Method 1: PIL image
img = sim.render_frame_image(pixel_size=8)
img.save("frame_5s.png")

# Method 2: Numpy array
frame = sim.get_frame_data()  # Shape: (6, 128, 3)
print(frame[0, 100])  # Strip 0, LED 100 RGB value
```

## Notes

- GIF playback frame timing is `duration=20` (20ms per frame for 50 FPS)
- Simulator does not use FastLED but closely mimics its color behavior
- Text rendering clips at strip boundaries (no wrapping)
- Animation loops automatically after 35 seconds in firmware via `patternChanged` flag
