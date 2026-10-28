/**
 * Google Apps Script (Code.gs) — Bi-Directional Portfolio Database Webhook
 * Bound to Google Sheet: https://docs.google.com/spreadsheets/d/1QvYmG86KlyvcsC-5nvnMpoWUakX2yFgCdXvxvjb9xjU/edit
 * Deploy as Web App -> Execute as: Me -> Who has access: Anyone
 */

function doPost(e) {
  var ss = SpreadsheetApp.openById("1QvYmG86KlyvcsC-5nvnMpoWUakX2yFgCdXvxvjb9xjU");
  var payload = JSON.parse(e.postData.contents);

  var tabMap = {
    "Personal_Info": [payload.personal_info],
    "Career_Summaries": payload.career_summaries,
    "Education": payload.education,
    "Skills": payload.skills,
    "Certifications": payload.certifications,
    "Projects": payload.projects,
    "Experience": payload.experience,
    "Achievements": payload.achievements,
    "Publications_Activities": payload.publications_activities,
    "Languages_Competencies": payload.languages_competencies
  };

  Object.keys(tabMap).forEach(function(tabName) {
    var rows = tabMap[tabName];
    if (!rows || rows.length === 0) return;
    var sheet = ss.getSheetByName(tabName) || ss.insertSheet(tabName);
    sheet.clearContents();
    var headers = Object.keys(rows[0]);
    sheet.appendRow(headers);
    rows.forEach(function(r) {
      var rowVals = headers.map(function(k) {
        var val = r[k];
        return Array.isArray(val) ? val.join(" | ") : (val !== undefined && val !== null ? String(val) : "");
      });
      sheet.appendRow(rowVals);
    });
  });

  return ContentService.createTextOutput(JSON.stringify({
    status: "success",
    updatedTabs: Object.keys(tabMap).length,
    sheetUrl: ss.getUrl()
  })).setMimeType(ContentService.MimeType.JSON);
}

function doGet(e) {
  var ss = SpreadsheetApp.openById("1QvYmG86KlyvcsC-5nvnMpoWUakX2yFgCdXvxvjb9xjU");
  var result = {};
  ss.getSheets().forEach(function(sheet) {
    var data = sheet.getDataRange().getValues();
    if (data.length < 2) return;
    var headers = data[0];
    result[sheet.getName()] = data.slice(1).map(function(row) {
      var obj = {};
      headers.forEach(function(h, idx) { obj[h] = row[idx]; });
      return obj;
    });
  });
  return ContentService.createTextOutput(JSON.stringify(result))
    .setMimeType(ContentService.MimeType.JSON);
}
