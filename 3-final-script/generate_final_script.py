#!/usr/bin/env python3
# Version: 20250713.1405

import pandas as pd
from pathlib import Path

def generate_final_script():
    """Generate the final Adobe Illustrator script from CSV translations."""
    
    # Input: CSV with manual translations
    input_file = "../2-csv-translation/map_translations.csv"
    output_file = "translate_map_from_csv.jsx"
    
    if not Path(input_file).exists():
        print(f"❌ Translation CSV not found: {input_file}")
        print("   Please run step 2 first to generate the CSV")
        return
    
    print("📖 Reading translation CSV...")
    
    # Read the translation CSV
    try:
        df = pd.read_csv(input_file, encoding='utf-8', sep=';')
        print(f"   Loaded {len(df)} translation entries")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return
    
    # Filter out empty translations
    translated_df = df[df['Translation'].notna() & (df['Translation'] != '')].copy()
    translation_count = len(translated_df)
    
    print(f"   Found {translation_count} completed translations")
    
    if translation_count == 0:
        print("❌ No translations found in CSV")
        print("   Please fill the 'Translation' column in the CSV file")
        return
    
    # Create translations dictionary
    translations = {}
    for _, row in translated_df.iterrows():
        translations[row['Text']] = row['Translation']
    
    # Generate JSX script
    jsx_content = f"""// Adobe Illustrator Map Translation Script - CSV Version
// Generated from manual CSV translations
// Contains {translation_count} verified translations

var translations = {{
"""
    
    # Add translations to JavaScript object
    for english, portuguese in translations.items():
        # Convert escaped \r from CSV to properly escaped \r for JavaScript
        english_js = str(english).replace('\\\\r', '\\r')
        portuguese_js = str(portuguese).replace('\\\\r', '\\r')
        
        # Escape quotes for JavaScript strings
        english_escaped = english_js.replace('"', '\\"').replace("'", "\\'")
        portuguese_escaped = portuguese_js.replace('"', '\\"').replace("'", "\\'") 
        jsx_content += f'  "{english_escaped}": "{portuguese_escaped}",\n'
    
    jsx_content += f"""
}};

// Statistics
var translationStats = {{
  totalTranslations: {translation_count},
  csvSource: "../2-csv-translation/map_translations.csv"
}};


function findTranslation(text) {{
  try {{
    // Manual trim
    text = text.replace(/^\\s+|\\s+$/g, '');
    
    // No line break normalization - keep original format
    
    // Direct match
    if (text in translations) {{
      return translations[text];
    }}
    
    // Case-insensitive match
    var textLower = text.toLowerCase();
    for (var key in translations) {{
      try {{
        if (key.toLowerCase() === textLower) {{
          return translations[key];
        }}
      }} catch (keyError) {{
        continue;
      }}
    }}
    
    return null;
  }} catch (error) {{
    return null;
  }}
}}

function translateDocument() {{
  var doc = app.activeDocument;
  var changesCount = 0;
  var processedCount = 0;
  var sampleChanges = [];
  var errorCount = 0;

  // Process all text frames with error handling
  for (var i = 0; i < doc.textFrames.length; i++) {{
    try {{
      var textFrame = doc.textFrames[i];
      var originalText = textFrame.contents;
      originalText = originalText.replace(/^\\s+|\\s+$/g, '');
      processedCount++;
      
      if (!originalText) {{
        continue;
      }}

      var translation = findTranslation(originalText);
      if (translation && translation !== originalText) {{
        textFrame.contents = translation;
        changesCount++;
        
        // Record sample changes
        if (sampleChanges.length < 8) {{
          sampleChanges.push(originalText + " → " + translation);
        }}
      }}
    }} catch (itemError) {{
      errorCount++;
    }}
  }}

  // Create results message
  var message = "Map Translation Results (CSV Version)\\n";
  message += "=" + Array(40).join("=") + "\\n\\n";
  message += "📊 STATISTICS:\\n";
  message += "   Processed: " + processedCount + " text elements\\n";
  message += "   Translated: " + changesCount + " elements\\n";
  message += "   Available: " + translationStats.totalTranslations + " translations\\n";
  
  if (errorCount > 0) {{
    message += "   Errors handled: " + errorCount + " (continued processing)\\n";
  }}
  message += "   Success rate: " + Math.round((changesCount / processedCount) * 100) + "%\\n\\n";
  
  if (changesCount > 0) {{
    message += "🌍 SAMPLE CHANGES:\\n";
    for (var i = 0; i < sampleChanges.length && i < 8; i++) {{
      message += "   • " + sampleChanges[i] + "\\n";
    }}
    if (changesCount > 8) {{
      message += "   ... and " + (changesCount - 8) + " more\\n";
    }}
  }} else {{
    message += "❌ NO MATCHES FOUND\\n";
    message += "   This might mean:\\n";
    message += "   • All text already translated\\n";
    message += "   • Need to add more translations to CSV\\n";
    message += "   • Check if correct map file is open\\n";
  }}
  
  message += "\\n📝 CSV Source: " + translationStats.csvSource + "\\n";
  
  alert(message);
}}

// Run the translation with robust error handling
try {{
  if (typeof app === 'undefined') {{
    alert("Script must be run from Adobe Illustrator.");
  }} else if (app.documents.length === 0) {{
    alert("Please open your map document first.");
  }} else {{
    translateDocument();
  }}
}} catch (error) {{
  var errorMsg = "Translation completed with some issues.\\n\\n";
  errorMsg += "Technical details: " + (error.message || "Unknown error");
  errorMsg += "\\n\\nSome translations may have been applied successfully.";
  errorMsg += "\\nYou can run the script again to continue processing.";
  alert(errorMsg);
}}"""
    
    # Save the script
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(jsx_content)
    
    print(f"✅ Final script generated: {output_file}")
    print(f"   - {translation_count} translations included")
    print(f"   - Ready to run in Adobe Illustrator")
    
    # Show breakdown by context
    print("\n📊 TRANSLATIONS BY CONTEXT:")
    if 'Context' in translated_df.columns:
        context_counts = translated_df['Context'].value_counts()
        for context, count in context_counts.items():
            print(f"   {context}: {count} translations")
    
    return translation_count

if __name__ == "__main__":
    generate_final_script()