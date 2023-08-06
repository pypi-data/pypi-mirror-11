/**
 * Main part of the JavaScript part of `esi_theme`.
 * Within this file, we're initialising all plugins.
 * The object of this file is created in `init.js`    
 * 
 * @module ItyouApplication
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:ItyouApplication
 * 
 * @param {String} callback
 * @param {Object} libSettings
 */
function Ityou(callback, libSettings) {
	this.name = 'ityou.application';
	this.version = '0.1.260814';
	
	// temp storage
	this.cache = {
		serverResponse: false,
		libs: {
			backtotop: null,
			dragdrop: null,
			extuserprofile: null,
			guidedtour: null,
			statusflags: null,
			thumbnails: null
		}
	};
	
	// settings
	this.settings = {
		language: this.detectLanguage(),
		userId: null,
		ajax: {
			remote: '',
			callback: callback
		},
		breakpoints: {
			xs: 480,
			sm: 768,
			md: 1024,
			lg: 1440
		},
		selector: {
			notifyAstream: '#link-to-astream',
			notifyImessage: '#link-to-imessage'
		},
		libs: {
			astream: {
				moderatable: false
			},
			backtotop: {},
			dragdrop: {},
			extuserprofile: {},
			guidedtour: {},
			imessage: {
				useWYSIWYG: false
			},
			thumbnails: {},
			whoisonline: {
				refreshState: 1000
			}
		}
	};
	
	// extend library settings
	if(libSettings) {
		$.extend(this.settings.libs, libSettings);
	}
	
	// save instances for debugging
	this.setInstance = function(name, instance) {
		this.cache.libs[name] = instance;
	};
	
	// initialize application
	this.constructor();
};

// inherits functionality of `module:Utilities`
/** @uses module:Utilities */
Ityou.prototype = new Utilities();


/**
 * Collect Settings and build things up
 * 
 * @uses `@@ajax-personal-profile`
 */
Ityou.prototype.initialize = function() {
	// load the JS dictionary `ityou.i18n.lang-dict.js`
	this.loadDictionary(window['lang_' + this.settings.language]);
	
	// read settings from DOM
	var data = $('#ESI_DATA').data();
	
	// memorize settings
	this.settings.userId = data.ityouUid;
	this.settings.ajax.remote = data.ityouPortalUrl;
	
	// check if the moderatable flag is set. if it's not set, default value = false.
	this.settings.libs.astream.moderatable = data.ityouCommentFlag === undefined ? false : (parseInt(data.ityouCommentFlag) === 0 ? false : true);
	
	// if the portal url has a slash at its ending, remove it
	if(!!this.settings.ajax.remote && this.settings.ajax.remote.charAt(this.settings.ajax.remote.length-1) === '/') {
		this.settings.ajax.remote = this.settings.ajax.remote.substr(0, this.settings.ajax.remote.length-2);
	}
	
	// replace links in notify area
	$(this.settings.selector.notifyAstream).attr('href', (this.settings.ajax.remote + '/@@activities'));
	$(this.settings.selector.notifyImessage).attr('href', (this.settings.ajax.remote + '/@@messages'));
	
	// Personal Tools
	// --------------
	// check if profile data is already stored in the `session` storage
	if(this.storage.session.get('userId') !== null && this.storage.session.get('portraitDefault') !== null && this.storage.session.get('portraitIcon') !== null && this.storage.session.get('profileURI') !== null && this.storage.session.get('homeFolderURI') !== null && this.storage.session.get('imessageURI') !== null && this.storage.session.get('portalUrl')) {
		this.personalToolbar({
			uid: this.storage.session.get('userId'),
			portraitDefault: this.storage.session.get('portraitDefault'),
            portraitIcon: this.storage.session.get('portraitIcon'),
            profileUrl: this.storage.session.get('profileUrl'),
            portalUrl: this.storage.session.get('portalUrl'),
            homefolderUrl: this.storage.session.get('homefolderUrl'),
            imessageUrl: this.settings.ajax.remote + '/@@messages'
		});
	} else {
		if(data.ityouProfileUrl !== undefined) {
			this.storage.session.set('profileUrl', data.ityouProfileUrl);
		}
		
		if(data.ityouPortalUrl !== undefined) {
			this.storage.session.set('portalUrl', data.ityouPortalUrl);
	    }
	    
	    if(data.ityouHomefolderUrl !== undefined) {
	    	this.storage.session.set('homefolderUrl', data.ityouHomefolderUrl);
	    }
	    
	    if(data.ityouImessageUrl !== undefined) {
	    	this.storage.session.set('imessageUrl', this.settings.ajax.remote + '/@@messages');
	    }
	    
	    // there is no profile data in the `session` storage, we need to get it via an ajax request
	    $.getJSON(this.settings.ajax.remote + '/@@ajax-personal-profile' + this.settings.ajax.callback, {action: 'whoami'}, $.proxy(function(response) {
	        if(response.user_id != null) {
	            // 128 thumb, 64 tile, 32 icon, 16 micro
	            $.getJSON(this.settings.ajax.remote + '/@@ajax-personal-profile' + this.settings.ajax.callback, {action: 'whoami', portrait_size: 'icon'}, $.proxy(function(small_portrait) {
                    $('#personal-tools').find('img.xs').attr('src', small_portrait.portrait);
                    
                    // save profile data to the `session` storage
                    this.storage.session.set('portraitIcon', small_portrait.portrait);
                }, this));
                
                this.personalToolbar({
                    uid: response.user_id,
                    portraitDefault: response.portrait,
                    portraitIcon: this.storage.session.get('portraitIcon'),
                    profileUrl: this.storage.session.get('profileUrl'),
                    portalUrl: this.storage.session.get('portalUrl'),
                    homefolderUrl: this.storage.session.get('homefolderUrl'),
		            imessageUrl: this.storage.session.get('imessageUrl')
                });
                
                // save userid and portrait to `session` storage
                this.storage.session.set('userId', response.user_id);
                this.storage.session.set('portraitDefault', response.portrait);
            }
	    }, this));
	}
	
	// translate sidepanel
	this.sidepanel();
};


/**
 * Build the personal toolbar in the header area.
 * 
 * @param {Object} options
 */
Ityou.prototype.personalToolbar = function(options) {
	// if the portal url has no slash at its end, add it
    options.portalUrl += options.portalUrl.charAt(options.portalUrl.length-1) !== '/' ? '/' : '';

    if(options.portraitIcon !== undefined) {
    	// if there's a portrait icon given in the options, change the source of the small image in the header
        $('#personal-tools').find('img.xs').attr('src', options.portraitIcon);
    }
    
    // change the source of the large portrait
    $('#personal-tools').find('img').not('.xs').attr('src', options.portraitDefault);

    // loop through each list element in the personal tools dropdown
    $('#personal-tools').find('ul').find('li:not(.divider)').each($.proxy(function(k, el) {
        var $el = $(el).find('a');
        
        // change the href location of each link in the list elements
        if(options.hasOwnProperty($el.data('type'))) {
            $el.attr('href', options[$el.data('type')]);
        } else {
            $el.attr('href', options.portalUrl + $el.data('type'));
        }
        
        // translation
        $el.text($.i18n._('pt' + this.capitalizeFirstLetter($el.data('type'))));
    }, this));
};


Ityou.prototype.sidepanel = function() {
	// translation
	$('#sidemenu').find('li').each($.proxy(function(i, el) {
		$(el).removeClass('plain');
		
		var cn = $(el).attr('class');
		
		if($.i18n.dict.hasOwnProperty('sidepanel-' + cn)) {
			$(el).find('a').text($.i18n._('sidepanel-' + cn));
		}
	}, this));
};


/**
 * Initialise and start our JavaScript Application
 */
Ityou.prototype.constructor = function() {
	// load settings from DOM
	this.initialize();
	
	
	// StatusFlags
	// ----------------------------------------------------------------------
	var statusFlags = new StatusFlags({
		astream: this.settings.libs.astream,
		imessage: this.settings.libs.imessage,
		whoisonline: this.settings.libs.whoisonline
	}, this.settings.ajax);
	statusFlags.init();
	// save instance to cache to make it accessible for debugging
	this.setInstance('statusflags', statusFlags);
	// ----------------------------------------------------------------------
	
	
	// BackToTop Button
	// ----------------------------------------------------------------------
	var backToTop = new BackToTop(this.settings.libs.backtotop);
	// save instance to cache to make it accessible for debugging
	this.setInstance('backtotop', backToTop);
	// ----------------------------------------------------------------------
	
	
	// Guided Tour
	// ----------------------------------------------------------------------
	var guidedTour = new GuidedTour($.extend(this.settings.libs.guidedtour, this.settings.ajax));
	// save instance to cache to make it accessible for debugging
	this.setInstance('guidedtour', guidedTour);
	// ----------------------------------------------------------------------
	
	
	// dont load this plugin's if editing or creating a new document
	if(!this.checkTemplate()) {
		// ThumbnailView
		// ----------------------------------------------------------------------
		var thumbnails = new ThumbnailView(this.settings.ajax);
	    thumbnails.init();
	    // save instance to cache to make it accessible for debugging
	    this.setInstance('thumbnails', thumbnails);
	    // ----------------------------------------------------------------------
		
	    
	    // DragAndDrop
	    // ----------------------------------------------------------------------
		var dragAndDrop = new DragDrop(this.settings.ajax, thumbnails);
		dragAndDrop.init();
		// save instance to cache to make it accessible for debugging
		this.setInstance('dragdrop', dragAndDrop);
		// ----------------------------------------------------------------------
	
		
	    // ExtUserProfile
	    // ----------------------------------------------------------------------
		var userDatatables = new UserDatatables(this.settings.ajax, statusFlags.whoisonline);
		userDatatables.init();
		// save instance to cache to make it accessible for debugging
		this.setInstance('extuserprofile', userDatatables);
		// ----------------------------------------------------------------------
	}
	
	
};
