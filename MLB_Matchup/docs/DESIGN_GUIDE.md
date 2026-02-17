# Design Guide - Easy Lineup Card Editing

## 🎨 Quick Start

Want to change how lineup cards look? Follow these steps:

### 1. Generate Live Preview

```bash
cd MLB_Matchup/image_generation
python generate_live_preview.py
```

This creates `live_preview.html` with sample data.

### 2. Open Preview in Browser

Open `MLB_Matchup/image_generation/live_preview.html` in your web browser.

Keep this tab open!

### 3. Edit Design Config

Open `MLB_Matchup/image_generation/design_config.py` and change values:

```python
DESIGN = {
    'team_font_size': 250,  # Make team names bigger/smaller
    'lineup_row_font_size': 24,  # Change player name size
    'card_width': 1200,  # Change card dimensions
    # etc...
}
```

### 4. Regenerate & Refresh

```bash
python generate_live_preview.py  # Regenerate
```

Then **refresh your browser** (F5) to see changes!

## 📝 What Can You Change?

### Card Dimensions
```python
'card_width': 1200,        # Card width in pixels
'card_height': 1400,       # Card height in pixels
'card_padding': '20px 30px 20px 20px',  # Space around edges
```

### Team Names
```python
'team_font_size': 250,     # Size of team abbreviations
'team_stroke_width': 6,    # Outline thickness
'team_vertical_offset': -80,  # Move names up/down
```

### Lineup Table
```python
'lineup_header_font_size': 32,  # "Batting Order" text size
'lineup_row_font_size': 24,     # Player name size
'lineup_row_height': 55,        # Space between players
'stats_font_size': 18,          # Player stats text size
```

### Spacing & Layout
```python
'section_spacing': 20,      # Space between sections
'table_margin_top': 30,     # Space above lineup table
```

### Visual Effects
```python
'border_radius': 12,        # Rounded corners
'box_shadow': '0 8px 32px rgba(0, 0, 0, 0.3)',  # Shadow effect
```

## 🔄 Workflow

```
1. Edit design_config.py
   ↓
2. Run generate_live_preview.py
   ↓
3. Refresh browser
   ↓
4. See changes immediately!
   ↓
   Repeat until satisfied
```

## 🎯 Common Changes

### Make Team Names Bigger
```python
'team_font_size': 300,  # Was 250
```

### Adjust Lineup Spacing
```python
'lineup_row_height': 65,  # Was 55 (more space)
'lineup_row_height': 45,  # Was 55 (less space)
```

### Change Card Size
```python
'card_width': 1400,   # Wider
'card_height': 1600,  # Taller
```

### Bigger Player Stats
```python
'stats_font_size': 20,  # Was 18
```

## 🖼️ Test with Different Teams

Edit the sample data in `design_config.py`:

```python
SAMPLE_DATA = {
    'away_team': 'BOS',  # Try different teams
    'home_team': 'SF',
    'away_primary_color': '#BD3039',  # Red Sox red
    'home_primary_color': '#FD5A1E',  # Giants orange
    # etc...
}
```

## 💡 Pro Tips

1. **Keep browser and editor side-by-side** - See changes instantly
2. **Use version control** - Commit before major design changes
3. **Test with real data** - Run the test script with actual game data
4. **Mobile preview** - Resize browser to see how it looks at different sizes

## 🐛 Troubleshooting

### Preview looks broken?
- Check for syntax errors in `design_config.py`
- Make sure all values are valid (numbers for sizes, strings for colors)

### Changes not showing?
- Did you run `generate_live_preview.py` again?
- Did you refresh the browser (not just focus it)?
- Try hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

### Want to revert?
```bash
git checkout design_config.py  # Reset to last commit
```

## 📚 Advanced

### Custom Colors
```python
'background_gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
'text_color': '#ffffff',
'border_color': 'rgba(255, 255, 255, 0.2)',
```

### Custom Fonts
Edit the font configurations:
```python
FONTS = {
    'primary': 'Anton',        # Team names
    'secondary': 'WorkSans-Bold',  # Headers
    'body': 'WorkSans-Regular',    # Body text
}
```

## 🎉 That's It!

No more digging through HTML and CSS. Just edit simple Python config values and see changes instantly!

---

**Questions?** Check the main README or ask in issues.
