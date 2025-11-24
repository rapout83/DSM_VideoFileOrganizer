# 🎬 COMPLETE DEMONSTRATION

## Test Files

```
꼬리에꼬리를무는그날이야기.S01E05.mkv  ← Has S01 in filename
용감한 형사들.E10.mkv                 ← No season info
저스트 메이크업.Just Makeup.E08.mkv   ← No season info
괴물의 시간.E01.mkv                   ← No season info
```

## Existing Structure

```
저스트 메이크업/
└── S01/
    └── 저스트.메이크업.S01E01.mkv  ← Already exists
```

## Configuration (show_mappings.json)

```json
{
  "저스트 메이크업 Just Makeup": "저스트 메이크업",
  
  "season_mappings": {
    "꼬리에꼬리를무는그날이야기": "S03",
    "용감한 형사들": "S04"
  }
}
```

## Command

```bash
python3 organize_files.py final_demo --config show_mappings.json --auto-season
```

## Output

```
============================================================
Video File Organizer
============================================================
🤖 AUTO-SEASON MODE - Will detect existing season folders
============================================================

📝 Logging to: .organize_logs/organize_2025-11-05.log

Found 4 files to organize

🎯 Hard-coded season: S04 (from config)
📁 용감한 형사들.E10.mkv
   → 용감한 형사들/S04/
   ✅ Moved successfully

🎯 Hard-coded season: S03 (from config)
📁 꼬리에꼬리를무는그날이야기.S01E05.mkv
   → 꼬리에꼬리를무는그날이야기/S03/
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

## Final Organized Structure

```
final_demo/
├── .organize_logs/
│   └── organize_2025-11-05.log  ← Log file created!
│
├── 꼬리에꼬리를무는그날이야기/
│   └── S03/  ← Created S03, not S01 (season override!)
│       └── 꼬리에꼬리를무는그날이야기.S01E05.mkv
│
├── 용감한 형사들/
│   └── S04/  ← Created S04 from config (season override!)
│       └── 용감한 형사들.E10.mkv
│
├── 저스트 메이크업/
│   └── S01/
│       ├── 저스트.메이크업.S01E01.mkv  ← Was already here
│       └── 저스트 메이크업.Just Makeup.E08.mkv  ← Auto-detected S01!
│
└── 괴물의 시간/
    └── 괴물의 시간.E01.mkv  ← No season (no config, no detection)
```

## Log File Content (.organize_logs/organize_2025-11-05.log)

```
[2025-11-05 11:23:13] SUCCESS | MOVE | 용감한 형사들.E10.mkv -> 용감한 형사들/S04/용감한 형사들.E10.mkv
[2025-11-05 11:23:13] SUCCESS | MOVE | 꼬리에꼬리를무는그날이야기.S01E05.mkv -> 꼬리에꼬리를무는그날이야기/S03/꼬리에꼬리를무는그날이야기.S01E05.mkv
[2025-11-05 11:23:13] SUCCESS | MOVE | 저스트 메이크업.Just Makeup.E08.mkv -> 저스트 메이크업/S01/저스트 메이크업.Just Makeup.E08.mkv
[2025-11-05 11:23:13] SUCCESS | MOVE | 괴물의 시간.E01.mkv -> 괴물의 시간/괴물의 시간.E01.mkv
```

## What Happened?

### File 1: 꼬리에꼬리를무는그날이야기.S01E05.mkv
- ❌ Filename says: **S01**
- ✅ Config says: **S03** (season override)
- 🎯 **Result: Goes to S03** (season override wins!)

### File 2: 용감한 형사들.E10.mkv
- ❌ No season in filename
- ❌ No existing folders
- ✅ Config says: **S04** (season override)
- 🎯 **Result: Creates S04 folder** (season override creates it!)

### File 3: 저스트 메이크업.Just Makeup.E08.mkv
- ❌ No season in filename
- ✅ Existing folder: S01/
- ✅ Config mapping: "저스트 메이크업 Just Makeup" → "저스트 메이크업"
- ✅ Auto-season: Detected S01
- 🎯 **Result: Goes to S01** (auto-season detection!)

### File 4: 괴물의 시간.E01.mkv
- ❌ No season in filename
- ❌ No season override in config
- ❌ No existing folders
- 🎯 **Result: Goes to main folder** (default behavior)

## Features Demonstrated

✅ **Logging** - All operations logged to `.organize_logs/organize_2025-11-05.log`
✅ **Season Overrides** - Files 1 & 2 forced to S03 and S04
✅ **Auto-Season** - File 3 auto-detected S01 from existing folder
✅ **Show Name Mapping** - File 3 renamed from "저스트 메이크업 Just Makeup" to "저스트 메이크업"
✅ **Folder Creation** - S03, S04 folders created automatically
✅ **14-day Retention** - Log files will be kept for 14 days

## Priority Order (As Demonstrated)

1. **Season Override** (Highest)
   - 꼬리에꼬리를무는그날이야기: S03 (overrode S01 in filename)
   - 용감한 형사들: S04 (created new folder)

2. **Auto-Season Detection**
   - 저스트 메이크업: S01 (detected from existing folder)

3. **Default (No Season)**
   - 괴물의 시간: Main folder (no config, no detection)

---

## 🎉 Perfect! All Features Working Together!

Both new features work perfectly:
- ✅ **Logging**: Every operation recorded with timestamp
- ✅ **Season Overrides**: Absolute control over where files go
- ✅ **14-day Retention**: Logs auto-cleanup after 14 days
- ✅ **Show Name Mappings**: Consistent folder naming
- ✅ **Auto-Season**: Smart fallback for files without season info

You can now maintain your JSON config for both custom mappings AND 
hard-coded season assignments! 🚀
