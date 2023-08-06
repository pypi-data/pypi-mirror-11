/**
 * Plugin to render user and group dialogs
 * 
 * @module iMessageDialog
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:iMessageDialog
 */
function IMessageDialog() {
	this.name = 'ityou.imessage.dialog';
	this.version = '0.5.260814';

    // temp storage
    this.cache = {
        // own userid
        userId: undefined,
        
        // handle view
        currentView: undefined,
        partnerId: undefined,
        type: undefined,
        
        // group member
        renderGroupMember: undefined
    };
    
    // animations
    this.animation = {
        speedDown: 400,
        speedUp: 200,
        removeHighlight: 1500
    };
    
    // selectors
    this.selector = {
        dialog: '#message-stream ul.latest-messages',
        editor: '#message-textarea',
        controls: '#messages-controls',
        editorControls: '.message-controls',
        // group-member
        groupMemberWrapper: '#messages-group-member',
        groupMemberContent: '#group-member-content',
        fixedNavbar: '.navbar-fixed-top',
        dialogPartnerWrapper: '#messages-dialog-partner',
        dialogPartnerContent: '#dialog-partner'
    };
    
    // templates
    this.template = {
        dialog: '#imessage-dialog-template',
        // group-member
        groupMemberWrapper: '#imessage-group-member-template',
        groupMemberContent: '#imessage-group-member-content-template',
    	// dialog-partner
        dialogPartner: '#imessage-dialog-partner-template'
    };
    
    // settings
    this.settings = {
        max: 20,
        minLength: 1,
        waiting: 5000,
        useWYSIWYG: false,
        // colors
        self: '#e0ffc1'
    };
}


// inherits functionality of `module:Utilities`
/** @uses module:Utilities */
IMessageDialog.prototype = new Utilities();

/** @uses module:ClientTimeZone */
IMessageDialog.prototype.TimeConverter = new ClientTimezone();

/** @uses module:Clipboard */
IMessageDialog.prototype.Clipboard = new Clipboard();


/**
 * initialise imessage dialog
 *
 * @param {Object} settings
 */
IMessageDialog.prototype.init = function(settings) {
    this.setCache('userId', $('#ESI_DATA').data('ityou-uid'));
    this.setSettings(settings);
    
    // define in which template we are
    this.defineView();
    
    // check if `dialog-view` is active
    if(this.isDialog()) {
        this.initEventHandler();
        
        if(this.getOption('useWYSIWYG', 'settings') === true) {
        	this.initTinyMCE();
        } else {
        	$(this.getOption('editor', 'selector')).autoGrow();
        }
        
        this.initDialog();
    }
};


/**
 * define which page is currently viewed
 */
IMessageDialog.prototype.defineView = function() {
    var pathname = document.location.pathname,
        matchAgainst = /@@messages/i,
        pathsearch = document.location.search;
    
    if(matchAgainst.exec(pathname) && pathsearch.length > 0) {
        this.setCache('currentView', 'dialog');
        
        var match_userid = /\?sid\=([\w]*)[&]{0,}/i,
            match_groupid = /\?rid\=([a-z0-9]*)/i;

        if(match_userid.exec(pathsearch)) {
            this.setCache('type', 'userDialog');
            this.setCache('partnerId', RegExp.$1);
            
            return true;
        } else if(match_groupid.exec(pathsearch)) {
            this.setCache('type', 'groupDialog');
            this.setCache('partnerId', RegExp.$1);
            
            return true;
        }
    }
    
    this.setCache('currentView', undefined);
    this.setCache('partnerId', undefined);
};


/**
 * helper function to check if template is `dialog` template
 *
 * @returns {Boolean}
 */
IMessageDialog.prototype.isDialog = function() {
    if(this.getCache('currentView') === 'dialog') {
        return true;
    }
    
    return false;
};


/**
 * @constructs
 * 
 * @uses `@@ajax-messages?action=get_dialog|get_messages` @ L183
 */
IMessageDialog.prototype.initDialog = function() {
    this.showSpinner();
    
    var ajaxData = {
        approved: 'all',
        max: this.getOption('max', 'settings')
    };
    
    if(this.getCache('type') === 'userDialog') {
        ajaxData = $.extend(ajaxData, {
            action: 'get_dialog',
            sender_id: this.getCache('partnerId')
        });
    } else if(this.getCache('type') === 'groupDialog') {
        ajaxData = $.extend(ajaxData, {
            action: 'get_messages',
            receiver_id: this.getCache('partnerId'),
            group: true
        });
    }
    
    /** @uses `@@ajax-messages?action=get_dialog|get_messages` */
    $.ajax({
        url: this.settings.ajax.remote + '/@@ajax-messages' + this.settings.ajax.callback,
        data: ajaxData,
        dataType: 'json',
        // event handler success
        success: $.proxy(function(response) {
            if(this.getCache('type') === 'groupDialog') {
                response.reverse();
                
                this.renderGroupMember(response);
            } else {
            	this.renderDialogPartner(response);
            }
            
            $.each(response, $.proxy(function(i, val) {
            	// need to change response[i][timestr]
            	response[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
            }, this));
            
            // render dialog
            this.render(response);
            
            // mark unread messages as read
            //this.waitForReading();
            this.markAsRead();
            
            // add clipboard controls
            this.Clipboard.addPasteControls();
        }, this)
    });
};


/**
 * helper function to update a dialog (livestreaming)
 * 
 * @uses `@@ajax-messages?action=get_messages` @ L264
 * @uses `ityou.imessage/ityou/imessage/browser/templates/imessage.pt:239` @ L245
 */
IMessageDialog.prototype.updateDialog = function(data) {
    var $dialog = $(this.getOption('dialog', 'selector')),
        $lastLi = $dialog.find('li').last(),
        lastTimestamp = $lastLi.find('.timestamp').attr('id'),
        lastHash = $lastLi.attr('id');
        
    if(data) {
    	// if data is given we dont need to ask the server again
        if(data.hash === lastHash) {
            var $latest = $('#' + lastHash);
        
            $latest.find('.message').append('<p>' +data.message + '</p>');
            $latest.find('.message-text').find('.timestamp')
                .attr('id', data.timestamp)
                .text(data.timestr);
            
            return ;
        }
        
        data.sent = true;
        
        // rendering
        /** @uses `ityou.imessage/ityou/imessage/browser/templates/imessage.pt:239` */
        $dialog.append(
            $(this.getOption('dialog', 'template')).render(data)
        );
    } else {
    	// otherwise aks the server again :)
        var ajaxData = {
            action: 'get_messages',
            timestamp: lastTimestamp,
            newer: true,
            approved: 'all'
        };
        
        if(this.getCache('type') === 'userDialog') {
            ajaxData = $.extend(ajaxData, {sender_id: this.getCache('partnerId')});
        } else if(this.getCache('type') === 'groupDialog') {
            ajaxData = $.extend(ajaxData, {receiver_id: this.getCache('partnerId'), group: true});
        }
    
        /** @uses `@@ajax-messages?action=get_messages` */
        $.ajax({
            url: this.settings.ajax.remote + '/@@ajax-messages' + this.settings.ajax.callback,
            data: ajaxData,
            dataType: 'json',
            // event handler success
            success: $.proxy(function(response) {
                response.reverse();
                
                $.each(response, $.proxy(function(i, val) {
                	// need to change response[i][timestr]
                	response[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
                }, this));
                
                // render updates
                this.render(response);
                
                // mark unread messages as read
                this.waitForReading();
            }, this)
        });
    }
};


/**
 * render messages
 * 
 * @uses `ityou.imessage/ityou/imessage/browser/templates/imessage.pt:239` @ L325
 * 
 * @param {Array} data
 * @param {Boolean} append
 */
IMessageDialog.prototype.render = function(data, append) {
	if(undefined === append) {
        append = true;
    }

    // loop through data
    $.each(data, $.proxy(function(key, value) {
        var rendered;
        
        var $item = $('#' + value.hash);
        
        if($item.length > 0 && $item.is(':last-child') === false) {
            $item.remove();
        } else if($item.length > 0 && $item.is(':last-child')) {
            $item.find('.message').html(value.message);
            $item.find('.message-text').find('.timestamp')
                    .attr('id', value.timestamp)
                    .text(value.timestr);
            
            return ;
        }
        
        value.sent = this.getCache('userId') === value.sender_id;
        
        var $msgTmpl = $(this.getOption('dialog', 'template')),
            dialog = this.getOption('dialog', 'selector');
            
        // rendering
        /** @uses `ityou.imessage/ityou/imessage/browser/templates/imessage.pt:239` */
        rendered = $($msgTmpl.render(value));
        
        if(append === true) {
            rendered.appendTo(dialog).hide();
        } else {
            rendered.prependTo(dialog).hide();
        }
        
        rendered.slideDown(this.getOption('speedDown', 'animation'));
    }, this));
    
    if(data.length > 0 && append === true) {
        setTimeout(function() {
            $('html, body').animate({scrollTop: $(document).height() + 'px'}, 1500);
        }, 50);
    }
    
    this.hideSpinner();
};


/**
 * helper function to load old messages
 * 
 * @uses `@@ajax-messages?action=get_dialog` @ L355
 * 
 * @param {String} timestamp
 */
IMessageDialog.prototype.loadPrevious = function(timestamp) {
	/** @uses `@@ajax-messages?action=get_dialog` */
    $.ajax({
        url: this.settings.ajax.remote + '/@@ajax-messages' + this.settings.ajax.callback,
        data: {
            action: 'get_dialog',
            sender_id: this.getCache('partnerId'),
            timestamp: timestamp
        },
        dataType: 'json',
        // event handler success
        success: $.proxy(function(response) {
        	$.each(response, $.proxy(function(i, val) {
            	// need to change response[i][timestr]
            	response[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
            }, this));
        	
            if(response.length > 0) {
            	// rendering
                this.render(response, false);
            }
        }, this)
    });
};


/**
 * helper function to render members of a group
 * 
 * @uses `ityou.imessage/ityou/imessage/browser/templates/imessage.pt:299` @ L396
 * @uses `ityou.imessage/ityou/imessage/browser/templates/imessage.pt:327` @ L400
 * 
 * @param {Array} data
 */
IMessageDialog.prototype.renderGroupMember = function(data) {
    if(data.length > 0 && data[0].hasOwnProperty('multiple_receivers') && data[0].multiple_receivers.length > 0) {
        var tmp = data[0].multiple_receivers,
            groupName = data[0].receiver_name;
            
        this.setCache('renderGroupMember', true);
            
        // render group name etc
        /** @uses `itoyu.imessage/ityou/imessage/browser/templates/imessage.pt:299` */
        $($(this.getOption('groupMemberWrapper', 'template')).render({groupname: groupName})).appendTo(this.getOption('groupMemberWrapper', 'selector'));
        
        // tmp = { id, name, portrait }
        /** @uses `ityou.imessage/ityou/imessage/browser/templates/imessage.pt:327` */
        $(this.getOption('groupMemberContent', 'selector')).find('ul.dropdown-menu')
            .append($(this.getOption('groupMemberContent', 'template')).render(tmp));
        
        this.setCache('group-member', $(this.getOption('groupMemberWrapper', 'selector')).html());
    }
};


/**
 * helper function to render dialog partner
 */
IMessageDialog.prototype.renderDialogPartner = function(data) {
	this.setCache('renderDialogPartner', true);
	this.setCache('dialog-partner', $(this.getOption('dialogPartnerWrapper', 'selector')).html());
};


/**
 * TODO: check implementation & documentation
 */
IMessageDialog.prototype.waitForReading = function() {
    setTimeout($.proxy(function() {
        // ???

        if(this.isWindowActive()) {
            this.markAsRead();
        } else {
            this.waitForReading();
        }
    }, this), this.getOption('waiting', 'settings'));
};


/**
 * helper function to collect message as read
 */
IMessageDialog.prototype.markAsRead = function() {
    var mids = new Array();
    
    $(this.getOption('dialog', 'selector')).find('.message-unread').each(function() {
        mids.push($(this).attr('id'));
    });
    
    if(mids.length > 0) {
        this.messageRead(mids);
    }
    
    $(this.getOption('dialog', 'selector')).find('.message-unread').removeClass('message-unread');
};


/**
 * helper function to mark messages as read
 * 
 * @uses `@@ajax-messages?action=message_read_by_receiver` @ L462
 * 
 * @param {Array} mid
 */
IMessageDialog.prototype.messageRead = function(mid) {
    var mids = JSON.stringify(mid);
    
    /** @uses `@@ajax-messages?action=message_read_by_receiver` */
    $.ajax({
        url: this.settings.ajax.remote + '/@@ajax-messages' + this.settings.ajax.callback,
        data: {
            action: 'message_read_by_receiver',
            mids: mids
        },
        dataType: 'json',
        complete: $.proxy(function() {
        	StatusFlags.prototype.imessageNotify.getNotify();
        }, this)
    });
};


/**
 * helper function to initialize tiny mce
 */
IMessageDialog.prototype.initTinyMCE = function() {
    $(this.getOption('editor', 'selector')).tinymce({
        script_url: 'tiny_mce_gzip.js',
        content_css: 'portal_tinymce/@@tinymce-getstyle',
        
        theme: 'advanced',
        skin: 'plone',
        
        plugins: 'paste',
        
        theme_advanced_buttons1: 'bold,italic,underline,separator,justifycenter,justifyright,justifyfull,separator,bullist,numlist',
        theme_advanced_buttons2: 'code',
        theme_advanced_buttons3: '',
        theme_advanced_toolbar_location: 'top',
        
        oninit: function(e) {},
        
        paste_preprocess: $.proxy(function(pl, o) {
            //o.content = this.stripTags(o.content, '<b><u><i><em><p><strong><small><ul><ul><li><a><img>');
            o.content = this.stripTags(o.content, '<img><strong><em><span><ul><ol><li><a><p>');
        }, this)
    });
};


//
// Event Handler Functions below
// -----------------------------------------------------------------------------

/**
 * initialite event handler
 * 
 * @uses `@@ajax-messages?action=get_dialog` @ L543
 * @uses `@@ajax-messages?action=message_hidden_by_receiver|message_hidden_by_sender` @ L610
 */
IMessageDialog.prototype.initEventHandler = function() {
    var $dialog = $(this.getOption('dialog', 'selector'));
    

    /** @events Event Handling for Buttons in #messages-controls */
    $(this.getOption('controls', 'selector')).on('click', '.messages-all-button, .messages-hideall-button, .previous-messages-trigger', $.proxy(function(e) {
        e.preventDefault();
        
        var $el = $(e.currentTarget),
            $msgs = $(this.getOption('dialog', 'selector')).find('.latest-message');
        
        if($el.hasClass('messages-all-button')) {
            $el.hide(); // hide messages-all-button
            
            $('.messages-hideall-button').show(); // show messages-hideall-button
            
            $msgs.slideDown(this.getOption('speedDown', 'animation')); // slidedown all messages
        } else if($el.hasClass('messages-hideall-button')) {
            $el.hide(); // hide messages-hideall-button
            
            $('.messages-all-button').show(); // show messages-all-button
            
            $msgs.slideUp(this.getOption('speedUp', 'animation')); // slideup all messages
        } else if($el.hasClass('previous-messages-trigger')) {
            var msgCount = $msgs.length;
            
            this.showSpinner();
            
            // load more msgs with max and offset
            /** @uses `@@ajax-messages?action=get_dialog` */
            $.ajax({
                url: this.settings.ajax.remote + '/@@ajax-messages' + this.settings.ajax.callback,
                data: {
                    action: 'get_dialog',
                    sender_id: this.getCache('partnerId'),
                    approved: 'all',
                    max: this.getOption('max', 'settings'),
                    offset: msgCount
                },
                dataType: 'json',
                // event handler success
                success: $.proxy(function(response) {
                    response.reverse();
                    
                    $.each(response, $.proxy(function(i, val) {
                    	// need to change response[i][timestr]
                    	response[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
                    }, this));
                    
                    this.render(response, false);
                    
                    // if there are no more messages hide this button
                    if(response.length === 0) {
                        $el.parents('.well.previous-messages').hide();
                    }
                }, this)
            });
        }
    }, this));
    
    
    /** @events hide single message */
    $dialog.on('click', '.message-hide-button', $.proxy(function(e) {
        e.preventDefault();
        
        var $el = $(e.currentTarget),
            $li = $el.parents('li');
            
        $li.slideUp(this.getOption('speedUp', 'animation'), $.proxy(function() {
            var visibleLi = $(this.getOption('dialog', 'selector')).find('li:visible').length;
        
            // if no more messages are visible, hide 'hideall' button
            if(visibleLi === 0) {
                $('.messages-hideall-button').hide();
            }
        }, this));
        
        $('.messages-all-button').show();
    }, this));
    
    
    /** @events delete message */
    $dialog.on('click', '.message-delete-button', $.proxy(function(e) {
        e.preventDefault();
        
        var $el = $(e.currentTarget),
            $li = $el.parents('li.latest-message');
            
        var hash = new Array();
        
        hash.push($li.attr('id'));
        
        var state = 'message_hidden_by_' + ($li.hasClass('message-received') ? 'receiver' : 'sender');
        
        if($li.hasClass('message-received') || $li.hasClass('message-sent')) {
        	/** @uses `@@ajax-messages?action=message_hidden_by_receiver|message_hidden_by_sender` */
            $.ajax({
                url: this.settings.ajax.remote + '/@@ajax-messages' + this.settings.ajax.callback,
                data: {
                    action: state,
                    mids: JSON.stringify(hash)
                },
                dataType: 'json',
                complete: $.proxy(function() {
                	StatusFlags.prototype.imessageNotify.getNotify();
                }, this)
            });
            
            $li.fadeOut(this.getOption('speedUp', 'animation'), function() {
                $li.remove();
            });
        }
    }, this));
    
    
    /** @events post/save a message */
    var $editorControls = $(this.getOption('editorControls', 'selector'));
    $editorControls.on('click', '.message-save-button', $.proxy(function(e) {
        e.preventDefault();
   
        var $el = $(e.currentTarget);
        
        this.save($el);
    }, this));
    
    
    if(this.getCache('type') === 'groupDialog') {
        var $groupMemberWrapper = $(this.getOption('groupMemberWrapper', 'selector')),
            groupMemberWrapper = this.getOption('groupMemberWrapper', 'selector').split('#')[1],
            $fixedNavbar = $(this.getOption('fixedNavbar', 'selector'));

    
        this.setCache('offsetLeft', $groupMemberWrapper.offset().left);
        this.setCache('height', ($fixedNavbar.length > 0 ? $fixedNavbar.height() : 0));
        
        this.setCache('outerHeight', $groupMemberWrapper.find('#dialog-partner').outerHeight(true) + 20);


        /** @events move the dialog partner bar on scroll */
        $(window).on('scroll', $.proxy(function(e) {
            this.setCache('offsetTop', $groupMemberWrapper.offset().top - ($fixedNavbar.length > 0 ? $fixedNavbar.height() : 0));
            this.setCache('width', $(this.getOption('dialog', 'selector')).width());
        
            var tmp = $('.' + groupMemberWrapper),
                scrollTop = $(window).scrollTop();
                
            if(this.getCache('offsetTop') < scrollTop && tmp.length === 0) {
                var t = $('<div class="' + groupMemberWrapper + '"/>').append(this.getCache('group-member'));
            
                t.addClass('is-fixed').css({
                    position: 'fixed',
                    top: this.getCache('height'),
                    left: this.getCache('offsetLeft'),
                    width: this.getCache('width')
                }).appendTo('body');
                
                $groupMemberWrapper.css({
                    //height: $groupMemberWrapper.height()
                	height: this.getCache('outerHeight')
                }).empty();
            } else if(this.getCache('offsetTop') > scrollTop && tmp.length > 0) {
                $('.' + groupMemberWrapper).remove();
                
                $groupMemberWrapper.css('height', 'auto').removeProp('styles').append(this.getCache('group-member'));
            }
            
            // trigger WhoIsOnline.onPortrait through StatusFlags
            StatusFlags.prototype.whoisonline.onPortrait(false);
        }, this));
        
        
        /** @events resizing*/
        $(window).on('resize', $.proxy(function(e) {
            this.setCache('offsetTop', $groupMemberWrapper.offset().top - $groupMemberWrapper.height() - ($fixedNavbar.length > 0 ? $fixedNavbar.height() : 0));
            this.setCache('offsetLeft', $groupMemberWrapper.offset().left);
            this.setCache('height', ($fixedNavbar.length > 0 ? $fixedNavbar.height() : 0));
            
            this.setCache('width', $(this.getOption('dialog', 'selector')).width());
            
            $('.' + groupMemberWrapper).css({
                left: this.getCache('offsetLeft'),
                width: this.getCache('width')
            });
        }, this));
    } else { // dialog partner
    	var $dialogPartnerWrapper = $(this.getOption('dialogPartnerWrapper', 'selector')),
    		dialogPartnerWrapper = this.getOption('dialogPartnerWrapper', 'selector').substr(1),
    		$fixedNavbar = $(this.getOption('fixedNavbar', 'selector'));
    	
    	this.setCache('offsetLeft', $dialogPartnerWrapper.offset().left);
    	this.setCache('height', ($fixedNavbar.length > 0 ? $fixedNavbar.height() : 0));
    	
    	this.setCache('outerHeight', $dialogPartnerWrapper.find('#dialog-partner').outerHeight(true) + 20);
    	
    	/** @events move dialog partner bar on scrolling */
    	$(window).on('scroll', $.proxy(function(e) {
    		this.setCache('offsetTop', $dialogPartnerWrapper.offset().top - ($fixedNavbar.length > 0 ? $fixedNavbar.height() : 0));
    		this.setCache('width', $(this.getOption('dialog', 'selector')). width());
    		
    		var tmp = $('.' + dialogPartnerWrapper),
    			scrollTop = $(window).scrollTop();
    		
    		if(this.getCache('offsetTop') < scrollTop && tmp.length === 0) {
    			var t = $('<div class="' + dialogPartnerWrapper + '"/>').append(this.getCache('dialog-partner'));
    			
    			t.addClass('is-fixed').css({
    				position: 'fixed',
    				top: this.getCache('height'),
					left: this.getCache('offsetLeft'),
					width: this.getCache('width')
    			}).appendTo('body');
    			
    			$dialogPartnerWrapper.css({
    				height: this.getCache('outerHeight')
    			}).empty();
    		} else if(this.getCache('offsetTop') > scrollTop && tmp.length > 0) {
    			$('.' + dialogPartnerWrapper).remove();
    			
    			$dialogPartnerWrapper.css('height', 'auto').removeProp('styles').append(this.getCache('dialog-partner'));
    		}
    		
    		StatusFlags.prototype.whoisonline.onPortrait(false);
    	}, this));
    	
    	/** @events resizing */
        $(window).on('resize', $.proxy(function(e) {
        	this.setCache('offsetTop', $dialogPartnerWrapper.offset().top - $dialogPartnerWrapper.height() - ($fixedNavbar.length > 0 ? $fixedNavbar.height() : 0));
        	this.setCache('offsetLeft', $dialogPartnerWrapper.offset().left);
        	this.setCache('height', ($fixedNavbar.length > 0 ? $fixedNavbar.height() : 0));
        	this.setCache('width', $(this.getOption('dialog', 'selector')).width());
        	
        	$('.' + dialogPartnerWrapper).css({
        		left: this.getCache('offsetLeft'),
        		width: this.getCache('width')
        	});
        }, this));
    }
};



/**
 * save a written message
 * 
 * @uses `@@ajax-messages?action=post_message` @ L801
 * 
 * @param {Object} $el
 */
IMessageDialog.prototype.save = function($el) {
    var tinymce = this.getOption('editor', 'selector'),
        $dialog = $(this.getOption('dialog', 'selector'));
        
    var buttonText = $el.html(),
        buttonLoader = '<i class="fa fa-spinner fa-spin"></i>';
    
    if(!$el.prop('disabled')) {
    	var content = '';
    	
    	// check if using textarea or wysiwyg editor
    	if(this.getOption('useWYSIWYG', 'settings')) {
    		content = $(tinymce).tinymce().getContent();
    	} else {
    		content = $(tinymce).val();
    	}
        
        if(content.length <= this.getOption('minLength', 'settings')) {
            return ;
        }
        
        $el.prop('disabled', true);
        $el.html(buttonLoader);
        
        var hash = $dialog.find('.latest-message').last().attr('id');
        
        var ajaxData = {
            action: 'post_message',
            hash: hash,
            message: content
        };
        
        if(this.getCache('type') === 'userDialog') {
            ajaxData = $.extend(ajaxData, {receiver_id: this.getCache('partnerId')});
        } else if(this.getCache('type') === 'groupDialog') {
            ajaxData = $.extend(ajaxData, {receiver_group_hash: this.getCache('partnerId')});
        }
        
        /** @uses `@@ajax-messages?action=post_message` */
        $.ajax({
            url: this.settings.ajax.remote + '/@@ajax-messages' + this.settings.ajax.callback,
            data: ajaxData,
            dataType: 'json',
            // event handler success
            success: $.proxy(function(response) {
            	response['timestr'] = this.TimeConverter.convertTime(response['timestamp']);
            	            	
                this.updateDialog(response);
                
                // reset tinymce or textarea
                if(this.getOption('useWYSIWYG', 'settings') === true) {
                	$(tinymce).html('');
                } else {
                	$(tinymce).val('');
                }
                
                $el.removeProp('disabled');
                $el.html(buttonText);
            }, this),
            // event handler error
            error: $.proxy(function(XMLHttpRequest, textStatus, errorThrown) {
                alert('Send message failed, please try again');
            
                $el.removeProp('disabled');
                $el.html(buttonText);
            }, this)
        });
    }
};
