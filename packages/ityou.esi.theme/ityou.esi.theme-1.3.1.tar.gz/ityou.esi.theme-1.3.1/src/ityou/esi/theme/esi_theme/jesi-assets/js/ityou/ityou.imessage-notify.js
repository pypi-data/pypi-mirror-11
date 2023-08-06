/**
 * Notify IMessage
 * 
 * @module iMessageNotify
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:iMesageNotify
 */
function IMessageNotify() {
	this.name = 'ityou.imessage.notify';
	this.version = '0.1.2608014';
	
    // temp storage
    this.cache = {
        userId: $('#ESI_DATA').data('ityou-uid')
    };
    
    // settings
    this.settings = {
        maxMessages: 500,
        maxLength: 30
    };
    
    // selector
    this.selector = {
        notify: '#notify-messages',
        notifyBox: '#notify-messages-box',
        messages: '.message-notify-list',
        counter: '#messages-counter'
    };
    
    // template
    this.template = {
        wrapper: '#imessage-notify-wrapper-template',
        dropdown: '#imessage-notify-template'
    };
    
    
    // get something from cache
    this.getCache = function(option) {
        if(this.cache.hasOwnProperty(option)) {
            return this.cache[option];
        }
        
        return undefined;
    };
    
    // set something to cache
    this.setCache = function(option, value) {
        this.cache[option] = value;
        return this;
    };
    
    // get option
    this.getOption = function(option, key) {
        if(undefined === key) {
            if(this.hasOwnProperty(option)) {
                return this[option];
            }
        } else {
            if(this.hasOwnProperty(key) && this[key].hasOwnProperty(option)) {
                return this[key][option];
            }
        }
        
        return undefined;
    };
    
    // set option
    this.setOption = function(option, value, key) {
        if(undefined === key) {
            this[option] = value;
        } else {
            this[key][option] = value;
        }
        
        return this;
    };
    
    this.setSettings = function(settings) {
    	if(settings) {
    		this.settings = $.extend(this.settings, settings);
    	}
    	
    	return this;
    };
}


// inherits functionality of `module:Utilities`
/** @uses module:Utilities */
IMessageNotify.prototype = new Utilities();

/** @uses module:ClientTimezone */
IMessageNotify.prototype.TimeConverter = new ClientTimezone();



/**
 * @constructs
 */
IMessageNotify.prototype.init = function() {
    this.getNotify();
};


/**
 * helper function to get notifies on imessage
 * 
 * @uses `@@ajax-message?action=get_messages&approved=false` @ L119
 * @uses `ityou.esi.theme/src/ityou/esi/theme/esi_theme/theme.html:282` @ L146
 */
IMessageNotify.prototype.getNotify = function() {
    var senderIds = [];
    
    /** @uses `@@ajax-messages?action=get_messages&approved=false` */
    $.ajax({
        url: this.settings.ajax.remote + '/@@ajax-messages' + this.settings.ajax.callback,
        data: {
            action: 'get_messages',
            approved: false,
            max: this.getOption('maxMessages', 'settings'),
            omit_sender: this.getCache('userId')
        },
        dataType: 'json',
        // event handler success
        success: $.proxy(function(response) {
            var $counter = $(this.getOption('counter', 'selector')),
                $box = $(this.getOption('notifyBox', 'selector'));
                
            $counter.text(response.length);
            
            if(response.length > 0) {
                $counter.removeClass('badge-hide');
                
                $.each(response, $.proxy(function(i, val) {
                	// need to change response[i][timestr]
                	response[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
                }, this));
                
                if($box.length === 0) {
                	// rendering
                	/** @uses `ityou.esi.theme/src/ityou/esi/theme/esi_theme/theme.html:282` */
                    $($(this.getOption('wrapper', 'template')).render()).appendTo(this.getOption('notify', 'selector'));
                }
            } else {
                $counter.addClass('badge-hide');
                
                if($box.length > 0) {
                    $box.prev('.arrow-top').remove();
                    $box.remove();
                }
            }
            
            // filtering
            response = this.filter(response);
            
            // rendering tooltip
            this.render(response);
        }, this)
    });
};


/**
 * helper function to render the imessage tooltip
 * 
 * @uses `ityou.esi.theme/src/ityou/esi/theme/esi_theme/theme.html:290` @ L182
 * 
 * @param {Array} data
 */
IMessageNotify.prototype.render = function(data) {
    var msgList = $('<ul/>'),
        messages = this.getOption('messages', 'selector'),
        $tmpl = $(this.getOption('dropdown', 'template'));
        
    $(messages).empty();
    
    $.each(data, function(key, value) {
    	/** @uses `ityou.esi.theme/src/ityou/esi/theme/esi_theme/theme.html:290` */
        $($tmpl.render(value)).appendTo(msgList);
    });
    
    msgList.appendTo(messages);
};


/**
 * helper function to filter group dialogs and change their results to fit the template
 * 
 * @param   {Array} data
 * @returns {Array}
 */
IMessageNotify.prototype.filter = function(data) {
    var sender = [],
        senderData = {};
        
    $.each(data, $.proxy(function(key, value) {
        if(value.hasOwnProperty('group') && value.group === true) {
            data[key].sender_id = value.receiver_id;
            data[key].sender_name = value.receiver_name;
            data[key].sender_portrait = value.receiver_portrait;
        }
        
        if($.inArray(value.sender_id, sender) === -1) {
            sender.push(value.sender_id);
            
            var regex = /<br\s*[\/]?>/gi,
                tmp = $('<p/>').append($.trim(value.message.replace(regex, ' '))).text();

            value.message = tmp.substr(0, this.getOption('maxLength', 'settings')) + (tmp.length > this.getOption('maxLength', 'settings') ? '...' : '');

            senderData[value.sender_id] = $.extend({}, {count: 1}, value);
        } else {
            senderData[value.sender_id].count += 1;
        }
    }, this));
    
    return senderData;
};

