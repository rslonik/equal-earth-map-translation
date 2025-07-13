#!/usr/bin/env python3
# Version: 20250713.0538

import pandas as pd
from pathlib import Path

def generate_translation_csv():
    """Generate a CSV file for manual translation editing."""
    
    # Input: extracted text from v3 tmp_files
    input_file = "../tmp_files/extracted_text_elements_utf8.csv"
    output_file = "map_translations.csv"
    
    print("📖 Reading extracted text...")
    
    # Read the extracted text data
    try:
        df = pd.read_csv(input_file, encoding='utf-8', sep=';')
        print(f"   Loaded {len(df)} text elements")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    # Create translation CSV with essential columns
    translation_df = pd.DataFrame({
        'ID': df['ID'],  # Keep original ID to distinguish duplicates
        'Text': df['Text'],
        'Layer': df['Layer'], 
        'Translation': '',  # Empty column for manual editing
        'Context': df['Layer'].apply(get_context_hint),
        'X': df['X'],  # Keep coordinates for reference
        'Y': df['Y']
    })
    
    # Sort by layer for easier editing
    translation_df = translation_df.sort_values(['Layer', 'Text'])
    
    # Show duplicate analysis before deciding what to do
    original_count = len(translation_df)
    duplicates_df = translation_df[translation_df.duplicated(subset=['Text'], keep=False)]
    
    if len(duplicates_df) > 0:
        print(f"\n🔍 DUPLICATE ANALYSIS:")
        print(f"   Total duplicates: {len(duplicates_df)}")
        
        # Show examples of duplicates across different layers
        duplicate_examples = duplicates_df.groupby('Text').agg({
            'Layer': lambda x: list(set(x)),
            'Context': lambda x: list(set(x))
        }).head(10)
        
        cross_layer_duplicates = 0
        for text, group in duplicate_examples.iterrows():
            if len(group['Layer']) > 1:
                cross_layer_duplicates += 1
                print(f"   '{text}' appears in: {group['Layer']}")
        
        print(f"\n   Cross-layer duplicates: {cross_layer_duplicates}")
        
        # Keep duplicates for now - user can decide in spreadsheet
        print(f"\n✅ KEEPING ALL ENTRIES (including duplicates)")
        print(f"   You can manually review and delete unwanted duplicates in the spreadsheet")
        unique_count = original_count
    else:
        print(f"   No duplicates found")
        unique_count = original_count
    
    # Save to CSV for manual editing
    translation_df.to_csv(output_file, index=False, encoding='utf-8', sep=';')
    
    print(f"✅ Translation CSV generated: {output_file}")
    print("\n📝 MANUAL EDITING INSTRUCTIONS:")
    print("1. Open map_translations.csv in your spreadsheet app")
    print("2. Fill the 'Translation' column with Portuguese translations")
    print("3. Use 'Context' column to understand what type of element it is")
    print("4. Leave empty for texts you don't want to translate")
    print("5. Save the file when done")
    print("\n📊 BREAKDOWN BY LAYER:")
    
    # Show breakdown by layer
    layer_counts = translation_df['Layer'].value_counts()
    for layer, count in layer_counts.items():
        print(f"   {layer}: {count} items")
    
    return unique_count

def get_context_hint(layer):
    """Get context hint based on layer name."""
    layer_hints = {
        'Country Type': 'Country',
        'River Type': 'River', 
        'Lake Type': 'Lake',
        'Ocean Type': 'Ocean/Sea',
        'Title Type': 'Map Title',
        'Legend Content': 'Legend/Instructions',
        'Graticule Type': 'Coordinates',
        'Geographic Line Type': 'Geographic Feature',
        'Magnetic Poles': 'Poles',
        'Misc Black Type': 'Miscellaneous'
    }
    return layer_hints.get(layer, 'Other')

if __name__ == "__main__":
    generate_translation_csv()