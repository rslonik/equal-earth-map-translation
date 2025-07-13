# Map Translation System v3 - Simplified Workflow

**Clean, streamlined approach for translating Adobe Illustrator maps to Portuguese.**

## 🎯 Overview

V3 simplifies the translation process to 3 essential steps:
1. **Extract** text from Illustrator map
2. **Edit** translations manually in a CSV spreadsheet  
3. **Apply** translations back to the map

## 📁 Directory Structure

```
map-translation-v3/
├── 1-extraction/
│   └── extract_with_encoding_fix.jsx     # Run in Illustrator
├── 2-csv-translation/
│   ├── generate_translation_csv.py       # Creates CSV for editing
│   └── map_translations.csv             # ← Edit this manually
└── 3-final-script/
    ├── generate_final_script.py         # Creates Illustrator script
    └── translate_map_from_csv.jsx       # ← Run in Illustrator
```

## 🚀 Complete Workflow

### Step 1: Extract Text from Map
```bash
# In Adobe Illustrator:
# 1. Open your map file  
# 2. Go to File > Scripts > Other Script...
# 3. Select: 1-extraction/extract_with_encoding_fix.jsx
# This creates: tmp_files/extracted_text_elements_utf8.csv (semicolon-delimited)
```

### Step 2: Generate and Edit Translation CSV
```bash
# Activate the Python environment first
source ../../venv/bin/activate

cd 2-csv-translation/
python3 generate_translation_csv.py
```
This creates `map_translations.csv` with columns:
- **ID**: Original element ID (helps distinguish duplicates)
- **Text**: Original text from map
- **Layer**: Which layer it came from  
- **Translation**: ← **Fill this column manually**
- **Context**: Hint about what type of element it is
- **X, Y**: Coordinates for reference

**Edit the CSV:**
1. Open `map_translations.csv` in Excel/LibreOffice/Google Sheets
2. Fill the `Translation` column with Portuguese translations  
3. Leave empty for items you don't want to translate
4. **Important**: Save the file with semicolon (`;`) delimiter in the same `2-csv-translation/` folder
   - Most spreadsheet apps will automatically detect/preserve the semicolon format
   - If asked about delimiter, choose semicolon (`;`)

### Step 3: Generate and Apply Final Script
```bash
# Make sure environment is still active
source ../../venv/bin/activate

cd 3-final-script/
python3 generate_final_script.py
```
This creates `translate_map_from_csv.jsx`

**Apply translations:**
1. Open your map in Adobe Illustrator
2. Go to File > Scripts > Other Script...
3. Select: 3-final-script/translate_map_from_csv.jsx
4. Check the results dialog for statistics

## ✨ Key Features

**✅ Manual Control**: You decide exactly what gets translated  
**✅ Spreadsheet Editing**: Easy to review and edit in familiar interface  
**✅ Context Aware**: See what type of element you're translating  
**✅ Exact Translation**: Uses exact text as entered in CSV (no automatic casing changes)  
**✅ Robust Error Handling**: Won't crash if something goes wrong  
**✅ Re-runnable**: Can run the final script multiple times safely  
**✅ Line Break Handling**: Properly preserves multi-line text (like "SOUTH\rAFRICA")  
**✅ Semicolon Delimiter**: Uses `;` for better spreadsheet compatibility  
**⚠️ CSV Format**: Files use semicolon (`;`) delimiter instead of comma for better compatibility with European spreadsheet software  

## 📝 Tips for Manual Translation

**Country Names**: 
- SOUTH AFRICA → ÁFRICA DO SUL
- UNITED KINGDOM → REINO UNIDO  
- NEW ZEALAND → NOVA ZELÂNDIA
- Multi-line entries like "SOUTH\rAFRICA" → "ÁFRICA\rDO SUL"

**Rivers**: Add "Rio" prefix
- Amazon → Rio Amazonas
- Nile → Rio Nilo

**Oceans/Seas**:
- Pacific Ocean → Oceano Pacífico
- Mediterranean Sea → Mar Mediterrâneo

**Leave Untranslated**:
- Coordinates (150° E, 30° N, etc.)
- Numbers (1,500, 2,000, etc.)
- URLs and technical text

## ⚠️ Important Notes

**CSV Delimiter**: All CSV files use semicolon (`;`) as the delimiter for better compatibility with spreadsheet software.

**Line Breaks**: Multi-line text elements (like "SOUTH\rAFRICA") are properly handled:
- **In CSV**: Stored as escaped `\r` sequences  
- **In Illustrator**: Converted back to actual line breaks for matching
- **Manual editing**: You can edit these normally in spreadsheet software

**File Locations**: Always save the edited `map_translations.csv` in the `2-csv-translation/` folder.

## 🔄 Re-running Process

If you need to add more translations:
1. Edit `map_translations.csv` to add more translations
2. Run `python3 generate_final_script.py` again  
3. Run the updated `translate_map_from_csv.jsx` in Illustrator

## 📊 Expected Results

With manual translations, you should achieve:
- **60-80%+ coverage** depending on how many items you translate
- **Perfect accuracy** since you control every translation
- **Consistent formatting** with proper Portuguese grammar and casing

---

*This simplified v3 workflow gives you complete control over the translation process while maintaining the technical automation for applying changes.*