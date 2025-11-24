# Advanced Features Guide

## 📝 Logging

### Overview
The script automatically logs all file operations, keeping logs for 14 days. Logs are stored in a `.organize_logs` folder within your video directory.

### Log Format
```
[2025-11-05 11:20:25] SUCCESS | MOVE | filename.mkv -> destination/folder/filename.mkv
[2025-11-05 11:21:30] ERROR | MOVE | badfile.mkv -> destination/ | Error: Permission denied
```

### Log Location
```
your-video-folder/
├── .organize_logs/
│   ├── organize_2025-11-05.log
│   ├── organize_2025-11-04.log
│   └── organize_2025-11-03.log  (logs older than 14 days are auto-deleted)
├── Show Name/
│   └── file.mkv
```

### Features
- ✅ **Automatic**: Enabled by default (not in dry-run mode)
- ✅ **Daily files**: One log file per day (appends to existing)
- ✅ **14-day retention**: Old logs automatically cleaned up
- ✅ **UTF-8 support**: Handles Korean characters perfectly
- ✅ **Tracks errors**: Logs both successes and failures

### Disabling Logs
```bash
# Logs are enabled by default, no flag needed
python3 organize_files.py /path/to/videos

# Note: dry-run mode doesn't create logs
python3 organize_files.py /path/to/videos --dry-run
```

---

## 🎯 Hard-Coded Season Overrides

### Overview
Sometimes you want specific shows to ALWAYS go into a specific season, regardless of what's in the filename or what folders already exist. This feature overrides both auto-detection and filename parsing.

### Priority Order
1. **Hard-coded season override** (highest priority) ← Config file
2. **Filename season** (S01E01 in filename) ← Detected from filename
3. **Auto-season detection** (--auto-season flag) ← Existing folders
4. **No season** (main folder) ← Default

### Configuration

#### In JSON Config File (Recommended)
Edit your `show_mappings.json`:

```json
{
  "비마이보이즈": "비 마이 보이즈",
  "저스트 메이크업 Just Makeup": "저스트 메이크업",
  
  "season_mappings": {
    "꼬리에꼬리를무는그날이야기": "S03",
    "용감한 형사들": "S04",
    "더 글로리": "S02"
  }
}
```

#### In Script File (Alternative)
Edit `organize_files.py` directly:

```python
SEASON_MAPPINGS = {
    "꼬리에꼬리를무는그날이야기": "S03",
    "용감한 형사들": "S04",
}
```

### How It Works

**Example 1: Override filename season**
```
File: 꼬리에꼬리를무는그날이야기.S01E05.mkv
Config: "꼬리에꼬리를무는그날이야기": "S03"

Result: 
🎯 Hard-coded season: S03 (from config)
📁 꼬리에꼬리를무는그날이야기.S01E05.mkv
   → 꼬리에꼬리를무는그날이야기/S03/
```

Even though the filename says "S01", the hard-coded override forces it to S03!

**Example 2: Create season folder even if it doesn't exist**
```
File: 용감한 형사들.E10.mkv
Config: "용감한 형사들": "S04"
Existing folders: NONE

Result:
🎯 Hard-coded season: S04 (from config)
📁 용감한 형사들.E10.mkv
   → 용감한 형사들/S04/  ← Creates S04 folder automatically!
```

**Example 3: Override auto-detection**
```
File: 저스트 메이크업.E08.mkv
Existing: 저스트 메이크업/S01/ (exists)
          저스트 메이크업/S02/ (exists)
Config: "저스트 메이크업": "S01"
Flag: --auto-season

Result:
🎯 Hard-coded season: S01 (from config)
📁 저스트 메이크업.E08.mkv
   → 저스트 메이크업/S01/
```

Even with --auto-season (which would pick S02 as latest), hard-coded override forces S01!

### Use Cases

#### 1. Shows With Inconsistent Naming
```json
{
  "season_mappings": {
    "런닝맨": "S01"  // Always S01, even if files have different season numbers
  }
}
```

#### 2. Compilation Episodes
```json
{
  "season_mappings": {
    "무한도전 레전드 모음": "SPECIALS"
  }
}
```

#### 3. Ongoing Shows
```json
{
  "season_mappings": {
    "현재방영중인쇼": "S08"  // Always current season
  }
}
```

#### 4. Fixing Misnamed Files
```
Files downloaded with wrong season numbers?
Just add a season override and they'll all go to the correct folder!
```

### Complete Example

**show_mappings.json:**
```json
{
  "용감한 형사들": "용감한 형사들",
  "런닝맨 레전드": "런닝맨",
  
  "season_mappings": {
    "용감한 형사들": "S04",
    "런닝맨": "S01",
    "꼬리에꼬리를무는그날이야기": "S03"
  }
}
```

**Command:**
```bash
python3 organize_files.py /downloads --config show_mappings.json
```

**Files:**
```
용감한 형사들.E10.mkv          → 용감한 형사들/S04/
런닝맨 레전드.E234.mkv          → 런닝맨/S01/
꼬리에꼬리를무는그날이야기.E05.mkv → 꼬리에꼬리를무는그날이야기/S03/
```

**Log Output:**
```
🎯 Hard-coded season: S04 (from config)
📁 용감한 형사들.E10.mkv
   → 용감한 형사들/S04/
   ✅ Moved successfully

🎯 Hard-coded season: S01 (from config)
📁 런닝맨 레전드.E234.mkv
   → 런닝맨/S01/
   ✅ Moved successfully

🎯 Hard-coded season: S03 (from config)
📁 꼬리에꼬리를무는그날이야기.E05.mkv
   → 꼬리에꼬리를무는그날이야기/S03/
   ✅ Moved successfully
```

**Log File (.organize_logs/organize_2025-11-05.log):**
```
[2025-11-05 11:20:25] SUCCESS | MOVE | 용감한 형사들.E10.mkv -> 용감한 형사들/S04/용감한 형사들.E10.mkv
[2025-11-05 11:20:25] SUCCESS | MOVE | 런닝맨 레전드.E234.mkv -> 런닝맨/S01/런닝맨 레전드.E234.mkv
[2025-11-05 11:20:25] SUCCESS | MOVE | 꼬리에꼬리를무는그날이야기.E05.mkv -> 꼬리에꼬리를무는그날이야기/S03/꼬리에꼬리를무는그날이야기.E05.mkv
```

---

## 🎯 Feature Comparison

| Feature | Priority | When to Use |
|---------|----------|-------------|
| **Hard-coded season** | 1 (Highest) | When you want absolute control over where files go |
| **Filename season** | 2 | When filenames have accurate season info (S01E01) |
| **Auto-season (--auto-season)** | 3 | When filenames lack season but folders exist |
| **No season** | 4 (Default) | When you want files in main show folder |

---

## 📋 Complete Workflow Example

```bash
# 1. Set up your config
cat > show_mappings.json << 'EOF'
{
  "저스트 메이크업 Just Makeup": "저스트 메이크업",
  "비마이보이즈": "비 마이 보이즈",
  
  "season_mappings": {
    "꼬리에꼬리를무는그날이야기": "S03",
    "용감한 형사들": "S04"
  }
}
EOF

# 2. Test with dry-run (no logs created in dry-run)
python3 organize_files.py /downloads --dry-run --config show_mappings.json --auto-season

# 3. Run for real (logs will be created)
python3 organize_files.py /downloads --config show_mappings.json --auto-season

# 4. Check the logs
cat /downloads/.organize_logs/organize_$(date +%Y-%m-%d).log

# 5. View old logs
ls -lh /downloads/.organize_logs/
```

---

## 🔍 Troubleshooting

### "Why isn't my season override working?"

Check these:
1. ✅ Is the show name spelled EXACTLY as detected? (Use --dry-run to see detected names)
2. ✅ Is your JSON valid? (Test with `python3 -m json.tool show_mappings.json`)
3. ✅ Are you using --config flag? `--config show_mappings.json`
4. ✅ Did you put season overrides in the "season_mappings" section?

### "I don't see any logs"

Logs are only created when:
- ✅ NOT in --dry-run mode
- ✅ Files are actually moved
- ✅ Script has write permissions

### "Where are my old logs?"

Logs older than 14 days are automatically deleted to save space. If you want to keep them longer, you can backup the `.organize_logs` folder.

---

## 💡 Pro Tips

1. **Always use --dry-run first** to see what will happen
2. **Check logs after organizing** to verify everything worked
3. **Backup the .organize_logs folder** if you need permanent records
4. **Use season overrides for problematic shows** that have inconsistent naming
5. **Combine all features** for maximum control:
   ```bash
   python3 organize_files.py . --config show_mappings.json --auto-season
   ```

This gives you:
- ✅ Custom show name mappings
- ✅ Hard-coded season overrides (highest priority)
- ✅ Auto-season detection (fallback)
- ✅ Complete operation logging
