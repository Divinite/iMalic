$(document).bind("mobileinit", function(){
	$.mobile.page.prototype.options.addBackBtn= true;
});
 function loadFooter(){
	$('footer').load('files/footer.txt');
	$('footer').css({'position': 'fixed', 'bottom': '0', 'left': '0'});
}