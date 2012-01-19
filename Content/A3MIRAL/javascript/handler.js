// Configure directories
// Relative to the ages they are called into action in
var sections="../../scripts/Sections.py";
var dock="../includes/dock.html";


// Let's get all our depends in line..
// Define functions
function loadSections(){
 $('#sections').load(sections);
}

function loadDock(){
 $('#contain-the-dock').load(dock);
}
