#!/usr/bin/env python3
"""
Script to organize video files into folders based on filename patterns.
Uses watchdog's 'on_closed' event for reliable, finished-file detection.
"""

import re
import shutil
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from watchdog.observers import Observer

# We need to explicitly import FileClosedEvent and FileSystemEventHandler
from watchdog.events import FileSystemEventHandler, FileClosedEvent

# --- CONFIGURATION (Keep your core logic configuration) ---
CUSTOM_SHOW_MAPPINGS = {}
SEASON_OVERRIDES = {}

# --- CORE LOGIC FUNCTIONS (Keep as is, no changes needed for these helpers) ---


def setup_logging(log_dir):
    # ... (function body remains the same) ...
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    log_file = log_path / "organize.log"
    return log_file


def cleanup_old_logs(log_file, days=14):
    # ... (function body remains the same) ...
    if not log_file.exists():
        return

    cutoff_date = datetime.now() - timedelta(days=days)

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        kept_lines = []
        removed_count = 0

        for line in lines:
            try:
                if line.startswith("["):
                    timestamp_str = line[1:20]
                    entry_date = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

                    if entry_date >= cutoff_date:
                        kept_lines.append(line)
                    else:
                        removed_count += 1
                else:
                    kept_lines.append(line)
            except (ValueError, IndexError):
                kept_lines.append(line)

        if removed_count > 0:
            with open(log_file, "w", encoding="utf-8") as f:
                f.writelines(kept_lines)
            print(
                f"🗑️  Cleaned up {removed_count} old log entries (older than {days} days)"
            )

    except Exception as e:
        print(f"⚠️  Warning: Could not cleanup old logs: {e}")


def log_operation(log_file, operation, filename, destination, success=True, error=None):
    # ... (function body remains the same) ...
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "ERROR"

    log_entry = f"[{timestamp}] {status} | {operation} | {filename} -> {destination}"
    if error:
        log_entry += f" | Error: {error}"
    log_entry += "\n"

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"❌ Error writing to log file: {e}")


def extract_season_from_show_name(show_name, season_patterns):
    # ... (function body remains the same) ...
    if not season_patterns:
        return show_name, None

    for base_name, mode in season_patterns.items():
        if mode != "auto":
            continue

        if show_name.startswith(base_name):
            suffix = show_name[len(base_name) :].strip()

            if suffix.isdigit():
                season_num = int(suffix)
                season = f"S{season_num:02d}"
                return base_name, season

    return show_name, None


def normalize_show_name(show_name):
    # ... (function body remains the same) ...
    normalized = show_name.replace("-", " ")
    normalized = normalized.replace("–", " ")
    normalized = normalized.replace("—", " ")

    normalized = re.sub(r"\s+", " ", normalized).strip()

    return normalized


def load_custom_mappings(config_file):
    # ... (function body remains the same) ...
    config_path = Path(config_file)
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
    return {}


def extract_show_info(
    filename, custom_mappings=None, episode_markers=None, season_patterns=None
):
    # ... (function body remains the same) ...
    name = Path(filename).stem
    name = name.replace(".", " ")

    season_pattern = r"S(\d+)E?\d*"
    season_match = re.search(season_pattern, name, re.IGNORECASE)
    season = None

    if season_match:
        season = f"S{season_match.group(1).zfill(2)}"
        name = name[: season_match.start()].strip()

    korean_season_pattern = r"시즌\s*(\d+)"
    korean_season_match = re.search(korean_season_pattern, name)

    if korean_season_match:
        season = f"S{korean_season_match.group(1).zfill(2)}"
        name = name[: korean_season_match.start()].strip()

    korean_episode_pattern = r"(\d+)회"
    korean_episode_match = re.search(korean_episode_pattern, name)

    if korean_episode_match:
        name = name[: korean_episode_match.start()].strip()

    if episode_markers is None:
        episode_markers = ["최종", "첫회"]

    stop_patterns = [
        r"E\d+",
        r"\d+회",
        r"\d{6}",
        r"\d{4}p",
        r"WEB-DL",
        r"H\.?264",
        r"H\.?265",
        r"HEVC",
        r"AAC",
        r"CPNG",
        r"WAVVE",
        r"F1RST",
        r"[Xx]264",
        r"[Xx]265",
    ]

    for marker in episode_markers:
        stop_patterns.append(re.escape(marker))

    earliest_pos = len(name)
    for pattern in stop_patterns:
        match = re.search(pattern, name, re.IGNORECASE)
        if match:
            earliest_pos = min(earliest_pos, match.start())

    show_name = name[:earliest_pos].strip()
    show_name = show_name.rstrip(". ")
    show_name = re.sub(r"\s+", " ", show_name)
    show_name = normalize_show_name(show_name)

    if season_patterns and season is None:
        detected_show, detected_season = extract_season_from_show_name(
            show_name, season_patterns
        )
        if detected_season:
            show_name = detected_show
            season = detected_season

    if custom_mappings is None:
        custom_mappings = CUSTOM_SHOW_MAPPINGS

    if show_name in custom_mappings:
        show_name = custom_mappings[show_name]

    return show_name, season


def find_existing_season_folders(show_folder):
    # ... (function body remains the same) ...
    if not show_folder.exists():
        return []

    season_pattern = re.compile(r"^S(\d+)$", re.IGNORECASE)
    seasons = []

    for item in show_folder.iterdir():
        if item.is_dir():
            match = season_pattern.match(item.name)
            if match:
                seasons.append((int(match.group(1)), item.name))

    seasons.sort()
    return [name for _, name in seasons]


# --- SINGLE-FILE ORGANIZATION FUNCTION ---
def organize_single_file(file_path, source_dir, config_data, auto_season, log_file):
    """
    Core organization logic for a SINGLE file, called upon file close.
    """

    if not file_path.exists():
        return

    filename = file_path.name

    # Skip directories, hidden files, and the log directory
    if (
        file_path.is_dir()
        or filename.startswith(".")
        or filename == "organize_closed_event.py"
        or file_path.name == ".organize_logs"
    ):
        return

    # Configuration extraction
    custom_mappings = {
        k: v
        for k, v in config_data.items()
        if isinstance(v, str) and not k.startswith("_")
    }
    season_mappings = config_data.get("season_mappings", {})
    episode_markers = config_data.get("episode_markers", [])
    season_patterns = config_data.get("season_patterns", {})

    # Skip temporary files
    if filename.endswith((".tmp", ".part", ".crdownload")):
        print(f"🟡 Skipping temporary file: {filename}")
        return

    # Extract show information
    show_name, season = extract_show_info(
        filename, custom_mappings, episode_markers, season_patterns
    )

    print(f"✅ Processing: {filename}")

    if not show_name:
        print(f"⚠️  Could not extract show name from: {filename}")
        if log_file:
            log_operation(
                log_file,
                "SKIP",
                filename,
                "N/A",
                success=False,
                error="Could not extract show name",
            )
        return

    # Check for hard-coded season mapping
    if show_name in season_mappings:
        season = season_mappings[show_name]
    elif auto_season and season is None:
        show_folder = source_dir / show_name
        existing_seasons = find_existing_season_folders(show_folder)

        if existing_seasons:
            season = existing_seasons[-1]

    # Build destination path
    dest_relative_dir = Path(show_name) / season if season else Path(show_name)
    dest_dir = source_dir / dest_relative_dir
    dest_path = dest_dir / filename

    print(f"   Moving: {filename} → {dest_relative_dir}/")

    # Create destination directory if it doesn't exist
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Move the file
    try:
        shutil.move(str(file_path), str(dest_path))

        if log_file:
            dest_relative = dest_path.relative_to(source_dir)
            log_operation(log_file, "MOVE", filename, str(dest_relative), success=True)

    except Exception as e:
        print(f"   ❌ Error moving {filename}: {e}")
        if log_file:
            log_operation(
                log_file, "MOVE", filename, str(dest_dir), success=False, error=str(e)
            )


# --- WATCHDOG IMPLEMENTATION (The final, elegant version) ---
class FileEventHandler(FileSystemEventHandler):
    """Handles closed (downloads), moved (transfers), and created (fallback/copy) events."""

    def __init__(self, source_dir, config_file, auto_season, log_file):
        super().__init__()
        self.source_dir = Path(source_dir).resolve()
        self.log_file = log_file
        self.auto_season = auto_season
        self.config_data = load_custom_mappings(config_file) if config_file else {}

    def _is_relevant(self, event):
        """Helper to ensure we only process top-level files."""
        return (
            not event.is_directory
            and Path(event.src_path).parent.resolve() == self.source_dir
        )

    def on_closed(self, event):
        """Priority 1: File finished writing (best signal)."""
        if self._is_relevant(event):
            print(f"--> EVENT: CLOSED for {Path(event.src_path).name}")
            organize_single_file(
                Path(event.src_path),
                self.source_dir,
                self.config_data,
                self.auto_season,
                self.log_file,
            )

    def on_moved(self, event):
        """Priority 2: File moved into the directory (if supported)."""
        # on_moved uses dest_path for the final location
        file_path = Path(event.dest_path).resolve()
        if not event.is_directory and file_path.parent == self.source_dir:
            print(f"--> EVENT: MOVED for {file_path.name}")
            organize_single_file(
                file_path,
                self.source_dir,
                self.config_data,
                self.auto_season,
                self.log_file,
            )

    def on_created(self, event):
        """
        Priority 3: Fallback for move/copy operations that don't trigger on_moved/on_closed.
        Includes a 1-second delay to ensure on_closed runs first if it's a fast write.
        """
        if self._is_relevant(event):
            file_path = Path(event.src_path)
            print(
                f"--> EVENT: CREATED for {file_path.name} (Waiting 1s for potential CLOSE event)"
            )

            # CRITICAL DELAY: Allows a quick 'on_closed' event to move the file first.
            time.sleep(1)

            # The file may no longer exist if on_closed already moved it.
            if file_path.exists():
                organize_single_file(
                    file_path,
                    self.source_dir,
                    self.config_data,
                    self.auto_season,
                    self.log_file,
                )


def process_existing_files(source_dir, config_data, auto_season, log_file):
    """Processes any files that exist before the watcher started."""
    source_path = Path(source_dir).resolve()

    existing_files = [
        f for f in source_path.iterdir() if f.is_file() and not f.name.startswith(".")
    ]

    if existing_files:
        print(
            f"--- Initial Cleanup: Processing {len(existing_files)} existing file(s) ---"
        )
        for file_path in existing_files:
            organize_single_file(
                file_path, source_path, config_data, auto_season, log_file
            )
        print("Initial cleanup complete.")
    else:
        print("No existing files to clean up.")


def run_watcher(source_dir, config_file=None, auto_season=False, enable_logging=True):
    """Starts the watchdog observer."""

    source_path = Path(source_dir).resolve()

    if not source_path.exists():
        print(f"Error: Directory '{source_dir}' does not exist")
        return

    # Setup logging
    log_file = None
    if enable_logging:
        log_dir = source_path / ".organize_logs"
        log_file = setup_logging(log_dir)
        cleanup_old_logs(log_file, days=14)
        print(f"📝 Logging to: {log_file.relative_to(source_path)}")

    print(f"👀 Watching directory: {source_path}")
    print("--------------------------------------------------")

    # Load config before starting
    config_data = load_custom_mappings(config_file) if config_file else {}

    # Perform initial cleanup for files added before the script started
    process_existing_files(source_path, config_data, auto_season, log_file)

    # Start the watchdog observer
    event_handler = FileEventHandler(source_path, config_file, auto_season, log_file)
    observer = Observer()

    observer.schedule(event_handler, str(source_path), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping Watcher...")
        observer.stop()

    observer.join()
    print("Watcher stopped cleanly.")


def main():
    """Main function to start the file organizer watcher."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Real-time file organizer using watchdog's non-blocking file close event."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to watch for new files (default: current directory)",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to JSON config file with custom show name mappings",
    )
    parser.add_argument(
        "--auto-season",
        action="store_true",
        help="Automatically detect season folder for files without season info",
    )
    parser.add_argument(
        "--no-log",
        action="store_true",
        help="Disable logging (logging is enabled by default)",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Video File Organizer Watcher (File Closed Mode)")
    print("=" * 60)
    if args.auto_season:
        print("🤖 AUTO-SEASON MODE ENABLED")
        print("=" * 60)

    run_watcher(
        args.directory,
        config_file=args.config,
        auto_season=args.auto_season,
        enable_logging=not args.no_log,
    )


if __name__ == "__main__":
    main()
