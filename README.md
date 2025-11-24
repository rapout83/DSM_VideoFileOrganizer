# Video File Organizer

A Python script to automatically organize video files into folders based on their filenames. Perfect for organizing Korean drama/show collections!

## Features

- 📁 Automatically creates folders based on show names
- 📂 Creates season subfolders (S01, S02, etc.) when detected
- 🔍 Handles both Korean and English season indicators (시즌2 → S02)
- ✏️ Custom show name mappings for better organization
- 🎯 Hard-coded season mappings for specific shows
- 📝 Automatic logging of all operations (kept for 14 days)
- 🔒 Safe dry-run mode to preview changes before executing
- 🌏 Full Unicode/Korean text support

## Installation

No installation required! Just Python 3.6+ with standard library.

```bash
# Make the script executable (optional)
chmod +x organize_files.py
```

## Usage

### Basic Usage

Organize files in the current directory:
```bash
python3 organize_files.py
```

Organize files in a specific directory:
```bash
python3 organize_files.py /path/to/your/videos
```

### Dry Run Mode (Recommended First!)

See what the script will do WITHOUT actually moving files:
```bash
python3 organize_files.py /path/to/videos --dry-run
```

### Using Custom Mappings

If you want to customize how show names appear, use a config file:
```bash
python3 organize_files.py /path/to/videos --config show_mappings.json
```

### Auto-Season Detection (Smart!)

When you have files without season indicators, the script can automatically detect the correct season folder:

```bash
python3 organize_files.py /path/to/videos --auto-season
```

**How it works:**
- If a file has no season info (no S01, 시즌2, etc.)
- The script checks if the show folder already exists
- If it finds season subfolders:
  - **One season only** → Automatically uses that season
  - **Multiple seasons** → Uses the latest (highest) season number

**Example:**
```
Existing structure:
저스트 메이크업/
├── S01/
│   └── 저스트.메이크업.S01E01.mkv
└── S02/
    └── 저스트.메이크업.S02E01.mkv

New file: 저스트 메이크업.Just Makeup.E08.mkv

With --auto-season:
🔍 Auto-detected season: S02 (latest of S01, S02)
→ Places file in 저스트 메이크업/S02/
```

## Logging

The script automatically logs all file operations to help you track what was moved.

### Log Location
```
your_videos_folder/
└── .organize_logs/
    ├── organize_2025-11-05.log
    ├── organize_2025-11-04.log
    └── organize_2025-11-03.log
```

### Log Format
```
[2025-11-05 11:07:20] SUCCESS | MOVE | filename.mkv -> show_name/S01/filename.mkv
[2025-11-05 11:07:21] ERROR | MOVE | badfile.mkv -> destination | Error: Permission denied
```

### Log Features
- **Daily logs**: One log file per day (e.g., `organize_2025-11-05.log`)
- **Appending**: Multiple runs on the same day append to the same log
- **Auto-cleanup**: Logs older than 14 days are automatically deleted
- **Timestamped**: Each entry includes the exact time of operation
- **Success/Error tracking**: Clear indication of what worked and what failed

### Disable Logging
```bash
python3 organize_files.py /path/to/videos --no-log
```

**Note**: Logging is automatically disabled in dry-run mode.

## Custom Show Mappings

### Built-in Mappings

The script includes these default mappings:
- `비마이보이즈` → `비 마이 보이즈`

### Creating Your Own Config File

Create a JSON file (e.g., `show_mappings.json`):

```json
{
  "비마이보이즈": "비 마이 보이즈",
  "저스트 메이크업 Just Makeup": "저스트 메이크업",
  "더글로리": "더 글로리",
  "나의해방일지": "나의 해방 일지",
  "season_mappings": {
    "꼬리에꼬리를무는그날이야기": "S03",
    "용감한 형사들": "S04"
  }
}
```

**Show Name Mappings** (top level): Renames how folders are created
**Season Mappings** (in `season_mappings`): Forces specific shows to always use a certain season

### Hard-Coded Season Mappings

Sometimes you want a show to ALWAYS go to a specific season, regardless of:
- What's detected in the filename
- What season folders already exist
- What --auto-season would choose

**Use case example:**
```
File: 꼬리에꼬리를무는그날이야기.E05.251015.1080p.H264.mkv
Without season_mappings: Goes to main folder
With season_mappings: 🎯 Always goes to S03 folder
```

This is perfect for shows where:
- Episodes are numbered continuously across seasons
- You want to organize them into a specific season manually
- The filename doesn't include season information

Then use it:
```bash
python3 organize_files.py --config show_mappings.json
```

You can also edit the `CUSTOM_SHOW_MAPPINGS` and `SEASON_MAPPINGS` dictionaries directly in the script.

## How It Works

### File Name Parsing

The script extracts show names by looking for common patterns:

**Example 1: Simple episode**
```
Input:  괴물의 시간.E01.251101.1080p.H264-F1RST.mkv
Output: 괴물의 시간/
        └── 괴물의 시간.E01.251101.1080p.H264-F1RST.mkv
```

**Example 2: Korean season indicator**
```
Input:  리얼 연애실험실 독사과 시즌2.E01.251101.1080p.H264-F1RST.mkv
Output: 리얼 연애실험실 독사과/
        └── S02/
            └── 리얼 연애실험실 독사과 시즌2.E01.251101.1080p.H264-F1RST.mkv
```

**Example 3: Standard season format**
```
Input:  저스트.메이크업.S01E01.CPNG.WEB-DL.1080p.H.264.AAC2.0.mkv
Output: 저스트 메이크업/
        └── S01/
            └── 저스트.메이크업.S01E01.CPNG.WEB-DL.1080p.H.264.AAC2.0.mkv
```

### Pattern Detection

The script stops parsing the show name when it encounters:
- Episode markers: `E01`, `E02`, etc.
- Season markers: `S01E01`, `시즌2`, etc.
- Technical terms: `1080p`, `WEB-DL`, `H264`, etc.
- Korean episode indicators: `최종` (final), `첫회` (first episode)
- Date patterns: `YYMMDD` format

## Command Line Options

```
usage: organize_files.py [-h] [--dry-run] [--config CONFIG] [--auto-season] [--no-log] [directory]

positional arguments:
  directory        Directory containing files to organize (default: current directory)

optional arguments:
  -h, --help       Show this help message and exit
  --dry-run        Show what would be done without actually moving files
  --config CONFIG  Path to JSON config file with custom show name mappings and season mappings
  --auto-season    Automatically detect season folder for files without season info
  --no-log         Disable logging (logging is enabled by default)
```

## Examples

### Example 1: Preview Changes
```bash
python3 organize_files.py ~/Downloads/dramas --dry-run
```

Output:
```
============================================================
Video File Organizer
============================================================
🔍 DRY RUN MODE - No files will be moved
============================================================

Found 3 files to organize

📁 괴물의 시간.E01.251101.1080p.H264-F1RST.mkv
   → 괴물의 시간/
   [DRY RUN - no action taken]

📁 비마이보이즈.E02.250628.1080p.H264-F1RST.mkv
   → 비 마이 보이즈/
   [DRY RUN - no action taken]
```

### Example 2: Organize Files
```bash
python3 organize_files.py ~/Downloads/dramas
```

Output:
```
============================================================
Video File Organizer
============================================================

Found 3 files to organize

📁 괴물의 시간.E01.251101.1080p.H264-F1RST.mkv
   → 괴물의 시간/
   ✅ Moved successfully

📁 비마이보이즈.E02.250628.1080p.H264-F1RST.mkv
   → 비 마이 보이즈/
   ✅ Moved successfully
```

### Example 3: Auto-Season Detection
```bash
python3 organize_files.py ~/Downloads/dramas --config show_mappings.json --auto-season
```

Output:
```
============================================================
Video File Organizer
============================================================
🤖 AUTO-SEASON MODE - Will detect existing season folders
============================================================

Found 1 files to organize

🔍 Auto-detected season: S02 (latest of S01, S02)
📁 저스트 메이크업.Just Makeup.E08.mkv
   → 저스트 메이크업/S02/
   ✅ Moved successfully
```

## Safety Features

1. **Dry run mode**: Always test with `--dry-run` first
2. **Folder creation**: Creates folders only when needed
3. **Skip system files**: Ignores hidden files and the script itself
4. **Error handling**: Reports errors without stopping the entire process

## Troubleshooting

### Files not being organized?

Check if the filename contains recognizable patterns like episode numbers (E01, E02) or season indicators (S01, 시즌2).

### Wrong folder name?

Add a custom mapping in the config file or in the `CUSTOM_SHOW_MAPPINGS` dictionary.

### Want to undo changes?

The script moves files (not copies), so you can manually move them back. Consider using dry-run mode first!

## Tips

1. **Always use --dry-run first** to preview changes
2. **Backup important files** before running the script
3. **Use custom mappings** for shows with unusual names
4. **Run periodically** to keep your collection organized

## License

Free to use and modify as needed!
