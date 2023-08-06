/**
 * whoisonline-plugin for filling whoisonline-portlet
 * 
 * @module WhoIsOnline
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:WhoIsOnline
 */
function WhoIsOnline(settings) {
	this.name = 'ityou.whoisonline';
	this.version = '0.3.260814';
	
	// temp storage
	this.cache = {};
    
    // settings
    this.settings = {
        timeout: 0,
        delta: 0,
        
        refreshState: 1000
    };
    
    // selector settings
    this.selector = {
        list: '#who-is-online ul',
        portlet: '.portletWhoIsOnline',
        profileBox: '.userprofile-box',
        profile: '.who-is-online-box',
        
        counter: '#whoisonline-counter'
    };
    
    // template settings
    this.template = {
        whoisonline: '#whoisonline-tmpl',
        profile: '#whoisonline-profile-tmpl'
    };
    
    /**
     * @param   {String} key
     * @returns {String}
     */
    this.getSelector = function(key) {
        return this.get(key, 'selector');
    };
    
    /**
     * @param   {String} key
     * @returns {String}
     */
    this.getTemplate = function(key) {
        return this.get(key, 'template');
    };
    
    /**
     * @param   {String} key
     * @returns {Object|Array|String|Number|Boolean}
     */
    this.getCache = function(key) {
        return this.get(key, 'cache');
    };
    
    /**
     * @param   {String} key
     * @returns {Object|Array|String|Number|Boolean}
     */
    this.getSettings = function(key) {
        return this.get(key, 'settings');
    };
    
    /**
     * @param {String} key
     * @param {Object|Array|String|Number|Boolean} value
     */
    this.setCache = function(key, value) {
        return this.set(key, value, 'cache');
    };
    
    /**
     * @param {String} key
     * @param {String} property
     * @returns {Object|Array|String|Number|Boolean}
     */
    this.get = function(key, property) {
        if(this.hasOwnProperty(property) && this[property].hasOwnProperty(key)) {
            return this[property][key];
        }
        
        return undefined;
    };
    
    /**
     * @param   {String} key
     * @param   {Object|Array|String|Number|Boolean} value
     * @param   {String} property
     * @returns {WhoIsOnline}
     */
    this.set = function(key, value, property) {
        this[property][key] = value;
        return this;
    };
    
    /**
     * @param {Object} settings
     */
    this.setSettings = function(settings) {
    	if(settings) {
    		this.settings = $.extend(this.settings, settings);
    	}
    };
    
    // attach event handler
    this.attachEventHandler();
};

// inherits functionality of `module:Utilities`
/** @uses module:Utilities */
WhoIsOnline.prototype = new Utilities();

/** @uses module:ClientTimezone */
WhoIsOnline.prototype.timezone = new ClientTimezone();


/**
 * helper function to check if the `whoisonline portlet` exists
 * 
 * @returns {Boolean}
 */
WhoIsOnline.prototype.hasPortlet = function() {
    if($(this.getSelector('portlet')).length > 0) {
        return true;
    }
    
    return false;
};


/**
 * show the count online users
 * 
 * @param {Array} data
 */
WhoIsOnline.prototype.counter = function(data) {
	$(this.getSelector('counter')).text(data.length);

	if(data.length === 0) {
		$(this.getSelector('counter')).addClass('hidden');
	} else {
		$(this.getSelector('counter')).removeClass('hidden');
	}
};


/**
 * mark users who are online with a `green badge` on their portrait (including user himself)
 * 
 * @param {Array} data
 */
WhoIsOnline.prototype.onPortrait = function(data) {
	var run = true;
	
	// do nothing if no data is given
	if(false === data) {
		run = false;
		data = this.getCache('online');
	}
	
	// push user's id into data array
	data.push({id:$('#ESI_DATA').data('ityou-uid')});
	
	// add a `green online badge` to each portrait in the data array
	$.each(data, $.proxy(function(i, val) {
		$('body').find('.user-portrait[data-uid="' + val.id + '"]').each($.proxy(function(k, el) {
			if($(el).find('.online-status').length === 0) {
				// add it only if it's not already there
				$(el).append('<div class="online-status online"></div>');
			}
		}, this));
	}, this));
	
	// if data array was ok (without users own id)
	// we need to perform extra run, e.g. whoisonline was triggered and someone came online
	if(run) {
		var x = 0, y = 0;
		var t = setInterval($.proxy(function() {
			y++;
			
			if((y > 10 && x === 0)) {
				clearInterval(t);
			} else {
				x = 0;
				$.each(data, $.proxy(function(i, val) {
					$('body').find('.user-portrait[data-uid="' + val.id + '"]').each($.proxy(function(k, el) {
						if($(el).find('.online-status').length === 0) {
							x++;
							$(el).append('<div class="online-status online"></div>');
						}
					}, this));
				}, this));
			}
		}, this), 350);
	}
};


/**
 * helper function to get all online users
 * 
 * @uses `@@ajax-whoisonline?time_client=...`
 */
WhoIsOnline.prototype.getAll = function() {
    clearInterval(this.getCache('opacity'));

    // ajax-request
    /** @uses `@@ajax-whoisonline?time_client=...` */
    $.ajax({
        url: this.settings.ajax.remote + '/@@ajax-whoisonline' + this.settings.ajax.callback,
        data: {
        	// current time as unix timestamp
            time_client: (new Date()).getTime() / 1000
        },
        dataType: 'json',
        timeout: 30000,
        // event handler success
        success: $.proxy(function(response) {
        	// save result of online users
        	this.setCache('online', response);
        	
        	// check if portlet exists
        	if(this.hasPortlet()) {
        		// andcheck if someones online except user himself
	            if(response.length > 0) {
	                this.render(response);
	                // show portlet
	                $(this.getSelector('portlet')).show();
	            } else {
	                // clear box
	                $(this.getSelector('list')).empty();
	                // hide portlet
	                $(this.getSelector('portlet')).hide();
	            }
        	}
        	
        	// trigger additional events
    		this.onPortrait(response);
    		this.counter(response);
        }, this),
        // event handler error
        error: $.proxy(function(XMLHttpRequest, textStatus, errorThrown) {
            
        }, this)
    });
};


/**
 * render data in `whoisonline-portlet`
 * 
 * @uses `ityou.whoisonline/ityou/whoisonline/portlets/whoisonline.pt:43`
 * 
 * @param {Array} data	{profile, portrait, bar, id, recent_time, timeout_online, time_delta}
 */
WhoIsOnline.prototype.render = function(data) {
    var tmp = this.getCache('userlist');
    this.setCache('userlist', data);
    
    var $tmpl = $(this.getTemplate('whoisonline')),
        $list = $(this.getSelector('list'));
        
    if(data.length > 0) {
        this.set('timeout', data[0].timeout_online, 'settings');
        this.set('delta', data[0].time_delta, 'settings');
    }
    
    // loop over data
    $.each(data, $.proxy(function(key, value) {
        var $li = $list.find('li[data-id="' + value.id + '"]');

        // rendering if user is not in portlet
        if($li.length === 0) {
        	/** @uses `ityou.whoisonline/ityou/whoisonline/portlets/whoisonline.pt:43` */
            $li = $($tmpl.render(value));
            $li.appendTo(this.getSelector('list'));
        }
        
        $li.find('img').css('opacity', value.bar);
        
        // render tooltips
        this.renderTooltip(value, $li);
    }, this));
    
    var opacity = setInterval($.proxy(function() {
        this.renderOpacity();
    }, this), this.getSettings('refreshState'));
    
    this.setCache('opacity', opacity);
};


/**
 * helper function to fade out inactive users
 */
WhoIsOnline.prototype.renderOpacity = function() {
    var savedUserlist = this.getCache('userlist'),
        $liPortletUserlist = $(this.getSelector('list')).find('li');
        
    var timeout = this.getSettings('timeout'),
        delta = this.getSettings('delta'),
        splitter = timeout / 10,
        bigSplitter = timeout / 100,
        now = Math.round((new Date()).getTime() / 1000);
        
    var $list = $(this.getSelector('list'));
    
    $.each(savedUserlist, $.proxy(function(key, val) {
    
        var $li = $list.find('li[data-id="' + val.id + '"]');
    
        if($li.length > 0) {
            var logout = val.recent_time - delta + timeout,
                logout_delta = logout - now;
            
            if(logout_delta <= 0) {
                $li.remove();
            } else {
                // opacity image
                $li.find('img.img-icon').css('opacity', (Math.round(logout_delta / splitter) / 10));
                // bar width
                $li.find(this.getSelector('profile')).find('.bar').width(Math.round(logout_delta / bigSplitter) + '%');
            }
        }
    
    }, this));
};


/**
 * render the tooltips for online user, showing profile data on hover
 * 
 * @uses `ityou.whoisonline/ityou/whoisonline/portlets/whoisonline.pt:76`
 * 
 * @param {Object} data
 * @param {Object} element
 */
WhoIsOnline.prototype.renderTooltip = function(data, element) {
	data.wioSendMsg = $.i18n._('wioSendMsg');
	data.wioLastActivity = $.i18n._('wioLastActivity');
	data.recent_time = this.timezone.convertTime((new Date(data.recent_time * 1000)).toISOString());
	
    if(element.find(this.getSelector('profile')).length <= 0) {
        var tmpl = $(this.getTemplate('profile'));
        /** @uses `ityou.whoisonline/ityou/whoisonline/portlets/whoisonline.pt:76` */
        element.find(this.getSelector('profileBox')).append(tmpl.render(data));
    }
};


// attach event handler
// -----------------------------------------------------------------------------

WhoIsOnline.prototype.attachEventHandler = function() {

    // mouse
    $(this.getSelector('list')).on({
    
        mouseenter: $.proxy(function(e) {
            var $li = $(e.currentTarget).parents('li');
            
            if($li.find(this.getSelector('profile')).length > 0) {
                $li.find(this.getSelector('profileBox')).find('> div').each(function() {
                    $(this).show();
                });
            }
        }, this),
        
        mouseleave: $.proxy(function(e) {
            var $li = $(e.currentTarget).parents('li');
            
            $li.find(this.getSelector('profileBox')).find('> div').each(function() {
                $(this).hide();
            });
        }, this)
    
    }, '.portrait');

};

