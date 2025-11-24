# ✨ NEW FEATURES SUMMARY

## 📝 Feature 1: Automatic Logging (14-day retention)

### What It Does
- Automatically logs every file move operation
- Keeps logs for 14 days, then auto-deletes old ones
- Appends to the same daily log file for multiple runs

### Log Location
```
your-videos-folder/
└── .organize_logs/
    ├── organize_2025-11-05.log  ← Today's log
    ├── organize_2025-11-04.log
    └── organize_2025-11-03.log
```

### Log Format
```
[2025-11-05 11:20:25] SUCCESS | MOVE | filename.mkv -> destination/folder/filename.mkv
[2025-11-05 11:21:30] ERROR | MOVE | badfile.mkv -> destination/ | Error: Permission denied
```

### Usage
```bash
# Logging is automatic (enabled by default)
python3 organize_files.py /path/to/videos

# To disable logging
python3 organize_files.py /path/to/videos --no-log

# Note: Dry-run mode doesn't create logs
python3 organize_files.py /path/to/videos --dry-run
```

### Example Output
```bash
$ python3 organize_files.py /videos --config show_mappings.json

============================================================
Video File Organizer
============================================================

📝 Logging to: .organize_logs/organize_2025-11-05.log

Found 2 files to organize

📁 괴물의 시간.E01.251101.mkv
   → 괴물의 시간/
   ✅ Moved successfully

📁 비마이보이즈.E02.mkv
   → 비 마이 보이즈/
   ✅ Moved successfully

============================================================
✅ Successfully moved: 2 files
============================================================

$ cat /videos/.organize_logs/organize_2025-11-05.log
[2025-11-05 11:20:25] SUCCESS | MOVE | 괴물의 시간.E01.251101.mkv -> 괴물의 시간/괴물의 시간.E01.251101.mkv
[2025-11-05 11:20:25] SUCCESS | MOVE | 비마이보이즈.E02.mkv -> 비 마이 보이즈/비마이보이즈.E02.mkv
```

---

## 🎯 Feature 2: Hard-Coded Season Overrides

### What It Does
Forces specific shows to ALWAYS use a specific season folder, overriding:
- ❌ Season info in filename (e.g., S01E01 → still goes to your chosen season)
- ❌ Auto-season detection (even if other seasons exist)
- ✅ Creates the season folder if it doesn't exist

### Priority Order
1. **Hard-coded season** (HIGHEST - from config) ← This feature!
2. Season in filename (S01E01)
3. Auto-season detection (--auto-season)
4. No season (main folder)

### Configuration

**show_mappings.json:**
```json
{
  "비마이보이즈": "비 마이 보이즈",
  "저스트 메이크업 Just Makeup": "저스트 메이크업",
  
  "season_mappings": {
    "꼬리에꼬리를무는그날이야기": "S03",
    "용감한 형사들": "S04"
  }
}
```

### Usage
```bash
python3 organize_files.py /path/to/videos --config show_mappings.json
```

### Example - Override Filename Season
```
File: 꼬리에꼬리를무는그날이야기.S01E05.mkv  ← Says S01 in filename
Config: "꼬리에꼬리를무는그날이야기": "S03"  ← But config says S03

Result:
🎯 Hard-coded season: S03 (from config)
📁 꼬리에꼬리를무는그날이야기.S01E05.mkv
   → 꼬리에꼬리를무는그날이야기/S03/  ← Goes to S03!
```

### Example - Create Non-Existent Season
```
File: 용감한 형사들.E10.mkv
Existing folders: NONE (show folder doesn't even exist yet)
Config: "용감한 형사들": "S04"

Result:
🎯 Hard-coded season: S04 (from config)
📁 용감한 형사들.E10.mkv
   → 용감한 형사들/S04/  ← Creates both folders!
```

### Example - Override Auto-Detection
```
File: 저스트 메이크업.E08.mkv (no season in filename)
Existing: 저스트 메이크업/S01/, 저스트 메이크업/S02/
Auto-season would choose: S02 (latest)
Config: "저스트 메이크업": "S01"

Result:
🎯 Hard-coded season: S01 (from config)
📁 저스트 메이크업.E08.mkv
   → 저스트 메이크업/S01/  ← Goes to S01, not S02!
```

### Real-World Use Cases

#### 1. Ongoing Show (Always Current Season)
```json
{
  "season_mappings": {
    "런닝맨": "S01"  // All episodes always go to S01
  }
}
```

#### 2. Fixing Misnamed Downloads
```
Downloaded files have wrong season numbers?
Just add a season override and they'll all go to the correct folder!

Example: Files say S02, but they're actually S03
Config: "ShowName": "S03"
Done! All files now go to S03 regardless of what they say
```

#### 3. Special Collections
```json
{
  "season_mappings": {
    "무한도전 레전드 모음": "SPECIALS",
    "1박2일 명장면": "HIGHLIGHTS"
  }
}
```

---

## 🎉 Complete Workflow Example

### 1. Create Config File
```json
{
  "저스트 메이크업 Just Makeup": "저스트 메이크업",
  "비마이보이즈": "비 마이 보이즈",
  
  "season_mappings": {
    "꼬리에꼬리를무는그날이야기": "S03",
    "용감한 형사들": "S04"
  }
}
```

### 2. Test First (Dry Run)
```bash
python3 organize_files.py /downloads --dry-run --config show_mappings.json --auto-season
```

### 3. Run For Real
```bash
python3 organize_files.py /downloads --config show_mappings.json --auto-season
```

### 4. Check The Logs
```bash
# View today's log
cat /downloads/.organize_logs/organize_$(date +%Y-%m-%d).log

# List all logs
ls -lh /downloads/.organize_logs/
```

### Sample Output
```
============================================================
Video File Organizer
============================================================
🤖 AUTO-SEASON MODE - Will detect existing season folders
============================================================

📝 Logging to: .organize_logs/organize_2025-11-05.log

Found 4 files to organize

🎯 Hard-coded season: S03 (from config)
📁 꼬리에꼬리를무는그날이야기.E01.mkv
   → 꼬리에꼬리를무는그날이야기/S03/
   ✅ Moved successfully

🎯 Hard-coded season: S04 (from config)
📁 용감한 형사들.E05.mkv
   → 용감한 형사들/S04/
   ✅ Moved successfully

🔍 Auto-detected season: S01 (only season found)
📁 저스트 메이크업.Just Makeup.E08.mkv
   → 저스트 메이크업/S01/
   ✅ Moved successfully

📁 괴물의 시간.E01.mkv
   → 괴물의 시간/
   ✅ Moved successfully

============================================================
✅ Successfully moved: 4 files
============================================================
```

---

## 📋 Command Reference

```bash
# Basic usage (with logging)
python3 organize_files.py /path/to/videos

# With config file (show mappings + season overrides)
python3 organize_files.py /path/to/videos --config show_mappings.json

# With auto-season detection
python3 organize_files.py /path/to/videos --auto-season

# All features combined
python3 organize_files.py /path/to/videos --config show_mappings.json --auto-season

# Preview only (no logs created)
python3 organize_files.py /path/to/videos --dry-run --config show_mappings.json --auto-season

# Disable logging
python3 organize_files.py /path/to/videos --no-log
```

---

## 🔍 Quick Comparison

| Scenario | Solution | Command |
|----------|----------|---------|
| Files have inconsistent naming | Season overrides | `--config show_mappings.json` |
| Files missing season info | Auto-season | `--auto-season` |
| Want permanent records | Default logging | (enabled by default) |
| Testing changes | Dry run | `--dry-run` |
| All of the above | Combine them! | `--config show_mappings.json --auto-season` |

---

## 📚 Documentation Files

1. **README.md** - Main documentation and getting started guide
2. **QUICKSTART.md** - Quick guide focusing on auto-season feature
3. **ADVANCED_FEATURES.md** - Deep dive into logging and season overrides
4. **show_mappings.json** - Example config file with both features
5. **organize_files.py** - The script itself (all features included)

---

## 💡 Pro Tips

1. ✅ **Always use --dry-run first** to see what will happen
2. ✅ **Check logs after organizing** to verify everything worked
3. ✅ **Use season overrides for problematic shows** with inconsistent naming
4. ✅ **Combine features** for maximum control:
   ```bash
   python3 organize_files.py . --config show_mappings.json --auto-season
   ```
5. ✅ **Backup .organize_logs/** if you need permanent records beyond 14 days

---

## ✅ Questions Answered

**Q: Will it keep logs for 14 days?**
✅ Yes! Logs append to daily files and auto-delete after 14 days.

**Q: Can I force a specific season even if the filename says different?**
✅ Yes! Use `season_mappings` in your config file.

**Q: Will it create the season folder if it doesn't exist?**
✅ Yes! Both auto-season and season overrides create folders as needed.

**Q: Can I use both season overrides and auto-season together?**
✅ Yes! Season overrides have highest priority, auto-season is the fallback.

---

Both features work perfectly and are ready to use! 🎉
