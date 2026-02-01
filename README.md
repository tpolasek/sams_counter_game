# Kids Counter Game

A fun counting game for children that displays numbers and cute items with rainbow colors while speaking each number aloud.
<img width="993" height="927" alt="image" src="https://github.com/user-attachments/assets/99e57498-467a-454b-a1c7-eb5fe53e87b2" />



## Features

- **SPACE**: Increment count by 1
- **ENTER**: Auto-increment every 0.5 seconds (press any key to stop)
- Large colorful numbers displayed in the center
- Cute items (stars, shapes, animals, fruits) added to the screen
- Rainbow colors that cycle through the spectrum
- Text-to-speech speaks each number using macOS built-in `say` command

## Setup

### Create and activate virtual environment

```bash
./setup_venv.sh
source venv/bin/activate
```

Or manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the Game

```bash
source venv/bin/activate
python counter_game.py
```

## Controls

| Key | Action |
|-----|--------|
| SPACE | Count by 1 |
| ENTER | Toggle auto-count (every 0.5s) |
| Any key | Stop auto-counting |
| ESC | Quit game |

## Technical Details

- Built with **pygame** for graphics
- Uses macOS built-in **say** command for text-to-speech
- HSV color space for smooth rainbow transitions
- Threading for non-blocking audio playback
- Items placed left-to-right, top-to-bottom (reading order)
