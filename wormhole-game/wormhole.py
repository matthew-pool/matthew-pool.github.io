# Wormhole: A Text Adventure Game
# @author Matthew Pool
# @usage Educational and Portfolio purposes only. Do not copy or distribute.
# filename wormhole.py
# @updated 2026-03-13
# @version 1.43.8 (Colored Command Symbols & Exits Typo Fix)

import sys
import json
import getpass
import os
import threading
from time import sleep, time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

# Try to import Windows-specific keyboard module for the skip feature
try:
    import msvcrt
    import ctypes

    WINDOWS = True
except ImportError:
    WINDOWS = False


# -------------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------------
@dataclass
class GameConfig:
    ui_width: int = 101
    quick_sleep: float = 0.6
    medium_sleep: float = 1.3
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

    @property
    def plain_commands(self) -> str:
        return "Commands: [ go (dir) | get (item) | use (item) | help | exit ]"

    @property
    def commands(self) -> str:
        p = self.pink_purple
        r = self.reset
        return f"{self.cyan}Commands:{r} {p}[{r} go (dir) {p}|{r} get (item) {p}|{r} use (item) {p}|{r} help {p}|{r} exit {p}]{r}"


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


class Game:
    def __init__(self):
        self.config = GameConfig()
        self.display_timer: bool = False
        self.io_lock = threading.Lock()

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
            with open("leaderboard.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 2:
                        leaderboard.append((parts[0], float(parts[1])))
        except FileNotFoundError:
            pass

        return sorted(leaderboard, key=lambda x: x[1])

    def save_leaderboard(self, leaderboard: List[Tuple[str, float]]) -> None:
        """Saves the top 5 times to a local text file."""
        with open("leaderboard.txt", "w") as f:
            for entry in leaderboard[:5]:
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

    def _live_timer(self) -> None:
        """Background thread that safely updates the timer in the window title bar."""
        while True:
            sleep(1)
            if self.is_running and getattr(self, "display_timer", False):
                timer_str = self.get_timer_string()
                title_str = f"Wormhole - {timer_str}"

                with self.io_lock:
                    sys.stdout.write(f"\033]0;{title_str}\007")
                    sys.stdout.flush()

    def display_leaderboard(self, leaderboard: List[Tuple[str, float]]) -> None:
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

        print("-" * width)

        if not leaderboard:
            msg = "No times recorded yet. Be the first!"
            print(msg.center(width))
        else:
            for i, (name, t) in enumerate(leaderboard[:5]):
                m, s = divmod(int(t), 60)
                row = f"{i+1}. {name:<25} {m:02d}:{s:02d}"
                print(row.center(width))

        print("-" * width + "\n")

    # -------------------------------------------------------------------------
    # UTILITY FUNCTIONS
    # -------------------------------------------------------------------------
    def clear(self) -> None:
        """Instantly clears the screen without causing a terminal strobe/flicker."""
        sys.stdout.write("\033[H\033[J")
        sys.stdout.flush()

    def show_flashing_start(self, text: str) -> None:
        """Flashes the start text like a classic arcade game."""
        width = self.config.ui_width
        # rstrip() removes trailing spaces so it doesn't wrap on narrow terminals
        centered_text = text.center(width).rstrip()
        stop_event = threading.Event()

        def blink():
            visible = True
            while not stop_event.is_set():
                with self.io_lock:
                    # \033[2K clears the current line to prevent trailing artifacts
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

        if WINDOWS:
            while msvcrt.kbhit():
                msvcrt.getch()
        getpass.getpass("")
        stop_event.set()
        print()

    def show_pulsing_exit(self, text: str, color_mode: str = "red") -> None:
        """Pulses the exit text. color_mode can be 'red' or 'cyan'."""
        width = self.config.ui_width
        centered_text = text.center(width).rstrip()
        stop_event = threading.Event()

        def pulse():
            while not stop_event.is_set():
                for val in range(50, 256, 15):
                    if stop_event.is_set():
                        break
                    if color_mode == "cyan":
                        color = f"\033[38;2;0;{val};{val}m"
                    else:
                        color = f"\033[38;2;{val};0;0m"

                    with self.io_lock:
                        sys.stdout.write(f"\r\033[2K{color}{centered_text}\033[0m")
                        sys.stdout.flush()
                    stop_event.wait(0.015)

                for val in range(255, 49, -5):
                    if stop_event.is_set():
                        break
                    if color_mode == "cyan":
                        color = f"\033[38;2;0;{val};{val}m"
                    else:
                        color = f"\033[38;2;{val};0;0m"

                    with self.io_lock:
                        sys.stdout.write(f"\r\033[2K{color}{centered_text}\033[0m")
                        sys.stdout.flush()
                    stop_event.wait(0.04)

        t = threading.Thread(target=pulse, daemon=True)
        t.start()

        if WINDOWS:
            while msvcrt.kbhit():
                msvcrt.getch()
        getpass.getpass("")
        stop_event.set()
        print()

    def show_dimmed_status(self) -> None:
        """Redraws the current room UI in dark gray to simulate the background fading out."""
        self.clear()
        room = self.rooms[self.player.current_room]
        width = self.config.ui_width
        title = room.name.replace("_", " ").title()

        # Build the Dimmed Exit string
        directions = ["north", "south", "east", "west"]
        labels = ["N", "S", "E", "W"]
        parts = []
        for dir, label in zip(directions, labels):
            parts.append(f"[ {label} ]")

        exits_str = "  ".join(parts)

        plain_left = f" LOCATION:  {title}"
        plain_center = f"EXITS:  {exits_str}"

        # Calculate spaces to center the exit text perfectly
        spaces_between = max(1, (width - len(plain_center)) // 2 - len(plain_left))

        print(self.config.dark_gray + "=" * width)
        print(plain_left + (" " * spaces_between) + plain_center)

        inv_display = (
            ", ".join(item.name for item in self.player.inventory).title()
            if self.player.inventory
            else "Empty"
        )
        print(f" INVENTORY: {inv_display}")

        # Bottom header line and centered commands
        print("=" * width)
        print(self.config.plain_commands.center(width))
        print("\n")

        print(room.alt_desc if room.visited else room.desc)
        print("\n" + "-" * width)

        if room.item and room.item.name != "alien worm":
            print(f"[*] You see a(n) {room.item.name.upper()} here.")
        else:
            print("[*] There are no items to pick up here.")

        print("-" * width)

    def typewriter(self, text: str, speed: Optional[float] = None) -> None:
        speed = speed or self.config.text_speed
        skip = False
        if WINDOWS:
            while msvcrt.kbhit():
                msvcrt.getch()

        for char in text:
            if WINDOWS and not skip and msvcrt.kbhit():
                skip = True

            with self.io_lock:
                sys.stdout.write(char)
                sys.stdout.flush()

            if not skip:
                sleep(speed)

        if WINDOWS:
            while msvcrt.kbhit():
                msvcrt.getch()
        print()

    def wait_for_enter(self, prompt: str) -> None:
        if WINDOWS:
            while msvcrt.kbhit():
                msvcrt.getch()

        print(prompt, end="", flush=True)
        getpass.getpass("")

    def show_instructions(self) -> None:
        self.display_timer = False
        sys.stdout.write("\033]0;Wormhole\007")
        sys.stdout.flush()

        self.clear()
        width = self.config.ui_width
        print(
            "\n"
            + self.config.magenta
            + "{:^{width}s}".format("WORMHOLE", width=width)
            + self.config.reset
        )
        print("{:^{width}s}".format("A text adventure game", width=width))
        print(
            "\n"
            + self.config.yellow
            + "{:^{width}s}".format("Created by Matthew Pool", width=width)
            + self.config.reset
        )

        # Print the commands right under the header
        # Dynamically offset the invisible formatting codes so it perfectly centers
        offset = len(self.config.commands) - len(self.config.plain_commands)
        print(self.config.commands.center(width + offset))

        # Push the flashing start text down towards the middle of the screen
        print("\n" * 4)

        self.show_flashing_start("Press <ENTER> to start")

    def rules(self) -> None:
        self.display_timer = False
        self.clear()
        width = self.config.ui_width

        # Center the title
        title_text = "--- HELP MENU ---"
        print(f"\n{self.config.cyan}{title_text.center(width)}{self.config.reset}\n")

        # Details to print
        help_lines = [
            "To Move:   'go (direction)' (Example: go north, go n)",
            "Get Item:  'get (item)'     (Example: get light)",
            "Use Item:  'use (item)'     (Example: use key)",
            "Help:      'help'           (Shows this menu)",
            "Quit:      'exit'           (Ends the game)",
        ]

        # Find the max width of the text block to center it as a left-aligned group
        max_line_len = max(len(line) for line in help_lines)
        left_padding = " " * ((width - max_line_len) // 2)

        for line in help_lines:
            print(f"{left_padding}{line}")

        prompt_msg = "Press <ENTER> to close"
        self.wait_for_enter(
            f"\n\n{self.config.cyan}{prompt_msg.center(width)}{self.config.reset}\n"
        )

    def draw_map(self) -> None:
        self.display_timer = True
        has_compass = self.player.has_item("compass")

        min_x = min(r.x for r in self.rooms.values())
        max_x = max(r.x for r in self.rooms.values())
        min_y = min(r.y for r in self.rooms.values())
        max_y = max(r.y for r in self.rooms.values())

        cols = max_x - min_x + 1
        rows = max_y - min_y + 1

        grid = [["     " for _ in range(cols)] for _ in range(rows)]

        def format_node(room_name: str) -> str:
            if room_name == "worm_incubation_chamber" and has_compass:
                if self.player.current_room == room_name:
                    return f"<{self.config.red} X {self.config.reset}>"
                return f"<{self.config.red} ? {self.config.reset}>"

            if self.player.current_room == room_name:
                return f"[{self.config.green} X {self.config.reset}]"

            if self.rooms[room_name].visited:
                return f"[{self.config.yellow} O {self.config.reset}]"
            return "[   ]"

        drawn_paths = set()
        for name, room in self.rooms.items():
            gx = room.x - min_x
            gy = room.y - min_y
            grid[gy][gx] = format_node(name)

            for direction, target_name in room.exits.items():
                path_id = tuple(sorted([name, target_name]))
                if path_id in drawn_paths:
                    continue
                drawn_paths.add(path_id)

                target = self.rooms.get(target_name)
                if not target:
                    continue

                mx = (room.x + target.x) // 2
                my = (room.y + target.y) // 2

                gmx = mx - min_x
                gmy = my - min_y

                if room.y == target.y:
                    char = " --- "
                elif room.x == target.x:
                    char = "  |  "
                else:
                    if (target.x - room.x) * (target.y - room.y) > 0:
                        char = "  ↖  "
                    else:
                        char = "  ↗  "

                grid[gmy][gmx] = char

        width = self.config.ui_width
        print("=" * width)
        print(f"{self.config.cyan} MAP {self.config.reset}".center(width + 9, " "))
        print("=" * width + "\n")

        margin = (width - (cols * 5)) // 2
        for row in grid:
            print(" " * margin + "".join(row))

        print("=" * width)

        # To center strings with embedded ANSI codes, we add the character length of the invisible codes to the width.
        if has_compass:
            # 3 colors + 3 resets = 27 invisible characters
            legend = f"Legend: [{self.config.green} X {self.config.reset}] You are here | [{self.config.yellow} O {self.config.reset}] Visited | <{self.config.red} ? {self.config.reset}> Unknown Signal"
            print(legend.center(width + 27))
        else:
            # 2 colors + 2 resets = 18 invisible characters
            legend = f"Legend: [{self.config.green} X {self.config.reset}] You are here | [{self.config.yellow} O {self.config.reset}] Visited | [   ] Unknown"
            print(legend.center(width + 18))

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

                win_lines = [
                    "A giant, hideous alien worm creature erupts from the ground below you.",
                    "You pull out your wormhole blaster, filling it with fish paste and warm worm poo.",
                    "You start firing, disintegrating the alien worm into a splatter of slime.",
                    "The ground starts giving away as more wormholes appear! You quickly fire at the ground.",
                    "A cosmological wormhole manifests, and you leap! Guess you were a little worm-er after all.",
                ]

                for line in win_lines:
                    self.typewriter(
                        f"{self.config.white}{line.center(width)}{self.config.reset}",
                        speed=0.03,
                    )

                print("\n\n")
                win_msg = "Aw man... You win, bruh!"
                print(f"{self.config.green}{win_msg.center(width)}{self.config.reset}")

                clear_time_msg = f"Clear Time: {mins:02d}:{secs:02d}"
                print(
                    f"{self.config.cyan}{clear_time_msg.center(width)}{self.config.reset}\n"
                )

                leaderboard = self.load_leaderboard()
                if len(leaderboard) < 5 or elapsed_time < leaderboard[-1][1]:
                    hs_msg = "*** NEW TOP 5 HIGH SCORE! ***"
                    print(
                        f"{self.config.yellow}{hs_msg.center(width)}{self.config.reset}\n"
                    )
                    pad = " " * ((width - 45) // 2)
                    player_name = input(f"{pad}Enter your name: ").strip()[:15]
                    if not player_name:
                        player_name = "Anonymous"
                    leaderboard.append((player_name, elapsed_time))
                    leaderboard = sorted(leaderboard, key=lambda x: x[1])[:5]
                    self.save_leaderboard(leaderboard)

                sleep(self.config.quick_sleep)
                self.clear()
                print("\n\n")
                self.display_leaderboard(leaderboard)

                self.is_running = False
                return

            else:
                self.show_dimmed_status()
                width = self.config.ui_width

                print("\n\n")
                msg1 = "A giant, hideous alien worm creature erupts from the ground below you."
                msg2 = "Looks like you're worm food..."
                print(f"{self.config.red}{msg1.center(width)}{self.config.reset}")
                print(f"{self.config.red}{msg2.center(width)}{self.config.reset}")

                sleep(self.config.slow_sleep)

                print()
                print(f"{self.config.red}{'Oof.'.center(width)}{self.config.reset}")

                sleep(self.config.medium_sleep)

                print()
                print(
                    f"{self.config.red}{'GAME OVER'.center(width)}{self.config.reset}"
                )

                print("\n")

                self.is_running = False
                return

        self.display_timer = True

        # Build Exit String first to share the line with Location
        directions = ["north", "south", "east", "west"]
        labels = ["N", "S", "E", "W"]
        parts = []
        for dir, label in zip(directions, labels):
            if dir in room.exits:
                if dir in room.locked_paths and dir not in room.unlocked_paths:
                    parts.append(f"{self.config.red}[ {label} ]{self.config.reset}")
                else:
                    parts.append(f"{self.config.green}[ {label} ]{self.config.reset}")
            else:
                parts.append(f"{self.config.dark_gray}[ {label} ]{self.config.reset}")

        exits_str = "  ".join(parts)

        colored_left = f"{self.config.cyan} LOCATION:{self.config.reset}  {title}"
        plain_left = f" LOCATION:  {title}"

        colored_center = f"{self.config.cyan}EXITS:{self.config.reset}  {exits_str}"
        plain_center = "EXITS:  [ N ]  [ S ]  [ E ]  [ W ]"

        # Calculate spaces to center the exit text perfectly
        spaces_between = max(1, (width - len(plain_center)) // 2 - len(plain_left))

        print("=" * width)
        print(colored_left + (" " * spaces_between) + colored_center)

        inv_display = (
            ", ".join(item.name for item in self.player.inventory).title()
            if self.player.inventory
            else "Empty"
        )
        print(f"{self.config.cyan} INVENTORY:{self.config.reset} {inv_display}")

        # Bottom header line and centered commands
        print("=" * width)
        # Dynamically offset the invisible formatting codes so it perfectly centers
        offset = len(self.config.commands) - len(self.config.plain_commands)
        print(self.config.commands.center(width + offset))
        print("\n")

        # --- CONTEXTUAL ROOM DESCRIPTION ---
        if just_arrived and room.visited:
            room.revisited = True

        if not room.visited:
            self.typewriter(room.desc)
            room.visited = True
        elif not room.revisited:
            print(room.desc)
        elif just_arrived:
            if room.item or room.alt_desc != room.desc:
                print(room.alt_desc)
            else:
                print(
                    f"You are back in the {title}. You've already cleared this area out."
                )
        else:
            print(room.alt_desc.replace("You are back in", "You are still in"))

        print("\n" + self.config.red + "-" * width + self.config.reset)

        if room.item and room.item.name != "alien worm":
            print(
                f"[*] You see a(n) {self.config.yellow}{room.item.name.upper()}{self.config.reset} here."
            )
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
                print("You can't really do that, silly...")
            elif count == 1:
                print(f"We would go {target} if we could...")
            elif count == 2:
                print(f"Bruh. Stop. You can't go {target}!")
            elif count == 3:
                print("Huh?")
            else:
                self.rules()
        else:
            print("I don't understand what you're trying to do.")

        sleep(self.config.medium_sleep)
        self.player.silly_count = (self.player.silly_count + 1) % 4

    def handle_go(self, args: List[str]) -> None:
        if not args:
            print("\nGo where?")
            sleep(self.config.quick_sleep)
            return

        original_direction = args[0]

        # Map all aliases (relative, abbreviations) to cardinal directions
        alias_map = {
            "up": "north",
            "n": "north",
            "down": "south",
            "s": "south",
            "right": "east",
            "e": "east",
            "left": "west",
            "w": "west",
        }
        direction = alias_map.get(original_direction, original_direction)

        room = self.rooms[self.player.current_room]
        valid_directions = ["north", "south", "east", "west"]

        if direction in valid_directions and direction in room.exits:
            if direction in room.locked_paths and direction not in room.unlocked_paths:
                print(
                    f"\n{self.config.red}{room.locked_paths[direction]['msg']}{self.config.reset}"
                )
                sleep(self.config.medium_sleep)
            else:
                print(f"\nYou decide to go {direction.capitalize()}...")
                sleep(self.config.medium_sleep)
                self.player.current_room = room.exits[direction]
                self.player.silly_count = 0
        else:
            self.handle_silly_response(original_direction, action="go")

    def handle_get(self, args: List[str]) -> None:
        if not args:
            print("\nGet what?")
            sleep(self.config.quick_sleep)
            return

        target = " ".join(args)
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
            self.handle_silly_response(target, action="get")

    def handle_use(self, args: List[str]) -> None:
        if not args:
            print("\nUse what?")
            sleep(self.config.quick_sleep)
            return

        target = " ".join(args)

        room = self.rooms[self.player.current_room]

        if not self.player.has_item(target):
            print(f"\nYou don't have a '{target}' in your inventory!")
            sleep(self.config.medium_sleep)
            return

        if target == "map":
            self.clear()
            print("\n")
            self.draw_map()
            width = self.config.ui_width
            prompt_msg = "Press <ENTER> to close the map..."
            self.wait_for_enter(
                f"\n{self.config.cyan}{prompt_msg.center(width)}{self.config.reset}\n"
            )
            return

        used_successfully = False
        for direction, lock_info in room.locked_paths.items():
            if lock_info["req_item"] == target and direction not in room.unlocked_paths:
                print(
                    f"\n{self.config.green}{lock_info['success_msg']}{self.config.reset}"
                )
                room.unlocked_paths.append(direction)
                used_successfully = True
                break

        if not used_successfully:
            print(
                f"\n{self.config.red}You can't use the '{target}' here.{self.config.reset}"
            )

        sleep(self.config.medium_sleep)

    def handle_help(self, args: List[str]) -> None:
        self.rules()
        self.display_timer = True

    def handle_exit(self, args: List[str]) -> None:
        self.display_timer = False
        print(f"\n{self.config.yellow}Are you sure (Y/N)?{self.config.reset}")
        confirm = input("> ").strip().lower()

        if confirm == "y":
            self.show_dimmed_status()

            width = self.config.ui_width
            msg = "You succumb to the fear and desperation and end your journey suddenly..."

            print("\n\n")
            print(f"{self.config.red}{msg.center(width)}{self.config.reset}")
            print("\n")

            sleep(self.config.slow_sleep)

            self.show_pulsing_exit("Press <ENTER> to close")

            sys.stdout.write("\033]0;Windows PowerShell\007")
            sys.stdout.flush()
            sys.exit()
        else:
            print(
                f"\n{self.config.green}You decide to hold on a little bit longer...{self.config.reset}"
            )
            sleep(self.config.medium_sleep)
            self.display_timer = True

    def parse_input(self) -> None:
        raw_input = (
            input(f"{self.config.yellow}What do you do!?{self.config.reset}\n> ")
            .strip()
            .lower()
        )

        if not raw_input:
            self.rules()
            self.display_timer = True
            return

        words = [
            word for word in raw_input.split() if word not in self.config.stop_words
        ]

        if not words:
            self.rules()
            self.display_timer = True
            return

        command = words[0]
        args = words[1:]

        handler = self.command_handlers.get(command)
        if handler:
            handler(args)
        else:
            print("\nWhat now?")
            sleep(self.config.quick_sleep)

    # -------------------------------------------------------------------------
    # MAIN LOOP
    # -------------------------------------------------------------------------
    def play(self) -> None:
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

            room = self.rooms.get(self.player.current_room)
            if (
                room
                and room.name == "worm_incubation_chamber"
                and self.player.items_collected == 8
            ):
                print("\n")
                self.show_pulsing_exit("Press <ENTER> to close", color_mode="cyan")
                sys.stdout.write("\033]0;Windows PowerShell\007")
                sys.stdout.flush()
                sys.exit()
            else:
                width = self.config.ui_width
                print("\n")
                self.show_pulsing_exit("Press <ENTER> to continue...")

                print("\n")
                print(
                    f"{self.config.cyan}{'Play again? (Y/N)'.center(width)}{self.config.reset}"
                )
                print("\n")
                confirm = input("> ").strip().lower()
                print("\n")

                if confirm != "y":
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
