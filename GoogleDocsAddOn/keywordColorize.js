// colorize keywords like "bought", "sold", and tickers "$..."
function colorize() {
  console.log('starting... word-coloring');
  var body = DocumentApp.getActiveDocument().getBody();
  bodyText = body.editAsText(); // convert to "text" obj to apply formatting
  
  // search for "bought"
  searchPattern = "\W*((?i)bought(?-i))\W*" // this grabs the entire sentence instead of just "bought"
  boughtText = bodyText.findText(searchPattern)
  
  // no matches
  if (boughtText == null){
    console.log('no matches')
    return
  }
  // format the match 
  boughtInstances = boughtText.getElement();
  console.log("applying to: " + boughtInstances.getText())
  boughtInstances.setForegroundColor("#39bf75");
}