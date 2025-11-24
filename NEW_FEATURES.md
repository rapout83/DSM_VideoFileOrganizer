# 🆕 New Features: Season Patterns & Custom Episode Markers

## ✅ Feature 1: Season Pattern Detection

### The Problem
Shows with season numbers in their names:
```
싱어게인4.E04.251104.1080p.H264-F1RST.mp4
```

You want: `싱어게인/S04/` not `싱어게인4/`

### The Solution
Configure which shows use auto-pattern detection in JSON:

```json
{
  "season_patterns": {
    "싱어게인": "auto",
    "복면가왕": "auto",
    "나는솔로": "auto"
  }
}
```

### How It Works

**Pattern Detection:**
- `싱어게인4` → Base: `싱어게인`, Number: `4` → Season: `S04`
- `싱어게인3` → Base: `싱어게인`, Number: `3` → Season: `S03`
- `복면가왕2` → Base: `복면가왕`, Number: `2` → Season: `S02`

**Safety:**
- Only works for shows YOU specify
- Won't incorrectly parse shows like `24시` or `1박2일`
- Opt-in design - explicit control

### Examples

#### Example 1: 싱어게인 Series
```
Files:
  싱어게인3.E10.251101.1080p.H264-F1RST.mp4
  싱어게인4.E04.251104.1080p.H264-F1RST.mp4

Config:
  "season_patterns": {
    "싱어게인": "auto"
  }

Result:
  싱어게인/
  ├── S03/
  │   └── 싱어게인3.E10...mp4
  └── S04/
      └── 싱어게인4.E04...mp4
```

#### Example 2: Multiple Shows
```
Files:
  싱어게인4.E04.mp4
  복면가왕2.E15.mp4
  나는솔로5.E08.mp4

Config:
  "season_patterns": {
    "싱어게인": "auto",
    "복면가왕": "auto",
    "나는솔로": "auto"
  }

Result:
  싱어게인/S04/싱어게인4.E04.mp4
  복면가왕/S02/복면가왕2.E15.mp4
  나는솔로/S05/나는솔로5.E08.mp4
```

### Priority Order

Season detection priority (highest to lowest):

1. **Season Override** (season_mappings) ← HIGHEST
2. **Filename Season** (S01E01, 시즌2)
3. **Season Pattern** (싱어게인4 → S04) ← NEW!
4. **Auto-Season** (--auto-season flag)
5. **No Season** ← DEFAULT

**Example of Priority:**
```json
{
  "season_patterns": {
    "런닝맨": "auto"
  },
  "season_mappings": {
    "런닝맨": "S01"
  }
}
```

File: `런닝맨5.E100.mp4`
- Pattern says: S05
- Override says: S01
- **Result: S01** (season_mappings wins!)

---

## ✅ Feature 2: Custom Episode Markers

### The Problem
Korean shows use various episode indicators:
- `최종회` (final episode)
- `첫방송` (first broadcast)  
- `특집` (special)
- `마지막회` (last episode)
- Many more...

These were **hardcoded** in the script - hard to maintain!

### The Solution
Manage them in JSON - easy to add new ones:

```json
{
  "episode_markers": [
    "최종",
    "최종회",
    "첫회",
    "첫방송",
    "첫 방송",
    "마지막회",
    "마지막 회",
    "특집",
    "특별편",
    "파일럿"
  ]
}
```

### How It Works

**Episode markers are removed** from show name:
- `런닝맨.최종회.E500.mkv` → Show: `런닝맨`
- `나는솔로.특집.E20.mkv` → Show: `나는솔로`
- `복면가왕.첫방송.E01.mkv` → Show: `복면가왕`

### Adding New Markers

Discovered a new one? Just add it to JSON:

```json
{
  "episode_markers": [
    "최종",
    "최종회",
    "첫회",
    "첫방송",
    "특집",
    "특별편",
    "파일럿",
    "설특집",     ← New!
    "추석특집",   ← New!
    "신년특집"    ← New!
  ]
}
```

No need to edit the script!

### Examples

#### Example 1: Special Episodes
```
Files:
  런닝맨.설특집.E580.mkv
  복면가왕.추석특집.E300.mkv

Config:
  "episode_markers": ["설특집", "추석특집"]

Result:
  런닝맨/런닝맨.설특집.E580.mkv
  복면가왕/복면가왕.추석특집.E300.mkv
```

#### Example 2: Finale Episodes
```
Files:
  괴물의 시간.최종회.E12.mkv
  괴물의 시간.마지막회.E12.mkv  ← Same episode, different naming

Config:
  "episode_markers": ["최종회", "마지막회"]

Result:
  괴물의 시간/
  ├── 괴물의 시간.최종회.E12.mkv
  └── 괴물의 시간.마지막회.E12.mkv
```

---

## 📋 Complete Configuration Example

```json
{
  "비마이보이즈": "비 마이 보이즈",
  "저스트 메이크업 Just Makeup": "저스트 메이크업",
  
  "season_mappings": {
    "꼬리에꼬리를무는그날이야기": "S03",
    "용감한 형사들": "S04",
    "런닝맨": "S01"
  },
  
  "season_patterns": {
    "싱어게인": "auto",
    "복면가왕": "auto",
    "나는솔로": "auto"
  },
  
  "episode_markers": [
    "최종",
    "최종회",
    "첫회",
    "첫방송",
    "첫 방송",
    "마지막회",
    "마지막 회",
    "특집",
    "특별편",
    "파일럿",
    "설특집",
    "추석특집"
  ]
}
```

---

## 🎯 Real-World Test

### Input Files:
```
싱어게인4.E04.251104.1080p.H264-F1RST.mp4
싱어게인3.E10.251101.1080p.H264-F1RST.mp4
런닝맨.최종회.E500.mkv
나는솔로.특집.E20.mkv
```

### Command:
```bash
python3 organize_files.py /downloads --config show_mappings.json
```

### Output:
```
📁 싱어게인3.E10.251101.1080p.H264-F1RST.mp4
   → 싱어게인/S03/                    ← Pattern detected!
   ✅ Moved successfully

📁 싱어게인4.E04.251104.1080p.H264-F1RST.mp4
   → 싱어게인/S04/                    ← Pattern detected!
   ✅ Moved successfully

🎯 Hard-coded season: S01 (from config)
📁 런닝맨.최종회.E500.mkv
   → 런닝맨/S01/                      ← Override + marker removed!
   ✅ Moved successfully

📁 나는솔로.특집.E20.mkv
   → 나는솔로/                        ← Marker removed!
   ✅ Moved successfully
```

### Final Structure:
```
downloads/
├── 싱어게인/
│   ├── S03/
│   │   └── 싱어게인3.E10...mp4
│   └── S04/
│       └── 싱어게인4.E04...mp4
│
├── 런닝맨/
│   └── S01/
│       └── 런닝맨.최종회.E500.mkv
│
└── 나는솔로/
    └── 나는솔로.특집.E20.mkv
```

---

## 💡 Best Practices

### 1. Season Patterns
**Do:**
- Add shows where the number IS the season
- Use for ongoing variety shows

**Don't:**
- Add shows where numbers are part of the name (`24시`, `1박2일`)
- Use if the show only has one season

### 2. Episode Markers
**Do:**
- Add new markers as you discover them
- Include variations (e.g., `첫방송`, `첫 방송`)

**Don't:**
- Remove built-in markers unless you're sure
- Add general words that might be in show names

### 3. Testing
Always test with `--dry-run` first:
```bash
python3 organize_files.py /path --config show_mappings.json --dry-run
```

---

## 📊 Feature Summary

| Feature | Config Section | Example | Priority |
|---------|---------------|---------|----------|
| Season Pattern | `season_patterns` | `싱어게인4` → `S04` | 3 |
| Episode Markers | `episode_markers` | `최종회` removed | N/A |
| Season Override | `season_mappings` | Force `S03` | 1 (Highest) |
| Show Mapping | Top level | Rename folder | After pattern |

---

## ✅ Summary

**Two new powerful features:**

1. **Season Patterns** 
   - Auto-detect seasons from show names with numbers
   - Opt-in per show - safe and explicit
   - `싱어게인4` → `싱어게인/S04/`

2. **Custom Episode Markers**
   - Manage Korean episode indicators in JSON
   - Easy to add new ones without editing code
   - `런닝맨.최종회.E500` → `런닝맨/`

Both features work seamlessly with existing functionality! 🎉
