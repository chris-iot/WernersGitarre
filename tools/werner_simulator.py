"""
Werner LED pattern simulator - 9-scene sequence.
Generates animation frames without physical hardware.
"""

import numpy as np
from PIL import Image, ImageDraw
from font_generator import create_font_bitmaps

# LED Configuration (matches firmware)
NUM_STRIPS = 6
NUM_LEDS = 128
FRAME_RATE = 50  # ~20ms per iteration
BRIGHTNESS = 120

# Scene timing (in seconds)
SCENE_TIMING = {
    'booting': (0, 2),
    'jahre': (2, 10),
    'highway': (10, 22),
    'pause': (22, 37)
}

class LEDStrip:
    """Simulate a single WS2812B LED strip."""
    
    def __init__(self, num_leds=128):
        self.leds = np.zeros((num_leds, 3), dtype=np.uint8)  # RGB
    
    def set_pixel(self, index, r, g, b):
        """Set pixel at index to RGB color."""
        if 0 <= index < len(self.leds):
            self.leds[index] = [r, g, b]
    
    def set_hsv(self, index, h, s, v):
        """Set pixel using HSV color (h: 0-255, s: 0-255, v: 0-255)."""
        if 0 <= index < len(self.leds):
            # Convert HSV to RGB
            c = (v / 255.0) * (s / 255.0)
            h_dash = (h / 255.0) * 6.0
            x = c * (1 - abs((h_dash % 2) - 1))
            
            if h_dash < 1:
                r, g, b = c, x, 0
            elif h_dash < 2:
                r, g, b = x, c, 0
            elif h_dash < 3:
                r, g, b = 0, c, x
            elif h_dash < 4:
                r, g, b = 0, x, c
            elif h_dash < 5:
                r, g, b = x, 0, c
            else:
                r, g, b = c, 0, x
            
            m = (v / 255.0) - c
            r = int((r + m) * 255)
            g = int((g + m) * 255)
            b = int((b + m) * 255)
            self.leds[index] = [r, g, b]
    
    def clear(self):
        """Clear all pixels."""
        self.leds.fill(0)
    
    def fill_solid(self, r, g, b):
        """Fill strip with solid color."""
        self.leds[:] = [r, g, b]
    
    def get_frame(self):
        """Return current LED state."""
        return self.leds.copy()


class WernerSimulator:
    """Simulate the 9-scene Werner pattern."""
    
    def __init__(self):
        self.strips = [LEDStrip(NUM_LEDS) for _ in range(NUM_STRIPS)]
        self.fonts = create_font_bitmaps()
        self.time_ms = 0
        self.frame_count = 0
    
    def update(self, elapsed_ms):
        """Update LED state for given elapsed time in milliseconds."""
        self.time_ms = elapsed_ms
        self.frame_count = elapsed_ms // (1000 // FRAME_RATE)
        
        # Clear strips
        for strip in self.strips:
            strip.clear()
        
        # Determine which scene to render
        elapsed_sec = elapsed_ms / 1000.0
        
        if elapsed_sec < 2:
            self._scene_booting(elapsed_sec)
        elif elapsed_sec < 10:
            self._scene_jahre(elapsed_sec - 2)
        elif elapsed_sec < 22:
            self._scene_highway(elapsed_sec - 10)
        elif elapsed_sec < 24:
            self._scene_frequency(elapsed_sec - 22)
        elif elapsed_sec < 25:
            pass  # Short black transition
        elif elapsed_sec < 30:
            self._scene_missing(elapsed_sec - 25)
        elif elapsed_sec < 32:
            self._scene_firmware(elapsed_sec - 30)
        elif elapsed_sec < 34:
            self._scene_flames(elapsed_sec - 32)
        elif elapsed_sec < 37:
            pass  # Final pause
    
    def _render_text(self, text, scroll_pos, color_hsv=None):
        """
        Render scrolling text across all strips.
        scroll_pos: 0-128 horizontal scroll position
        color_hsv: (h, s, v) or None for gradient
        """
        char_width = 5
        spacing = 1
        scroll_pos = int(scroll_pos)  # Ensure integer
        
        for char_idx, char in enumerate(text):
            if char not in self.fonts:
                continue
            
            bitmap = self.fonts[char]
            char_x = char_idx * (char_width + spacing) - scroll_pos
            
            if char_x + char_width < 0 or char_x > NUM_LEDS:
                continue
            
            # Render character to all strips
            for led_idx in range(NUM_LEDS):
                col = led_idx - char_x
                if 0 <= col < char_width:
                    # Check which strips should have this pixel lit
                    for strip_idx, row_bits in enumerate(bitmap):
                        if row_bits & (1 << (4 - int(col))):
                            if color_hsv:
                                h, s, v = color_hsv
                                self.strips[strip_idx].set_hsv(led_idx, h, s, v)
                            else:
                                # Default white
                                self.strips[strip_idx].set_pixel(led_idx, 255, 255, 255)
    
    def _render_scrolling_text(self, text, elapsed, duration, color_hsv=None):
        """Render text that scrolls in from the right and out to the left."""
        char_width = 5
        spacing = 1
        total_width = len(text) * (char_width + spacing)
        if duration <= 0:
            duration = 1.0
        scroll_speed = (NUM_LEDS + total_width) / duration
        scroll_pos = scroll_speed * elapsed
        start_x = NUM_LEDS
        
        for char_idx, char in enumerate(text):
            if char not in self.fonts:
                continue
            
            bitmap = self.fonts[char]
            char_x = start_x + char_idx * (char_width + spacing) - scroll_pos
            
            if char_x + char_width < 0 or char_x > NUM_LEDS:
                continue
            
            for led_idx in range(NUM_LEDS):
                col = led_idx - char_x
                if 0 <= col < char_width:
                    for strip_idx, row_bits in enumerate(bitmap):
                        if row_bits & (1 << (4 - int(col))):
                            if color_hsv:
                                h, s, v = color_hsv
                                self.strips[strip_idx].set_hsv(led_idx, h, s, v)
                            else:
                                self.strips[strip_idx].set_pixel(led_idx, 255, 255, 255)
    
    def _scene_booting(self, elapsed):
        """Booting scene: "BOOTING" with animated dots."""
        text = "BOOTING"
        
        # Animated dots: cycle every 0.5 seconds
        dot_count = int((elapsed / 0.5) % 4)
        dots = "•" * dot_count
        
        # Center text with dots
        animation_text = f"{dots}{text}{dots}"
        
        # Render centered
        total_width = len(animation_text) * 6
        center = (NUM_LEDS - total_width) // 2
        
        for char_idx, char in enumerate(animation_text):
            if char == "•":
                # Render dot as small LED bright spot on center strip
                x = center + char_idx * 6 + 2
                if 0 <= x < NUM_LEDS:
                    for strip in self.strips:
                        strip.set_pixel(x, 255, 200, 0)  # Yellow
            elif char in self.fonts:
                bitmap = self.fonts[char]
                x = center + char_idx * 6
                
                for strip_idx, row_bits in enumerate(bitmap):
                    for col in range(5):
                        if row_bits & (1 << (4 - int(col))):
                            led_idx = x + col
                            if 0 <= led_idx < NUM_LEDS:
                                self.strips[strip_idx].set_pixel(led_idx, 0, 255, 255)  # Cyan
    
    def _scene_jahre(self, elapsed):
        """Jahre scene: white scrolling text."""
        text = "41+ JAHRE WERNER BEI ROHDE UND SCHWARZ"
        self._render_scrolling_text(text, elapsed, duration=8.0, color_hsv=(0, 0, 255))  # White
    
    def _scene_highway(self, elapsed):
        """Highway to Hell: white→red gradient scrolling."""
        text = "GET READY FOR THE HIGHWAY TO HELL"
        
        hue = 0
        saturation = int(255 * (elapsed / 12.0))
        saturation = min(saturation, 255)
        
        self._render_scrolling_text(text, elapsed, duration=12.0, color_hsv=(hue, saturation, 255))
    
    def _scene_frequency(self, elapsed):
        """Frequency unlocked: centered static text with fade."""
        text = "FREQUENCY UNLOCKED"
        total_width = len(text) * 6
        center = (NUM_LEDS - total_width) // 2
        
        # Fade out from 1-2s
        fade_factor = max(0, 1 - (elapsed - 1) / 1.0)
        brightness = int(255 * fade_factor)
        brightness = max(0, min(255, brightness))  # Clamp to 0-255
        
        for char_idx, char in enumerate(text):
            if char in self.fonts:
                bitmap = self.fonts[char]
                x = center + char_idx * 6
                
                for strip_idx, row_bits in enumerate(bitmap):
                    for col in range(5):
                        if row_bits & (1 << (4 - int(col))):
                            led_idx = x + col
                            if 0 <= led_idx < NUM_LEDS:
                                # Orange with fade
                                r = brightness
                                g = brightness // 2
                                b = 0
                                self.strips[strip_idx].set_pixel(led_idx, r, g, b)
    
    def _scene_missing(self, elapsed):
        """Missing K666: drops down row by row and holds for 2 seconds."""
        text = "MISSING K666"
        total_width = len(text) * 6
        target_x = (NUM_LEDS - total_width) // 2
        entrance_duration = 3.0
        
        if elapsed < entrance_duration:
            scroll_speed = (NUM_LEDS - target_x) / entrance_duration
            x_offset = NUM_LEDS - scroll_speed * elapsed
        else:
            x_offset = target_x
        
        reveal_time = min(6, (elapsed / entrance_duration) * 6)
        strips_to_show = int(reveal_time)
        
        for char_idx, char in enumerate(text):
            if char in self.fonts:
                bitmap = self.fonts[char]
                x = int(x_offset) + char_idx * 6
                
                for strip_idx, row_bits in enumerate(bitmap):
                    if strip_idx < strips_to_show:
                        for col in range(5):
                            if row_bits & (1 << (4 - int(col))):
                                led_idx = x + col
                                if 0 <= led_idx < NUM_LEDS:
                                    self.strips[strip_idx].set_pixel(led_idx, 255, 128, 0)  # Orange
    
    def _scene_firmware(self, elapsed):
        """Firmware error: red text with flicker."""
        text = "FIRMWARE ERROR"
        total_width = len(text) * 6
        center = (NUM_LEDS - total_width) // 2
        
        flicker = int((elapsed * 10) % 2)
        brightness = 255 if flicker else 100
        
        for char_idx, char in enumerate(text):
            if char in self.fonts:
                bitmap = self.fonts[char]
                x = center + char_idx * 6
                
                for strip_idx, row_bits in enumerate(bitmap):
                    for col in range(5):
                        if row_bits & (1 << (4 - int(col))):
                            led_idx = x + col
                            if 0 <= led_idx < NUM_LEDS:
                                self.strips[strip_idx].set_pixel(led_idx, brightness, 0, 0)  # Red
    
    def _scene_flames(self, elapsed):
        """Flames eating the Firmware Error text upwards."""
        text = "FIRMWARE ERROR"
        total_width = len(text) * 6
        center = (NUM_LEDS - total_width) // 2
        
        vertical_offset = int((elapsed / 2.0) * (NUM_STRIPS + 2))
        hue = int(32 + 64 * min(1.0, elapsed / 2.0))
        
        for char_idx, char in enumerate(text):
            if char in self.fonts:
                bitmap = self.fonts[char]
                x = center + char_idx * 6
                
                for strip_idx, row_bits in enumerate(bitmap):
                    for col in range(5):
                        if row_bits & (1 << (4 - int(col))):
                            led_idx = x + col
                            target_strip = strip_idx + vertical_offset
                            if 0 <= target_strip < NUM_STRIPS:
                                self.strips[target_strip].set_hsv(led_idx, hue, 255, 255)
    
    def get_frame_data(self):
        """Get current frame as numpy array (6, 128, 3) RGB."""
        frame = np.zeros((NUM_STRIPS, NUM_LEDS, 3), dtype=np.uint8)
        for strip_idx, strip in enumerate(self.strips):
            frame[strip_idx] = strip.get_frame()
        return frame
    
    def render_frame_image(self, pixel_size=8):
        """Render current frame as PIL Image."""
        frame = self.get_frame_data()
        
        # Create image: 128 LEDs wide, 6 strips tall
        img = Image.new('RGB', (NUM_LEDS * pixel_size, NUM_STRIPS * pixel_size))
        pixels = img.load()
        
        for strip_idx in range(NUM_STRIPS):
            for led_idx in range(NUM_LEDS):
                r, g, b = frame[strip_idx, led_idx]
                # Fill pixel_size x pixel_size block, mapping strip 0 to top
                x0 = led_idx * pixel_size
                y0 = strip_idx * pixel_size
                for dx in range(pixel_size):
                    for dy in range(pixel_size):
                        pixels[x0 + dx, y0 + dy] = (r, g, b)
        
        return img


def generate_animation(duration_sec=35, fps=50, output_gif=None):
    """Generate animation frames."""
    simulator = WernerSimulator()
    frames = []
    
    total_frames = duration_sec * fps
    for frame_idx in range(total_frames):
        elapsed_ms = int(frame_idx * 1000 / fps)
        simulator.update(elapsed_ms)
        
        # Render frame
        img = simulator.render_frame_image(pixel_size=8)
        frames.append(img)
        
        # Progress
        if (frame_idx + 1) % (fps * 5) == 0:
            print(f"Generated {frame_idx + 1}/{total_frames} frames ({elapsed_ms / 1000:.1f}s)")
    
    if output_gif:
        print(f"Saving to {output_gif}...")
        frames[0].save(
            output_gif,
            save_all=True,
            append_images=frames[1:],
            duration=20,  # 20ms per frame
            loop=0
        )
    
    return frames


if __name__ == "__main__":
    print("Generating Werner pattern animation...")
    frames = generate_animation(duration_sec=37, fps=50, output_gif="werner_pattern.gif")
    print(f"Done! Generated {len(frames)} frames.")
