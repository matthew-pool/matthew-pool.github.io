# 🪱 Wormhole
### A Text Adventure Game

> *"Guess you are a little worm-er after all."*

A terminal-based Python text adventure game featuring typewriter-style storytelling, a live in-game timer, an ASCII dungeon map, and a persistent leaderboard. Explore dark caverns, collect items, and survive the encounter with whatever lurks in the Worm Incubation Chamber.

---

## Features

- **Typewriter narration** — Story text prints character by character with a skippable animation (Windows)
- **Live timer** — Elapsed time updates in real time in your terminal's title bar
- **ASCII dungeon map** — Unlock and view a visual map of visited rooms using the `map` command
- **Persistent leaderboard** — Top 5 completion times are saved locally and displayed on victory
- **Locked paths** — Some routes require the right item to proceed
- **Play again loop** — On a loss, you're prompted to restart without quitting
- **Cross-platform** — Runs on Windows, macOS, and Linux (skip-on-keypress is Windows-only)

---

## Requirements

- Python 3.7+
- No external dependencies — uses only the Python standard library

---

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/wormhole.git
   cd wormhole
   ```

2. **Run the game**
   ```bash
   python game.py
   ```

3. Make sure `world.json` is in the same directory as `game.py`.

---

## How to Play

| Command | Description | Example |
|---|---|---|
| `go (direction)` | Move north, south, east, or west | `go north` |
| `get (item)` | Pick up an item in the current room | `get key` |
| `use (item)` | Use an item from your inventory | `use key` |
| `map` | View the dungeon map (requires map item) | `map` |
| `help` | Display the help/rules menu | `help` |
| `exit` / `quit` | End the game | `exit` |

**Tips:**
- Explore every room — you need to collect all 8 items to win.
- Some paths are locked. Find the right item and `use` it.
- Pick up the **compass** for a special hint on the map.
- Aliases `up`, `down`, `left`, `right` work in place of cardinal directions.

---

## Project Structure

```
wormhole/
├── game.py          # Main game logic
├── world.json       # Room and item definitions
├── leaderboard.txt  # Auto-generated on first win (top 5 times)
└── README.md
```

---

## Packaging as an Executable

The game supports [PyInstaller](https://pyinstaller.org/) for bundling into a standalone `.exe` or binary.

```bash
pip install pyinstaller
pyinstaller --onefile --add-data "world.json;." game.py
```

> On macOS/Linux, use `:` instead of `;` as the path separator in `--add-data`.

---

## Version History

| Version | Notes |
|---|---|
| 1.43.1 | Play Again prompt added on loss |
| 1.x | Leaderboard, map, timer, win/lose sequences |

---

## License

For educational and portfolio purposes only. Please do not copy or distribute.

© Matthew Pool
