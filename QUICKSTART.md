# Quick Start Guide - Auto-Season Feature

## Scenario: Organizing "저스트 메이크업" Files

You have files with mixed naming:
- Some have season info: `저스트.메이크업.S01E01.mkv`
- Some don't: `저스트 메이크업.Just Makeup.E08.mkv`

### Step 1: Set up custom mapping

Create `show_mappings.json`:
```json
{
  "저스트 메이크업 Just Makeup": "저스트 메이크업"
}
```

This ensures "저스트 메이크업 Just Makeup" is recognized as "저스트 메이크업"

### Step 2: Organize with auto-season

```bash
# Preview what will happen
python3 organize_files.py /path/to/videos --dry-run --config show_mappings.json --auto-season

# If it looks good, run for real
python3 organize_files.py /path/to/videos --config show_mappings.json --auto-season
```

### Result:

**Before:**
```
videos/
├── 저스트.메이크업.S01E01.mkv
├── 저스트.메이크업.S01E05.mkv
└── 저스트 메이크업.Just Makeup.E08.mkv  ← No season info!
```

**After:**
```
videos/
└── 저스트 메이크업/
    └── S01/
        ├── 저스트.메이크업.S01E01.mkv
        ├── 저스트.메이크업.S01E05.mkv
        └── 저스트 메이크업.Just Makeup.E08.mkv  ← Auto-placed in S01!
```

### How Auto-Season Works

1. **File without season**: `저스트 메이크업.Just Makeup.E08.mkv`
2. **Custom mapping applied**: Name becomes "저스트 메이크업"
3. **Check existing folders**: Found "저스트 메이크업/S01/"
4. **Auto-detect**: Only S01 exists → use S01
5. **Result**: File goes to `저스트 메이크업/S01/`

### Multiple Seasons Example

If you have:
```
저스트 메이크업/
├── S01/
├── S02/
└── S03/
```

New file without season info will go to **S03** (latest season)

```
🔍 Auto-detected season: S03 (latest of S01, S02, S03)
📁 저스트 메이크업.Just Makeup.E08.mkv
   → 저스트 메이크업/S03/
```

## Best Practice Workflow

```bash
# 1. Always test first
python3 organize_files.py . --dry-run --config show_mappings.json --auto-season

# 2. Review the output carefully

# 3. Run for real if everything looks good
python3 organize_files.py . --config show_mappings.json --auto-season
```

## When to Use --auto-season

✅ **Use it when:**
- You have files with inconsistent naming
- Some files have season info, some don't
- You want files automatically organized into existing season folders

❌ **Don't use it when:**
- All your files already have season info (not needed)
- You want files in the main folder, not season subfolders
- You're not sure which season a file belongs to

## Tips

1. **Start with one show** to test the feature
2. **Use --dry-run** first ALWAYS
3. **Keep your show_mappings.json** updated
4. **Manual override**: If auto-season picks wrong, just add S01/S02 to the filename
