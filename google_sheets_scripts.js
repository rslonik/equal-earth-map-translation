function populateTranslations() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const csvSheet = spreadsheet.getSheetByName("CSV");

  if (!csvSheet) {
    throw new Error("CSV sheet not found");
  }

  // Get all data from CSV sheet
  const csvData = csvSheet.getDataRange().getValues();
  const headerRow = csvData[0];

  // Find column indices
  const textColumnIndex = headerRow.indexOf("Text");
  const translationColumnIndex = headerRow.indexOf("Translation");

  if (textColumnIndex === -1 || translationColumnIndex === -1) {
    throw new Error("Text or Translation column not found in CSV sheet");
  }

  // Get all sheets except CSV
  const allSheets = spreadsheet.getSheets();
  const translationSheets = allSheets.filter(
    (sheet) => sheet.getName() !== "CSV",
  );

  // Create a lookup map from all translation sheets
  const translationMap = {};

  translationSheets.forEach((sheet) => {
    const sheetData = sheet.getDataRange().getValues();

    // Skip header row and process data
    for (let i = 1; i < sheetData.length; i++) {
      const key = sheetData[i][0]; // Column A (English)
      const value = sheetData[i][1]; // Column B (Portuguese)

      if (key && value) {
        // Store both original key and cleaned key (without \r)
        translationMap[key] = value;
        translationMap[key.replace(/\\r/g, " ")] = value;
        translationMap[key.replace(/\r/g, " ")] = value;
      }
    }
  });

  // Process CSV data and update translations
  const updates = [];

  for (let i = 1; i < csvData.length; i++) {
    const textValue = csvData[i][textColumnIndex];

    if (textValue) {
      let translation = "";
      let hasBackslashR = textValue.includes("\\r");

      // Try exact match first
      if (translationMap[textValue]) {
        translation = translationMap[textValue];
      }
      // Try with \r replaced by space
      else if (translationMap[textValue.replace(/\\r/g, " ")]) {
        translation = translationMap[textValue.replace(/\\r/g, " ")];
      }
      // Try with actual carriage return replaced by space
      else if (translationMap[textValue.replace(/\r/g, " ")]) {
        translation = translationMap[textValue.replace(/\r/g, " ")];
      }

      // If translation found and original text had \r, add \r to translation
      if (translation && hasBackslashR) {
        translation = translation.replace(/ /g, "\\r");
      }

      if (translation) {
        updates.push([i + 1, translationColumnIndex + 1, translation]);
      }
    }
  }

  // Apply all updates at once for better performance
  updates.forEach((update) => {
    csvSheet.getRange(update[0], update[1]).setValue(update[2]);
  });

  Logger.log(`Updated ${updates.length} translations`);
  return `Updated ${updates.length} translations`;
}

// Alternative function to get translation for a single text value
function getTranslation(textValue) {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const allSheets = spreadsheet.getSheets();
  const translationSheets = allSheets.filter(
    (sheet) => sheet.getName() !== "CSV",
  );

  let hasBackslashR = textValue.includes("\\r");

  // Search through all translation sheets
  for (let sheet of translationSheets) {
    const sheetData = sheet.getDataRange().getValues();

    for (let i = 1; i < sheetData.length; i++) {
      const key = sheetData[i][0]; // Column A (English)
      const value = sheetData[i][1]; // Column B (Portuguese)

      if (key && value) {
        // Check for exact match or match with \r handling
        if (
          key === textValue ||
          key === textValue.replace(/\\r/g, " ") ||
          key.replace(/\\r/g, " ") === textValue
        ) {
          // If original text had \r, add \r to translation
          if (hasBackslashR && value.includes(" ")) {
            return value.replace(/ /g, "\\r");
          }

          return value;
        }
      }
    }
  }

  return ""; // Return empty string if no translation found
}

// Custom formula function - use this in spreadsheet cells
function TRANSLATE(textValue) {
  return getTranslation(textValue);
}

function s2csv() {
  var s, d, sname, vals, f;
  d = ";"; //<<<set the desired delimiter
  s = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sname = s.getName();
  vals = s
    .getDataRange()
    .getValues()
    .map(function (x) {
      return x.join(d);
    })
    .join("\n");
  f = DriveApp.createFile(sname + ".csv", vals, MimeType.CSV);
}
