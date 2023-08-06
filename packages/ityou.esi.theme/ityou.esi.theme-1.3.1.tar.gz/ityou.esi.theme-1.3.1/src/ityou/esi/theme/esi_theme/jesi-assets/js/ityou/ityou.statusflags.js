/**
 * Status Flags
 * 
 * Retrieving new Activities, IMessages and online users.
 * Within this "class" we're configuring, initializing and starting:
 * 	* ActivityStream
 *  * IMessage Components
 *  * WhoIsOnline
 * 
 * @module StatusFlags
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:StatusFlags
 * @param {Object} settings
 * @param {Object} ajaxSettings
 */
function StatusFlags(settings, ajaxSettings) {
	this.name = 'ityou.statusflags';
	this.version = '0.3.260814';
	
	this.settings = $.extend({
		astream: {},
		inbox: {},
		imessage: {},
		whoisonline: {}
	}, settings);
	
	// ajax.remote, ajax.callback
	this.ajax = $.extend({}, ajaxSettings);
    this.delayStatus = $('#ESI_DATA').data('ityou-statusflags-delay') !== undefined ? $('#ESI_DATA').data('ityou-statusflags-delay') * 1000 : 5000;
    this.retryTimer = 30000; // 30 seconds

    // astream options
    this.astreamBadge = '#activities-counter';
    
    /**
     * @param {String} option
     * @return {Object|Array|String|Number|Boolean}
     */
    this.getOption = function(option) {
        if(undefined !== this[option]) {
            return this[option];
        }
        
        return undefined;
    };
    
    /**
     * @param {String} option
     * @param {Object|Array|String|Number|Boolean} value
     * @return {StatusFlags}
     */
    this.setOption = function(option, value) {
        this[option] = value;
        return this;
    };
    
    /**
	 * @param {String} key
	 * @return {Object|Array|String|Number|Boolean}
	 */
	this.getSettings = function(key) {
		if(this.settings.hasOwnProperty(key)) {
			return this.settings[key];
		}
		
		return {};
	};
}


// inherits functionality of `module:Utilities`
/** @uses module:Utilities */
StatusFlags.prototype = new Utilities();

/** @uses module:ActivityStream */
StatusFlags.prototype.astream = new ActivityStream();

/** @uses module:iMessageOverview */
StatusFlags.prototype.inbox = new ImessageOverview();

/** @uses module:iMessageDialog */
StatusFlags.prototype.dialog = new IMessageDialog();

/** @uses module:iMessageNotify */
StatusFlags.prototype.imessageNotify = new IMessageNotify();

/** @uses module:iMessageCleanNewMessage */
StatusFlags.prototype.cleanMessage = new IMessageCleanNewMessage();

/** @uses module:WhoIsOnline */
StatusFlags.prototype.whoisonline = new WhoIsOnline();

/** @uses module:Clipboard */
//StatusFlags.prototype.clipboard = new Clipboard();


/**
 * constructor
 */
StatusFlags.prototype.init = function() {
	// this.ajax.remote, this.ajax.callback
	var globalSettings = {
		ajax: this.ajax
	};
	
	// init imessage scripts
	this.dialog.setSettings($.extend(globalSettings, this.getSettings('imessage'))).init();
	this.cleanMessage.setSettings($.extend(globalSettings, this.getSettings('imessage'))).init();
	this.inbox.setSettings($.extend(globalSettings, this.getSettings('inbox'))).init();
	this.imessageNotify.setSettings($.extend(globalSettings, this.getSettings('imessage'))).init();
	// set whoisonline settings
	this.whoisonline.setSettings($.extend(globalSettings, this.getSettings('whoisonline')));
	// set astream settings
	this.astream.setSettings($.extend(globalSettings, this.getSettings('astream'))).init();
	
	// init notify
    this.astreamProcess();
    
    // init whoisonline
    this.whoisonlineProcess();

    // init StatusFlags only when a user id is set
    if($('#ESI_DATA').length > 0 && $('#ESI_DATA').data('ityou-uid') !== undefined) {
        // set userid
        this.setOption('userId', $('#ESI_DATA').data('ityou-uid'));
        
        // start streaming
        this.requestStatus();
    }
    
    //this.clipboard.init(this.getOption('userId'));
};


/**
 * status flags request
 * 
 * @uses `@@ajax-statusflags`
 */
StatusFlags.prototype.requestStatus = function() {
	$.ajax({
        url: this.ajax.remote + '/@@ajax-statusflags' + this.ajax.callback,
        dataType: 'json',
        timeout: 30000,
        // event handler success
        success: $.proxy(function(response) {
            if(this.size(response) > 0) {
                this.processResponse(response);
            }
            
            // repeat status flags each X milliseconds
            setTimeout($.proxy(function() {
                this.requestStatus();
            }, this), this.getOption('delayStatus'));
        }, this),
        // event handler error
        error: $.proxy(function(XMLHttpRequest, textStatus, errorThrown) {
            this.log('StatusFlags', (new Date()).toISOString(), XMLHttpRequest, textStatus, errorThrown);
            
            if(textStatus.toLowerCase() === 'timeout') {
                this.log('Request timed out...');
            }
            
            // try to reestablish connection with server
            this.retry();
        }, this)
    });
};

/**
 * try to reestablish connection with server after X milliseconds
 */
StatusFlags.prototype.retry = function() {
	var t = setTimeout($.proxy(function() {
		this.requestStatus();
	}, this), this.retryTimer);
};


/**
 * process the response given by ajax request
 *
 * @param {Object} values
 */
StatusFlags.prototype.processResponse = function(values) {
	// if values has property called imessage
    if(values.hasOwnProperty('imessage') && parseInt(values.imessage) === 1) {
        this.imessageProcess();
    }
    
    // if values has property called astream
    if(values.hasOwnProperty('astream') && parseInt(values.astream) === 1) {
        this.astreamProcess();
    }
    
    // if values has property called astream_comments
    if(values.hasOwnProperty('astream_comments') && parseInt(values.astream_comments) === 1) {
        this.astreamCommentsProcess();
    }
    
    // if values has property called whoisonline
    if(values.hasOwnProperty('whoisonline') && parseInt(values.whoisonline) === 1) {
        this.whoisonlineProcess();
    }
};


/**
 * change text and visibility based on value in notify sector
 *
 * @param {String} state
 * @param {String} value
 */
StatusFlags.prototype.notifyBadge = function(state, value) {
    var $badge = $(this.getOption(state + 'Badge'));
    
    // change value
    $badge.text(value);
    
    // hide or show badge
    if(value > 0) {
        $badge.removeClass('badge-hide');
    } else {
        $badge.addClass('badge-hide');
    }
};


/**
 * process imessage and call get_messages via ajax
 */
StatusFlags.prototype.imessageProcess = function() {
    this.imessageNotify.getNotify();
    
    // if we are currently viewing the inbox, load new messages in inbox
    if(this.inbox.isInbox() || this.inbox.isDialogOverview()) {
        this.inbox.inboxStream();
    }
    
    // if we are currently vieweing the dialog, load new messages in dialog
    if(this.dialog.isDialog()) {
        this.dialog.updateDialog();
    }
};


/**
 * process astream and call count_latest_activities via ajax
 * 
 * @uses `@@ajax-notify`
 */
StatusFlags.prototype.astreamProcess = function() {
	// get latest activity timestamp from localStorage
    var latest_activity_timestamp = this.storage.local.get('activitiesTimestamp'); // activitiesTimestamp needs to be set with JSON.stringify()

    // request activity notify
    $.ajax({
        url: this.ajax.remote + '/@@ajax-notify' + this.ajax.callback,
        data: {
            action: 'count_latest_activities',
            timestamp: latest_activity_timestamp
        },
        dataType: 'json',
        // event handler success
        success: $.proxy(function(response) {
            this.notifyBadge('astream', response);
            
            if(response > 0) {
                this.astreamRenderer();
            }
        }, this)
    });
};


/**
 * get new activities
 */
StatusFlags.prototype.astreamRenderer = function() {
    // follow state
    var followInstalled = $('#astream-tabs').length > 0 ? true : false,
        // followState = all | follow
        followState = followInstalled ? ($('#astream-tabs').find('li.active').find('a').hasClass('astream-tab-all') ? 'all' : 'follow') : false;
    
    if(this.astream.isActivityStream()) {
    	this.astream.getActivities('get_latest_activities');
    	/*
        if(followInstalled) {
            this.astream.getActivities('get_latest_activities');
        } else {
            this.astream.getActivities('get_latest_activities');
        }
        */
    }
};


/**
 * get new comments
 */
StatusFlags.prototype.astreamCommentsProcess = function() {
    if(this.astream.isActivityStream()) {
        this.astream.getComments();
    }
};


/**
 * get all online users
 */
StatusFlags.prototype.whoisonlineProcess = function() {
    this.whoisonline.getAll();
};