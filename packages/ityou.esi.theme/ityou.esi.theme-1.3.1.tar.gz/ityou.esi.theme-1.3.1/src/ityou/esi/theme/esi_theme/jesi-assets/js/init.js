/**
 * Settings for Plugins here
 * 
 * Possible Settings with default values
 * 
 * BackToTop Settings: {
 * 	button		: '#back-to-top',
 * 	text		: 'Back to Top',
 * 	min			: 5,
 * 	minWidth	: 480,
 * 	fadeIn	   	: 400,
 * 	fadeOut    	: 400,
 * 	scrollSpeed	: 800,
 * 	easingType 	: 'easeInOut'
 * }
 * 
 * GuidedTour Settings: {
 *  initializer: '#btn-help',
 * 	views: []
 * }
 */


$(function() {
	var libSettings = {
		astream: {},
		backtotop: {
			min: 200
		},
		dragdrop: {},
		extuserprofile: {},
		guidedtour: {
			views: [
		        'activities'
	        ]
		},
		imessage: {},
		thumbnails: {},
		whoisonline: {
			refreshState: 2000
		}
	};	
	
	
	var ityou = new Ityou('', libSettings);
	
	// debugging only
	// ----------------------------------------------------------------------
	window.ityouDebugging = ityou;
	// ----------------------------------------------------------------------
	
	
	// if you need to clear local/session storage
	// uncomment following lines
	//ityou.storage.local.clear();
	//ityou.storage.session.clear();
	
	
	// Fixes issue #386
	if($.fn.multiSelect === undefined) {
		$.fn.multiSelect = function(){};
	}
});
