// all depends have been loaded already
// there is no reliable way to accomplish this anyways




// This function fixes the dock's current tab based on the active #page or if no page by the URL

$('div').live('pageshow',function(){
	$('#contain-dock').load("../includes/dock.html");
});