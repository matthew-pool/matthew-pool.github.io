# Wormhole: A Text Adventure Game
# @author Matthew Pool
# @usage Educational and Portfolio purposes only. Do not copy or distribute.
# @filename wormhole.py
# @updated 2026-03-16
# @version 1.46.4

import sys
import json
import getpass
import os
import threading
import shutil
import re
import atexit
from time import sleep, time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

# Try to import Windows-specific keyboard module for the skip feature
try:
    import msvcrt
    import ctypes

    WINDOWS = True
except ImportError:
    import termios
    import tty
    import select
    WINDOWS = False


# -------------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------------
@dataclass
class GameConfig:
    DEBUG_MODE: bool = True
    quick_sleep: float = 0.6
    medium_sleep: float = 1.3
    long_sleep: float = 2.5
    slow_sleep: float = 2.0
    text_speed: float = 0.02
    fade_sleep: float = 0.1
    bye_msg: str = "Thanks for playing!\n"
    stop_words: set = field(
        default_factory=lambda: {"the", "a", "an", "to", "at", "my", "some"}
    )

    # ANSI Color Codes
    green: str = "\033[92m"
    yellow: str = "\033[93m"
    cyan: str = "\033[96m"
    magenta: str = "\033[95m"
    red: str = "\033[91m"
    white: str = "\033[97m"
    dark_gray: str = "\033[90m"
    pink_purple: str = "\033[38;5;207m"
    blink: str = "\033[5m"
    reset: str = "\033[0m"

    # Darker ANSI Color Codes for the Title Screen
    dark_cyan: str = "\033[36m"             # Standard cyan (darker than bright cyan 96m)
    dark_yellow: str = "\033[33m"           # Standard yellow (darker than bright yellow 93m)
    dark_pink_purple: str = "\033[38;5;127m" # Darker 256-color magenta/pink

    @property
    def ui_width(self) -> int:
        return shutil.get_terminal_size(fallback=(101, 20)).columns

    @property
    def plain_commands(self) -> str:
        return "Commands: [ go direction | get item | use item | help | exit ]"

    @property
    def commands(self) -> str:
        p = self.pink_purple
        d = self.dark_gray
        r = self.reset
        y = self.yellow
        c = self.cyan
        return f"{c}Commands:{r} {c}[{r} go {y}direction{r} {d}|{r} get {y}item{r} {d}|{r} use {y}item{r} {d}|{r} help {d}|{r} exit {c}]{r}"

    @property
    def dark_commands(self) -> str:
        p = self.pink_purple
        d = self.dark_gray
        r = self.reset
        y = self.yellow
        c = self.cyan
        return f"{c}Commands:{r} {c}[{r} go {y}direction{r} {d}|{r} get {y}item{r} {d}|{r} use {y}item{r} {d}|{r} help {d}|{r} exit {c}]{r}"   


# -------------------------------------------------------------------------
# CLASSES
# -------------------------------------------------------------------------
@dataclass
class Item:
    name: str
    desc: str


class Player:
    def __init__(self, start_room: str):
        self.inventory: List[Item] = []
        self.items_collected: int = 0
        self.current_room: str = start_room
        self.previous_room: Optional[str] = None
        self.silly_count: int = 0

    def has_item(self, item_name: str) -> bool:
        return any(item.name == item_name for item in self.inventory)

    def get_item(self, item_name: str) -> Optional[Item]:
        for item in self.inventory:
            if item.name == item_name:
                return item
        return None

    def remove_item(self, item_name: str) -> None:
        item = self.get_item(item_name)
        if item:
            self.inventory.remove(item)


class Room:
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        desc: str,
        alt_desc: Optional[str] = None,
        item: Optional[Item] = None,
        exits: Optional[Dict] = None,
        locked_paths: Optional[Dict] = None,
    ):
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.desc: str = desc
        self.alt_desc: str = alt_desc if alt_desc else desc
        self.item: Optional[Item] = item
        self.visited: bool = False
        self.revisited: bool = False
        self.exits: Dict[str, str] = exits or {}
        self.locked_paths: Dict[str, Dict[str, str]] = locked_paths or {}
        self.unlocked_paths: List[str] = []
        self.discovered_locks: List[str] = []


class Game:
    def __init__(self):
        self.config = GameConfig()
        self.display_timer: bool = False
        self.io_lock = threading.Lock()
        atexit.register(self.restore_console)

        # Apply custom icon if on Windows
        self.set_console_icon("wormhole.ico")

        # Command Pattern Dispatcher
        self.command_handlers = {
            "go": self.handle_go,
            "get": self.handle_get,
            "use": self.handle_use,
            "help": self.handle_help,
            "exit": self.handle_exit,
            "quit": self.handle_exit,
            "debug": self.handle_debug,
        }

    def set_console_icon(self, icon_name: str) -> None:
        """Attempts to set the console window icon using Windows API."""
        if not WINDOWS:
            return

        try:
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if not hwnd:
                return

            icon_path = self.get_resource_path(icon_name)
            if not os.path.exists(icon_path):
                return

            WM_SETICON = 0x80
            ICON_SMALL = 0
            ICON_BIG = 1
            LR_LOADFROMFILE = 0x0010
            IMAGE_ICON = 1

            h_icon = ctypes.windll.user32.LoadImageW(
                0, icon_path, IMAGE_ICON, 0, 0, LR_LOADFROMFILE
            )

            if h_icon:
                ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, h_icon)
                ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, h_icon)
        except Exception:
            pass

    def reset_session(self) -> None:
        """Resets the world and player state for a new playthrough."""
        self.items: Dict[str, Item] = {}
        self.rooms: Dict[str, Room] = {}
        self.build_world("world.json")
        self.player = Player(start_room="cavern")
        self.is_running: bool = True
        self.current_run = None
        self.start_time: float = time()

        if not hasattr(self, "timer_thread") or not self.timer_thread.is_alive():
            self.timer_thread = threading.Thread(target=self._live_timer, daemon=True)
            self.timer_thread.start()

    def get_resource_path(self, relative_path: str) -> str:
        """Get absolute path to resource, works for dev and for PyInstaller"""
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def build_world(self, filename: str) -> None:
        """Instantiates all items and rooms directly from a JSON data file."""
        filepath = self.get_resource_path(filename)
        try:
            with open(filepath, "r") as file:
                data = json.load(file)

        except FileNotFoundError:
            print(
                f"Error: Could not find {filepath}. Please ensure it is in the same directory."
            )
            sys.exit(1)

        for key, item_data in data.get("items", {}).items():
            self.items[key] = Item(name=item_data["name"], desc=item_data["desc"])

        for key, room_data in data.get("rooms", {}).items():
            room_item = (
                self.items.get(room_data.get("item_id"))
                if room_data.get("item_id")
                else None
            )
            coords = room_data.get("coords", [0, 0])

            self.rooms[key] = Room(
                name=room_data["name"],
                x=coords[0],
                y=coords[1],
                desc=room_data["desc"],
                alt_desc=room_data.get("alt_desc"),
                item=room_item,
                exits=room_data.get("exits"),
                locked_paths=room_data.get("locked_paths"),
            )

    # -------------------------------------------------------------------------
    # DATA PERSISTENCE & TIMING
    # -------------------------------------------------------------------------
    def load_leaderboard(self) -> List[Tuple[str, float]]:
        """Loads and sorts the leaderboard from a local text file."""
        leaderboard = []
        try:
            # ADDED: encoding="utf-8"
            with open("leaderboard.txt", "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().rsplit(",", 1)
                    if len(parts) == 2:
                        try:
                            leaderboard.append((parts[0], float(parts[1])))
                        except ValueError:
                            pass
        except FileNotFoundError:
            pass

        return sorted(leaderboard, key=lambda x: x[1])

    def save_leaderboard(self, leaderboard: List[Tuple[str, float]]) -> None:
        """Saves the top 10 times to a local text file."""
        # ADDED: encoding="utf-8"
        with open("leaderboard.txt", "w", encoding="utf-8") as f:
            for entry in leaderboard[:10]:
                f.write(f"{entry[0]},{entry[1]}\n")

    def get_timer_string(self) -> str:
        """Calculates current time and fetches best time."""
        elapsed_time = time() - self.start_time
        mins, secs = divmod(int(elapsed_time), 60)

        leaderboard = self.load_leaderboard()
        if leaderboard:
            b_mins, b_secs = divmod(int(leaderboard[0][1]), 60)
            return f"Time: {mins:02d}:{secs:02d} | Best: {b_mins:02d}:{b_secs:02d}"

        return f"Time: {mins:02d}:{secs:02d} | Best: --:--"

    def _live_background_task(self) -> None:
        """Background thread that safely updates the timer and the pulsing UI LED."""
        # Custom gradient of red shades for the rapid pulsing effect
        reds = [
            (100, 0, 0), (150, 0, 0), (200, 0, 0), (255, 0, 0),
            (255, 100, 100), (255, 0, 0), (200, 0, 0), (150, 0, 0)
        ]
        led_idx = 0
        ticks = 0

        while True:
            sleep(0.1) # Run at a blistering 10 ticks-per-second
            if not self.is_running:
                break

            with self.io_lock:
                # Update LED every 1 tick (0.1s)
                if getattr(self, "display_timer", False) and getattr(self, "led_active", False):
                    title_len = getattr(self, "current_title_length", 0)
                    center_len = getattr(self, "center_length", 37) # dynamic fallback
                    if title_len > 0:
                        # Dynamically calculate the target column based on LIVE terminal width
                        live_width = self.config.ui_width
                        spaces = max(1, (live_width - center_len) // 2 - title_len) 
                        dynamic_col = title_len + spaces + 1 # +1 because * is the very first character

                        r, g, b = reds[led_idx]
                        led_idx = (led_idx + 1) % len(reds)
                        color = f"\033[38;2;{r};{g};{b}m"
                        
                        # Save cursor, jump to live LED coordinate, draw, restore cursor
                        sys.stdout.write(f"\0337\033[2;{dynamic_col}H{color}*\0338")

                # Update Window Timer every 10 ticks (1.0s)
                if ticks % 10 == 0 and getattr(self, "display_timer", False):
                    timer_str = self.get_timer_string()
                    title_str = f"Wormhole - {timer_str}"
                    sys.stdout.write(f"\033]0;{title_str}\007")

                sys.stdout.flush()
            ticks += 1

    def reset_session(self) -> None:
        """Resets the world and player state for a new playthrough."""
        self.items: Dict[str, Item] = {}
        self.rooms: Dict[str, Room] = {}
        self.build_world("world.json")
        self.player = Player(start_room="cavern")
        self.is_running: bool = True
        self.current_run = None
        self.start_time: float = time()

        # Target the new combined background task
        if not hasattr(self, "bg_thread") or not self.bg_thread.is_alive():
            self.bg_thread = threading.Thread(target=self._live_background_task, daemon=True)
            self.bg_thread.start()

    def display_leaderboard(
        self,
        leaderboard: List[Tuple[str, float]],
        current_run: Optional[Tuple[str, float]] = None,
    ) -> None:
        """Renders the horizontally centered ASCII art leaderboard."""
        width = self.config.ui_width

        ascii_art = [
            r"  _                      _           _                         _ ",
            r" | |                    | |         | |                       | |",
            r" | |     ___  __ _    __| | ___ _ __| |__   ___   __ _ _ __ __| |",
            r" | |    / _ \/ _` |  / _` |/ _ \ '__| '_ \ / _ \ / _` | '__/ _` |",
            r" | |___|  __/ (_| | | (_| |  __/ |  | |_) | (_) | (_| | | | (_| |",
            r" \_____/\___|\__,_|  \__,_|\___|_|  |_.__/ \___/ \__,_|_|  \__,_|",
        ]

        print()

        for line in ascii_art:
            print(f"{self.config.yellow}{line.center(width)}{self.config.reset}")

        # --- Explicit Top 10 Header ---
        print(f"{self.config.cyan}{'--- TOP 10 SCORES ---'.center(width)}{self.config.reset}")
        print("-" * width)
        # -----------------------------------

        if not leaderboard and not current_run:
            msg = "No times recorded yet. Be the first!"
            print(msg.center(width))
        else:
            display_list = leaderboard[:10]

            # If current_run isn't in the top 10 display list, append it to the end
            if current_run and current_run not in display_list:
                display_list.append(current_run)

            for i, (name, t) in enumerate(display_list):
                m, s = divmod(int(t), 60)

                # Use a dash for rank if they are displaying outside the top 10
                rank = f"{i+1}." if i < 10 else "-"
                
                # CHANGED: {name:<25} is now {name:<29}
                row = f"{rank:<3} {name:<29} {m:02d}:{s:02d}"

                # Flash the row if it exactly matches the current run
                if current_run and name == current_run[0] and t == current_run[1]:
                    print(
                        f"{self.config.blink}{self.config.green}{row.center(width)}{self.config.reset}"
                    )
                else:
                    print(row.center(width))

        print("-" * width + "\n")

    # -------------------------------------------------------------------------
    # UTILITY FUNCTIONS
    # -------------------------------------------------------------------------
    def clear(self) -> None:
        """Instantly clears the screen without causing a terminal strobe/flicker."""
        self.led_active = False # Safely turn off the LED thread while the screen is wiping
        sys.stdout.write("\033[H\033[J")
        sys.stdout.flush()

    def restore_console(self) -> None:
        """Ensures terminal echo is re-enabled when the game closes."""
        self.set_console_echo(True)

    def set_console_echo(self, enable: bool) -> None:
        """Enables or disables terminal echo to prevent typing from showing on screen."""
        try:
            if WINDOWS:
                kernel32 = ctypes.windll.kernel32
                h_stdin = kernel32.GetStdHandle(-10) # STD_INPUT_HANDLE
                mode = ctypes.c_uint32()
                kernel32.GetConsoleMode(h_stdin, ctypes.byref(mode))
                if enable:
                    new_mode = mode.value | 0x0004
                else:
                    new_mode = mode.value & ~0x0004
                kernel32.SetConsoleMode(h_stdin, new_mode)
            else:
                fd = sys.stdin.fileno()
                settings = termios.tcgetattr(fd)
                if enable:
                    settings[3] |= termios.ECHO
                else:
                    settings[3] &= ~termios.ECHO
                termios.tcsetattr(fd, termios.TCSADRAIN, settings)
        except Exception:
            pass

    def flush_input(self) -> None:
        """Clears any unread keystrokes from the input buffer."""
        try:
            if WINDOWS:
                while msvcrt.kbhit():
                    msvcrt.getch()
            else:
                termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)
        except Exception:
            pass

    def format_text_colors(self, text: str) -> str:
        """Finds directions and items, coloring them yellow and the rest white."""
        keywords = [
            "north", "south", "east", "west", "left", "right", "up", "down",
            "up ahead", "back down", "back up ahead", # <-- NEW ALIASES ADDED HERE
            "compass", "map", "shroom", "gun", "key", "fish", "scripture", "poop", "alien worm"
        ]
        # Sort keywords by length descending to prevent partial match overlaps
        keywords.sort(key=len, reverse=True)
        
        pattern = re.compile(r'\b(' + '|'.join(keywords) + r')\b', re.IGNORECASE)
        
        def replacer(match):
            word = match.group(0)
            
            # Prevent coloring 'up' if it is part of 'woke up' or 'pick up'
            if word.lower() == "up":
                start_idx = match.start()
                # Check the 5 characters immediately preceding the match
                prefix = text[max(0, start_idx - 5):start_idx].lower()
                if "woke " in prefix or "pick " in prefix:
                    return word
                    
            return f"{self.config.yellow}{word}{self.config.white}"

        highlighted = pattern.sub(replacer, text)
        return f"{self.config.white}{highlighted}{self.config.reset}"

    def show_flashing_start(self, text: str) -> None:
        """Flashes the start text like a classic arcade game."""
        width = self.config.ui_width
        centered_text = text.center(width).rstrip()
        stop_event = threading.Event()

        def blink():
            visible = True
            while not stop_event.is_set():
                with self.io_lock:
                    sys.stdout.write("\r\033[2K")
                    if visible:
                        sys.stdout.write(
                            f"{self.config.white}{centered_text}{self.config.reset}"
                        )
                    sys.stdout.flush()
                visible = not visible
                stop_event.wait(0.6)

        t = threading.Thread(target=blink, daemon=True)
        t.start()

        self.flush_input()
        getpass.getpass("")
        stop_event.set()
        self.flush_input()
        print()

    def show_flashing_prompt(self, text: str) -> None:
        """Flashes text on and off like a classic arcade game."""
        width = self.config.ui_width
        
        # Calculate exact left padding for perfect centering without trailing spaces
        pad = " " * ((width - len(text)) // 2)
        formatted_text = f"{pad}{self.config.white}{text}{self.config.reset}"
        
        stop_event = threading.Event()

        def blink():
            visible = True
            while not stop_event.is_set():
                with self.io_lock:
                    sys.stdout.write("\r\033[2K")
                    if visible:
                        sys.stdout.write(formatted_text)
                    sys.stdout.flush()
                visible = not visible
                stop_event.wait(0.6)

        t = threading.Thread(target=blink, daemon=True)
        t.start()

        self.flush_input()
        getpass.getpass("")
        stop_event.set()
        
        # --- CLEANUP: Wipe the prompt and any accidental newlines ---
        with self.io_lock:
            sys.stdout.write("\r\033[2K")
            sys.stdout.write("\033[1A\033[2K\r")  # Move up one line and clear it too
            sys.stdout.flush()
            
        self.flush_input()

    def show_pulsing_exit(self, text: str, color_mode: str = "red") -> None:
        """Pulses the exit text with a long bright phase and very short dark phase."""
        width = self.config.ui_width
        stop_event = threading.Event()

        # Calculate exact left padding
        pad = " " * ((width - len(text)) // 2)

        def pulse():
            while not stop_event.is_set():
                # 1. Quick fade IN
                for val in range(50, 256, 20):
                    if stop_event.is_set(): break
                    if color_mode == "cyan": color = f"\033[38;2;0;{val};{val}m"
                    elif color_mode == "white": color = f"\033[38;2;{val};{val};{val}m"
                    else: color = f"\033[38;2;{val};0;0m"
                    
                    with self.io_lock:
                        sys.stdout.write(f"\r\033[2K{pad}{color}{text}\033[0m")
                        sys.stdout.flush()
                    stop_event.wait(0.02)

                # 2. HOLD fully bright for a long time
                if not stop_event.is_set():
                    stop_event.wait(0.8)

                # 3. Quick fade OUT
                for val in range(255, 49, -30):
                    if stop_event.is_set(): break
                    if color_mode == "cyan": color = f"\033[38;2;0;{val};{val}m"
                    elif color_mode == "white": color = f"\033[38;2;{val};{val};{val}m"
                    else: color = f"\033[38;2;{val};0;0m"
                    
                    with self.io_lock:
                        sys.stdout.write(f"\r\033[2K{pad}{color}{text}\033[0m")
                        sys.stdout.flush()
                    stop_event.wait(0.02)

                # 4. HOLD dark for a very brief moment
                if not stop_event.is_set():
                    stop_event.wait(0.1)

        t = threading.Thread(target=pulse, daemon=True)
        t.start()

        self.flush_input()
        getpass.getpass("")
        stop_event.set()
        
        # Cleanup: wipe the prompt and any accidental newlines
        with self.io_lock:
            sys.stdout.write("\r\033[2K")
            sys.stdout.write("\033[1A\033[2K\r") 
            sys.stdout.flush()
            
        self.flush_input()

    def prompt_play_again(self, text: str) -> bool:
        """Pulses text in red and waits for a single 'y' or 'n' keypress without Enter."""
        width = self.config.ui_width
        pad = " " * ((width - len(text)) // 2)
        stop_event = threading.Event()

        def pulse():
            while not stop_event.is_set():
                # 1. Quick fade IN (Red)
                for val in range(50, 256, 20):
                    if stop_event.is_set(): break
                    color = f"\033[38;2;{val};0;0m"
                    with self.io_lock:
                        sys.stdout.write(f"\r\033[2K{pad}{color}{text}\033[0m")
                        sys.stdout.flush()
                    stop_event.wait(0.02)

                if not stop_event.is_set(): stop_event.wait(0.8)

                # 3. Quick fade OUT
                for val in range(255, 49, -30):
                    if stop_event.is_set(): break
                    color = f"\033[38;2;{val};0;0m"
                    with self.io_lock:
                        sys.stdout.write(f"\r\033[2K{pad}{color}{text}\033[0m")
                        sys.stdout.flush()
                    stop_event.wait(0.02)

                if not stop_event.is_set(): stop_event.wait(0.1)

        t = threading.Thread(target=pulse, daemon=True)
        t.start()

        self.flush_input()
        choice = False
        
        # Non-blocking single character input loop
        while True:
            if WINDOWS:
                if msvcrt.kbhit():
                    char = msvcrt.getch()
                    try:
                        decoded = char.decode('utf-8').lower()
                        if decoded == 'y':
                            choice = True
                            break
                        elif decoded == 'n':
                            choice = False
                            break
                    except:
                        pass
                sleep(0.05)
            else:
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
                    if rlist:
                        char = sys.stdin.read(1).lower()
                        if char == 'y':
                            choice = True
                            break
                        elif char == 'n':
                            choice = False
                            break
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        stop_event.set()
        
        with self.io_lock:
            sys.stdout.write("\r\033[2K")
            sys.stdout.flush()

        self.flush_input()
        return choice

    def fade_in_text(
        self, text: str, color_mode: str = "red", speed: float = 0.03
    ) -> None:
        """Gradually fades text in from black using 24-bit ANSI colors."""
        width = self.config.ui_width
        centered_text = text.center(width).rstrip()

        self.flush_input()

        for val in range(0, 256, 4):  # Steps of 4 give a smooth ~2 second fade
            if color_mode == "red":
                color = f"\033[38;2;{val};0;0m"
            else:
                color = f"\033[38;2;{val};{val};{val}m"

            with self.io_lock:
                sys.stdout.write(f"\r\033[2K{color}{centered_text}\033[0m")
                sys.stdout.flush()
            sleep(speed)

        print()  # Lock in the final line

    def fade_item_box(self, room: Room) -> None:
        """Fades in the item box after typewriter text."""
        width = self.config.ui_width
        self.flush_input()

        # Determine the text components so we can color them individually
        if room.item and room.item.name != "alien worm":
            part1 = "[*] You see a(n) "
            item_name = room.item.name.upper()
            part2 = " here."
            if self.player.items_collected == 0:
                part2 += " Maybe you should get that."
        else:
            part1 = "[*] There are no items to pick up here."
            item_name = ""
            part2 = ""

        # Print initial spacing
        print()
        
        # Reserve 3 blank lines for the UI block so the terminal doesn't scroll mid-fade
        sys.stdout.write("\n\n\n")
        sys.stdout.flush()

        # Hide cursor during the animation for a cleaner look
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

        for val in range(0, 256, 6):  # Adjust step size for animation speed
            if WINDOWS and msvcrt.kbhit():
                break  # Allow the user to skip the fade if they start typing

            # Calculate the fading 24-bit RGB values
            red_color = f"\033[38;2;{val};0;0m"
            white_color = f"\033[38;2;{val};{val};{val}m"
            yellow_color = f"\033[38;2;{val};{val};0m"

            # Move cursor up 3 lines and return to the start of the line
            sys.stdout.write("\033[3A\r")
            
            # Construct the three lines dynamically
            line1 = f"{red_color}{'-' * width}\033[0m\n"
            if item_name:
                line2 = f"{white_color}{part1}{yellow_color}{item_name}{white_color}{part2}\033[0m\n"
            else:
                line2 = f"{white_color}{part1}\033[0m\n"
            line3 = f"{red_color}{'-' * width}\033[0m\n"

            sys.stdout.write(line1 + line2 + line3)
            sys.stdout.flush()
            sleep(0.02)

        # Guarantee it finishes on the exact, bright config colors
        sys.stdout.write("\033[3A\r")
        line1 = f"{self.config.red}{'-' * width}{self.config.reset}\n"
        if item_name:
            line2 = f"{self.config.white}{part1}{self.config.yellow}{item_name}{self.config.white}{part2}{self.config.reset}\n"
        else:
            line2 = f"{self.config.white}{part1}{self.config.reset}\n"
        line3 = f"{self.config.red}{'-' * width}{self.config.reset}\n"
        
        sys.stdout.write(line1 + line2 + line3)

        # Restore the cursor
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        self.flush_input()

    def show_dimmed_status(self) -> None:
        """Fades the entire UI from its original colors to dark gray simultaneously."""
        self.led_active = False
        room = self.rooms[self.player.current_room]
        width = self.config.ui_width

        # --- 1. REBUILD THE ORIGINAL COLOREVED UI ---
        lines = []
        c_dg = self.config.dark_gray
        c_cy = self.config.cyan
        c_res = self.config.reset
        
        # Border
        lines.append(f"{c_dg}{'=' * width}{c_res}")
        
        # Location & Exits
        title = room.name.replace("_", " ").title()
        plain_left = f" LOCATION:  {title}"
        colored_left = f"{c_cy} LOCATION:{c_res}  {title}"
        
        plain_center = "* EXITS:  [ N ]  [ S ]  [ E ]  [ W ]"
        spaces = max(1, (width - len(plain_center)) // 2 - len(plain_left))
        
        has_compass = self.player.has_item("compass")
        if has_compass:
            parts = []
            for dir_name, label in zip(["north", "south", "east", "west"], ["N", "S", "E", "W"]):
                if dir_name in room.exits:
                    if dir_name in room.locked_paths and dir_name not in room.unlocked_paths:
                        if dir_name in room.discovered_locks:
                            parts.append(f"{self.config.red}[ {label} ]{c_res}")
                        else:
                            parts.append(f"{self.config.green}[ {label} ]{c_res}")
                    else:
                        parts.append(f"{self.config.green}[ {label} ]{c_res}")
                else:
                    parts.append(f"{c_dg}[ {label} ]{c_res}")
            
            colored_center = f"{self.config.red}*{c_res} {c_cy}EXITS:{c_res}  {'  '.join(parts)}"
            lines.append(colored_left + (" " * spaces) + colored_center)
        else:
            lines.append(colored_left)

        # Inventory
        inv_display = (
            ", ".join(item.name for item in self.player.inventory).title()
            if self.player.inventory else "Empty"
        )
        lines.append(f"{c_cy} INVENTORY:{c_res} {inv_display}")
        
        # Header Bottom
        lines.append(f"{c_dg}{'=' * width}{c_res}")
        lines.append("")
        
        # Commands
        offset = len(self.config.commands) - len(self.config.plain_commands)
        lines.append(self.config.commands.center(width + offset))
        lines.append("")
        
        # Description
        raw_desc = getattr(self, 'last_printed_desc', room.desc)
        colored_desc = self.format_text_colors(raw_desc)
        for line in colored_desc.split('\n'):
            lines.append(line)
            
        lines.append("")
        
        # Item Box
        lines.append(f"{self.config.red}{'-' * width}{c_res}")
        if room.item and room.item.name != "alien worm":
            item_msg = f"[*] You see a(n) {self.config.yellow}{room.item.name.upper()}{c_res} here."
            if self.player.items_collected == 0:
                item_msg += " Maybe you should get that."
        else:
            item_msg = "[*] There are no items to pick up here."
        lines.append(item_msg)
        lines.append(f"{self.config.red}{'-' * width}{c_res}")

        full_text = "\n".join(lines)

        # --- 2. PARSE INTO CHARACTERS AND STARTING RGB VALUES ---
        color_map = {
            self.config.green: (0, 255, 0),
            self.config.yellow: (255, 255, 0),
            self.config.cyan: (0, 255, 255),
            self.config.magenta: (255, 0, 255),
            self.config.red: (255, 0, 0),
            self.config.white: (255, 255, 255),
            self.config.dark_gray: (100, 100, 100),
            self.config.reset: (255, 255, 255)
        }

        chars = []
        current_rgb = (255, 255, 255)
        
        ansi_regex = re.compile(r'(\033\[[0-9;]*m)')
        tokens = ansi_regex.split(full_text)
        
        for token in tokens:
            if not token: continue
            if token.startswith('\033'):
                if token in color_map:
                    current_rgb = color_map[token]
            else:
                for c in token:
                    chars.append({'c': c, 'start_rgb': current_rgb})

        # --- 3. ANIMATE THE FADE TO GRAY ---
        target_rgb = (90, 90, 90)  # The final dark gray color
        steps = 20                 # Number of frames in the animation
        
        with self.io_lock:
            sys.stdout.write("\033[?25l")  # Hide cursor
            sys.stdout.flush()

        for step in range(steps + 1):
            ratio = step / steps
            frame_str = ""
            
            for char_dict in chars:
                c = char_dict['c']
                if c == '\n':
                    frame_str += "\033[K\n"
                    continue
                if c == ' ':
                    frame_str += c
                    continue
                    
                sr, sg, sb = char_dict['start_rgb']
                tr, tg, tb = target_rgb
                
                # Interpolate from start color to target gray based on the current step
                r = int(sr + (tr - sr) * ratio)
                g = int(sg + (tg - sg) * ratio)
                b = int(sb + (tb - sb) * ratio)
                
                frame_str += f"\033[38;2;{r};{g};{b}m{c}"
                
            with self.io_lock:
                sys.stdout.write("\033[H")  # Jump to top left
                sys.stdout.write(frame_str + "\033[0m\033[K\n")
                sys.stdout.write("\033[J")  # Clear the prompt/inputs below the UI
                sys.stdout.flush()
                
            sleep(0.04)  # Framerate of the fade

        with self.io_lock:
            sys.stdout.write("\033[?25h")  # Bring the cursor back
            sys.stdout.flush()

    def typewriter(self, text: str, speed: Optional[float] = None) -> None:
        speed = speed or self.config.text_speed
        self.flush_input()

        # Safe width to prevent auto-wrapping terminal bugs
        width = self.config.ui_width - 1
        wrapped_text = ""

        # Pre-wrap text taking invisible ANSI codes into account
        for line in text.split('\n'):
            current_len = 0
            for word in line.split(' '):
                vis_len = len(re.sub(r'\033\[[0-9;]*m', '', word))

                if current_len + vis_len > width and current_len > 0:
                    wrapped_text = wrapped_text.rstrip(' ') + '\n'
                    current_len = 0

                wrapped_text += word + ' '
                current_len += vis_len + 1

            wrapped_text = wrapped_text.rstrip(' ') + '\n'
        wrapped_text = wrapped_text.rstrip('\n')

        # --- Parse into Characters and Target RGB ---
        chars = []
        current_rgb = (255, 255, 255) # Default White
        
        # Map our standard config colors to RGB tuples for the fade math
        color_map = {
            self.config.green: (0, 255, 0),
            self.config.yellow: (255, 255, 0),
            self.config.cyan: (0, 255, 255),
            self.config.magenta: (255, 0, 255),
            self.config.red: (255, 0, 0),
            self.config.white: (255, 255, 255),
            self.config.dark_gray: (100, 100, 100),
            self.config.reset: (255, 255, 255)
        }

        ansi_regex = re.compile(r'(\033\[[0-9;]*m)')
        tokens = ansi_regex.split(wrapped_text)
        
        for token in tokens:
            if not token:
                continue
            if token.startswith('\033'):
                if token in color_map:
                    current_rgb = color_map[token]
            else:
                for c in token:
                    chars.append({'c': c, 'rgb': current_rgb})

        # --- Render Setup ---
        sys.stdout.write("\033[?25l") # Hide cursor during animation
        line_count = wrapped_text.count('\n') + 1
        
        # Pre-print empty lines to safely reserve terminal space without crawling
        if line_count > 1:
            sys.stdout.write("\n" * (line_count - 1))
        sys.stdout.flush()

        fade_tail = 12  
        skip = False

        # Generate the upward movement string ONCE
        up_moves = line_count - 1
        up_str = f"\033[{up_moves}A" if up_moves > 0 else ""

        # --- Fading Render Loop ---
        for pos in range(len(chars) + fade_tail):
            if WINDOWS and not skip and msvcrt.kbhit():
                skip = True
                
            if skip:
                break
                
            frame_str = ""
            for i in range(min(pos + 1, len(chars))):
                char_dict = chars[i]
                c = char_dict['c']
                
                if c == '\n':
                    frame_str += "\033[0m\033[K\n"
                    continue
                if c == ' ':
                    frame_str += c
                    continue
                    
                age = pos - i
                ratio = min(1.0, max(0.0, age / fade_tail))
                
                # Start at a dark gray (30,30,30) so it is slightly visible instantly 
                base_val = 30
                r = int(base_val + (char_dict['rgb'][0] - base_val) * ratio)
                g = int(base_val + (char_dict['rgb'][1] - base_val) * ratio)
                b = int(base_val + (char_dict['rgb'][2] - base_val) * ratio)
                
                frame_str += f"\033[38;2;{r};{g};{b}m{c}"
                
            # End the current line cleanly
            frame_str += "\033[0m\033[K"

            # Pad remaining newlines to keep cursor anchored at the bottom
            current_newlines = frame_str.count('\n')
            total_newlines = line_count - 1
            if current_newlines < total_newlines:
                for _ in range(total_newlines - current_newlines):
                    frame_str += '\n\033[K'
                
            # Move cursor to start of text block, redraw, flush
            with self.io_lock:
                sys.stdout.write(f"\r{up_str}{frame_str}")
                sys.stdout.flush()
                
            sleep(speed)

        # --- Final Output Lock ---
        final_str = ""
        for char_dict in chars:
            c = char_dict['c']
            if c == '\n':
                final_str += "\033[0m\033[K\n"
            elif c == ' ':
                final_str += c
            else:
                r, g, b = char_dict['rgb']
                final_str += f"\033[38;2;{r};{g};{b}m{c}"
        final_str += "\033[0m\033[K"
                
        with self.io_lock:
            # Final draw pushes the cursor down one clean line so the prompt renders nicely below it
            sys.stdout.write(f"\r{up_str}{final_str}\n")
            sys.stdout.write("\033[?25h") 
            sys.stdout.flush()

        self.flush_input()
                
    def wait_for_enter(self, prompt: str) -> None:
        self.flush_input()
        print(prompt, end="", flush=True)
        getpass.getpass("")
        self.flush_input()
        
    def show_instructions(self) -> None:
        self.display_timer = False
        sys.stdout.write("\033]0;Wormhole\007")
        sys.stdout.flush()

        self.clear()
        width = self.config.ui_width

        # 1. Define the plain text strings
        title = "W O R M H O L E"
        sub = "A text adventure game"
        author = "created by matthew pool"

        print("\n" * 4)  # Initial newlines for vertical space above title
        title_pad = " " * ((width - len(title)) // 2)
        sub_pad = " " * ((width - len(sub)) // 2)
        author_pad = " " * ((width - len(author)) // 2)
        
        self.flush_input()
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

        skip = False

        # 2, 3, & 4. OVERLAPPING FADE for Title, Subtitle, and Author
        sub_offset = 140
        author_offset = 240  # Author starts fading in much sooner now!
        
        # Calculate max step based on author finish
        max_step = 255 + author_offset

        for step in range(0, max_step, 4):
            if WINDOWS and msvcrt.kbhit():
                skip = True
                break

            # Title String (Magenta, left-to-right)
            title_str = ""
            for i, char in enumerate(title):
                val = max(0, min(255, step - (i * 20)))
                title_str += f"\033[38;2;{val};0;{val}m{char}"

            # Subtitle String (White, left-to-right)
            sub_str = ""
            sub_step = step - sub_offset
            for i, char in enumerate(sub):
                val = max(0, min(255, sub_step - (i * 8)))
                sub_str += f"\033[38;2;{val};{val};{val}m{char}"

            # Author String (Yellow, fades in uniformly)
            author_step = step - author_offset
            val_auth = max(0, min(255, author_step))
            author_str = f"\033[38;2;{val_auth};{val_auth};0m{author}"

            sys.stdout.write(f"\r{title_pad}{title_str}{self.config.reset}\n")
            sys.stdout.write(f"\r{sub_pad}{sub_str}{self.config.reset}\n")
            sys.stdout.write("\n")
            sys.stdout.write(f"\r{author_pad}{author_str}{self.config.reset}")
            
            # Move cursor back up 3 lines to neatly overwrite the next frame
            sys.stdout.write("\033[3A") 
            sys.stdout.flush()
            sleep(0.03)

        # Lock in final colors instantly and push cursor past the text block
        sys.stdout.write(f"\r{title_pad}\033[38;2;255;0;255m{title}{self.config.reset}\n")
        sys.stdout.write(f"\r{sub_pad}\033[38;2;255;255;255m{sub}{self.config.reset}\n")
        sys.stdout.write("\n")
        sys.stdout.write(f"\r{author_pad}\033[38;2;255;255;0m{author}{self.config.reset}\n")
        sys.stdout.flush()

        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

        # Define the spaced prompt
        prompt_msg = "P R E S S  < E N T E R >  T O  S T A R T"
        prompt_pad = " " * ((width - len(prompt_msg)) // 2)

        print("\n" * 2)
        
        # Use the pulsing exit for the title screen
        self.show_flashing_prompt(prompt_msg)

        # --- FADE OUT SEQUENCE ---
        sys.stdout.write("\033[?25l")
        self.clear() 
        sys.stdout.flush()

        for val in range(255, -1, -5):
            sys.stdout.write("\033[H")
            
            title_color = f"\033[38;2;{val};0;{val}m"
            sub_color = f"\033[38;2;{val};{val};{val}m"
            author_color = f"\033[38;2;{val};{val};0m"
            prompt_color = f"\033[38;2;{val};{val};{val}m"
            
            output = (
                "\n\n\n\n\n"
                f"{title_pad}{title_color}{title}{self.config.reset}\n"
                f"{sub_pad}{sub_color}{sub}{self.config.reset}\n"
                "\n"
                f"{author_pad}{author_color}{author}{self.config.reset}\n"
                "\n\n\n"  # <--- Changed this from 5 newlines to 3
                f"{prompt_pad}{prompt_color}{prompt_msg}{self.config.reset}\n"
            )
            
            sys.stdout.write(output)
            sys.stdout.flush()
            sleep(0.04)

        self.clear()
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        self.flush_input()

    def draw_map(self) -> None:
        self.display_timer = True
        has_compass = self.player.has_item("compass")

        min_x = min(r.x for r in self.rooms.values())
        max_x = max(r.x for r in self.rooms.values())
        min_y = min(r.y for r in self.rooms.values())
        max_y = max(r.y for r in self.rooms.values())

        cols = (max_x - min_x) * 2 + 1
        rows = (max_y - min_y) * 2 + 1

        # Build alternating grid: Even cols = 3 chars, Odd cols = 1 char
        grid = []
        for r in range(rows):
            row_list = []
            for c in range(cols):
                if c % 2 == 0:
                    row_list.append("   ")  # 3 spaces for rooms and vertical paths
                else:
                    row_list.append(" ")  # 1 space for horizontal and diagonal paths
            grid.append(row_list)

        def format_node(room_name: str) -> str:
            if room_name == "worm_incubation_chamber" and has_compass:
                if self.player.current_room == room_name:
                    return f"<{self.config.red}X{self.config.reset}>"
                return f"<{self.config.red}?{self.config.reset}>"

            if self.player.current_room == room_name:
                return f"[{self.config.green}X{self.config.reset}]"

            if self.rooms[room_name].visited:
                # Replaced 'O' with '*' for visited rooms
                return f"[{self.config.yellow}*{self.config.reset}]"

            return "[ ]"

        drawn_paths = set()
        for name, room in self.rooms.items():
            gx = (room.x - min_x) * 2
            gy = (room.y - min_y) * 2
            grid[gy][gx] = format_node(name)

            for direction, target_name in room.exits.items():
                path_id = tuple(sorted([name, target_name]))
                if path_id in drawn_paths:
                    continue
                drawn_paths.add(path_id)

                target = self.rooms.get(target_name)
                if not target:
                    continue

                tx = (target.x - min_x) * 2
                ty = (target.y - min_y) * 2

                gmx = (gx + tx) // 2
                gmy = (gy + ty) // 2

                # Enforce strict cell widths to prevent terminal alignment rendering bugs
                col_width = 3 if gmx % 2 == 0 else 1

                if room.y == target.y:
                    char = "---" if col_width == 3 else "-"
                elif room.x == target.x:
                    char = " | " if col_width == 3 else "|"
                else:
                    if (target.x - room.x) * (target.y - room.y) > 0:
                        char = " ↖ " if col_width == 3 else "↖"
                    else:
                        char = " ↗ " if col_width == 3 else "↗"

                grid[gmy][gmx] = char

        width = self.config.ui_width
        
        # ASCII Art for MAP
        map_art = [
            r" __  __             ",
            r"|  \/  | __ _ _ __  ",
            r"| |\/| |/ _` | '_ \ ",
            r"| |  | | (_| | |_) |",
            r"|_|  |_|\__,_| .__/ ",
            r"             |_|    "
        ]

        print()
        for line in map_art:
            print(f"{self.config.cyan}{line.center(width)}{self.config.reset}")
        print()

        # Calculate the precise width of the alternating rows for perfect centering
        visible_row_width = ((cols + 1) // 2) * 3 + (cols // 2) * 1
        margin = max(0, (width - visible_row_width) // 2)

        for row in grid:
            print(" " * margin + "".join(row))

        # Add a blank row below the map
        print()
        print("=" * width)

        # Updated legend to match the new asterisk character
        if has_compass:
            legend = f"Legend: [{self.config.green}X{self.config.reset}] You are here | [{self.config.yellow}*{self.config.reset}] Visited | <{self.config.red}?{self.config.reset}> Unknown Signal"
            print(legend.center(width + 27))
        else:
            legend = f"Legend: [{self.config.green}X{self.config.reset}] You are here | [{self.config.yellow}*{self.config.reset}] Visited | [ ] Unknown"
            print(legend.center(width + 18))

    def help_menu(self) -> None:
        self.display_timer = False
        self.clear()
        width = self.config.ui_width

        # ASCII Art for HELP
        help_art = [
            r" _   _      _       ",
            r"| | | | ___| |___   ",
            r"| |_| |/ _ \ | '_ \ ",
            r"|  _  |  __/ | |_) |",
            r"|_| |_|\___|_| .__/ ",
            r"             |_|    "
        ]

        print()
        for line in help_art:
            print(f"{self.config.cyan}{line.center(width)}{self.config.reset}")
        print("\n")

        # Details to print (without formatting to measure length)
        plain_help_lines = [
            "To Move:       go direction    Example: go north, go up",
            "Get Item:      get item        Example: get light",
            "Use Item:      use item        Example: use key",
            "Help:          help            Shows this menu",
            "Quit:          exit            Ends the game",
        ]

        # Pre-formatted lines with exact color placements
        w = self.config.white
        y = self.config.yellow
        
        formatted_help_lines = [
            f"{w}To Move:       go {y}direction{w}    Example: go {y}north{w}, go {y}up{w}",
            f"{w}Get Item:      get {y}item{w}        Example: get {y}light{w}",
            f"{w}Use Item:      use {y}item{w}        Example: use {y}key{w}",
            f"{w}Help:          help            Shows this menu",
            f"{w}Quit:          exit            Ends the game",
        ]

        # Find the max width of the text block to center it as a left-aligned group
        max_line_len = max(len(line) for line in plain_help_lines)
        left_padding = " " * ((width - max_line_len) // 2)

        for line in formatted_help_lines:
            print(f"{left_padding}{line}{self.config.reset}")

        print("\n")
        
        # Use the white pulsing method to match the map screen
        self.show_pulsing_exit("P R E S S  < E N T E R >  T O  C L O S E", color_mode="white")

    def handle_debug(self, args: List[str]) -> None:
        # Failsafe: Act like the command doesnt exist if DEBUG_MODE is False
        if not getattr(self.config, "DEBUG_MODE", False):
            self.handle_silly_response("debug", action="other")
            return

        if not args:
                width = self.config.ui_width
                print(f"\n{self.config.magenta}--- DEBUG MENU ---{self.config.reset}")
                print("  debug 1 : Test Exit (Y) Sequence")
                print("  debug 2 : Boss Room (Loss - 0 items)")
                print("  debug 3 : Boss Room (Win - 8 items)")
                print("-" * width)
                print()
                
                self.show_pulsing_exit("P R E S S  < E N T E R >  T O  C L O S E")
                return

        choice = args[0]

        if choice == "1":
            print(
                f"\n{self.config.magenta}[DEBUG] Triggering Exit Sequence...{self.config.reset}"
            )
            sleep(self.config.quick_sleep)
            self.handle_exit([], force_yes=True)

        elif choice == "2":
            print(
                f"\n{self.config.magenta}[DEBUG] Teleporting to Boss (Loss)...{self.config.reset}"
            )
            sleep(self.config.quick_sleep)
            self.player.current_room = "worm_incubation_chamber"
            self.player.items_collected = 0

        elif choice == "3":
            print(
                f"\n{self.config.magenta}[DEBUG] Teleporting to Boss (Win)...{self.config.reset}"
            )
            sleep(self.config.quick_sleep)
            self.player.current_room = "worm_incubation_chamber"
            self.player.items_collected = 8

        else:
            print(f"\n{self.config.red}Invalid debug trigger.{self.config.reset}")
            sleep(self.config.quick_sleep)

    def show_status(self) -> None:
        self.clear()
        room = self.rooms[self.player.current_room]
        just_arrived = self.player.current_room != self.player.previous_room
        width = self.config.ui_width

        title = room.name.replace("_", " ").title()

        # Win Condition in show_status
        if room.name == "worm_incubation_chamber":
            self.display_timer = False

            if self.player.items_collected == 8:
                elapsed_time = time() - self.start_time
                mins, secs = divmod(int(elapsed_time), 60)

                self.clear()
                width = self.config.ui_width
                print("\n\n\n")

                # --- NEW: Hide the terminal cursor ---
                sys.stdout.write("\033[?25l")
                sys.stdout.flush()

                win_lines = [
                    "A giant, hideous alien worm creature erupts from the ground below you.",
                    "You pull out your wormhole blaster, filling it with fish paste and warm worm poo.",
                    "You start firing, disintegrating the alien worm into a splatter of slime.",
                    "The ground starts giving away as more wormholes appear! You quickly fire at the ground.",
                    "A cosmological wormhole manifests, and you leap! Guess you were a little worm-er after all.",
                ]

                for line in win_lines:
                    # REMOVED the manual self.config.white wrapping here
                    formatted_line = self.format_text_colors(line)
                    self.typewriter(
                        formatted_line.center(width + len(formatted_line) - len(line)), # Adjust centering for invisible ANSI codes
                        speed=0.03,
                    )
                    # --- Add a blank line between each sentence ---
                    print()

                # --- Bring the cursor back so they can see it for the name input ---
                sys.stdout.write("\033[?25h")
                sys.stdout.flush()

                print("\n\n")
                win_msg = "Aw man... You win, bruh!"
                print(f"{self.config.green}{win_msg.center(width)}{self.config.reset}")
                print("\n\n")

                clear_time_msg = f"Clear Time: {mins:02d}:{secs:02d}"
                print(
                    f"{self.config.cyan}{clear_time_msg.center(width)}{self.config.reset}\n"
                )

                leaderboard = self.load_leaderboard()
                current_run = ("Anonymous", elapsed_time)

                if len(leaderboard) < 10 or elapsed_time < leaderboard[-1][1]:
                    hs_msg = "*** NEW TOP 10 HIGH SCORE! ***"

                    print(
                        f"{self.config.yellow}{hs_msg.center(width)}{self.config.reset}\n\n"
                    )

                    pad = " " * ((width - 45) // 2)
                    self.flush_input()
                    self.set_console_echo(True)
                    try:
                        # CHANGED: [:15] is now [:27]
                        player_name = input(f"{pad}Enter your name: ").strip()[:27]
                    finally:
                        self.set_console_echo(False)

                    if not player_name:
                        player_name = "Anonymous"
                        
                    current_run = (player_name, elapsed_time)
                    leaderboard.append(current_run)
                    leaderboard = sorted(leaderboard, key=lambda x: x[1])[:10]
                    self.save_leaderboard(leaderboard)

                # Set unified exit flow logic here
                self.current_run = current_run
                print()
                self.show_pulsing_exit("P R E S S  < E N T E R >")

                self.is_running = False
                return

            else:
                self.show_dimmed_status()
                width = self.config.ui_width

                print("\n\n")
                msg1 = "A giant, hideous alien worm creature erupts from the ground below you."
                msg2 = "Looks like you're worm food..."

                self.typewriter(
                    f"{self.config.red}{msg1.center(width)}{self.config.reset}"
                )
                print(f"{self.config.red}{msg2.center(width)}{self.config.reset}")

                sleep(self.config.slow_sleep)

                print()
                print(
                    f"{self.config.red}{'GAME OVER'.center(width)}{self.config.reset}"
                )

                print("\n")
                sleep(self.config.medium_sleep)
                
                # Set unified exit flow logic here
                print()
                self.show_pulsing_exit("P R E S S  < E N T E R >")
                
                self.current_run = None
                self.is_running = False
                return

        self.display_timer = True

        # --- Global Compass Check ---
        has_compass = self.player.has_item("compass")
        # ----------------------------

        # Build Exit String first to share the line with Location
        directions = ["north", "south", "east", "west"]
        labels = ["N", "S", "E", "W"]
        parts = []
        gray_parts = []

        for dir, label in zip(directions, labels):
            gray_parts.append(f"{self.config.dark_gray}[ {label} ]{self.config.reset}")

            if dir in room.exits:
                if dir in room.locked_paths and dir not in room.unlocked_paths:
                    if dir in room.discovered_locks:
                        parts.append(f"{self.config.red}[ {label} ]{self.config.reset}")
                    else:
                        parts.append(f"{self.config.green}[ {label} ]{self.config.reset}")
                else:
                    parts.append(f"{self.config.green}[ {label} ]{self.config.reset}")
            else:
                parts.append(f"{self.config.dark_gray}[ {label} ]{self.config.reset}")

        exits_str = "  ".join(parts)
        gray_exits_str = "  ".join(gray_parts)

        # --- NEW: UI Header Layout & LED Logic ---
        led_off = " "
        
        # We start the "on" state with a generic red color, but the background thread will overwrite it instantly
        led_on = f"{self.config.red}*{self.config.reset}"

        if has_compass:
            colored_center = f"{led_on} {self.config.cyan}EXITS:{self.config.reset}  {exits_str}"
            gray_center = f"{led_on} {self.config.cyan}EXITS:{self.config.reset}  {gray_exits_str}"
            self.led_active = True
        else:
            colored_center = f"{led_off} {self.config.cyan}EXITS:{self.config.reset}  {exits_str}"
            gray_center = f"{led_off} {self.config.cyan}EXITS:{self.config.reset}  {gray_exits_str}"
            self.led_active = False

        colored_left = f"{self.config.cyan} LOCATION:{self.config.reset}  {title}"
        plain_left = f" LOCATION:  {title}"

        plain_center = "* EXITS:  [ N ]  [ S ]  [ E ]  [ W ]"
        spaces_between = max(1, (width - len(plain_center)) // 2 - len(plain_left))
        
        # Save the exact metrics for the background thread to target
        self.current_title_length = len(plain_left)
        self.center_length = len(plain_center)

        print("=" * width)

        # --- Hide exits globally if no compass, otherwise show them ---
        if not has_compass:
            print(colored_left)
        elif not room.visited:
            print(colored_left + (" " * spaces_between) + gray_center)
        else:
            print(colored_left + (" " * spaces_between) + colored_center)
        # --------------------------------------------------------------
        inv_display = (
            ", ".join(item.name for item in self.player.inventory).title()
            if self.player.inventory
            else "Empty"
        )
        print(f"{self.config.cyan} INVENTORY:{self.config.reset} {inv_display}")

        # Bottom header line and centered commands
        print("=" * width)
        print()
        offset = len(self.config.commands) - len(self.config.plain_commands)
        print(self.config.commands.center(width + offset))
        print("\n")

        # --- Dynamic description variables ---
        active_desc = room.desc
        active_alt_desc = room.alt_desc

        if room.name == "entryway" and not has_compass:
            # Swap cardinal directions for relative ones until they get the compass
            active_desc = active_desc.replace("west", "left").replace("east", "right").replace("The path to the south", "The path down")
            active_alt_desc = active_alt_desc.replace("west", "left").replace("east", "right").replace("The path to the south", "The path down")
            
        if room.name == "cavern" and not has_compass:
            active_alt_desc = active_alt_desc.replace("to the north", "back up ahead")
        # ----------------------------------------

        # --- CONTEXTUAL ROOM DESCRIPTION ---
        used_typewriter = False
        desc_to_print = ""

        if just_arrived and room.visited:
            room.revisited = True

        if not room.visited:
            desc_to_print = active_desc
            
            # Optional: Keep a small dramatic pause before the very first text types out
            if room.name == "cavern" and self.player.items_collected == 0:
                sleep(1.0) 
                
            self.typewriter(self.format_text_colors(desc_to_print))
            room.visited = True
            used_typewriter = True

            if has_compass:
                sys.stdout.write("\0337\033[2;1H" + colored_left + (" " * spaces_between) + colored_center + "\0338")
                sys.stdout.flush()

        elif not room.revisited:
            desc_to_print = active_desc
            print(self.format_text_colors(desc_to_print))
            
        elif just_arrived:
            if room.item or active_alt_desc != active_desc:
                desc_to_print = active_alt_desc
                print(self.format_text_colors(desc_to_print))
            else:
                desc_to_print = f"You are back in the {title}. You've already cleared this area out."
                print(self.format_text_colors(desc_to_print))
                
        else:
            desc_to_print = active_alt_desc.replace("You are back in", "You are still in")
            print(self.format_text_colors(desc_to_print))

        # Save the exact string that hit the screen so the dimmed UI can mirror it
        self.last_printed_desc = desc_to_print

        # --- Trigger the fade if the typewriter was active ---
        if used_typewriter:
            self.fade_item_box(room)
        else:
            print()
            print(self.config.red + "-" * width + self.config.reset)

            if room.item and room.item.name != "alien worm":
                item_msg = f"[*] You see a(n) {self.config.yellow}{room.item.name.upper()}{self.config.reset} here."

                if self.player.items_collected == 0:
                    item_msg += " Maybe you should get that."

                print(item_msg)
            else:
                print("[*] There are no items to pick up here.")

            print(self.config.red + "-" * width + self.config.reset)

        print("\n")

    # -------------------------------------------------------------------------
    # COMMAND HANDLERS
    # -------------------------------------------------------------------------
    def handle_silly_response(self, target: str, action: str) -> None:
        print()
        count = self.player.silly_count
        if action == "go" or action == "get":
            if count == 0:
                print(f"{self.config.white}You can't really do that, silly...{self.config.reset}")
            elif count == 1:
                print(f"{self.config.white}We would {action} {self.config.yellow}{target}{self.config.white} if we could...{self.config.reset}")
            elif count == 2:
                print(f"{self.config.white}Bruh. Stop. You can't {action} {self.config.yellow}{target}{self.config.white}!{self.config.reset}")
            elif count == 3:
                print(f"{self.config.white}Huh?{self.config.reset}")
            else:
                self.help_menu()
        else:
            print(f"{self.config.white}I don't understand what you're trying to do.{self.config.reset}")

        sleep(self.config.medium_sleep)
        self.player.silly_count = (self.player.silly_count + 1) % 4

    def normalize_item_name(self, target: str) -> str:
        """Maps multi-word or descriptive item names to their core IDs."""
        aliases = {
            "damp map": "map",
            "crude map": "map",
            "digital compass": "compass",
            "magnetic compass": "compass",
            "alien mushroom": "shroom",
            "acidic shroom": "shroom",
            "vivid mushroom": "shroom",
            "wormhole blaster": "gun",
            "blaster": "gun",
            "rusty key": "key",
            "iron key": "key",
            "heavy key": "key",
            "alien fish": "fish",
            "pink fish": "fish",
            "glowing fish": "fish",
            "ancient text": "scripture",
            "alien scripture": "scripture",
            "text": "scripture",
            "worm poop": "poop",
            "alien poop": "poop",
            "alien worm poop": "poop",
            "worm": "alien worm"
        }
        return aliases.get(target, target)

    def handle_go(self, args: List[str]) -> None:
        if not args:
            print(f"\n{self.config.white}Go where?{self.config.reset}") 
            sleep(self.config.quick_sleep)
            return

        # Safely handle multi-word directions
        if len(args) >= 3 and args[:3] == ["back", "up", "ahead"]:
            raw_dir = "back up ahead"
        elif len(args) >= 2 and args[:2] == ["up", "ahead"]:
            raw_dir = "up ahead"
        elif len(args) >= 2 and args[:2] == ["back", "down"]:
            raw_dir = "back down"
        else:
            raw_dir = " ".join(args)  # Captures the full phrase for handle_silly_response

        has_compass = self.player.has_item("compass")

        # 1. Expand abbreviations to full words
        abbrev_map = {
            "n": "north", "s": "south", "e": "east", "w": "west",
            "u": "up", "d": "down", "l": "left", "r": "right"
        }
        display_dir = abbrev_map.get(raw_dir, raw_dir)

        cardinals = ["north", "south", "east", "west"]
        relatives = ["up", "down", "left", "right", "up ahead", "back down", "back up ahead"]

        # 2. Enforce the Compass Rules
        width = self.config.ui_width

        if not has_compass and display_dir in cardinals:
            formatted_msg = f"{self.config.white}You have no idea which way {self.config.yellow}{display_dir}{self.config.white} is!{self.config.reset}"
            print(f"\n{formatted_msg}")
            sleep(self.config.medium_sleep)
            return

        if has_compass and display_dir in relatives:
            formatted_msg = f"{self.config.white}You have a reliable compass now! You should use cardinal directions.{self.config.reset}"
            print(f"\n{formatted_msg}")
            sleep(self.config.long_sleep)
            return

        # 3. Map to the internal game engine logic (which always uses cardinals)
        rel_to_cardinal = {
            "up": "north",
            "up ahead": "north",
            "back up ahead": "north",
            "down": "south",
            "back down": "south",
            "left": "west",
            "right": "east"
        }
        internal_dir = rel_to_cardinal.get(display_dir, display_dir)

        room = self.rooms[self.player.current_room]

        if internal_dir in cardinals and internal_dir in room.exits:
            
            # --- Entryway Navigation Lock ---
            if room.name == "entryway" and internal_dir in ["east", "west"]:
                if not (self.player.has_item("compass") and self.player.has_item("map")):
                    width = self.config.ui_width
                    
                    base_msg = "I shouldn't go any farther until I figure out where I am."
                    formatted_msg = f"{self.config.red}{base_msg}{self.config.reset}"
                    offset = len(formatted_msg) - len(base_msg)
                    
                    print(f"\n{formatted_msg.center(width + offset)}")
                    sleep(self.config.slow_sleep)
                    return
            # -------------------------------------

            if internal_dir in room.locked_paths and internal_dir not in room.unlocked_paths:
                if internal_dir not in room.discovered_locks:
                    room.discovered_locks.append(internal_dir)

                width = self.config.ui_width
                
                base_msg = room.locked_paths[internal_dir]["msg"]
                formatted_msg = f"{self.config.red}{base_msg}{self.config.reset}"
                offset = len(formatted_msg) - len(base_msg)

                print(f"\n{formatted_msg.center(width + offset)}")
                print() 
                
                self.show_pulsing_exit("P R E S S  < E N T E R >")

            else:
                print(f"\n{self.config.white}You decide to go {self.config.yellow}{display_dir}{self.config.white}...{self.config.reset}")
                sleep(self.config.medium_sleep)
                self.player.current_room = room.exits[internal_dir]
                self.player.silly_count = 0

        else:
            self.handle_silly_response(raw_dir, action="go")  # Passed the raw_dir!

    def handle_get(self, args: List[str]) -> None:
        if not args:
            print(f"\n{self.config.white}Get what?{self.config.reset}") 
            sleep(self.config.quick_sleep)
            return

        raw_target = " ".join(args)
        target = self.normalize_item_name(raw_target)
        room = self.rooms[self.player.current_room]

        if room.item and target == room.item.name:
            print(
                f"\n{self.config.yellow}{target.upper()}{self.config.reset} retrieved!"
            )
            self.player.inventory.append(room.item)
            self.player.items_collected += 1
            room.item = None
            self.player.silly_count = 0
            sleep(self.config.medium_sleep)
        else:
            self.handle_silly_response(raw_target, action="get")

    def handle_use(self, args: List[str]) -> None:
        if not args:
            print(f"\n{self.config.white}Use what?{self.config.reset}") 
            sleep(self.config.quick_sleep)
            return

        raw_target = " ".join(args)
        target = self.normalize_item_name(raw_target)
        room = self.rooms[self.player.current_room]

        if not self.player.has_item(target):
            print(f"\n{self.config.white}You don't have a {self.config.yellow}{raw_target}{self.config.white} in your inventory!{self.config.reset}")
            sleep(self.config.medium_sleep)
            return

        if target == "map":
            self.clear()
            print("\n")
            self.draw_map()
            
            print() # Add a little spacing below the map
            
            # Use the pulsing exit method
            self.show_pulsing_exit("P R E S S  < E N T E R >  T O  C L O S E", color_mode="white")
            return

        used_successfully = False
        width = self.config.ui_width

        for direction, lock_info in room.locked_paths.items():
            if lock_info["req_item"] == target and direction not in room.unlocked_paths:
                
                # FIX: Standardized unlock UI centering
                base_msg = lock_info["success_msg"]
                formatted_msg = f"{self.config.green}{base_msg}{self.config.reset}"
                offset = len(formatted_msg) - len(base_msg)

                print(f"\n{formatted_msg.center(width + offset)}")
                room.unlocked_paths.append(direction)
                used_successfully = True

                print() # Add a blank line for spacing
                
                # Use the pulsing exit method without the ellipses
                self.show_pulsing_exit("P R E S S  < E N T E R >")
                break

        if not used_successfully:
            # FIX: Ensure outer white color and reset are encapsulated for clean centering
            formatted_msg = f"{self.config.white}You can't use the {self.config.yellow}{raw_target}{self.config.white} here.{self.config.reset}"
            print(f"\n{formatted_msg}")
            sleep(self.config.medium_sleep)

    def handle_help(self, args: List[str]) -> None:
        self.help_menu()
        self.display_timer = True

    def handle_exit(self, args: List[str], force_yes: bool = False) -> None:
        self.display_timer = False

        if force_yes:
            confirm = "y"
        else:
            # Print the question OUTSIDE the loop so it doesn't stack
            print(f"\n{self.config.yellow}Are you sure (Y/N)?{self.config.reset}")
            
            while True:
                self.flush_input()
                self.set_console_echo(True)
                try:
                    confirm = input("> ").strip().lower()
                finally:
                    self.set_console_echo(False)
                
                if confirm in ["y", "n"]:
                    break
                else:
                    # Print left-aligned error
                    print(f"{self.config.red}Please enter 'Y' or 'N'{self.config.reset}")
                    sleep(self.config.medium_sleep)
                    
                    # Move cursor up 2 lines (over the error and the input) and clear them out
                    with self.io_lock:
                        sys.stdout.write("\033[2A\033[J")
                        sys.stdout.flush()

        if confirm == "y":
            self.show_dimmed_status()

            width = self.config.ui_width
            msg = "You succumb to the fear and desperation and end your journey suddenly..."

            print("\n\n")

            # Use the fade effect
            self.fade_in_text(msg, color_mode="red")

            # Vertical space before the enter prompt
            print("\n\n")

            # Set unified exit flow logic here
            self.show_pulsing_exit("P R E S S  < E N T E R >")

            # --- CHANGED: Set to None instead of tracking the losing time ---
            self.current_run = None
            
            self.is_running = False
            return
            
        else:
            # Perfectly center the cancellation text
            width = self.config.ui_width
            base_msg = "You decide ending it all just isn't worth it and continue on."
            formatted_msg = f"{self.config.white}{base_msg}{self.config.reset}"
            offset = len(formatted_msg) - len(base_msg)
            
            print(f"\n{formatted_msg.center(width + offset)}")
            sleep(self.config.medium_sleep)
            self.display_timer = True

    def parse_input(self) -> None:
        self.flush_input()
        self.set_console_echo(True)
        
        try:
            raw_input = (
                input(f"{self.config.yellow}What do you do!?{self.config.reset}\n> ")
                .strip()
                .lower()
            )
        finally:
            self.set_console_echo(False)

        if not raw_input:
            self.help_menu()
            self.display_timer = True
            return
        
        words = [
            word for word in raw_input.split() if word not in self.config.stop_words
        ]

        if not words:
            self.help_menu()
            self.display_timer = True
            return

        command = words[0]
        args = words[1:]

        handler = self.command_handlers.get(command)
        if handler:
            handler(args)
        else:
            print(f"\n{self.config.white}What?{self.config.reset}")
            sleep(self.config.quick_sleep)


    # -------------------------------------------------------------------------
    # MAIN LOOP
    # -------------------------------------------------------------------------
    def play(self) -> None:
        self.set_console_echo(False)
        
        while True:
            self.reset_session()
            self.show_instructions()

            self.start_time = time()

            while self.is_running:
                self.display_timer = True
                self.show_status()

                if not self.is_running:
                    self.display_timer = False
                    break

                self.player.previous_room = self.player.current_room
                self.parse_input()

            # --- OUT OF THE GAME LOOP: END GAME SEQUENCE ---
            self.clear()
            print("\n\n")

            # Fetch the final updated leaderboard data and render it. 
            # We explicitly pass the cached run from whichever ending handler fired. 
            leaderboard = self.load_leaderboard()
            current_run = getattr(self, "current_run", None)
            self.display_leaderboard(leaderboard, current_run=current_run)

            print("\n")
            
            play_again = self.prompt_play_again("P L A Y  A G A I N  ( Y / N ) ?")

            if play_again:
                continue
            else:
                sys.stdout.write("\033]0;Windows PowerShell\007")
                sys.stdout.flush()
                sys.exit()


if __name__ == "__main__":
    try:
        game = Game()
        game.play()
    except SystemExit:
        # This catches the sys.exit() calls from within the handlers
        pass
    finally:
        # Final cleanup before the terminal returns to the prompt
        if WINDOWS:
            os.system("cls")
        else:
            os.system("clear")