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

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
BG_COLOR = (245, 245, 250)  # Soft off-white
FONT_SIZE = 150
ITEM_SIZE = 30
COLS = 12
ROWS = 8
ITEM_SPACING_X = SCREEN_WIDTH // (COLS + 1)
ITEM_SPACING_Y = 80
MARGIN_TOP = 100

# Cute item shapes (emojis as text, or simple shapes)
CUTE_ITEMS = [
    "★", "♦", "♠", "♣", "♥", "●", "■", "▲", "◆", "✦", "✧", "★",
    "⚪", "⚫", "🔴", "🔵", "🟢", "🟡", "🟣", "🟠", "🟤", "⭐",
    "🌟", "💫", "✨", "🔷", "🔶", "🔸", "🔹", "💎", "🌙", "☀️",
    "🍎", "🍊", "🍋", "🍇", "🍓", "🍒", "🥕", "🌸", "🌺", "🌻",
    "🦋", "🐝", "🐞", "🦄", "🐳", "🦊", "🐻", "🐼", "🐨", "🦁",
]

class CounterGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Kids Counter Game! Press SPACE or ENTER")
        self.clock = pygame.time.Clock()

        self.count = 0
        self.items = []  # List of (x, y, color, item_char)
        self.auto_incrementing = False
        self.last_auto_increment = 0
        self.auto_increment_delay = 1000  # milliseconds

        # Fonts
        self.number_font = pygame.font.Font(None, FONT_SIZE)
        self.item_font = pygame.font.Font(None, int(ITEM_SIZE * 1.5))

        # Check if we're on macOS for 'say' command
        self.is_macos = platform.system() == "Darwin"
        self.say_available = self.is_macos

        if not self.say_available:
            print("Warning: 'say' command only available on macOS.")
            print("Audio will be disabled.")

    def speak_number(self, number):
        """Speak a number using macOS 'say' command"""
        if not self.say_available:
            return

        def speak():
            try:
                # Use number as digit for clearer counting
                # e.g., "21" instead of "twenty one"
                subprocess.run(["say", "-v", "Fred", str(number)])
            except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError) as e:
                pass  # Silently fail if say command has issues

        # Run in separate thread to not block the game
        thread = threading.Thread(target=speak, daemon=True)
        thread.start()

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
        self.count += 1

        # Get color for this count
        color = self.get_rainbow_color(self.count)

        # Get position for new item
        x, y = self.get_item_position(self.count - 1)

        # Select cute item (cycle through them)
        item_char = CUTE_ITEMS[(self.count - 1) % len(CUTE_ITEMS)]

        # Add item
        self.items.append((x, y, color, item_char))

        # Speak the number
        self.speak_number(self.count)

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

    def draw(self):
        """Draw everything to screen"""
        self.screen.fill(BG_COLOR)

        # Draw all items
        for x, y, color, item_char in self.items:
            item_surface = self.item_font.render(item_char, True, color)
            item_rect = item_surface.get_rect(center=(x, y))
            self.screen.blit(item_surface, item_rect)

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
