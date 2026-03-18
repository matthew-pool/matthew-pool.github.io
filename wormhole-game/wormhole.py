# Wormhole: A Text Adventure Game
# @author Matthew Pool
# @usage Educational and Portfolio purposes only. Do not copy or distribute.
# @filename wormhole.py
# @updated 2026-03-18
# @version 1.49.11

import sys
import json
import getpass
import os
import threading
import shutil
import re
import atexit
import textwrap
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
    light_gray: str = "\033[37m"
    pink_purple: str = "\033[38;5;207m" 
    blink: str = "\033[5m"
    reset: str = "\033[0m"

    # Darker ANSI Color Codes for the Title Screen
    dark_cyan: str = "\033[36m"             
    dark_yellow: str = "\033[33m"           
    dark_pink_purple: str = "\033[38;5;127m"

    @property
    def ui_width(self) -> int:
        return shutil.get_terminal_size(fallback=(101, 20)).columns

    @property
    def plain_commands(self) -> str:
        return "Commands: [ go direction | get item | use item | help | exit ]"

    @property
    def commands(self) -> str:
        d = self.dark_gray
        r = self.reset
        y = self.yellow
        c = self.cyan
        return f"{c}Commands:{r} {c}[{r} go {y}direction{r} {d}|{r} get {y}item{r} {d}|{r} use {y}item{r} {d}|{r} help {d}|{r} exit {c}]{r}"

    @property
    def dark_commands(self) -> str:
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
        self.ui_line_count = 0
        self.prompt_needs_full_draw = True
        atexit.register(self.restore_console)

        self.set_console_icon("wormhole.ico")

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

    def get_resource_path(self, relative_path: str) -> str:
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def build_world(self, filename: str) -> None:
        filepath = self.get_resource_path(filename)
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print(
                f"Error: Could not find {filepath}. Please ensure it is in the same directory."
            )
            sys.exit(1)

        self.items = {}
        for key, item_data in data.get("items", {}).items():
            self.items[key] = Item(name=item_data["name"], desc=item_data["desc"])

        self.rooms = {}
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
        leaderboard = []
        try:
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
        with open("leaderboard.txt", "w", encoding="utf-8") as f:
            for entry in leaderboard[:10]:
                f.write(f"{entry[0]},{entry[1]}\n")

    def get_timer_string(self) -> str:
        elapsed_time = time() - self.start_time
        mins, secs = divmod(int(elapsed_time), 60)

        leaderboard = self.load_leaderboard()
        if leaderboard:
            b_mins, b_secs = divmod(int(leaderboard[0][1]), 60)
            return f"Time: {mins:02d}:{secs:02d} | Best: {b_mins:02d}:{b_secs:02d}"

        return f"Time: {mins:02d}:{secs:02d} | Best: --:--"

    def _live_background_task(self) -> None:
        reds = [
            (100, 0, 0), (150, 0, 0), (200, 0, 0), (255, 0, 0),
            (255, 100, 100), (255, 0, 0), (200, 0, 0), (150, 0, 0)
        ]
        led_idx = 0
        ticks = 0

        while True:
            sleep(0.1)
            if not getattr(self, "is_running", False):
                break

            # Dynamic Resize Check
            current_width = self.config.ui_width
            last_width = getattr(self, "last_width", current_width)
            if current_width != last_width:
                self.last_width = current_width
                if getattr(self, "waiting_for_input", False):
                    with self.io_lock:
                        sys.stdout.write("\033[H\033[J")
                        self.show_status(resize=True)
                        sys.stdout.write(f"{self.config.yellow}What do you do!?{self.config.reset}\n> ")
                        sys.stdout.flush()

            with self.io_lock:
                if getattr(self, "display_timer", False) and getattr(self, "led_active", False):
                    title_len = getattr(self, "current_title_length", 0)
                    center_len = getattr(self, "center_length", 37)
                    if title_len > 0:
                        live_width = self.config.ui_width
                        spaces = max(1, (live_width - center_len) // 2 - title_len) 
                        dynamic_col = title_len + spaces + 1

                        r, g, b = reds[led_idx]
                        led_idx = (led_idx + 1) % len(reds)
                        color = f"\033[38;2;{r};{g};{b}m"
                        
                        sys.stdout.write(f"\0337\033[2;{dynamic_col}H{color}*\0338")

                if ticks % 10 == 0 and getattr(self, "display_timer", False):
                    timer_str = self.get_timer_string()
                    title_str = f"Wormhole - {timer_str}"
                    sys.stdout.write(f"\033]0;{title_str}\007")

                sys.stdout.flush()
            ticks += 1

    def reset_session(self) -> None:
        self.items: Dict[str, Item] = {}
        self.rooms: Dict[str, Room] = {}
        self.build_world("world.json")
        self.player = Player(start_room="cavern")
        self.needs_redraw: bool = True
        
        self.is_running: bool = True
        self.current_run = None
        self.start_time: float = time()
        self.last_width = self.config.ui_width

        if not hasattr(self, "bg_thread") or not self.bg_thread.is_alive():
            self.bg_thread = threading.Thread(target=self._live_background_task, daemon=True)
            self.bg_thread.start()

    def display_leaderboard(
        self,
        leaderboard: List[Tuple[str, float]],
        current_run: Optional[Tuple[str, float]] = None,
    ) -> None:
        width = self.config.ui_width

        ascii_art = [
            r"  _                      _           _                         _ ",
            r" | |                    | |         | |                       | |",
            r" | |   ___  __ _    __| | ___ _ __| |__   ___   __ _ _ __ __| |",
            r" | |  / _ \/ _` |  / _` |/ _ \ '__| '_ \ / _ \ / _` | '__/ _` |",
            r" | |___|  __/ (_| | | (_| |  __/ |  | |_) | (_) | (_| | | | (_| |",
            r" \_____/\___|\__,_|  \__,_|\___|_|  |_.__/ \___/ \__,_|_|  \__,_|",
        ]

        print()

        for line in ascii_art:
            print(f"{self.config.yellow}{line.center(width)}{self.config.reset}")

        print(f"{self.config.cyan}{'--- TOP 10 SCORES ---'.center(width)}{self.config.reset}")
        print("-" * width)

        if not leaderboard and not current_run:
            msg = "No times recorded yet. Be the first!"
            print(msg.center(width))
        else:
            display_list = leaderboard[:10]

            if current_run and current_run not in display_list:
                display_list.append(current_run)

            for i, (name, t) in enumerate(display_list):
                m, s = divmod(int(t), 60)

                rank = f"{i+1}." if i < 10 else "-"
                row = f"{rank:<3} {name:<29} {m:02d}:{s:02d}"

                if current_run and name == current_run[0] and t == current_run[1]:
                    print(
                        f"{self.config.blink}{self.config.white}{row.center(width)}{self.config.reset}"
                    )
                else:
                    print(row.center(width))

        print("-" * width + "\n")

    # -------------------------------------------------------------------------
    # UTILITY FUNCTIONS
    # -------------------------------------------------------------------------
    def wrap_text(self, text: str, width: int) -> str:
        """Dynamically wraps plain text to fit the terminal width without clipping words."""
        lines = []
        for p in text.split('\n'):
            if not p.strip():
                lines.append("")
            else:
                lines.extend(textwrap.wrap(p, width=width, replace_whitespace=False))
        return '\n'.join(lines)

    def clear(self) -> None:
        self.led_active = False
        sys.stdout.write("\033[H\033[J")
        sys.stdout.flush()
        
    def get_gradient_separator(self, width: int, fade_ratio: float = 1.0) -> str:
        sep = ""
        for i in range(width):
            ratio = i / max(1, width - 1)
            if ratio < 0.5:
                local_ratio = ratio * 2
                r = int((255 - 105 * local_ratio) * fade_ratio)
                g = int(50 * fade_ratio)
                b = int((150 + 105 * local_ratio) * fade_ratio)
            else:
                local_ratio = (ratio - 0.5) * 2
                r = int((150 - 100 * local_ratio) * fade_ratio)
                g = int((50 + 50 * local_ratio) * fade_ratio)
                b = int(255 * fade_ratio)
            sep += f"\033[38;2;{r};{g};{b}m-"
        return sep + self.config.reset

    def _out(self, text: str = "") -> None:
        """Helper to safely wipe the current console line while writing and log absolute height."""
        for line in str(text).split('\n'):
            sys.stdout.write(f"{line}\033[K\n")
            if hasattr(self, 'ui_line_count'):
                self.ui_line_count += 1

    def transient_notify(self, text: str, sleep_time: float = None) -> None:
        """Flashes a temporary message at the bottom of the screen, erasing it flawlessly afterward."""
        if sleep_time is None:
            sleep_time = self.config.medium_sleep
        
        width = self.config.ui_width
        wrapped_text = self.wrap_text(text, width)
        colored_text = self.format_text_colors(wrapped_text)
        
        lines = colored_text.split('\n')
        
        with self.io_lock:
            sys.stdout.write("\n")
            for line in lines:
                sys.stdout.write(line + "\n")
            sys.stdout.flush()
        
        sleep(sleep_time)
        
        # Moves cursor up exactly over the printed text + the user's input line to perfectly preserve the original prompt.
        lines_to_up = len(lines) + 2
        with self.io_lock:
            sys.stdout.write(f"\033[{lines_to_up}A\r\033[J")
            sys.stdout.flush()

    def restore_console(self) -> None:
        self.set_console_echo(True)

    def set_console_echo(self, enable: bool) -> None:
        try:
            if WINDOWS:
                kernel32 = ctypes.windll.kernel32
                h_stdin = kernel32.GetStdHandle(-10)
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
        try:
            if WINDOWS:
                while msvcrt.kbhit():
                    msvcrt.getch()
            else:
                termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)
        except Exception:
            pass

    def format_text_colors(self, text: str) -> str:
        """Finds contextual keywords and maps them cleanly without breaking wrapped edges."""
        keywords = [
            "north", "south", "east", "west", "left", "right", "up", "down",
            "up ahead", "back down", "back up ahead",
            "compass", "map", "shroom", "gun", "key", "fish", "scripture", "poop",
            "wormhole blaster", "fish paste", "worm poo", "wormhole",
            "alien worm creature", "alien worm", "wormy creatures"
        ]
        keywords.sort(key=len, reverse=True)
        
        pattern = re.compile(r'\b(' + '|'.join(keywords) + r')\b', re.IGNORECASE)
        
        def replacer(match):
            word = match.group(0)
            lw = word.lower()
            
            if lw == "up":
                start_idx = match.start()
                prefix = text[max(0, start_idx - 10):start_idx].lower()
                if "woke " in prefix or "pick " in prefix or "crawling " in prefix:
                    return word
                    
            if lw in ["alien worm creature", "alien worm", "wormy creatures"]:
                color = self.config.red
            else:
                color = self.config.yellow
                
            return f"{color}{word}{self.config.white}"

        highlighted = pattern.sub(replacer, text)
        return f"{self.config.white}{highlighted}{self.config.reset}"

    def show_flashing_start(self, text: str) -> None:
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
        width = self.config.ui_width
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
        
        with self.io_lock:
            sys.stdout.write("\r\033[2K")
            sys.stdout.write("\033[1A\033[2K\r")
            sys.stdout.flush()
            
        self.flush_input()

    def show_pulsing_exit(self, text: str, color_mode: str = "red") -> None:
        width = self.config.ui_width
        stop_event = threading.Event()
        pad = " " * ((width - len(text)) // 2)

        def pulse():
            while not stop_event.is_set():
                for val in range(50, 256, 20):
                    if stop_event.is_set(): break
                    if color_mode == "cyan": color = f"\033[38;2;0;{val};{val}m"
                    elif color_mode == "white": color = f"\033[38;2;{val};{val};{val}m"
                    else: color = f"\033[38;2;{val};0;0m"
                    
                    with self.io_lock:
                        sys.stdout.write(f"\r\033[2K{pad}{color}{text}\033[0m")
                        sys.stdout.flush()
                    stop_event.wait(0.02)

                if not stop_event.is_set():
                    stop_event.wait(0.8)

                for val in range(255, 49, -30):
                    if stop_event.is_set(): break
                    if color_mode == "cyan": color = f"\033[38;2;0;{val};{val}m"
                    elif color_mode == "white": color = f"\033[38;2;{val};{val};{val}m"
                    else: color = f"\033[38;2;{val};0;0m"
                    
                    with self.io_lock:
                        sys.stdout.write(f"\r\033[2K{pad}{color}{text}\033[0m")
                        sys.stdout.flush()
                    stop_event.wait(0.02)

                if not stop_event.is_set():
                    stop_event.wait(0.1)

        t = threading.Thread(target=pulse, daemon=True)
        t.start()

        self.flush_input()
        getpass.getpass("")
        stop_event.set()
        
        with self.io_lock:
            sys.stdout.write("\r\033[2K")
            sys.stdout.write("\033[1A\033[2K\r") 
            sys.stdout.flush()
            
        self.flush_input()

    def prompt_play_again(self, text: str) -> bool:
        width = self.config.ui_width
        pad = " " * ((width - len(text)) // 2)
        stop_event = threading.Event()

        def pulse():
            while not stop_event.is_set():
                for val in range(50, 256, 20):
                    if stop_event.is_set(): break
                    color = f"\033[38;2;{val};0;0m"
                    with self.io_lock:
                        sys.stdout.write(f"\r\033[2K{pad}{color}{text}\033[0m")
                        sys.stdout.flush()
                    stop_event.wait(0.02)

                if not stop_event.is_set(): stop_event.wait(0.8)

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
        width = self.config.ui_width
        centered_text = text.center(width).rstrip()

        self.flush_input()

        for val in range(0, 256, 4):
            if color_mode == "red":
                color = f"\033[38;2;{val};0;0m"
            else:
                color = f"\033[38;2;{val};{val};{val}m"

            with self.io_lock:
                sys.stdout.write(f"\r\033[2K{color}{centered_text}\033[0m")
                sys.stdout.flush()
            sleep(speed)

        print()

    def fade_item_box(self, room: Room) -> None:
        width = self.config.ui_width
        self.flush_input()

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

        self._out()
        self._out() # Blank line of space above gradient
        self._out()
        self._out()
        sys.stdout.flush()

        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

        for val in range(0, 256, 6):
            if WINDOWS and msvcrt.kbhit():
                break

            fade_ratio = val / 255.0
            sep_line = self.get_gradient_separator(width, fade_ratio) + "\n"
            
            white_color = f"\033[38;2;{val};{val};{val}m"
            yellow_color = f"\033[38;2;{val};{val};0m"

            sys.stdout.write("\033[3A\r")
            
            line1 = sep_line
            if item_name:
                line2 = f"{white_color}{part1}{yellow_color}{item_name}{white_color}{part2}\033[0m\033[K\n"
            else:
                line2 = f"{white_color}{part1}\033[0m\033[K\n"
            line3 = sep_line

            sys.stdout.write(line1 + line2 + line3)
            sys.stdout.flush()
            sleep(0.02)

        sys.stdout.write("\033[3A\r")
        
        static_sep = self.get_gradient_separator(width) + "\n"
        line1 = static_sep
        if item_name:
            line2 = f"{self.config.white}{part1}{self.config.yellow}{item_name}{self.config.white}{part2}{self.config.reset}\033[K\n"
        else:
            line2 = f"{self.config.white}{part1}{self.config.reset}\033[K\n"
        line3 = static_sep
        
        sys.stdout.write(line1 + line2 + line3)

        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        self.flush_input()

    def show_dimmed_status(self) -> None:
        self.led_active = False
        room = self.rooms[self.player.current_room]
        width = self.config.ui_width

        lines = []
        c_dg = self.config.dark_gray
        c_cy = self.config.cyan
        c_res = self.config.reset
        
        lines.append(f"{c_dg}{'=' * width}{c_res}")
        
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

        inv_display = (
            ", ".join(item.name for item in self.player.inventory).title()
            if self.player.inventory else "Empty"
        )
        lines.append(f"{c_cy} INVENTORY:{c_res} {inv_display}")
        
        lines.append(f"{c_dg}{'=' * width}{c_res}")
        lines.append("")
        
        offset = len(self.config.commands) - len(self.config.plain_commands)
        lines.append(self.config.commands.center(width + offset))
        lines.append("")
        
        raw_desc = getattr(self, 'last_printed_desc', room.desc)
        wrapped_desc = self.wrap_text(raw_desc, width)
        colored_desc = self.format_text_colors(wrapped_desc)
        for line in colored_desc.split('\n'):
            lines.append(line)
            
        lines.append("")
        lines.append("") # Blank line of space above gradient
        
        sep_str = self.get_gradient_separator(width)
        lines.append(sep_str.strip())
        if room.item and room.item.name != "alien worm":
            item_msg = f"[*] You see a(n) {self.config.yellow}{room.item.name.upper()}{c_res} here."
            if self.player.items_collected == 0:
                item_msg += " Maybe you should get that."
        else:
            item_msg = "[*] There are no items to pick up here."
        lines.append(item_msg)
        lines.append(sep_str.strip())

        full_text = "\n".join(lines)

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
                elif token.startswith("\033[38;2;"):
                    try:
                        parts = token.replace("\033[38;2;", "").replace("m", "").split(";")
                        current_rgb = (int(parts[0]), int(parts[1]), int(parts[2]))
                    except:
                        pass
            else:
                for c in token:
                    chars.append({'c': c, 'start_rgb': current_rgb})

        target_rgb = (90, 90, 90)
        steps = 20
        
        with self.io_lock:
            sys.stdout.write("\033[?25l")
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
                
                r = int(sr + (tr - sr) * ratio)
                g = int(sg + (tg - sg) * ratio)
                b = int(sb + (tb - sb) * ratio)
                
                frame_str += f"\033[38;2;{r};{g};{b}m{c}"
                
            with self.io_lock:
                sys.stdout.write("\033[H")
                sys.stdout.write(frame_str + "\033[0m\033[K\n")
                sys.stdout.write("\033[J")
                sys.stdout.flush()
                
            sleep(0.04)

        with self.io_lock:
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()

    def typewriter(self, text: str, speed: Optional[float] = None) -> None:
        """Draws animated text line by line to support absolute line counting."""
        speed = speed or self.config.text_speed
        self.flush_input()

        chars = []
        current_rgb = (255, 255, 255)
        
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
        tokens = ansi_regex.split(text)
        
        for token in tokens:
            if not token:
                continue
            if token.startswith('\033'):
                if token in color_map:
                    current_rgb = color_map[token]
            else:
                for c in token:
                    chars.append({'c': c, 'rgb': current_rgb})

        sys.stdout.write("\033[?25l")
        line_count = text.count('\n') + 1
        if hasattr(self, 'ui_line_count'):
            self.ui_line_count += line_count
        
        if line_count > 1:
            sys.stdout.write("\n" * (line_count - 1))
        sys.stdout.flush()

        fade_tail = 12  
        skip = False

        up_moves = line_count - 1
        up_str = f"\033[{up_moves}A" if up_moves > 0 else ""

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
                
                base_val = 30
                r = int(base_val + (char_dict['rgb'][0] - base_val) * ratio)
                g = int(base_val + (char_dict['rgb'][1] - base_val) * ratio)
                b = int(base_val + (char_dict['rgb'][2] - base_val) * ratio)
                
                frame_str += f"\033[38;2;{r};{g};{b}m{c}"
                
            frame_str += "\033[0m\033[K"

            current_newlines = frame_str.count('\n')
            total_newlines = line_count - 1
            if current_newlines < total_newlines:
                for _ in range(total_newlines - current_newlines):
                    frame_str += '\n\033[K'
                
            with self.io_lock:
                sys.stdout.write(f"\r{up_str}{frame_str}")
                sys.stdout.flush()
                
            sleep(speed)

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

        title = "W O R M H O L E"
        sub = "A  t e x t  a d v e n t u r e  g a m e"
        author = "created by matthew pool"

        print("\n" * 4)
        title_pad = " " * ((width - len(title)) // 2)
        sub_pad = " " * ((width - len(sub)) // 2)
        author_pad = " " * ((width - len(author)) // 2)
        
        self.flush_input()
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

        skip = False

        sub_offset = 140
        author_offset = 240
        max_step = 255 + author_offset

        for step in range(0, max_step, 4):
            if WINDOWS and msvcrt.kbhit():
                skip = True
                break

            title_str = ""
            for i, char in enumerate(title):
                val = max(0, min(255, step - (i * 20)))
                title_str += f"\033[38;2;{val};0;{val}m{char}"

            sub_str = ""
            sub_step = step - sub_offset
            for i, char in enumerate(sub):
                val = max(0, min(255, sub_step - (i * 8)))
                total_chars_sub = max(1, len(sub) - 1)
                spatial_ratio_sub = 1.0 - (0.4 * (i / total_chars_sub))
                final_v = int(val * spatial_ratio_sub)
                sub_str += f"\033[38;2;{final_v};{final_v};{final_v}m{char}"

            author_str = ""
            author_step = step - author_offset
            val_auth = max(0, min(255, author_step))
            
            total_chars_auth = max(1, len(author) - 1)
            mid_auth = total_chars_auth / 2.0
            
            for i, char in enumerate(author):
                dist = abs(i - mid_auth) / mid_auth if mid_auth > 0 else 0
                r_target = 255
                g_target = int(255 - 55 * dist)  
                b_target = int(255 * (1.0 - dist)) 
                
                master_fade = val_auth / 255.0
                r = int(r_target * master_fade)
                g = int(g_target * master_fade)
                b = int(b_target * master_fade)
                
                author_str += f"\033[38;2;{r};{g};{b}m{char}"

            sys.stdout.write(f"\r{title_pad}{title_str}{self.config.reset}\n")
            sys.stdout.write(f"\r{sub_pad}{sub_str}{self.config.reset}\n")
            sys.stdout.write("\n")
            sys.stdout.write(f"\r{author_pad}{author_str}{self.config.reset}")
            
            sys.stdout.write("\033[3A") 
            sys.stdout.flush()
            sleep(0.03)

        sys.stdout.write(f"\r{title_pad}\033[38;2;255;0;255m{title}{self.config.reset}\n")
        
        final_sub_gradient = ""
        total_chars_sub = max(1, len(sub) - 1)
        for i, char in enumerate(sub):
            spatial_ratio_sub = 1.0 - (0.4 * (i / total_chars_sub))
            v = int(255 * spatial_ratio_sub)
            final_sub_gradient += f"\033[38;2;{v};{v};{v}m{char}"
        sys.stdout.write(f"\r{sub_pad}{final_sub_gradient}{self.config.reset}\n")
            
        sys.stdout.write("\n")
        
        final_author_gradient = ""
        total_chars_auth = max(1, len(author) - 1)
        mid_auth = total_chars_auth / 2.0
        for i, char in enumerate(author):
            dist = abs(i - mid_auth) / mid_auth if mid_auth > 0 else 0
            r_target = 255
            g_target = int(255 - 55 * dist)
            b_target = int(255 * (1.0 - dist))
            final_author_gradient += f"\033[38;2;{r_target};{g_target};{b_target}m{char}"
        sys.stdout.write(f"\r{author_pad}{final_author_gradient}{self.config.reset}\n")
        
        sys.stdout.flush()
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

        prompt_msg = "P R E S S  < E N T E R >  T O  S T A R T"
        prompt_pad = " " * ((width - len(prompt_msg)) // 2)
        
        print("\n" * 2)
        self.show_flashing_prompt(prompt_msg)

        sys.stdout.write("\033[?25l")
        self.clear() 
        sys.stdout.flush()

        for val in range(255, -1, -5):
            sys.stdout.write("\033[H")
            
            title_color = f"\033[38;2;{val};0;{val}m"
            
            exit_sub_str = ""
            for i, char in enumerate(sub):
                spatial_ratio_sub = 1.0 - (0.4 * (i / total_chars_sub))
                final_v = int(val * spatial_ratio_sub)
                exit_sub_str += f"\033[38;2;{final_v};{final_v};{final_v}m{char}"
            
            exit_auth_str = ""
            for i, char in enumerate(author):
                dist = abs(i - mid_auth) / mid_auth if mid_auth > 0 else 0
                r_target = 255
                g_target = int(255 - 55 * dist)
                b_target = int(255 * (1.0 - dist))
                
                master_fade = val / 255.0
                r = int(r_target * master_fade)
                g = int(g_target * master_fade)
                b = int(b_target * master_fade)
                exit_auth_str += f"\033[38;2;{r};{g};{b}m{char}"

            prompt_color = f"\033[38;2;{val};{val};{val}m"
            
            output = (
                "\n\n\n\n\n"
                f"{title_pad}{title_color}{title}{self.config.reset}\n"
                f"{sub_pad}{exit_sub_str}{self.config.reset}\n"
                "\n"
                f"{author_pad}{exit_auth_str}{self.config.reset}\n"
                "\n\n\n"
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

        grid = []
        for r in range(rows):
            row_list = []
            for c in range(cols):
                if c % 2 == 0:
                    row_list.append("   ")
                else:
                    row_list.append(" ")
            grid.append(row_list)

        def format_node(room_name: str) -> str:
            if room_name == "worm_incubation_chamber" and has_compass:
                if self.player.current_room == room_name:
                    return f"<{self.config.red}X{self.config.reset}>"
                return f"<{self.config.red}?{self.config.reset}>"

            if self.player.current_room == room_name:
                return f"[{self.config.green}X{self.config.reset}]"

            if self.rooms[room_name].visited:
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

        visible_row_width = ((cols + 1) // 2) * 3 + (cols // 2) * 1
        margin = max(0, (width - visible_row_width) // 2)

        for row in grid:
            print(" " * margin + "".join(row))

        print()
        print("=" * width)

        if has_compass:
            legend = f"Legend: [{self.config.green}X{self.config.reset}] You are here | [{self.config.yellow}*{self.config.reset}] Visited | <{self.config.red}?{self.config.reset}> Unknown Signal"
            print(legend.center(width + 27))
        else:
            legend = f"Legend: [{self.config.green}X{self.config.reset}] You are here | [{self.config.yellow}*{self.config.reset}] Visited | [ ] Unknown"
            print(legend.center(width + 18))

    def help_menu(self) -> None:
        self.display_timer = False
        
        with self.io_lock:
            sys.stdout.write("\033[H")
            sys.stdout.flush()
            
        width = self.config.ui_width

        help_art = [
            r" _   _      _       ",
            r"| | | | ___| |___   ",
            r"| |_| |/ _ \ | '_ \ ",
            r"|  _  |  __/ | |_) |",
            r"|_| |_|\___|_| .__/ ",
            r"             |_|    "
        ]

        self._out()
        for line in help_art:
            self._out(f"{self.config.cyan}{line.center(width)}{self.config.reset}")
        self._out()

        plain_help_lines = [
            "To Move:       go  direction   Example: go  north, go up",
            "Get Item:      get item        Example: get light",
            "Use Item:      use item        Example: use key",
            "Help:          help            Shows this menu",
            "Quit:          exit            Ends the game",
        ]

        w = self.config.white
        lg = self.config.light_gray
        y = self.config.yellow
        
        formatted_help_lines = [
            f"{lg}To Move:       {w}go  {y}direction   {lg}Example: {w}go {y} north{w}, go {y}up",
            f"{lg}Get Item:      {w}get {y}item        {lg}Example: {w}get {y}light",
            f"{lg}Use Item:      {w}use {y}item        {lg}Example: {w}use {y}key",
            f"{lg}Help:          {w}help            {lg}Shows this menu",
            f"{lg}Quit:          {w}exit            {lg}Ends the game",
        ]

        max_line_len = max(len(line) for line in plain_help_lines)
        left_padding = " " * ((width - max_line_len) // 2)

        for line in formatted_help_lines:
            self._out(f"{left_padding}{line}{self.config.reset}")

        self._out()
        
        with self.io_lock:
            sys.stdout.write("\033[J")
            sys.stdout.flush()
            
        self.show_pulsing_exit("P R E S S  < E N T E R >  T O  C L O S E", color_mode="white")

    def handle_debug(self, args: List[str]) -> None:
        if not getattr(self.config, "DEBUG_MODE", False):
            self.handle_silly_response("debug", action="other")
            return

        if not args:
            with self.io_lock:
                sys.stdout.write("\033[H")
                sys.stdout.flush()
                
            width = self.config.ui_width
            self._out()
            self._out(f"{self.config.magenta}--- DEBUG MENU ---{self.config.reset}".center(width + len(self.config.magenta) + len(self.config.reset)))
            self._out("  debug 1 : Test Exit (Y) Sequence".center(width))
            self._out("  debug 2 : Boss Room (Loss - 0 items)".center(width))
            self._out("  debug 3 : Boss Room (Win - 8 items)".center(width))
            self._out(("-" * 36).center(width))
            self._out()
            
            with self.io_lock:
                sys.stdout.write("\033[J")
                sys.stdout.flush()
                
            self.show_pulsing_exit("P R E S S  < E N T E R >  T O  C L O S E", color_mode="white")
            self.needs_redraw = True
            return

        choice = args[0]

        if choice == "1":
            self.transient_notify(f"{self.config.magenta}[DEBUG] Triggering Exit Sequence...{self.config.reset}", self.config.quick_sleep)
            self.handle_exit([], force_yes=True)

        elif choice == "2":
            self.transient_notify(f"{self.config.magenta}[DEBUG] Teleporting to Boss (Loss)...{self.config.reset}", self.config.quick_sleep)
            self.player.current_room = "worm_incubation_chamber"
            self.player.items_collected = 0
            self.needs_redraw = True

        elif choice == "3":
            self.transient_notify(f"{self.config.magenta}[DEBUG] Teleporting to Boss (Win)...{self.config.reset}", self.config.quick_sleep)
            self.player.current_room = "worm_incubation_chamber"
            self.player.items_collected = 8
            self.needs_redraw = True

        else:
            self.transient_notify("Invalid debug trigger.", self.config.quick_sleep)

    def show_status(self, resize=False) -> None:
        self.led_active = False
        self.ui_line_count = 0
        
        with self.io_lock:
            sys.stdout.write("\033[H")
            sys.stdout.flush()

        room = self.rooms[self.player.current_room]
        just_arrived = self.player.current_room != self.player.previous_room
        width = self.config.ui_width

        title = room.name.replace("_", " ").title()

        if room.name == "worm_incubation_chamber":
            self.display_timer = False

            if self.player.items_collected == 8:
                elapsed_time = time() - self.start_time
                mins, secs = divmod(int(elapsed_time), 60)

                self.clear()
                width = self.config.ui_width

                sys.stdout.write("\033[?25l")
                sys.stdout.flush()

                win_art = [
                    r"  ____ ___  _   _  ____ ____      _ _____ ____  _ ",
                    r" / ___/ _ \| \ | |/ ___|  _ \    / \_   _/ ___|| |",
                    r"| |  | | | |  \| | |  _| |_) |  / _ \| | \___ \| |",
                    r"| |__| |_| | |\  | |_| |  _ <  / ___ \ |  ___) |_|",
                    r" \____\___/|_| \_|\____|_| \_\/_/   \_\| |____/(_)"
                ]
                print("\n\n")
                for line in win_art:
                    print(f"{self.config.green}{line.center(width)}{self.config.reset}")
                print("\n\n")

                block_1_lines = [
                    "A giant, hideous alien worm creature—with elongated, razor-sharp fangs in its gaping, fleshy mouth—erupts from the ground beneath you, letting out a piercing, high-pitched screech that chills you to the bone.",
                    "You pull out your wormhole blaster and load it with fish paste and warm worm poo, creating a bioactive, glowing alien mush.",
                    "As the creature starts slithering towards you at high velocity, you open fire, disintegrating the alien worm into a splatter of thick, slimy goo and guts.",
                    "The ground rumbles and gives way as more wormholes appear and countless more wormy creatures emerge!",
                    "You aim your blaster at the ground and squeeze the cold, metallic trigger.",
                    "A cosmological wormhole manifests, and you leap inside!",
                    "A stream of vibrant colored lights and geometric shapes, along with unfamiliar sounds, floods your surroundings.",
                    "You pass out."
                ]

                block_2_lines = [
                    "When you awaken, you find yourself back in the cold, damp cavern where you first started—thick goo oozing down your face and clothes.",
                    "An eerie silence fills the air. You hear yourself breathe: short, quick, panicked breaths.",
                    "\"Why the hell am I back here?\" you mumble under your breath, frantically looking around.",
                    "\"Why the hell am I back here?!\" you yell, a concoction of saliva and still-warm goo spraying from your lips with every syllable.",
                    "You look down to see hundreds, if not thousands, of tiny, foreign-looking worms crawling up your legs.",
                    "The tiny creatures begin biting your bare skin. You drop your blaster, watching it shatter on the ground below. Your skin burns as the acidic juices from their little mouths dissolve right through your flesh—deep into your bones.",
                    "Your body drops to the ground. You scarf down the shroom from your inventory in hopes of relieving the pain and escaping the severity of the situation.",
                    "It doesnt work. The ground beneath you begins to rumble, and your terror peaks. You know that sound. You know what's coming, and now you know there's no escape.",
                    "You're worm food."
                ]

                # Run Block 1
                for line in block_1_lines:
                    is_centered = line.strip() == "You pass out."
                    if is_centered:
                        centered_line = line.strip().center(width)
                        colored_line = self.format_text_colors(centered_line)
                    else:
                        wrapped_line = self.wrap_text(line, width)
                        colored_line = self.format_text_colors(wrapped_line)
                    
                    self.typewriter(colored_line, speed=0.03)
                    print()

                self.show_pulsing_exit("P R E S S  < E N T E R >", color_mode="white")

                sys.stdout.write("\033[H\033[J")
                sys.stdout.write("\033[?25l")
                sys.stdout.flush()
                
                print("\n\n")
                for line in win_art:
                    print(f"{self.config.green}{line.center(width)}{self.config.reset}")
                print("\n\n")

                # Run Block 2
                for line in block_2_lines:
                    is_centered = line.strip() == "You're worm food."
                    if is_centered:
                        centered_line = line.strip().center(width)
                        colored_line = self.format_text_colors(centered_line)
                    else:
                        wrapped_line = self.wrap_text(line, width)
                        colored_line = self.format_text_colors(wrapped_line)
                    
                    self.typewriter(colored_line, speed=0.03)
                    print()

                self.show_pulsing_exit("P R E S S  < E N T E R >", color_mode="white")

                sys.stdout.write("\033[?25h")
                sys.stdout.flush()

                print("\n\n")
                win_msg = "Aw man... You win, bruh!"
                print(f"{self.config.green}{win_msg.center(width)}{self.config.reset}")
                print("\n\n")

                clear_time_msg = f"Clear Time: {mins:02d}:{secs:02d}"
                print(
                    f"{self.config.white}{clear_time_msg.center(width)}{self.config.reset}\n"
                )

                leaderboard = self.load_leaderboard()
                current_run = ("Anonymous", elapsed_time)

                if len(leaderboard) < 10 or elapsed_time < leaderboard[-1][1]:
                    hs_msg = "*** NEW TOP 10 HIGH SCORE! ***"

                    print(
                        f"{self.config.blink}{self.config.yellow}{hs_msg.center(width)}{self.config.reset}\n\n"
                    )

                    pad = " " * ((width - 45) // 2)
                    prompt_color = self.config.white
                    prompt_text = "Enter Name: "
                    
                    while True:
                        self.flush_input()
                        self.set_console_echo(True)
                        try:
                            sys.stdout.write(f"\r\033[2K{pad}{prompt_color}{prompt_text}{self.config.reset}")
                            sys.stdout.flush()
                            player_name = input().strip()[:27]
                        finally:
                            self.set_console_echo(False)
                            
                        if not player_name:
                            sys.stdout.write("\033[1A")
                            for _ in range(2):
                                sys.stdout.write(f"\r\033[2K{pad}{self.config.red}{prompt_text}{self.config.reset}")
                                sys.stdout.flush()
                                sleep(0.15)
                                sys.stdout.write(f"\r\033[2K{pad}{self.config.white}{prompt_text}{self.config.reset}")
                                sys.stdout.flush()
                                sleep(0.15)
                            prompt_color = self.config.white
                        else:
                            sys.stdout.write("\033[1A")
                            sys.stdout.write(f"\r\033[2K{pad}{self.config.white}{prompt_text}{self.config.green}{player_name}{self.config.reset}\n")
                            sys.stdout.flush()
                            break

                    current_run = (player_name, elapsed_time)
                    leaderboard.append(current_run)
                    leaderboard = sorted(leaderboard, key=lambda x: x[1])[:10]
                    self.save_leaderboard(leaderboard)

                self.current_run = current_run
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
                
                print()
                self.show_pulsing_exit("P R E S S  < E N T E R >", color_mode="white")
                
                self.current_run = None
                self.is_running = False
                return

        self.display_timer = True

        has_compass = self.player.has_item("compass")

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

        led_off = " "
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
        
        self.current_title_length = len(plain_left)
        self.center_length = len(plain_center)

        self._out("=" * width)

        if not has_compass:
            self._out(colored_left)
        elif not room.visited:
            self._out(colored_left + (" " * spaces_between) + gray_center)
        else:
            self._out(colored_left + (" " * spaces_between) + colored_center)

        inv_display = (
            ", ".join(item.name for item in self.player.inventory).title()
            if self.player.inventory
            else "Empty"
        )
        self._out(f"{self.config.cyan} INVENTORY:{self.config.reset} {inv_display}")

        self._out("=" * width)
        self._out()
        offset = len(self.config.commands) - len(self.config.plain_commands)
        self._out(self.config.commands.center(width + offset))

        if not resize:
            with self.io_lock:
                sys.stdout.write("\033[J")
                sys.stdout.flush()

        active_desc = room.desc
        active_alt_desc = room.alt_desc

        if room.name == "entryway" and not has_compass:
            active_desc = active_desc.replace("west", "left").replace("east", "right").replace("The path to the south", "The path down")
            active_alt_desc = active_alt_desc.replace("west", "left").replace("east", "right").replace("The path to the south", "The path down")
            
        if room.name == "cavern" and not has_compass:
            active_alt_desc = active_alt_desc.replace("to the north", "back up ahead")

        used_typewriter = False
        desc_to_print = ""

        if just_arrived and room.visited and not resize:
            room.revisited = True

        if not room.visited and not resize:
            desc_to_print = active_desc
            wrapped_desc = self.wrap_text(desc_to_print, width)
            
            if room.name == "cavern" and self.player.items_collected == 0:
                sleep(1.0) 
                
            self._out("\n") # Add blank line before typewriter text natively
            self.typewriter(self.format_text_colors(wrapped_desc))
            room.visited = True
            used_typewriter = True

        elif not room.revisited or resize:
            desc_to_print = active_desc
            wrapped_desc = self.wrap_text(desc_to_print, width)
            self._out("\n")
            self._out(self.format_text_colors(wrapped_desc))
            
        elif just_arrived:
            if room.item or active_alt_desc != active_desc:
                desc_to_print = active_alt_desc
                wrapped_desc = self.wrap_text(desc_to_print, width)
                self._out("\n")
                self._out(self.format_text_colors(wrapped_desc))
            else:
                desc_to_print = f"You are back in the {title}. You've already cleared this area out."
                wrapped_desc = self.wrap_text(desc_to_print, width)
                self._out("\n")
                self._out(self.format_text_colors(wrapped_desc))
                
        else:
            desc_to_print = active_alt_desc.replace("You are back in", "You are still in")
            wrapped_desc = self.wrap_text(desc_to_print, width)
            self._out("\n")
            self._out(self.format_text_colors(wrapped_desc))

        self.last_printed_desc = desc_to_print

        if used_typewriter:
            self.fade_item_box(room)
        else:
            self._out()
            self._out() # Blank line of space above gradient
            self._out(self.get_gradient_separator(width).strip())

            if room.item and room.item.name != "alien worm":
                item_msg = f"[*] You see a(n) {self.config.yellow}{room.item.name.upper()}{self.config.reset} here."

                if self.player.items_collected == 0:
                    item_msg += " Maybe you should get that."

                self._out(item_msg)
            else:
                self._out("[*] There are no items to pick up here.")

            self._out(self.get_gradient_separator(width).strip())

        if used_typewriter and has_compass:
            # Let the player see the gray exits for a brief moment before activating them
            sleep(0.3)
            lines_up = self.ui_line_count - 1
            with self.io_lock:
                sys.stdout.write(f"\033[{lines_up}A\r")
                sys.stdout.write(colored_left + (" " * spaces_between) + colored_center + "\033[K")
                sys.stdout.write(f"\033[{lines_up}B\r")
                sys.stdout.flush()

        self.prompt_needs_full_draw = True

    # -------------------------------------------------------------------------
    # COMMAND HANDLERS
    # -------------------------------------------------------------------------
    def handle_silly_response(self, target: str, action: str) -> None:
        count = self.player.silly_count
        msg = ""
        if action == "go" or action == "get":
            if count == 0:
                msg = "You can't really do that, silly..."
            elif count == 1:
                msg = f"We would {action} {target} if we could..."
            elif count == 2:
                msg = f"Bruh. Stop. You can't {action} {target}!"
            else:
                self.help_menu()
                self.needs_redraw = True 
        else:
            msg = "I don't understand what you're trying to do."

        if msg:
            self.transient_notify(msg)
            self.needs_redraw = False

        self.player.silly_count = (self.player.silly_count + 1) % 4

    def normalize_item_name(self, target: str) -> str:
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
            self.transient_notify("Go where?", self.config.quick_sleep)
            self.needs_redraw = False
            return

        if len(args) >= 3 and args[:3] == ["back", "up", "ahead"]:
            raw_dir = "back up ahead"
        elif len(args) >= 2 and args[:2] == ["up", "ahead"]:
            raw_dir = "up ahead"
        elif len(args) >= 2 and args[:2] == ["back", "down"]:
            raw_dir = "back down"
        else:
            raw_dir = " ".join(args)

        has_compass = self.player.has_item("compass")

        abbrev_map = {
            "n": "north", "s": "south", "e": "east", "w": "west",
            "u": "up", "d": "down", "l": "left", "r": "right"
        }
        display_dir = abbrev_map.get(raw_dir, raw_dir)

        cardinals = ["north", "south", "east", "west"]
        relatives = ["up", "down", "left", "right", "up ahead", "back down", "back up ahead"]

        width = self.config.ui_width

        if not has_compass and display_dir in cardinals:
            self.transient_notify(f"You have no idea which way {display_dir} is!", self.config.medium_sleep)
            self.needs_redraw = False
            return

        if has_compass and display_dir in relatives:
            self.transient_notify("You have a high-tech digital compass now! You should use cardinal directions.", self.config.long_sleep)
            self.needs_redraw = False
            return

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
            
            if room.name == "entryway" and internal_dir in ["east", "west"]:
                if not (self.player.has_item("compass") and self.player.has_item("map")):
                    self.transient_notify("I shouldnt go any farther until I figure out where I am.", self.config.slow_sleep)
                    self.needs_redraw = False
                    return

            if internal_dir in room.locked_paths and internal_dir not in room.unlocked_paths:
                if internal_dir not in room.discovered_locks:
                    room.discovered_locks.append(internal_dir)
                
                base_msg = room.locked_paths[internal_dir]["msg"]
                wrapped_msg = self.wrap_text(base_msg, width)
                
                centered_lines = []
                for line in wrapped_msg.split('\n'):
                    centered_lines.append(line.center(width))
                colored_msg = f"{self.config.red}{chr(10).join(centered_lines)}{self.config.reset}"

                sys.stdout.write("\n")
                self.typewriter(colored_msg, speed=0.03)
                print() 
                
                sleep(1.0)
                self.needs_redraw = True 

            else:
                self.transient_notify(f"You decide to go {display_dir}...", self.config.medium_sleep)
                self.player.current_room = room.exits[internal_dir]
                self.player.silly_count = 0
                self.needs_redraw = True

        else:
            self.handle_silly_response(raw_dir, action="go")

    def handle_get(self, args: List[str]) -> None:
        if not args:
            self.transient_notify("Get what?", self.config.quick_sleep)
            self.needs_redraw = False
            return

        raw_target = " ".join(args)
        target = self.normalize_item_name(raw_target)
        room = self.rooms[self.player.current_room]

        if room.item and target == room.item.name:
            self.transient_notify(f"{target.upper()} retrieved!", self.config.medium_sleep)
            self.player.inventory.append(room.item)
            self.player.items_collected += 1
            room.item = None
            self.player.silly_count = 0
            self.needs_redraw = True
        else:
            self.handle_silly_response(raw_target, action="get")

    def handle_use(self, args: List[str]) -> None:
        if not args:
            self.transient_notify("Use what?", self.config.quick_sleep)
            self.needs_redraw = False
            return

        raw_target = " ".join(args)
        target = self.normalize_item_name(raw_target)
        room = self.rooms[self.player.current_room]

        if not self.player.has_item(target):
            self.transient_notify(f"You don't have a {raw_target} in your inventory!", self.config.medium_sleep)
            self.needs_redraw = False
            return

        if target == "map":
            self.clear()
            print("\n")
            self.draw_map()
            
            print()
            
            self.show_pulsing_exit("P R E S S  < E N T E R >  T O  C L O S E", color_mode="white")
            self.needs_redraw = True
            return

        used_successfully = False
        width = self.config.ui_width

        for direction, lock_info in room.locked_paths.items():
            if lock_info["req_item"] == target and direction not in room.unlocked_paths:
                
                base_msg = lock_info["success_msg"]
                wrapped_msg = self.wrap_text(base_msg, width)
                
                centered_lines = []
                for line in wrapped_msg.split('\n'):
                    centered_lines.append(line.center(width))
                colored_msg = f"{self.config.green}{chr(10).join(centered_lines)}{self.config.reset}"

                sys.stdout.write("\n")
                self.typewriter(colored_msg, speed=0.03)
                print() 
                
                room.unlocked_paths.append(direction)
                used_successfully = True

                sleep(1.0)
                self.needs_redraw = True
                break

        if not used_successfully:
            self.transient_notify(f"You can't use the {raw_target} here.", self.config.medium_sleep)
            self.needs_redraw = False

    def handle_help(self, args: List[str]) -> None:
        self.help_menu()
        self.display_timer = True
        self.needs_redraw = True

    def handle_exit(self, args: List[str], force_yes: bool = False) -> None:
        self.display_timer = False

        if force_yes:
            confirm = "y"
        else:
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
                    print(f"{self.config.red}Please enter 'Y' or 'N'{self.config.reset}")
                    sleep(self.config.medium_sleep)
                    
                    with self.io_lock:
                        sys.stdout.write("\033[2A\033[J")
                        sys.stdout.flush()

        if confirm == "y":
            self.show_dimmed_status()

            width = self.config.ui_width
            msg = "You succumb to the fear and desperation and end your journey suddenly..."

            print("\n\n")

            self.fade_in_text(msg, color_mode="red")

            print("\n\n")

            self.show_pulsing_exit("P R E S S  < E N T E R >", color_mode="white")

            self.current_run = None
            
            self.is_running = False
            return
            
        else:
            width = self.config.ui_width
            base_msg = "You decide ending it all just isn't worth it and continue on."
            wrapped_msg = self.wrap_text(base_msg, width)
            colored_msg = self.format_text_colors(wrapped_msg)
            
            print(f"\n{colored_msg}")
            sleep(self.config.medium_sleep)
            self.display_timer = True
            
            self.needs_redraw = True

    def parse_input(self) -> None:
        if getattr(self, "prompt_needs_full_draw", True):
            prompt_text = f"\n{self.config.yellow}What do you do!?{self.config.reset}\n> "
            self.prompt_needs_full_draw = False
        else:
            prompt_text = "> "

        self.flush_input()
        self.set_console_echo(True)
        
        self.waiting_for_input = True
        try:
            raw_input = input(prompt_text).strip().lower()
        finally:
            self.waiting_for_input = False
            self.set_console_echo(False)

        words = [word for word in raw_input.split() if word not in self.config.stop_words]

        if not words:
            self.help_menu()
            self.display_timer = True
            self.needs_redraw = True
            return

        command = words[0]
        args = words[1:]

        handler = self.command_handlers.get(command)
        if handler:
            handler(args)
        else:
            self.handle_silly_response(" ".join(args), command)


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
                
                if getattr(self, "needs_redraw", True):
                    self.show_status()
                    self.needs_redraw = False

                if not self.is_running:
                    self.display_timer = False
                    break

                self.player.previous_room = self.player.current_room
                self.parse_input()

            self.clear()
            print("\n\n")

            leaderboard = self.load_leaderboard()
            current_run = getattr(self, "current_run", None)
            self.display_leaderboard(leaderboard, current_run=current_run)

            print("\n")
            sleep(1.0)
            
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
        pass
    finally:
        if WINDOWS:
            os.system("cls")
        else:
            os.system("clear")