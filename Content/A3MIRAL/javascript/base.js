// all depends have been loaded already
// there is no reliable way to accomplish this anyways




$('#home').live('pageshow',function(){
 $('#contain-dock').load("../includes/dock-home.html");
});
$('#sections').live('pageshow',function(){
 $('#contain-dock').load("../includes/dock-sections.html");
});
$('#packages').live('pageshow',function(){
 $('#contain-dock').load("../includes/dock-packages.html");
});
$('#sources').live('pageshow',function(){
 $('#contain-dock').load("../includes/dock-sources.html");
});
$.mobile.loadPage('../includes/menu.html', { showLoadMsg: false } );