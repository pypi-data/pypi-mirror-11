/**
 * IMessage Inbox and Dialog Overview
 * 
 * @module iMessageOverview
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:iMessageOverview
 */
function ImessageOverview() {
	this.name = 'ityou.imessage.box';
	this.version = '0.5.260814';
	
	// template and selector
	this.messageTemplate = '#inbox-tmpl';
    this.messageList = '#imessage-inbox table > tbody';
    
    // max items
    this.max = 20;
    this.filterMax = 5;
    
    this.minValue = 2;
    
    this.runningRequest = false;
    this.latestTimestamp = null;
    this.lastScrollTop = 0;
    
    this.user_id = $('#ESI_DATA').data('ityou-uid');
    
    this.runningStream = false;
    this.inboxStreamDelay = 5000;
    
    
    // temp storage
    this.cache = {
        // own userid
        userId: undefined,
        
        // handle view
        currentView: undefined,
        
        // lastScrolltop
        lastScrollTop: 0,
        
        // filter
        filter: undefined
    };
    
    
    // templates
    this.template = {
        messageTemplate: '#inbox-tmpl',
        do_messageTemplate: '#dialog-overview-tmpl'
    };
    
    // selectors
    this.selector = {
        messageList: '#imessage-inbox table > tbody',
    	dialogMessageList: '#dialog-overview-messages-list',
    	dialogLoadMoreTrigger: '#dialog-overview-load-more-trigger'
    };
    
    // settings
    this.settings = {
        max: 20,
        filterMax: 5,
        minValue: 2
    };
}

// inherits functionality of `module:Utilities` 
/** @uses module:Utilities */
ImessageOverview.prototype = new Utilities();

/** @uses module:ClientTimezone */
ImessageOverview.prototype.TimeConverter = new ClientTimezone();


/**
 * initialize imessage overview plugin
 */
ImessageOverview.prototype.init = function(settings) {
    this.setCache('userId', $('#ESI_DATA').data('ityou-uid'));
    this.setSettings(settings);
    
    // define in which template we are
    this.defineView();
    
    if(this.isInbox()) {
    	// template is inbox
        this.eventHandler();
    
        this.getMessages(0);
    } else if(this.isDialogOverview()) {
    	// template is dialog overview
    	this.eventHandler();
    	
    	this.getMessages(0);
    }
};


/**
 * define which page is currently viewed
 */
ImessageOverview.prototype.defineView = function() {
    var pathname = document.location.pathname,
        matchAgainst = /@@message-inbox/i,
        elseMatchAgainst = /@@dialog-overview/i;
    
    if(matchAgainst.exec(pathname)) {
        this.setCache('currentView', 'inbox');
    
        return ;
    } else if(elseMatchAgainst.exec(pathname)) {
    	this.setCache('currentView', 'dialog-overview');
    	
    	return ;
    }
    
    this.setCache('currentView', undefined);
};


/**
 * helper function to check if we can build `inbox`
 *
 * @returns {Boolean}
 */
ImessageOverview.prototype.isInbox = function() {
    if(this.getCache('currentView') === 'inbox') {
        return true;
    }
    
    return false;
};


/**
 * helper function to check if we can build `dialog-overview`
 * 
 * @returns {Boolean}
 */
ImessageOverview.prototype.isDialogOverview = function() {
	if(this.getCache('currentView') === 'dialog-overview') {
		return true;
	}
	
	return false;
};


/**
 * get messages
 * 
 * @uses `@@ajax-messages?action=get_messages[&dialog=true]` @ L221, L292
 *
 * @param int offset
 */
ImessageOverview.prototype.getMessages = function(offset) {
    var $messageList = $(this.getOption('messageList', 'selector'));
    
    if(this.isInbox()) {
    	// template is `inbox`
    	// check if user is searching specific messages
	    if(undefined !== this.filteredUsers) {
	    	// if there's a request still running, do nothing
	        if(!this.runningRequest) {
	        	// otherwise perform action
	            this.runningRequest = true;
	            
	            this.clearFiltering();
	            this.showSpinner();
	            
	            var tmpUid = new Array();
	            $messageList.children().each(function() {
	                var $el = $(this).find('td[data-uid]');
	                
	                if($el.length > 0 && $.inArray($el.data('uid'), tmpUid) === -1) {
	                    tmpUid.push($el.data('uid'));
	                }
	            });
	            
	            var tmpOffsets = new Array();
	            $.each(tmpUid, $.proxy(function(k, v) {
	                tmpOffsets.push($messageList.children().find('td[data-uid="' + v + '"]').length);
	            }, this));
	            
	            offset = this.sortNumeric(tmpOffsets, 'desc')[0];
	            
	            this.fetchMessages(this.filteredUsers, offset);
	            this.timerCallback('filteredMessages', 'sortMessages');
	            
	            var timer = setInterval($.proxy(function() {
	                if(undefined !== this.returnValue) {
	                    clearInterval(timer);
	                
	                    if(this.returnValue.length > 0) {
	                        this.renderMessages(this.returnValue, 'append');
	                        
	                        this.sortByDate();
	                        
	                        this.loadMoreEvent();
	                    }
	                    
	                    this.runningRequest = false;
	                    this.hideSpinner();
	                }
	            }, this), 100);
	        }
	    } else {
	    	// if there's a request still running, do nothing
	        if(!this.runningRequest) {
	        	// otherwise perform action
	            this.runningRequest = true;
	            
	            this.showSpinner();
	        
	            /** @uses `@@ajax-messages?action=get_messages` */
	            $.getJSON(this.settings.ajax.remote + '/@@ajax-messages', {action: 'get_messages', approved: 'all', max: this.max, offset: offset, omit_sender: this.user_id}, $.proxy(function(response) {
	            	$.each(response, $.proxy(function(i, val) {
	                	// need to change response[i][timestr]
	                	response[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
	                }, this));
	            	
	                this.renderMessages(response, 'append');
	                this.runningRequest = false;
	                
	                if(response.length > 0) {
	                    this.loadMoreEvent();
	                }
	                
	                this.hideSpinner();
	            }, this));
	        }
	    }
    } else if(this.isDialogOverview()) {
    	// template is `dialog-overview`
    	if(undefined !== this.filteredUsers) {
	        if(!this.runningRequest) {
	            this.runningRequest = true;
	            
	            this.clearFiltering();
	            this.showSpinner();
	            
	            var tmpUid = new Array();
	            $messageList.children().each(function() {
	                var $el = $(this).find('td[data-uid]');
	                
	                if($el.length > 0 && $.inArray($el.data('uid'), tmpUid) === -1) {
	                    tmpUid.push($el.data('uid'));
	                }
	            });
	            
	            var tmpOffsets = new Array();
	            $.each(tmpUid, $.proxy(function(k, v) {
	                tmpOffsets.push($messageList.children().find('td[data-uid="' + v + '"]').length);
	            }, this));
	            
	            offset = this.sortNumeric(tmpOffsets, 'desc')[0];
	            
	            this.fetchMessages(this.filteredUsers, offset);
	            this.timerCallback('filteredMessages', 'sortMessages');
	            
	            var timer = setInterval($.proxy(function() {
	                if(undefined !== this.returnValue) {
	                    clearInterval(timer);
	                
	                    if(this.returnValue.length > 0) {
	                        this.renderMessages(this.returnValue, 'append');
	                        
	                        this.sortByDate();
	                        
	                        this.loadMoreEvent();
	                    }
	                    
	                    this.runningRequest = false;
	                    this.hideSpinner();
	                }
	            }, this), 100);
	        }
	    } else {
	        if(!this.runningRequest) {
	            this.runningRequest = true;
	            
	            if(offset === 0) {
	            	this.showSpinner();
	            }
	        
	            /** @uses `@@ajax-messages?action=get_messages&dialog=true` */
	            $.getJSON(this.settings.ajax.remote + '/@@ajax-messages', {action: 'get_messages', approved: 'all', max: 50, offset: offset, dialog: true}, $.proxy(function(response) {
	            	$.each(response, $.proxy(function(i, val) {
	                	// need to change response[i][timestr]
	                	response[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
	                }, this));
	            	
	            	if(response.length > 0) {
	            		if(response.length > 2) {
	            			$('.new-message').removeClass('hidden');
	            		}
	            	}
	            	
	                this.renderMessages(response, 'append');
	                this.runningRequest = false;
	                
	                if(response.length > 0) {
                		this.getMessages(offset + 50);
	                }
	                
	                this.hideSpinner();
	            }, this));
	        }
	    }
    }
};


/**
 * streamer function
 * 
 * @uses `@@ajax-messages?action=get_messages[&dialog=true]` @ L349
 */
ImessageOverview.prototype.getLatestMessages = function() {
	var ajaxData;
	
	// define ajax data based on current-view
	if(this.isInbox()) {
	    ajaxData = {
	        action: 'get_messages',
	        approved: 'all',
	        newer: true,
	        omit_sender: this.user_id
	    };
	} else if(this.isDialogOverview()) {
		ajaxData = {
			action: 'get_messages',
			approved: 'all',
			newer: true,
			dialog: true
		}
	}
    
    if(this.getLatestTimestamp()) {
        ajaxData = $.extend(ajaxData, {timestamp: this.getLatestTimestamp()});
    }
    
	/** @uses `@@ajax-messages?action=get_messages[&dialog=true]` */
    $.getJSON(this.settings.ajax.remote + '/@@ajax-messages', ajaxData, $.proxy(function(response) {
        if(response.length > 0) {
            this.setLatestTimestamp(response[0]['timestamp']);
            
            $.each(response, $.proxy(function(i, val) {
            	// need to change response[i][timestr]
            	response[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
            }, this));
    
            this.renderMessages(response, 'prepend');
        }
    }, this));
};


/**
 * helper function to render the messages
 * 
 * @uses `ityou.imessage/ityou/imessage/browser/templates/imessage-inbox.pt:126` @ L403, L405
 * @uses `ityou.imessage/ityou/imessage/browser/templates/dialog-overview.pt:70` @ L
 * 
 * @param {Array} data
 * @param {String} direction
 */
ImessageOverview.prototype.renderMessages = function(data, direction) {
	if(this.isInbox()) {
		// current-view is `inbox`
	    $.each(data, $.proxy(function(index, val) {
	        var dataToRender = {};
	        
	        if(val.group === true) {
	            val.sender_id = val.receiver_id;
	            val.sender_portrait = val.receiver_portrait;
	            val.sender_name = val.receiver_name;
	        }
	        
	        dataToRender.hash = val.hash;
	        dataToRender.sender_name = val.sender_name;
	        dataToRender.sender_id = val.sender_id;
	        dataToRender.sender_portrait = val.sender_portrait;
	        dataToRender.timestr = val.timestr;
	        dataToRender.ploneTimeStamp = val.timestamp;
	        dataToRender.timeStamp = this.convertToUNIXTimestamp(val.timestamp);
	        dataToRender.approved = val.approved;
	        dataToRender.siteUrl = val.site_url;
	        dataToRender.group = val.group;
	
	        var strip = $('<div>' + val.message + '</div>').text();
	        dataToRender.msg = strip.substr(0,30) + (strip.length > 30 ? '...' : '');
	        
	        // rendering
	        /** @uses `ityou.imessage/ityou/imessage/browser/templates/imessage-inbox.pt:126` */
	        if(direction === 'append') {
	            $($(this.messageTemplate).render(dataToRender)).appendTo(this.messageList);
	        } else if(direction === 'prepend') {
	            $($(this.messageTemplate).render(dataToRender)).prependTo(this.messageList);
	        }
	    }, this));
	} else if(this.isDialogOverview()) {
		// current-view is `dialog-overview`
		$.each(data, $.proxy(function(index, val) {
			var dataToRender = {},
				unread = 0;
			var changed = val.sender_id === this.user_id;
			var replace_text = true;
			
			if(val.group === true || val.sender_id === this.user_id) {
				val.sender_id = val.receiver_id;
				val.sender_portrait = val.receiver_portrait;
				val.sender_name = val.receiver_name;
			}
			
			var tmp = $('div[data-dialog="' + val.sender_id + '"]');
			
			if(tmp.length > 0) {
				unread = tmp.find('span.badge').length > 0 ? parseInt(tmp.find('span.badge').text()) : 0;
				
				if(tmp.data('timestamp') > val.timestamp) {
					replace_text = false;
				} else {
					tmp.remove();
				}
			}
			
			if(replace_text) {
				dataToRender.hash = val.hash;
		        dataToRender.sender_name = val.sender_name;
		        dataToRender.sender_id = val.sender_id;
		        dataToRender.sender_portrait = val.sender_portrait;
		        dataToRender.timestr = val.timestr;
		        dataToRender.ploneTimeStamp = val.timestamp;
		        dataToRender.timeStamp = this.convertToUNIXTimestamp(val.timestamp);
		        dataToRender.siteUrl = val.site_url;
		        dataToRender.group = val.group;
		        dataToRender.unread = val.unread + unread;
		        dataToRender.lastFromMe = changed;
		
		        var strip = $('<div>' + val.message + '</div>').text();
		        dataToRender.msg = strip.substr(0,30) + (strip.length > 30 ? '...' : '');
		        
		        // rendering
		        /** @uses @uses `ityou.imessage/ityou/imessage/browser/templates/dialog-overview.pt:70` @ L453, 455 */
		        if(direction === 'append') {
		            $($(this.template.do_messageTemplate).render(dataToRender)).appendTo(this.selector.dialogMessageList);
		        } else if(direction === 'prepend') {
		            $($(this.template.do_messageTemplate).render(dataToRender)).prependTo(this.selector.dialogMessageList);
		        }
			}
		}, this));
		
		// set latest timetamp
		var d = [];
		$(this.selector.dialogMessageList).find('> div[data-timestamp]').each(function() {
			d.push($(this).data('timestamp'));
		});
		
		this.setLatestTimestamp(this.maxDate(d));
	}
};


/**
 * helper function to define newest date
 * 
 * @param   {Array} dates
 * @returns {String}
 */
ImessageOverview.prototype.maxDate = function(dates) {
	var max = dates[0];
	
	for(var i = 1; i < dates.length; i++) {
		if(dates[i-1] < dates[i]) {
			max = dates[i];
		}
	}
	
	return max;
};


/**
 * event handler registration
 * 
 * @events
 */
ImessageOverview.prototype.eventHandler = function() {
	if(this.isDialogOverview()) {
		/** @events what to do if user clicks on a user portrait */
		$(this.getOption('dialogMessageList', 'selector')).on('click', '.user-information > .user-portrait + div', $.proxy(function(e) {
			location.href = $(e.currentTarget).find('a').attr('href');
		}, this));
	} else {
		/** @events de-/selection of checkbox `select-all` */
	    $('#imessage-inbox').on('change', 'thead input[type="checkbox"][name="selectAll"]', $.proxy(function(e) {
	        var $this = $(e.currentTarget),
	            $checkboxes = $('#imessage-inbox').find('tbody').find('input[type="checkbox"]');
	        
	        if($this.prop('checked')) {
	            this.checkAll($checkboxes);
	        } else {
	            this.uncheckAll($checkboxes);
	        }
	    }, this));
	    
	    /** @events de-/selection of checkboxes */
	    $('#imessage-inbox').on('change', 'tbody input[type="checkbox"]', $.proxy(function(e) {
	        var $this = $(e.currentTarget),
	            $checkAll = $('#imessage-inbox').find('thead').find('input[type="checkbox"][name="selectAll"]');
	        
	        if(!$this.prop('checked') && $checkAll.prop('checked')) {
	            $checkAll.prop('checked', false);
	        }
	    }, this));
	    
	    /** @events selection what to do with selected items */
	    $('#imessage-inbox').on('change', 'select[name="doWithSelected"]', $.proxy(function(e) {
	        var $this = $(e.currentTarget),
	            val = $this.val(),
	            $checked = $('#imessage-inbox').find('tbody').find('input[type="checkbox"]:checked');
	        
	        if(val.toLowerCase() === 'markasread' && $checked.length > 0) {
	            this.markAsRead($checked);
	        } else if(val.toLowerCase() === 'delete' && $checked.length > 0) {
	            this.deleteMessage($checked);
	        }
	    }, this));
	    
	    /** @events what to do when sorting the table */
	    $('#imessage-inbox').on('click', 'thead th.sortable', $.proxy(function(e) {
	        var $el = $(e.currentTarget),
	            direction = $el.data('sort-direction') || 'asc';
	        
	        switch($el.data('sort-by')) {
	            case 'date':
	                this.sortByDate($el, direction);
	                
	                break;
	        }
	    }, this));
	    
	    /** @events forwarding to a dialog */
	    $('#imessage-inbox').on('click', 'tbody tr', $.proxy(function(e) {
	        if(e.target.nodeName.toLowerCase() === 'td') {
	        	location.href = $(e.currentTarget).data('url');
	        }
	    }, this));
	    
	    /** @events mark as read */
	    $('#imessage-inbox').on('click', 'button[data-action="markAsRead"]', $.proxy(function(e) {
	        this.markAsRead($(e.target));
	    }, this));
	    
	    /** @events delete */
	    $('#imessage-inbox').on('click', 'button[data-action="delete"]', $.proxy(function(e) {
	        this.deleteMessage($(e.target));
	    }, this));
	    
	    /** @events keyboard filter */
	    $('#imessage-inbox').on('keyup', '#filter_inbox', $.proxy(function(e) {
	        this.filter(e);
	    }, this));
	    
	    /** @events clear filter */
	    $('#imessage-inbox').on('click', '.inbox-clear-filter', $.proxy(function(e) {
	        this.resetInboxFilters();
	    }, this));
	}
};


/**
 * helper function to sort by dates
 * 
 * @param {Object} $el
 * @param {String} direction
 */
ImessageOverview.prototype.sortByDate = function($el, direction) {
    var timestamps = [];
        
    $('#imessage-inbox').find('tbody td[data-unix]').each($.proxy(function(k, el) {
        timestamps.push($(el).data('unix'));
    }, this));
    
    if(undefined !== $el) {
        if(direction === 'asc') {
            $el.data('sort-direction', 'desc').removeClass('sort-desc').addClass('sort-asc');
        } else {
            $el.data('sort-direction', 'asc').removeClass('sort-asc').addClass('sort-desc');
        }
    } else {
        direction = 'desc';
    }

    timestamps = this.sortNumeric(timestamps, direction);

    var rows = [];

    $.each(timestamps, $.proxy(function(k, v) {
        var $row = $('#imessage-inbox').find('tbody td[data-unix="' + v + '"]').parents('tr');
        
        rows.push($row);
    }, this));

    this.tableSort($('#imessage-inbox').find('tbody'), rows);
};


/**
 * load more messages
 */
ImessageOverview.prototype.loadMoreEvent = function() {
    var $tr = $('#imessage-inbox').find('tfoot .load-more-messages').parents('tr');
    $tr.removeClass('hidden');

    /** @events load more messages when clicking table footer */
    $('#imessage-inbox').one('click', 'tfoot .load-more-messages', $.proxy(function(e) {
        var offset = $('#imessage-inbox').find('table').find('tbody').children().length;
        
        this.getMessages(offset);
        
        $tr.addClass('hidden');
    }, this));

    /** @events load more messages on scrolling */
    $(window).one('scroll', $.proxy(function(e) {
        var loadMore = $('#imessage-inbox').find('tfoot .load-more-messages');
        
        var st = $(e.currentTarget).scrollTop();
    
        if(loadMore.is(':in-viewport') && loadMore.is(':visible') && st > this.lastScrollTop) {
            var offset = $('#imessage-inbox').find('table').find('tbody').children().length;
            
            this.getMessages(offset);
            
            $tr.addClass('hidden');
        } else {
            this.loadMoreEvent();
        }
        
        this.lastScrollTop = st;
    }, this));
};


/**
 * helper function to switch checkbox status
 * 
 * @param {Array} els
 * @param {Boolean} status
 */
ImessageOverview.prototype.checkboxStatus = function(els, status) {
    els.each($.proxy(function(k, el) {
        $(el).prop('checked', status);
    }, this));
};


/**
 * helper function to select all checkboxes 
 * 
 * @param {Array} els
 */
ImessageOverview.prototype.checkAll = function(els) {
    this.checkboxStatus(els, true);
};


/**
 * helper function to deselect all checkboxes
 * 
 * @param {Array} els
 */
ImessageOverview.prototype.uncheckAll = function(els) {
    this.checkboxStatus(els, false);
};


/**
 * helper function to mark a message as read
 * 
 * @param {Object} el
 */
ImessageOverview.prototype.markAsRead = function(el) {
    this.changeMessageStatus(el, 'message_read_by_receiver');
};


/**
 * helper function to mark a message as deleted
 * 
 * @param {Object} el
 */
ImessageOverview.prototype.deleteMessage = function(el) {
    this.changeMessageStatus(el, 'message_hidden_by_receiver');
};


/**
 * helper function to change the status of one or more messages
 * 
 * @uses `@@ajax-messages?action=message_read_by_receiver|message_hidden_by_receiver` @ L726
 * 
 * @param {Object} el
 * @param {String} state	message_read_by_receiver|message_hidden_by_receiver
 */
ImessageOverview.prototype.changeMessageStatus = function(el, state) {
    var hash = new Array();
    
    if(el.length > 1) {
        el.each($.proxy(function(k, elem) {
            hash.push($(elem).parents('tr').data('hash'));
        }, this));
    } else {
        hash.push(el.parents('tr').data('hash'));
    }
   
    /** @uses `@@ajax-messages?action=message_read_by_receiver|message_hidden_by_receiver` */
    $.getJSON(this.settings.ajax.remote + '/@@ajax-messages', {action: state, mids: JSON.stringify(hash)}, function() {
    	StatusFlags.prototype.imessageNotify.getNotify();
    });
    
    if(state === 'message_read_by_receiver') {
        this.renderReadMessages(hash);
    } else {
        this.renderDeletedMessages(hash);
    }
};


/**
 * helper function to render messages marked as read
 * 
 * @param {Array} hash
 */
ImessageOverview.prototype.renderReadMessages = function(hash) {
    $.each(hash, $.proxy(function(k, val) {
        $('tr[data-hash="' + val + '"]').removeClass('unread')
                .find('button[data-action="markAsRead"]').remove();
    }, this));
};


/**
 * helper function to render messages marked as deleted
 * 
 * @param {Array} hash
 */
ImessageOverview.prototype.renderDeletedMessages = function(hash) {
    $.each(hash, $.proxy(function(k, val) {
        var $el = $('tr[data-hash="' + val + '"]');
        
        $el.fadeOut(500, function() {
            $el.remove();
        });
    }, this));
};


/**
 * inbox streamer
 * 
 * @TODO possible deprecated?
 */
ImessageOverview.prototype.inboxStream = function() {
	if(null === this.getLatestTimestamp() || undefined == this.getLatestTimestamp()) {
		var els = $('#imessage-inbox').find('tr[data-tiemstamp'),
			timestamps = new Array();
		
		$.each(els, $.proxy(function(k, el) {
			timestamps.push([$(el).data('hash'), $.trim($(el).find('td[data-unix]').data('unix'))]);
		}, this));
		
		timestamps = this.sortNumericArray(timestamps, 'desc');
        
        if(timestamps.length > 0) {
            var latestTimestamp = $('tr[data-hash="' + timestamps[0][0] + '"]').data('timestamp');
            
            this.setLatestTimestamp(latestTimestamp);
        }
	}
	
	this.getLatestMessages();
};


/**
 * stop inbox streamer
 * 
 * @TODO possible deprecated
 */
ImessageOverview.prototype.stopInboxStream = function() {
    if(this.runningStream) {
        this.runningStream = clearInterval(this.runningStream);
        this.setLatestTimestamp(null);
    }
};


/**
 * save latest (=newest) timestamp to local storage
 * 
 * @param {String} timestamp
 */
ImessageOverview.prototype.setLatestTimestamp = function(timestamp) {
	if(this.isInbox()) {
		this.storage.local.set('imessageInboxTimestamp', timestamp);
		this.latestTimestamp = timestamp;
	} else if(this.isDialogOverview()) {
		this.storage.local.set('imessageDialogOverviewTimestamp', timestamp);
		this.latestTimestamp = timestamp;
	}
    
    return this;
};


/**
 * get latest timestamp from local storage
 * 
 * @returns {String}
 */
ImessageOverview.prototype.getLatestTimestamp = function() {
    return this.latestTimestamp || (this.isInbox() ? this.storage.local.get('imessageInboxTimestamp') : this.storage.local.get('imessageDialogOverviewTimestamp'));
};


/**
 * filter a result list
 * 
 * @TODO check implementation
 * 
 * @param {KeyboardEvent} keyEvent
 */
ImessageOverview.prototype.filter = function(keyEvent) {
    var $target = $(keyEvent.currentTarget);
    
    this.clearFiltering(true);

    if(undefined === this.keyupDelay || false === this.keyupDelay) {
        this.keyupDelay = setTimeout($.proxy(function() {
            var val = $target.val();
            
            if(val.length > this.minValue && val !== this.cachedVal) {
                this.cachedVal = val;
                
                this.stopInboxStream();
                this.clearFiltering();
                
                $(this.messageList).empty();;
                this.showSpinner();
                
                this.searchUser(val);
                this.timerCallback('filteredUsers', 'fetchFromDialog');
                
                this.keyupDelay = clearTimeout(this.keyupDelay);
            }
        }, this), 500);
    } else {
        this.keyupDelay = clearTimeout(this.keyupDelay);
    }
};


/**
 * @TODO possible deprecated
 */
ImessageOverview.prototype.timerCallback = function(property, callback) {
    var timer = setInterval($.proxy(function() {
        if(undefined !== this[property]) {
            clearInterval(timer);

            var funcValue = this[callback]();
            
            if(undefined !== funcValue) {
                this.returnValue = funcValue;
            }
        }
    }, this), 100);
};


/**
 * @TODO check implementation & documentation
 */
ImessageOverview.prototype.fetchFromDialog = function() {
    this.fetchMessages(this.filteredUsers);
    this.timerCallback('filteredMessages', 'sortMessages');
    
    var timer = setInterval($.proxy(function() {
        if(undefined !== this.returnValue) {
            clearInterval(timer);
            
            $(this.messageList).empty();
        
            if(this.returnValue.length > 0) {
                this.renderMessages(this.returnValue, 'append');
            } else {
                $($('#inbox-filter-nomatch-tmpl').render()).appendTo(this.messageList);
            }
            
            this.hideSpinner();
        }
    }, this), 100);
};


/**
 * @TODO check implementation & documentation
 */
ImessageOverview.prototype.sortMessages = function() {
    var tmp = new Array();

    if(this.filteredMessages.length > 0) {
        // breaking outer arrays
        $.each(this.filteredMessages, $.proxy(function(k, value) {
            $.each(value, $.proxy(function(i, innerValue) {
                innerValue.unixTimestamp = this.convertToUNIXTimestamp(innerValue.timestamp);
                
                tmp.push(innerValue);
            }, this));
        }, this));
        
        // sorting
        return this.sortReverse(tmp, 'unixTimestamp');
    }
    
    return tmp;
};


/**
 * @TODO check implementation & documentation
 */
ImessageOverview.prototype.searchUser = function(value) {
    var userList = new Array();

    $.getJSON(this.settings.ajax.remote + '/@@ajax-users', {action: 'query', q: value, l: 5}, $.proxy(function(response) {
        $.each(response, $.proxy(function(k, val) {
            userList.push(val.id);
        }, this));
        
        this.filteredUsers = userList;
    }, this));
};


/**
 * @TODO check implementation & documentation
 */
ImessageOverview.prototype.fetchMessages = function(userlist, offset, messages) {
    if(undefined === messages) {
        messages = new Array();
    }
    
    if(undefined === offset) {
        offset = 0;
    }
    
    if(userlist.length === 0) {
        this.filteredMessages = messages;
        return ;
    }
    
    $.getJSON(this.settings.ajax.remote + '/@@ajax-messages', {action: 'get_messages', sender_id: userlist[0], approved: 'all', max: this.filterMax, offset: offset}, $.proxy(function(resp) {
        if(resp.length > 0 && resp[0].sender_id !== this.user_id) {
        	$.each(resp, $.proxy(function(i, val) {
            	// need to change response[i][timestr]
            	resp[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
            }, this));
        	
            messages.push(resp);
        }
    
        return this.fetchMessages(userlist.slice(1, userlist.length), offset, messages);
    }, this));
};


/**
 * @TODO check implementation & documentation
 */
ImessageOverview.prototype.sortReverse = function(data, property) {
    var tmp = data.sort(function(a, b) {
        a = a[property];
        b = b[property];
    
        return a-b;
    });
    
    tmp.reverse();
    
    return tmp;
};


/**
 * @TODO check implementation & documentation
 */
ImessageOverview.prototype.clearFiltering = function(userlist) {
    this.filteredMessages = undefined;
    this.returnValue = undefined;
    
    if(undefined !== userlist) {
        this.filteredUsers = undefined;
    }
};


/**
 * @TODO check implementation & documentation
 */
ImessageOverview.prototype.resetInboxFilters = function() {
    this.clearFiltering(true);
    
    $(this.messageList).empty();
    $('#filter_inbox').val('').blur();
    
    this.getMessages(0);
    this.inboxStream();
};








/**
 * Example Output:
 * [Array[3], Array[2]]
 *  0: Array[3]
 *    0: "lmeise"
 *    1: "Lisa Meise"
 *    2: "Li Mei"
 *  1: Array[2]
 *    0: "hmustermann"
 *    1: "Hans Mustermann"
 */
/**
 * @TODO check implementation & documentation
 */
ImessageOverview.prototype.getAllSenderNames = function() {
    var uid = new Array(),
        sender = new Array();

    $('#imessage-inbox').find('td[data-uid]').each($.proxy(function(k, el) {
        var currentUid = $(el).data('uid'),
            currentName = $.trim($(el).text());

        if($.inArray(currentUid, uid) === -1) {
            uid.push(currentUid);
            sender.push([currentUid, currentName]);
        } else {
            $.each(sender, function(i, val) {
                if(currentUid === val[0] && $.inArray(currentName, val) === -1) {
                    val.push(currentName);
                }
            });
        }
    }, this));
    
    return sender;
};







