// This is a custom handler written by A3MIRAL that tackles the setup of every page
// The main use of this is to keep code isolated and therefore easy to fix, add, and enchance the pages all at the same time
// This is refered to as a CMS. Although it is unusual for it to be written in a client side language, I don't know mush python and we aren't using PHP, so this is my option :)

// Since all the jQuery requirements are already called, let's begin setting up our interface.

// We are only defining functions that can be called by the page that needs them.

// Function to load sections list
function loadSections(){
 $('#sections_list').load('../scripts/Sections.py');
}




