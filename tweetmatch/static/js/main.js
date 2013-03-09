//Find the elements
var overL = document.getElementById('label-left');
var overR = document.getElementById('label-right');
var underL = document.getElementById('underL');
var underR = document.getElementById('underR');
var footerBar = document.getElementById('fBar');
var footerContent = document.getElementById('fContent');

//Set the variables
var isExpanded = 0;

//BG hover stuff        
overL.onmouseover = function() {
    underL.style.background = 'blue';
};
overL.onmouseout = function() {
    underL.style.background = 'white';
};
overR.onmouseover = function() {
    underR.style.background = 'blue';
};
overR.onmouseout = function() {
    underR.style.background = 'white';
};

//Drawer stuff
function toggleDrawer() {
    footerContent.className = isExpanded ? 'drawerDown' : 'drawerUp';
    isExpanded = 1 - isExpanded;
};
footerBar.onclick = function() {
    toggleDrawer();
};
overL.onclick = function() {
    if(isExpanded) toggleDrawer();
};
overR.onclick = function() {
    if(isExpanded) toggleDrawer();
};

// practical code

$('input[type="radio"]').on('change', function() {
    $("#challenge-submit").click();
});

$('html').removeClass('no-js').addClass('js');
