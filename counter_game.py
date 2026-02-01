#!/usr/bin/env python3
"""
Kids Counter Game - A fun counting game for children
- Press SPACE to increment count by 1
- Press ENTER to auto-increment every 0.5s (any key stops it)
- Displays numbers and cute items with rainbow colors
- Speaks each number using macOS 'say' command
"""

import pygame
import math
import colorsys
import time
import threading
import subprocess
import platform
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 900
BG_COLOR = (245, 245, 250)  # Soft off-white
FONT_SIZE = 150
ITEM_SIZE = 30
COLS = 20
ROWS = 20
ITEM_SPACING_X = SCREEN_WIDTH // (COLS + 1)
ITEM_SPACING_Y = 35
MARGIN_TOP = 10

# Shape types for drawing
SHAPES = ["circle", "square", "triangle", "diamond", "star", "heart", "hexagon", "cross"]

class CounterGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Kids Counter Game! Press SPACE or ENTER")
        self.clock = pygame.time.Clock()

        self.count = int(sys.argv[1]) if len(sys.argv) > 1 else 0
        self.auto_incrementing = False
        self.last_auto_increment = 0
        self.auto_increment_delay = 50  # milliseconds

        # Fonts
        self.number_font = pygame.font.Font(None, FONT_SIZE)

        # Check if we're on macOS for 'say' command
        self.is_macos = platform.system() == "Darwin"
        self.say_available = self.is_macos

        if not self.say_available:
            print("Warning: 'say' command only available on macOS.")
            print("Audio will be disabled.")

    def number_to_words(self, number):
        """Convert a number to its English word representation (up to quadrillion)"""
        if number == 0:
            return "zero"

        units = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
                 "seventeen", "eighteen", "nineteen"]
        tens = ["", "ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
                "eighty", "ninety"]
        scales = ["", "thousand", "million", "billion", "trillion", "quadrillion"]

        def convert_less_than_thousand(n):
            """Convert numbers less than 1000 to words"""
            if n == 0:
                return ""
            result = ""

            # Hundreds
            if n >= 100:
                result += units[n // 100] + " hundred"
                n %= 100
                if n > 0:
                    result += " "

            # Tens and units
            if n >= 20:
                result += tens[n // 10]
                n %= 10
                if n > 0:
                    result += " " + units[n]
            elif n >= 10:
                result += teens[n - 10]
            elif n > 0:
                result += units[n]

            return result

        # Handle negative numbers (though unlikely for a counter game)
        is_negative = number < 0
        number = abs(number)

        parts = []
        scale_index = 0

        while number > 0:
            chunk = number % 1000
            number = number // 1000

            if chunk > 0:
                chunk_words = convert_less_than_thousand(chunk)
                if scale_index > 0:
                    chunk_words += " " + scales[scale_index]
                parts.append(chunk_words)

            scale_index += 1

        # Combine parts from largest to smallest
        result = " ".join(reversed(parts))

        # Add "and" after hundreds/thousands if there's a remainder less than 100
        # E.g., "one thousand and one" instead of "one thousand one"
        if len(parts) > 1:
            # Check if the smallest part is less than 100
            smallest_part = parts[0]
            if " hundred" not in smallest_part and smallest_part != "":
                # Find the last scale word position
                for i, scale in enumerate(scales[1:], 1):
                    if scale in result:
                        # Insert "and" before the final part
                        last_space_idx = result.rfind(" ")
                        if last_space_idx > 0:
                            result = result[:last_space_idx] + " and" + result[last_space_idx:]
                            break

        if is_negative:
            result = "negative " + result

        return result.strip()

    def speak_number(self, number):
        """Speak a number using macOS 'say' command"""
        if not self.say_available:
            return

        try:
            # Convert number to words before speaking
            # e.g., 1000001 becomes "one million and one"
            words = self.number_to_words(number)
            subprocess.run(["say", "-v", "Fred", "-r", "180", words])
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError) as e:
            pass  # Silently fail if say command has issues

      
    def get_rainbow_color(self, n):
        """Get rainbow color based on number"""
        # Use HSV color space for smooth rainbow transition
        hue = (n * 0.1) % 1.0  # Cycle through hues
        saturation = 0.85
        value = 0.9

        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        return int(r * 255), int(g * 255), int(b * 255)

    def get_item_position(self, index):
        """Get position for item based on index (left to right, top to bottom)"""
        col = index % COLS
        row = index // COLS

        x = ITEM_SPACING_X * (col + 1)
        y = MARGIN_TOP + ITEM_SPACING_Y * (row + 1)

        return x, y

    def increment_count(self):
        """Increment the count"""
        # Speak the current number, rendering is slow
        self.speak_number(self.count)
        self.count += 1



    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                # Stop auto-increment on any key press
                if self.auto_incrementing:
                    self.auto_incrementing = False

                # Space bar - increment by 1
                if event.key == pygame.K_SPACE:
                    self.increment_count()

                # Enter - start auto-increment
                elif event.key == pygame.K_RETURN:
                    self.auto_incrementing = not self.auto_incrementing
                    if self.auto_incrementing:
                        self.last_auto_increment = pygame.time.get_ticks()

                # Escape - quit
                elif event.key == pygame.K_ESCAPE:
                    return False

        return True

    def update(self):
        """Update game state"""
        current_time = pygame.time.get_ticks()

        # Auto-increment logic
        if self.auto_incrementing:
            if current_time - self.last_auto_increment >= self.auto_increment_delay:
                self.increment_count()
                self.last_auto_increment = current_time

    def draw_shape(self, surface, shape_type, x, y, color, size):
        """Draw a shape at the given position"""
        half_size = size // 2

        if shape_type == "circle":
            pygame.draw.circle(surface, color, (x, y), half_size)

        elif shape_type == "square":
            rect = pygame.Rect(x - half_size, y - half_size, size, size)
            pygame.draw.rect(surface, color, rect)

        elif shape_type == "triangle":
            points = [
                (x, y - half_size),
                (x - half_size, y + half_size),
                (x + half_size, y + half_size)
            ]
            pygame.draw.polygon(surface, color, points)

        elif shape_type == "diamond":
            points = [
                (x, y - half_size),
                (x + half_size, y),
                (x, y + half_size),
                (x - half_size, y)
            ]
            pygame.draw.polygon(surface, color, points)

        elif shape_type == "star":
            points = []
            for i in range(10):
                angle = i * 36 - 90
                radius = half_size if i % 2 == 0 else half_size // 2
                px = x + radius * math.cos(math.radians(angle))
                py = y + radius * math.sin(math.radians(angle))
                points.append((px, py))
            pygame.draw.polygon(surface, color, points)

        elif shape_type == "heart":
            # Draw heart using two circles and a triangle
            pygame.draw.circle(surface, color, (x - half_size // 2, y - half_size // 3), half_size // 2)
            pygame.draw.circle(surface, color, (x + half_size // 2, y - half_size // 3), half_size // 2)
            points = [
                (x - half_size, y - half_size // 6),
                (x, y + half_size),
                (x + half_size, y - half_size // 6)
            ]
            pygame.draw.polygon(surface, color, points)

        elif shape_type == "hexagon":
            points = []
            for i in range(6):
                angle = i * 60
                px = x + half_size * math.cos(math.radians(angle))
                py = y + half_size * math.sin(math.radians(angle))
                points.append((px, py))
            pygame.draw.polygon(surface, color, points)

        elif shape_type == "cross":
            thickness = size // 3
            pygame.draw.rect(surface, color, (x - thickness // 2, y - half_size, thickness, size))
            pygame.draw.rect(surface, color, (x - half_size, y - thickness // 2, size, thickness))

    def draw(self):
        """Draw everything to screen"""
        self.screen.fill(BG_COLOR)

        # Compute and draw items dynamically based on count
        num_items = self.count % 400
        for i in range(num_items):
            x, y = self.get_item_position(i)
            color = self.get_rainbow_color(i + 1)
            shape_type = SHAPES[i % len(SHAPES)]
            self.draw_shape(self.screen, shape_type, x, y, color, ITEM_SIZE)

        # Draw current count in center
        if self.count > 0:
            color = self.get_rainbow_color(self.count)
            number_text = str(self.count)
            number_surface = self.number_font.render(number_text, True, color)
            number_rect = number_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

            # Draw a subtle shadow
            shadow_surface = self.number_font.render(number_text, True, (200, 200, 200))
            shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 + 3))
            self.screen.blit(shadow_surface, shadow_rect)

            # Draw main number
            self.screen.blit(number_surface, number_rect)

        # Draw instructions at bottom
        instr_font = pygame.font.Font(None, 28)
        instructions = [
            "SPACE: Count by 1 | ENTER: Auto-count (any key stops) | ESC: Quit"
        ]
        for i, text in enumerate(instructions):
            instr_surface = instr_font.render(text, True, (100, 100, 120))
            instr_rect = instr_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            self.screen.blit(instr_surface, instr_rect)

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()


def main():
    """Entry point"""
    print("Kids Counter Game")
    print("=" * 40)
    print("Controls:")
    print("  SPACE - Increment count by 1")
    print("  ENTER - Toggle auto-increment (0.5s)")
    print("  ESC   - Quit")
    print("=" * 40)

    game = CounterGame()
    game.run()


if __name__ == "__main__":
    main()
