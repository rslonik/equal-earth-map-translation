// Text Extraction with Encoding Fix - Version: 20250713.0857
// Handles special characters and encoding issues

function extractWithEncodingFix() {
  var doc = app.activeDocument;

  // Create file with UTF-8 encoding in v3 tmp_files folder
  // FULL PATH for Illustrator know where to save.
  var csvFile = new File(
    "/Users/rs/qgis/equal-earth-translation/map-translation-v3/tmp_files/extracted_text_elements_utf8.csv",
  );
  csvFile.encoding = "UTF-8";
  csvFile.open("w");

  // Write UTF-8 BOM (Byte Order Mark) for better compatibility
  csvFile.write("\uFEFF");

  // Write header
  csvFile.write("ID;Text;Layer;X;Y;Width;Height\n");

  var validCount = 0;
  var totalProcessed = 0;

  // Process all text frames
  for (var i = 0; i < doc.textFrames.length; i++) {
    totalProcessed++;
    var textFrame = doc.textFrames[i];
    var text = textFrame.contents;

    // Clean text
    text = text.replace(/^\s+|\s+$/g, "");

    if (!text || text.length === 0) {
      continue;
    }

    validCount++;

    // Get layer name
    var layerName = "Unknown";
    try {
      if (textFrame.layer && textFrame.layer.name) {
        layerName = textFrame.layer.name;
      }
    } catch (e) {}

    // Get position
    var x = 0,
      y = 0,
      width = 0,
      height = 0;
    try {
      var bounds = textFrame.geometricBounds;
      x = Math.round(bounds[0]);
      y = Math.round(bounds[1]);
      width = Math.round(bounds[2] - bounds[0]);
      height = Math.round(bounds[1] - bounds[3]);
    } catch (e) {}

    // Clean special characters that might cause encoding issues
    var cleanText = cleanForCSV(text);
    var cleanLayer = cleanForCSV(layerName);

    // Write line
    csvFile.write(
      validCount +
        ';"' +
        cleanText +
        '";"' +
        cleanLayer +
        '";' +
        x +
        ";" +
        y +
        ";" +
        width +
        ";" +
        height +
        "\n",
    );

    // Show progress every 500 elements
    if (validCount % 500 === 0) {
      // Progress indicator
    }
  }

  csvFile.close();

  alert(
    "🎉 EXTRACTION COMPLETE!\n\n" +
      "📊 RESULTS:\n" +
      "   Total elements: " +
      validCount +
      "\n\n" +
      "📁 FILE CREATED:\n" +
      "   • tmp_files/extracted_text_elements_utf8.csv\n\n" +
      "✅ NEXT STEP:\n" +
      "   Run: python3 generate_translation_csv.py\n" +
      "   to create the editable translation spreadsheet!",
  );
}

// Function to clean text for CSV with proper line break handling
function cleanForCSV(text) {
  // Escape quotes
  text = text.replace(/"/g, '""');

  // Replace line breaks with \r escape sequence (preserves them as text for Illustrator)
  text = text.replace(/\r\n/g, "\\r");
  text = text.replace(/\r/g, "\\r");
  text = text.replace(/\n/g, "\\r");

  // Handle common problematic characters
  text = text.replace(/'/g, "'"); // Replace smart quotes
  text = text.replace(/'/g, "'");
  text = text.replace(/"/g, '"');
  text = text.replace(/"/g, '"');
  text = text.replace(/–/g, "-"); // Replace en dash
  text = text.replace(/—/g, "-"); // Replace em dash
  text = text.replace(/…/g, "..."); // Replace ellipsis

  return text;
}

// Run extraction
try {
  if (app.documents.length === 0) {
    alert("Please open your map document first.");
  } else {
    extractWithEncodingFix();
  }
} catch (error) {
  alert("❌ EXTRACTION FAILED: " + error.message);
}
