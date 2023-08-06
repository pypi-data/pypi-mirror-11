$(document).ready(function() {

    // ====== ANFANG

    //  activity steam notify
    var NOTIFY_REPEAT = 10000; // milisekunden
    //var latest_activity_timestamp = $.cookie('latest-activity-timestamp');
    var latest_activity_timestamp = window.ITYOU.storage.get('activitiesTimestamp');
	
    // --- notify-viewlet ------------------------------------------------
    function notify_activities(latest_activity_timestamp) {
        $.getJSON("@@ajax-notify", {action: 'count_latest_activities', timestamp: latest_activity_timestamp}, function(data) {
            $('#activities-counter').text(data);
            
            if(data > 0) {
                $('#activities-counter').removeClass('badge-hide');
            } else {
                $('#activities-counter').addClass('badge-hide');
            }
        });       	
    }
    
    
	//  activities
	/*if (latest_activity_timestamp) {        
        notify_activities(latest_activity_timestamp);
        setInterval( function () {
        	notify_activities(latest_activity_timestamp);
        }, NOTIFY_REPEAT); 
    };*/
	
	
	// ====== ENDE
});
