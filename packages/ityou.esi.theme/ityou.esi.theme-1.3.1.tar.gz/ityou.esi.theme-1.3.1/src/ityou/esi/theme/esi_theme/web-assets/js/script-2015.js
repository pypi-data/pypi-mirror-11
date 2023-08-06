/*
$(function() {
	$("#tabswitcher").tabs("div.divtab", {event:'mouseover'});
});
*/


<!-- Original: Ronnie T. Moore -->
<!-- Dynamic 'fix' by: Nannette Thacker -->
function textCounter(field, countfield, maxlimit) {
    var fieldval = $(field).attr('value');
    if (fieldval.length > maxlimit) {
        // if too long...trim it!
        $(field).attr('value', fieldval.substring(0, maxlimit));
        alert( 'Sie können nur bis zu  ' + maxlimit + ' Zeichen eingeben.' );
    }
    // update 'characters left' counter
    $('input[name="' + countfield + '"]').attr('value', Math.max(maxlimit - fieldval.length, 0));
}


// =============== JQ ANFANG ================================
$(document).ready(				
    function () { 
                      	
        // BEGIN ------
                
        // --- ? ----------------------------------------        
        var mc = $("#carousel").msCarousel({
            boxclass:'.set', 
            defaultid:0, 
            height:240, 
            width:958, 
            autoSlide:10000}).data("msCarousel");
 		
        // --- /? ---------------------------------------     
        $('img').remove(".downarrowclass");
       
       
        // END ---
    }
); 
// ============ JQ ENDE =======================================


