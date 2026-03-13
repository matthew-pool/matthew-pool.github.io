

wormhole.html
html


game.py
py


wormhole.ico
ico


wormhole.exe
exe


leaderboard.txt
13 lines

txt


world.json
129 lines

json

create a README.md for the repo of my Wormhole game - i have

3:54 AM

Viewed 3 files
Viewed 3 files
Now I have everything I need. Let me create the README.


Created a file, read a file
Created a file, read a file
Here's your README! It covers:

Project overview with both the terminal and browser versions called out
Full command reference table
ASCII world map reconstructed from the coordinates in world.json
Item table showing where each item is found and what it unlocks
Leaderboard section explaining both the local .txt system and PlayFab integration
Setup instructions for Python, the .exe, and the browser version
Project structure file tree
Architecture notes highlighting the data-driven design, command dispatcher, background timer thread, and PyInstaller compatibility
Let me know if you'd like to add screenshots, a GIF demo, a changelog, or anything else!

Readme
Document · MD 





Claude is AI and can make mistakes. Please double-check responses.
Readme · MD
Copy

# 🪱 Wormhole
 
**Wormhole** is a terminal-based text adventure game written in Python. You wake up disoriented in an alien cave system with no memory of how you got there. Navigate through 13 rooms, collect 8 items, unlock paths, and survive the Worm Incubation Chamber — before it's too late.
 
Available in two flavors:
- **`game.py`** — A full-featured terminal app with a live timer, ANSI color, and an ASCII map
- **`wormhole.html`** — A standalone browser version with a CRT aesthetic and online leaderboards via PlayFab
 
---
 
## 📸 Preview
 
> *Retro green-on-black terminal UI with typewriter-style narration, color-coded feedback, and a live timer displayed in the title bar.*
 
---
 
## 🎮 How to Play
 
Your only goal: **escape the cave**. Find items, use them to unlock blocked paths, and make it to the final room with all 8 items collected.
 
### Commands
 
| Command | Description |
|---|---|
| `go <direction>` | Move in a direction (`north`, `south`, `east`, `west`) |
| `get <item>` | Pick up an item in the current room |
| `use <item>` | Use an item to unlock a path |
| `map` | View the ASCII map (requires the map item) |
| `help` | Show the rules and command list |
| `exit` / `quit` | Quit the game |
 
Stop words like `the`, `a`, and `to` are automatically filtered, so natural phrasing like `go to the north` works fine.
 
---
 
## 🗺️ World
 
The cave system consists of 13 interconnected rooms across two versions of the world file (`world.json`). Several paths are **locked** and require a specific item to open.
 
```
Worm Incubation Chamber  ← Final Boss Room
       ↑           ↑
  Graveyard      Dump
       ↑           ↑
  Pink Pond    Laboratory
       ↑           ↑
    Garden  ←  Entryway  →  Freezer
       ↑                        ↑
    Mud Pit   Cavern (Start)  Storage
```
 
### Items
 
| Item | Found In | Used To Unlock |
|---|---|---|
| Map | Cavern | View ASCII map |
| Compass | Entryway | *(collectible)* |
| Shroom | Garden | Open the steel door to the Freezer |
| Gun | Laboratory | Blast through vines in the Garden |
| Key | Storage | Open the iron gate at the Pink Pond |
| Fish | Pink Pond | Feed the mutant plant in the Laboratory |
| Scripture | Graveyard | *(collectible — contains a hint)* |
| Poop | Dump | *(collectible)* |
 
> **Hint:** The graveyard scripture says it all — *"If you've collected more than seven, then straight ahead lies Heaven."*
 
---
 
## 🏆 Leaderboard
 
The terminal version tracks your completion time and saves the **top 5 fastest times** to `leaderboard.txt`. Your best time is displayed live in the window title bar alongside your current run time.
 
The browser version uses **PlayFab** to maintain an online global leaderboard.
 
Sample leaderboard entries (from `leaderboard.txt`):
 
```
Earthworm Jimmy        1:00
Boggy Bubba            1:15
Matthew Pool           1:31
Edgar the Conqueror    1:51
...
You're Getting Worm-er   ∞
```
 
---
 
## 🚀 Running the Game
 
### Terminal Version (Python)
 
**Requirements:** Python 3.8+
 
```bash
# Clone the repo and navigate to the project folder
git clone https://github.com/your-username/wormhole.git
cd wormhole
 
# Run the game
python game.py
```
 
> `world.json` and `leaderboard.txt` must be in the same directory as `game.py`. The game will generate a fresh `leaderboard.txt` automatically if one isn't found.
 
### Executable (Windows)
 
A pre-built Windows executable is included as `wormhole.exe`. Just double-click to run — no Python installation needed.
 
> Best experienced in Windows Terminal or PowerShell for full ANSI color and title bar timer support.
 
### Browser Version
 
Open `wormhole.html` directly in any modern browser. No server or install required.
 
---
 
## 🛠️ Project Structure
 
```
wormhole/
├── game.py              # Core Python game logic
├── world.json           # Room and item definitions
├── leaderboard.txt      # Local high score file (top 5)
├── wormhole.html        # Standalone browser version
├── wormhole.ico         # App icon
└── wormhole.exe         # Pre-built Windows executable
```
 
---
 
## 🧱 Architecture Notes
 
- **World data is fully data-driven** via `world.json` — rooms, items, exits, locked paths, and unlock conditions are all defined there, not hardcoded.
- **Command dispatch** uses a dictionary-based handler pattern (`command_handlers`) for clean, extensible input parsing.
- **Live timer** runs on a background daemon thread and updates the terminal window title every second without blocking input.
- **PyInstaller-compatible** resource loading via `get_resource_path()` for the `.exe` build.
- The browser version is a faithful port — same world data, same command parser, same locked path logic — implemented in vanilla JavaScript with a CRT-style CSS aesthetic.
 
---
 
## 👤 Author
 
**Matthew Pool**
Educational and portfolio purposes only. Do not copy or distribute.
 
---
 
## 📄 License
 
This project is for educational and portfolio use only. All rights reserved.
 








