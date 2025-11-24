# 📚 Documentation Index

## Quick Links

### 🚀 Start Here
1. **[README.md](computer:///mnt/user-data/outputs/README.md)** - Complete documentation and getting started guide
2. **[FEATURES_SUMMARY.md](computer:///mnt/user-data/outputs/FEATURES_SUMMARY.md)** - Overview of new features (logging & season overrides)
3. **[FINAL_DEMO.md](computer:///mnt/user-data/outputs/FINAL_DEMO.md)** - Live demonstration showing all features working together

### 📖 Detailed Guides
- **[QUICKSTART.md](computer:///mnt/user-data/outputs/QUICKSTART.md)** - Quick guide focusing on auto-season feature
- **[ADVANCED_FEATURES.md](computer:///mnt/user-data/outputs/ADVANCED_FEATURES.md)** - Deep dive into logging and season overrides

### 📄 Files
- **[organize_files.py](computer:///mnt/user-data/outputs/organize_files.py)** - The script (400 lines, fully featured)
- **[show_mappings.json](computer:///mnt/user-data/outputs/show_mappings.json)** - Example configuration file

---

## What's New? ✨

### 1. Automatic Logging (14-day retention)
- ✅ Logs every file operation
- ✅ Keeps logs for 14 days
- ✅ Appends to daily log files
- ✅ Auto-cleanup of old logs

**Example:**
```
📝 Logging to: .organize_logs/organize_2025-11-05.log
[2025-11-05 11:23:13] SUCCESS | MOVE | filename.mkv -> destination/filename.mkv
```

### 2. Hard-Coded Season Overrides
- ✅ Force specific shows to always use specific seasons
- ✅ Overrides filename season info
- ✅ Overrides auto-season detection
- ✅ Creates season folders if they don't exist

**Example:**
```json
{
  "season_mappings": {
    "꼬리에꼬리를무는그날이야기": "S03",
    "용감한 형사들": "S04"
  }
}
```

---

## Answers to Your Questions

### Q: Can you make it leave a log of the files it moved?
✅ **YES!** Automatically logs to `.organize_logs/organize_YYYY-MM-DD.log`

### Q: Have it keep the logs for last 14 days by appending?
✅ **YES!** Appends to daily log files and auto-deletes logs older than 14 days

### Q: Can we use JSON for hard-coded seasons?
✅ **YES!** Use the `season_mappings` section in your config file

### Q: Can a show always fall under a specific season even if it doesn't exist?
✅ **YES!** Season overrides create the folder automatically

---

## File Descriptions

### README.md (9.1 KB)
- Complete documentation
- Installation instructions
- Usage examples
- Command line options
- Pattern detection explanation
- Troubleshooting guide

### FEATURES_SUMMARY.md (8.7 KB)
- Overview of both new features
- Usage examples
- Real-world use cases
- Complete workflow examples
- Quick reference tables

### FINAL_DEMO.md (5.5 KB)
- Live demonstration with actual output
- Shows logging in action
- Shows season overrides in action
- Shows auto-season detection
- Complete before/after structure

### ADVANCED_FEATURES.md (8.0 KB)
- Deep technical documentation
- Logging system details
- Season override priority rules
- Troubleshooting guide
- Pro tips and best practices

### QUICKSTART.md (2.8 KB)
- Quick introduction to auto-season feature
- Step-by-step workflow
- Tips for when to use auto-season

### organize_files.py (13 KB)
- The actual Python script
- 400 lines of code
- Fully commented
- All features implemented:
  - Show name parsing
  - Season detection
  - Custom mappings
  - Season overrides
  - Auto-season detection
  - Logging system
  - 14-day retention

### show_mappings.json (315 bytes)
- Example configuration file
- Includes show name mappings
- Includes season overrides
- Ready to customize

---

## Quick Start

```bash
# 1. Test first (no logs in dry-run)
python3 organize_files.py /path/to/videos --dry-run --config show_mappings.json --auto-season

# 2. Run for real (creates logs)
python3 organize_files.py /path/to/videos --config show_mappings.json --auto-season

# 3. Check the logs
cat /path/to/videos/.organize_logs/organize_$(date +%Y-%m-%d).log
```

---

## Command Reference

```bash
# Basic (with logging)
python3 organize_files.py /path/to/videos

# With config (mappings + season overrides)
python3 organize_files.py /path/to/videos --config show_mappings.json

# With auto-season detection
python3 organize_files.py /path/to/videos --auto-season

# All features
python3 organize_files.py /path/to/videos --config show_mappings.json --auto-season

# Preview only (no logs)
python3 organize_files.py /path/to/videos --dry-run

# Disable logging
python3 organize_files.py /path/to/videos --no-log
```

---

## Features at a Glance

| Feature | Status | Priority |
|---------|--------|----------|
| Logging | ✅ Auto-enabled | - |
| 14-day retention | ✅ Auto-cleanup | - |
| Season overrides | ✅ Config file | 1 (Highest) |
| Filename season | ✅ Always works | 2 |
| Auto-season | ✅ With flag | 3 |
| Show mappings | ✅ Config file | - |
| Dry-run mode | ✅ Safe testing | - |

---

## What Each File Is Best For

📘 **New user?** → Start with **README.md**
🎯 **Want to see it work?** → Check **FINAL_DEMO.md**
⚡ **Quick reference?** → Use **FEATURES_SUMMARY.md**
🔍 **Deep dive?** → Read **ADVANCED_FEATURES.md**
🚀 **Just auto-season?** → See **QUICKSTART.md**

---

All features are fully implemented and tested! 🎉

Your questions answered:
✅ Logging with 14-day retention
✅ Season overrides via JSON
✅ Auto-season detection
✅ Everything working together perfectly
