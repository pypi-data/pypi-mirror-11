/**
 * Back to top button
 * 
 * @module BackToTop
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:BackToTop
 */
function BackToTop(settings) {
	this.name = 'ityou.backtotop';
	this.version = '0.2.260814';
	
	// temp storage
	this.cache = {
		oldiOS: false,
		oldAndroid: false
	};
	
	// settubgs
	this.settings = {
		button: '#back-to-top',
		text: 'Back to Top',
		min: 5,
		minWidth: 480,
		fadeIn: 400,
		fadeOut: 400,
		scrollSpeed: 800,
		easingType: 'easeInOut'
	};
	
	if(settings) {
		$.extend(this.settings, settings);
	}
	
	// initializer
	this.init = function() {
		// detect client's operating system
		this.detectOS();
		
		// append our button to the `body`
		$('body').append('<a href="#" id="' + this.settings.button.substring(1) + '" title="' + this.settings.text + '">' + this.settings.text + '</a>');
		
		/** @events	define what to do if user clicks on button (e.g. scroll top) */
		$(document).on('click', this.settings.button, $.proxy(function(e) {
			e.preventDefault();
			
			// animate the scrolling
			$('html, body').animate({
				scrollTop: 0
			}, this.settings.scrollSpeed);
		}, this));
		
		/** @events	scroll event handling for showing/hiding the button at a certain position */
		$(window).scroll($.proxy(function() {
			var position = $(window).scrollTop();
			
			// bug fixing on old ios devices
			if(this.cache.oldiOS) {
				$(this.settings.button).css({
					position: 'absolute',
					top: position + $(window).height()
				});
			}
			
			if(position > this.settings.min && $(window).width() > this.settings.minWidth) {
				$(this.settings.button).fadeIn(this.settings.fadeIn);
			} else {
				$(this.settings.button).fadeOut(this.settings.fadeOut);
			}
		}, this));
	};
	
	// operating system detection for apple and android
	this.detectOS = function() {
		if(/(iPhone|iPod|iPad)\sOS\s[0-4][_\d]+/i.test(navigator.userAgent)) {
			this.cache.oldiOS = true;
		} else if(/Android\s+([0-2][\.\d]+)/i.test(navigator.userAgent)) {
			this.cache.oldAndroid = true;
		}
	};
	
	this.init();
};
