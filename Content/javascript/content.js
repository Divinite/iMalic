// Content handler written in jQuery
// Makes editing specific parts of the website easy

$(document).ready(function(){
// the DOM is now ready to be manipulated...
     // Enable back button generation
     $('div[data-role="page"]').attr('data-add-back-btn', 'true');

     //Load the sections script
      $("#sections_content").load('../scripts/Sections.py');

});
