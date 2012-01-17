// Style handler written in jQuery

//Using jQuery selectors to create global styles based on tags and other criteria with ease

$(document).ready(function(){
//the DOM is now ready to e manipulated...

     // all footer tags will now be fixed to the bottom correctly
     $('footer').css({'position': 'fixed', 'bottom': '0', 'left': '0', 'width': '100%'});

//end
});