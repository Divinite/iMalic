<script type="text/javascript">

function showMenu(){
$('#menu').toggle();
alert('yup');
}
$('#app-3-link').click(function(){
 $('#contain-the-dock').load('../includes/dock.html');
});
var parsedUrl=$.mobile.path.parseUrl(window.location.href);
var filename=parsedUrl.filename;


var app1="home.html";
var app2="packages.html";
var app3="sections.html";
var app4="sources.html";

if (filename == app1){
 document.getElementById("app-1").setAttribute("src","../images/home-active.png");
 document.getElementById("app-1-link").setAttribute("href","javascript:showMenu();");
} else if (filenane == app2){
 document.getElementById('app-2').setAttribute("src","../images/packages-active.png");
 document.getElementById("app-2-link").setAttribute("href","javascript:showMenu();");
} else if (filenane == app3){
 document.getElementById('app-2').setAttribute("src","../images/sections-active.png");
 document.getElementById("app-3-link").setAttribute("href","javascript:showMenu();");
} else if (filenane == app4){
 document.getElementById('app-2').setAttribute("src","../images/sources-active.png");
 document.getElementById("app-4-link").setAttribute("href","javascript:showMenu();");
}
</script>