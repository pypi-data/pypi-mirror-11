/**
 * Guided Tour
 * 
 * @module GuidedTour
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:GuidedTour
 * 
 * @param {Object} settings
 */
function GuidedTour(settings) {
	this.name = 'ityou.guidedtour';
	this.version = '0.2.260814';

	// guide id tells us which guide template to use
	this.guideId = false;
	// bootstrapTour instance
	this.tour;
	// namespaces for identifying tours from local storage
	this.NAMESPACE;
	this.END = '_end';
	this.CURRENT_STEP = '_current_step';
	
	// settings
	this.settings = {
		initializer: '#btn-help',
		language: this.detectLanguage(),
		views: []
	}
	
	// language settings, need nothing to change here
	this.lang = {
		previous: $.i18n._('gtBack'),
		next: $.i18n._('gtNext'),
		end: $.i18n._('gtEnd')
	};
	
	// extend settings, e.g. with the views we want to use
	if(settings) {
		$.extend(this.settings, settings);
	}
	
	// read esi data and extract current-view
	var esi_data = $('#ESI_DATA').data(),
		currentView = esi_data != null ? (esi_data.hasOwnProperty('ityouView') ? esi_data.ityouView : false) : false;
		
	/**
	 * @returns {String}
	 */
	this.getGuideId = function() {
		return this.guideId;
	};
	
	/**
	 * set namespace for current tour
	 */
	this.setNamespace = function() {
		if(this.getGuideId()) {
			this.NAMESPACE = 'esi_' + this.getGuideId() + '_tour';
		}
	};
	
	/**
	 * create a help button, that triggers a guided tour
	 */
	this.createHelpButton = function() {
		$('<a href="javascript:void(0);" id="' + this.settings.initializer.substr(1) + '"><i class="fa fa-question"></i></a>').appendTo('body');
	};
	
	// check if current view is present in esi-data
	if(currentView) {
		// check if we want to start a tour for the given view
		var active = true,
			length = this.settings.views.length,
			i = 0;
		
		while(active && i != length) {
			var regex = new RegExp(this.settings.views[i], 'i');
			
			// test
			if(regex.test(currentView)) {
				active = false;
				
				// create a help trigger
				this.createHelpButton();
			}
			
			// save guide id
			this.guideId = currentView;
			
			// increase counter
			i++;
		}
		
		this.setNamespace();
	}
	
	/**
	 * get tour steps for the given guide id
	 * 
	 * @uses `@@guide?p=...` 
	 */
	this.getGuide = function() {
		// check if user already ended this tour
		// and if there is a guide id present (only if we defined it in view settings)
		if(!this.storage.local.get(this.NAMESPACE + this.END, true) && this.getGuideId()) {
			/** @uses `@@guide?p=...` */
			$.getJSON(this.settings.remote + '/@@guide' + this.settings.callback, {p: this.getGuideId()}, $.proxy(function(response) {
				if(!response.hasOwnProperty('error')) {
					// translation
					response = this.translate(response);
					
					// start guide only if there was no error returned from server
					this.guide(response);
				}
			}, this));
		}
	};
	
	/**
	 * translate title and content of each step
	 * 
	 * @param   {Array} data
	 * @returns {Array}
	 */
	this.translate = function(data) {
		var lang = eval('lang_' + this.settings.language);
		
		$.each(data, $.proxy(function(i, value) {
			data[i].title = lang[this.getGuideId()]['step_' + (i+1)].title;
			data[i].content = lang[this.getGuideId()]['step_' + (i+1)].content;
		}, this));
		
		return data;
	};
	
	/**
	 * start bootstrap tour
	 * 
	 * @param {Array} data
	 */
	this.guide = function(data) {
		// reset tour history
		this.storage.local.unset(this.NAMESPACE + this.END);
		this.storage.local.unset(this.NAMESPACE + this.CURRENT_STEP);
		
		// initialize bootstrap tour
		this.tour = new Tour({
			name: this.NAMESPACE,
			onStart: $.proxy(function() {
				$(this.settings.initializer).addClass('help-active');
			}, this),
			onEnd: $.proxy(function() {
				$(this.settings.initializer).removeClass('help-active');
			}, this),
			template: '<div class="popover tour">' +
				'<div class="arrow"></div>' +
				'<h3 class="popover-title"></h3>' + 
				'<div class="popover-content"></div>' +
				'<div class="popover-navigation">' +
					'<div class="btn-group">' +
						'<button class="btn btn-default" data-role="prev">&laquo; ' + this.lang.previous + '</button>' +
						'<button class="btn btn-default" data-role="next">' + this.lang.next + ' &raquo;</button>' +
					'</div>' +
					'<button class="btn btn-default" data-role="end">' + this.lang.end + '</button>' +
				'</div>' +
			'</div>'
		});
		
		// add steps for tour
		for(var i in data) {
			this.tour.addStep(data[i]);
		}
		
		// set current step to first step
		this.tour.setCurrentStep(null);
		
		// init & start tour
		this.tour.init();
		this.tour.start();
	};
	
	/** @events click handler if user clicks help button */
	$(document).on('click', this.settings.initializer, $.proxy(function(e) {
		e.preventDefault();
		
		// user want to start a tour, reset tour history for current namespace
		this.storage.local.unset(this.NAMESPACE + this.END);
		this.storage.local.unset(this.NAMESPACE + this.CURRENT_STEP);
		
		// reset the tour, if it already exists
		if(this.tour) {
			this.tour.setCurrentStep(null);
		}
		
		// re-get guide data
		this.getGuide();
	}, this));
};


// inherits functionality of `module:Utilities`
/** @uses module:Utilities */
GuidedTour.prototype = new Utilities();