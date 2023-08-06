/**
 * IMessage Form where user can search users/groups and write them single messages or create a chat group
 * 
 * @module iMessageClearNewMessage
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:iMessageCleanNewMessage
 */
function IMessageCleanNewMessage(settings) {
	this.name = 'ityou.imessage.cleanmessage';
	this.version = '0.3.260814';
	
    // temp storage
    this.cache = {
        // own userid
        userId: undefined,
        
        // handle view
        currentView: undefined,
        partnerId: undefined,
        
        // search
        input_value: undefined,
        currentSelectedElement: undefined,
        receiverList: [],
        receiverGroupList: []
    };
    
    // animations
    this.animation = {
        speedDown: 400,
        speedUp: 200,
        removeHighlight: 1500
    };
    
    // selectors
    this.selector = {
        editor: '#message-textarea',
        editorControls: '.message-controls',
        // search
        form: '#message_receiver',
        ids: '#w_user_id',
        input: '#w_user_name',
        resultList: '.usersearch ul.users',
        receiverList: '#receiver_list ul',
        group: '.group-creation',
        groupName: '#group-name',
        // translation
        noMatch: '#imessage_no_match_found',
        // creation mode
        creation: '#create-dialog-as-groupchat',
        modal: '#imessage-message-successfully-sent'
    };
    
    // templates
    this.template = {
        search: '#imessage-usersearch-template',
        list: '#imessage-receiverlist-template'
    };
    
    // settings
    this.settings = {
        max: 10,
        minLength: 1,
        minContentLength: 1,
        minGroupnameLength: 1,
        waiting: 500,
        useGroups: false,
        useWYSIWYG: false
    };
    
    // extend settings object with given settings in constructor
    if(settings) {
    	this.settings = $.extend(this.settings, settings);
    }
};



// inherits functionality of `module:Utilities`
/** @uses module:Utilities */
IMessageCleanNewMessage.prototype = new Utilities();

/** @uses module:Clipboard */
IMessageCleanNewMessage.prototype.Clipboard = new Clipboard();



/**
 * initialize clean new message
 * 
 * @constructs
 *
 * @param {Object} settings
 */
IMessageCleanNewMessage.prototype.init = function(settings) {
	// memorize userid to cache
    this.setCache('userId', $('#ESI_DATA').data('ityou-uid'));
    // set settings if given
    this.setSettings(settings);
    
    // define in which template we are
    this.defineView();
    
    // check if template is for clean new message
    if(this.isCleanNewMessage()) {
    	// register event handler
        this.initEventHandler();
        
        // detect either user can create groups or not
        if(parseInt($(this.getOption('form', 'selector')).data('use-groups')) === 1) {
        	this.setOption('useGroups', true, 'settings');
        }
        
        // detect if we should usw a `What You See Is What You Get` Editor
        if(this.getOption('useWYSIWYG', 'settings') === true) {
        	this.initTinyMCE();
        } else {
        	// register auto grow plugin if not using `WYSIWYG`
        	$(this.getOption('editor', 'selector')).autoGrow();
        	
        	// register clipboard controls
        	this.Clipboard.addPasteControls();
        }
        
        // initialize groups if user may use them
        if(this.getOption('useGroups', 'settings') === true) {
        	this.groups();
        }        
    }
};


/**
 * define which page is currently viewed
 */
IMessageCleanNewMessage.prototype.defineView = function() {
    var pathname = document.location.pathname,
        matchAgainst = /@@messages/i,
        pathsearch = document.location.search;
    
    // check if we're currently viewing the form without a dialog
    if(matchAgainst.exec(pathname) && pathsearch.length === 0) {
        this.setCache('currentView', 'clean_message');
    
        return ;
    }
    
    // not viewing form
    this.setCache('currentView', undefined);
    this.setCache('partnerId', undefined);
};


/**
 * helper function to ask if we can build clean imessage form
 *
 * @returns {Boolean}
 */
IMessageCleanNewMessage.prototype.isCleanNewMessage = function() {
    if(this.getCache('currentView') === 'clean_message') {
        return true;
    }
    
    return false;
};


/**
 * helper function get catch groups from server
 * 
 * @uses `@@ajax-users?action=groups`
 * 
 * @TODO: group image
 */
IMessageCleanNewMessage.prototype.groups = function() {
	if(!this.storage.session.get('user_groups')) {
		// ajax request
		/** @uses `@@ajax-users?action=groups` */
		$.ajax({
			url: this.settings.ajax.remote + '/@@ajax-users' + this.settings.ajax.callback,
			data: {
				action: 'groups'
			},
			dataType: 'json',
			// event handler success
			success: $.proxy(function(response) {
				/** @TODO: solange keine bilder fuer gruppen existieren (MR) */
				$.each(response, $.proxy(function(i, v) {
					response[i]['portrait'] = this.settings.ajax.remote + '/++resource++ityou.esi.theme.img/group_icon.png';
				}, this));
				
				// save groups to session storage
				this.storage.session.set('user_groups', response);
			}, this),
			// event handler success
			error: $.proxy(function(XMLHttpRequest, textStatus, errorThrown) {
	            this.log(XMLHttpRequest, textStatus, errorThrown);
			}, this)
		});
	}
};


/**
 * search for users and groups by given string
 * 
 * @uses `@@ajax-users?action=query`
 * @uses `ityou.imessage/ityou/imessage/browser/templates/imessage.pt:156` @ L270
 * 
 * @param {String} value 
 */
IMessageCleanNewMessage.prototype.search = function(value) {
    var $wrapper = $(this.getOption('form', 'selector')).find('.input_holder').find('.usersearch');
    
    // ajax request
    /** @uses `@@ajax-users?action=query` */
    $.ajax({
        url: this.settings.ajax.remote + '/@@ajax-users' + this.settings.ajax.callback,
        data: {
            action: 'query',
            q: value,
            l: this.getOption('max', 'settings')
        },
        dataType: 'json',
        // event handler success
        success: $.proxy(function(response) {
        	// pointer to the result list
            var $resultList = $(this.getOption('resultList', 'selector'));
            
            if(response.length == 0 && $('#group-creation').length == 0) {
            	// if the result is empty clear result list and tell the user there was no match
            	this.emptyResultList();
            	
            	setTimeout($.proxy(function() {
            		this.noMatch();
            	}, this), 1);
            	
            	$wrapper.fadeIn('fast');
            } else {
            	var list;
            	
            	if($('#group-creation').length > 0) {
            		// put receiver lists together (users + groups)
            		list = [].concat(this.getCache('receiverList')).concat(this.getCache('receiverGroupList'));
            	} else {
            		// only users
            		list = [].concat(this.getCache('receiverList'));
            	}
            	// add user himself to temp receiver list, need to filter him out of search results aswell
            	list.push(this.getCache('userId'));
                
                // add groups if activated
                if(this.getOption('useGroups', 'settings') === true && $('#group-creation').length > 0) {
                	response = this.filterGroups(value).concat(response);
                }
                
                // filter myself and duplicates of the response 
                response = this.filter(response, list);
                
                if(!$(this.getOption('input', 'selector')).is(':focus')) {
                    $wrapper.hide();
                } else {
                    $wrapper.fadeIn('fast');
                }
                
                if(response.length > 0) {
                	// empty result list and refill it
                    this.emptyResultList();
                    /** @uses `ityou.imessage/ityou/imessage/browser/templates/imessage.pt:156` */
                    $resultList.show().append($(this.getOption('search', 'template')).render(response));
                } else {
                	// hide result list if there are no results left
                    this.emptyResultList();
                    this.noMatch();
                    $wrapper.fadeIn('fast');
                }
            }
        }, this)
    });
};


/**
 * helper function to filter all groups by search string
 * the `@` is a selector for returning all groups
 * 
 * @param   {String} searchStr
 * @returns {Array}
 */
IMessageCleanNewMessage.prototype.filterGroups = function(searchStr) {
	// catch groups from session storage
	var groups = this.storage.session.get('user_groups'),
		output = [];
	
	// check which string is given
	if(searchStr === '@') {
		// return all groups
		$.each(groups, $.proxy(function(key, value) {
			value.group = true;
			output.push(value);
		}, this));
	} else {
		// loop through groups and match group names with given pattern
		// if found, push it into an array
		$.each(groups, $.proxy(function(key, value) {
			// value.name
			var regexp = new RegExp(searchStr, 'i');
	
			// found
			if(value.name.search(regexp) > -1) {
				value.group = true;
				
				output.push(value);
			}
		}, this));
	}
	
	return output;
};


/**
 * helper function to filter users/groups out if they're already on the receiver-list
 * 
 * @param   {Object} data
 * @param   {Array} list
 * @returns {Object}
 */
IMessageCleanNewMessage.prototype.filter = function(data, list) {
    if(data.length === 0 || list.length === 0) {
        return data;
    }
    
    // throw an error if data is not given
    if(!data) {
        this.log('ImessageCleanNewMessage', 'ERROR IN FILTER');
    }
    
    var tmpList = [],
        found = -1;
        
    $.each(data, $.proxy(function(index, tmp) {
        $.each(list, $.proxy(function(key, value) {
        	if(tmp.id === value) {
                // remove if found
                list.splice(key, 1);
                data.splice(index, 1);
                
                // call me again
                this.filter(data, list);
                
                // define found so we can break the outer each loop
                found = key;
                return false;
            }
        }, this));
        
        if(found > -1) {
            return false;
        }
    }, this));
    
    return data;
};


/**
 * helper function to give user feedback that his search has no match
 */
IMessageCleanNewMessage.prototype.noMatch = function() {
    var no_match_found = $(this.getOption('noMatch', 'selector')).text(),
        $resultList = $(this.getOption('resultList', 'selector'));
        
    $resultList.append('<li class="text-center nomatch-found"><em>' + no_match_found + '</em></li>').show();
};


/**
 * add user/group to receiver list
 * 
 * @param {String} uid
 * @param {String} portrait
 * @param {String} name
 * @param {Boolean} group
 */
IMessageCleanNewMessage.prototype.addToReceiverList = function(uid, portrait, name, group) {
	// check if receiver is group or not
	if(group) {
		// receiver = group
		var tmp = this.getCache('receiverGroupList');
		
		if($.inArray(uid, tmp) === -1) {
			tmp.push(uid);
			this.setCache('receiverGroupList', tmp);
			this.renderReceiverList({id: uid, portrait_url: portrait, group: true, name: name});
		}
	} else {
		// receiver = user
	    var tmp = this.getCache('receiverList');
	
	    if($.inArray(uid, tmp) === -1) {
	        tmp.push(uid);
	        this.setCache('receiverList', tmp);
	        this.renderReceiverList({id: uid, portrait_url: portrait, name: name, portal_url: $('#ESI_DATA').data('ityouPortalUrl')});
	    }
	}
	
	this.hideResultList();
	    
    this.setCache('currentSelectedElement', undefined);
    
    // show option to create a groupchat
    if(this.getCache('receiverGroupList').length > 0 || this.getCache('receiverList').length > 1) {
    	$(this.getOption('group', 'selector')).removeClass('hidden');
    }
};


/**
 * remove user/group from receiver lit
 * 
 * @param {String} uid
 * @param {Boolean} group
 */
IMessageCleanNewMessage.prototype.removeFromReceiverList = function(uid, group) {
	// check if receiver is group or not
	if(group) {
		// receiver = group
		var tmp = [],
			current = this.getCache('receiverGroupList');
		
		$.each(current, $.proxy(function(index, value) {
			if(value !== uid) {
				tmp.push(value);
			}
		}, this));
		
		this.setCache('receiverGroupList', tmp);
	} else {
		// receiver = user
	    var tmp = [],
	        current = this.getCache('receiverList');
	    
	    $.each(current, $.proxy(function(index, value) {
	        if(value !== uid) {
	            tmp.push(value);
	        }
	    }, this));
	    
	    this.setCache('receiverList', tmp);
	}
	
	// hide option to create a groupchat
	if(this.getCache('receiverGroupList').length < 1 && this.getCache('receiverList').length < 2) {
		var groupCreation = $(this.getOption('group', 'selector')); 
    	
		groupCreation.addClass('hidden');
		groupCreation.find(this.getOption('groupName', 'selector')).val('');
		groupCreation.find(this.getOption('creation', 'selector')).prop('checked', false).trigger('change');
    }
};


/**
 * render the receiver list
 * 
 * @uses `ityou.imessage/ityou/imessage/browser/templates/imessage.pt:190` @ L471
 */
IMessageCleanNewMessage.prototype.renderReceiverList = function(data) {
	/** @uses `ityou.imessage/ityou/imessage/browser/templates/imessage.pt:190` */
    $(this.getOption('receiverList', 'selector')).append($(this.getOption('list', 'template')).render(data));
};


/**
 * helper function to toggle selection highlighting
 */
IMessageCleanNewMessage.prototype.toggleHighlight = function(element, state) {
    if(state === true) {
        element.addClass('hover');
    } else {
        element.removeClass('hover');
    }
};


/**
 * helper function to hide the result list
 */
IMessageCleanNewMessage.prototype.hideResultList = function() {
    $(this.getOption('resultList', 'selector')).hide();
    
    $(this.getOption('input', 'selector')).val('');
};


/**
 * helper function to empty the result list
 */
IMessageCleanNewMessage.prototype.emptyResultList = function() {
    $(this.getOption('resultList', 'selector')).empty();
};


/**
 * initialize TinyMCE, a `What You See Is What You Get` text-editor
 */
IMessageCleanNewMessage.prototype.initTinyMCE = function() {
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
            // filter html out of the result
        	// the second property defines html tags which should NOT be filtered out,
        	// they will be left
            o.content = this.stripTags(o.content, '<img><strong><em><span><ul><ol><li><a><p>');
        }, this)
    });
};


//
// Event Handler Functions below
// -----------------------------------------------------------------------------

/**
 * initialize event handler for mouse and keyboard events
 * 
 * @events
 */
IMessageCleanNewMessage.prototype.initEventHandler = function() {

    var $input = $(this.getOption('input', 'selector')),
        keyDelay = this.getOption('waiting', 'settings');
    
    
    /** @events handle keyboard events on input */
    $(document).on({
    	/** @eventy keyup */
        keyup: $.proxy(function(e) {
            var key = e.which;
            
            // 38 = uparrow
            // 40 = downarrow
            // do nothing when these keys are pressed,
            // we need their event at another place (LXY) 
            if(key === 38 || key === 40) {
                return ;
            }
            
            // user is typing and searching
            this.setCache('currentSelectedElement', undefined);
            
            if(this.getCache('key_timer')) {
                clearTimeout(this.getCache('key_timer'));
            }
            
            var t = setTimeout($.proxy(function() {
                if($input.val().length >= this.getOption('minLength', 'settings')) {
                    this.setCache('input_value', $input.val());
                    this.search($input.val());
                } else {
                    this.hideResultList();
                }
            }, this), keyDelay);
            
            this.setCache('key_timer', t);
        }, this),
        /** @events keydown */
        keydown: $.proxy(function(e) {
            var key = e.which,
                $resultList = $(this.getOption('resultList', 'selector'));
            
            //  9 = tab
            // 13 = enter
            // 27 = esc
            // 38 = uparrow
            // 40 = downarrow
            switch(key) {
            
                case 13: // adding first search result
                    if($resultList.find('li').length > 0 && $input.val().length >= this.getOption('minLength', 'settings') && !$resultList.find('li').first().hasClass('nomatch-found')) {
                        if(this.getCache('currentSelectedElement')) {
                            this.getCache('currentSelectedElement').trigger('click');
                        } else {
                            $resultList.find('li').first().trigger('click');
                        }
                    }
                    
                    break;
                    
                case 27: // cancel user search
                    this.hideResultList();
                    
                    break;
                    
                case 38:
                case 40: // navigate
                    if($resultList.find('li').length > 0) {
                        var $currentElement = this.getCache('currentSelectedElement');
                        
                        if(!$currentElement) {
                            this.setCache('currentSelectedElement', $resultList.find('li').first());
                            
                            this.toggleHighlight(this.getCache('currentSelectedElement'), true);
                        } else {
                            if(key === 38) { // navigate up
                                if($currentElement.prev().length > 0) {
                                    this.toggleHighlight($currentElement, false);
                                    this.setCache('currentSelectedElement', $currentElement.prev());
                                    this.toggleHighlight(this.getCache('currentSelectedElement'), true);
                                }
                            } else { // navigate down
                                if($currentElement.next().length > 0) {
                                    this.toggleHighlight($currentElement, false);
                                    this.setCache('currentSelectedElement', $currentElement.next());
                                    this.toggleHighlight(this.getCache('currentSelectedElement'), true);
                                }
                            }
                        }
                    }
                    
                    break;
            }
        }, this),
        /** @events blur */
        blur: $.proxy(function(e) {
        
        }, this),
        /** @events focus */
        focus: $.proxy(function(e) {
            $input.trigger('keyup');
        }, this)
    }, this.getOption('input', 'selector'));
    
    
    /** @events prevent form submit */
    $(this.getOption('form', 'selector')).on('submit', $.proxy(function(e) {
        e.preventDefault();
        
        return false; // IE
    }, this));
    
    
    /** @events handle click events on document */
    $(document).on('click', $.proxy(function(e) {
        var $target = $(e.target);
        
        // we want the result list to be closed if the user clicks anywhere else on the page,
        // so we are watching the click event on document
        
        if($target.parents('.usersearch').length > 0) {
        	/** @events user clicked somewhere in the search area */
        	// check if user clicked on a list element
            var $li = $target[0].nodeName.toLowerCase() === 'li' ? $target : ($target.parents('li').length > 0 ? $target.parents('li') : false);

            if($li && !$li.hasClass('nomatch-found')) {
            	// user clicked on a list element and the result list has user/groups as result
                var userid = $li.find('a').attr('title'),
                    img = $li.find('img').attr('src'),
                    name = $li.find('h2').text(),
                    isGroup = $li.find('a').data('group') ? true : false;
                
                // add user/group to receiver list
                if(isGroup) {
                	// list element represents a group
                	this.addToReceiverList(userid, img, name, true);
                } else {
                	// list element represents an user
                	this.addToReceiverList(userid, img, name);
                }
                
                // remove the list element from the result list
                $li.remove();
                
                if($('.usersearch').find('li').length === 0) {
                    this.hideResultList();
                }
            }
        } else if($target.attr('id') === $input.attr('id')) {
        	/** @events user clicked again in the input element */
            ; // nothing to do here
        } else if($target.hasClass('remove') && $target.parents('#receiver_list').length > 0) {
        	/** @events user clicked on `remove from receiver list` icon */
        	var containerId = $target.parents('.thumbnail').attr('id'),
        		uid = containerId.split('-')[1],
        		isGroup = $('[data-group="' + uid + '"]').data('group') ? true : false,
				$li = isGroup ? $('[data-group="' + uid + '"]').parents('li') : $('#' + containerId).parents('li');
				
			// remove user/group from receiver list
			if(isGroup) {
				// element represents a group
				this.removeFromReceiverList(uid, true);
			} else {
				// element represents an user
				this.removeFromReceiverList(uid);
			}
			
			// fadeout the element
			$li.fadeOut(200, function() {
				// after animation has ended, remove it from DOM
				$li.remove();
			});
        } else if($target.hasClass('fa fa-times') && $target.parents('.remove').length > 0 && $target.parents('#receiver_list').length > 0) {
        	/** @events user clicked on `remove from receiver list` icon */
            var containerId = $target.parents('.user').attr('id'),
                uid = containerId.split('-')[1],
                isGroup = $('[data-group="' + uid + '"]').data('group') ? true : false,
                $li = isGroup ? $('[data-group="' + uid + '"]').parents('li') : $('#' + containerId).parents('li');
            
                // remove user/group from receiver list
            if(isGroup) {
            	// element represents a group
            	this.removeFromReceiverList(uid, true);
            } else {
            	// element represents an user
            	this.removeFromReceiverList(uid);
            }
            
            // fadeout the element
            $li.fadeOut(200, function() {
            	// after animation has ended, remove it from DOM
                $li.remove();
            });
        } else if($target.parents(this.getOption('modal', 'selector')).length > 0) {
        	/** @events user sent the message and clicked `ok` in the now opened modal dialog */
        	document.location.href = '/@@dialog-overview';
        } else {
        	/** @events user clicked anywhere else, so we wanna hide the result list */
            this.hideResultList();
        }
    }, this));
    
    
    /** @events toogle group chat */
    var $checkbox = $(this.getOption('creation', 'selector')),
        $groupName = $(this.getOption('group', 'selector')).find('.form-group');
    /** @events change (toggle) */
    $checkbox.on('change', $.proxy(function(e) {
        if($checkbox.prop('checked')) {
            $groupName.removeClass('hidden');
        } else {
            $groupName.addClass('hidden');
        }
    }, this));
    
    /** @events send message */
    $('#message-stream').on('click', 'button.message-save-button', $.proxy(function(e) {
    	var $target = $(e.currentTarget);
    	
    	if(this.getOption('useWYSIWYG', 'settings') === true) {
    		// using `WYSIWYG` editor
    		// check the length of the string
    		// must be longer then `minContentLength` (Default: 1)
			if($(this.getOption('editor', 'selector')).tinymce().getContent().length >= this.getOption('minContentLength', 'settings') && (this.getCache('receiverList').length > 0 || this.getCache('receiverGroupList').length > 0)) {
				$('.mceIframeContainer').removeClass('has-error');
				this.save($target);
			} else if($(this.getOption('editor', 'selector')).tinymce().getContent.length < this.getOption('minContentLength', 'settings')) {
				$('.mceIframeContainer').addClass('has-error');
			}
    	} else {
    		// using simple textarea
    		// check the length of the string
    		// must be longer then `minContentLength` (Default: 1)
    		if($(this.getOption('editor', 'selector')).length >= this.getOption('minContentLength', 'settings') && (this.getCache('receiverList').length > 0 || this.getCache('receiverGroupList').length > 0)) {
				$(this.getOption('editor', 'selector')).removeClass('has-error');
				// save
				this.save($target);
			} else {
				$(this.getOption('editor', 'selector')).addClass('has-error');
			}
    	}
    }, this));
};


/**
 * processing saving message
 * 
 * @param {Object} $el
 */
IMessageCleanNewMessage.prototype.save = function($el) {
	// pointer to the textarea, either to a `WYSIWYG` editor or a simple textarea
    var tinymce = this.getOption('editor', 'selector');
    // give the button a loading symbol
    var buttonText = $el.text(),
        buttonLoader = '<i class="fa fa-spinner fa-spin"></i>';
    // catch receiver list from cache
    var receiver = this.getCache('receiverList'),
        groupReceiver = this.getCache('receiverGroupList');
    
    if(!$el.prop('disabled')) {
    	// avoid send multiple times, so we set the button to disabled after the first submit
    	var content = '';
    	
    	// get message
    	if(this.getOption('useWYSIWYG', 'settings') === true) {
    		content = $(tinymce).tinymce().getContent();
    	} else {
    		content = $(tinymce).val();
    	}
    	
    	// get group name
        var groupName = $(this.getOption('group', 'selector')).find(this.getOption('groupName', 'selector')).val();
        
        // check the value length
        if(content.length <= this.getOption('minContentLength', 'settings') || ($(this.getOption('creation', 'selector')).prop('checked') && groupName.length <= this.getOption('minGroupnameLength', 'settings'))) {
            return ;
        }
        
        // disable button to avoid multiple requests
        $el.prop('disabled', true);
        // show loading symbol
        $el.html(buttonLoader);
        
        var buttonData = {
            button: $el,
            text: buttonText
        };

        if($(this.getOption('creation', 'selector')).prop('checked') === true) {
        	/** @events save as group chat --> redirection */
            this.saveMessage('group', content, buttonData);
        } else {
            if(receiver.length === 1) {
            	/** @events single messages && one receiver --> redirection to dialog */
                this.saveMessage('single', content, buttonData);
            } else if(receiver.length > 1 || groupReceiver.length >= 1) {
            	/** @events single message multiple receiver --> modal dialog */
                this.saveMessage('multi', content, buttonData);
            }
        }
    }
};


/**
 * doing ajax stuff in here for saving a message
 * 
 * @uses `@@ajax-messages?action=post_message`
 * 
 * @param {String} state	single|multi|group
 * @param {String} msg
 * @param {Object} button
 */
IMessageCleanNewMessage.prototype.saveMessage = function(state, msg, button) {
    var $modal = $(this.getOption('modal', 'selector'));
    
    var baseData = {
        action: 'post_message',
        dataType: 'json',
        message: msg
    };
    
    var data,
        userReceiver = this.getCache('receiverList'),
        groupReceiver = this.getCache('receiverGroupList');
        
    var action = 'post_message';
    
    if(state === 'single') {
    	// single messages && one receiver
        data = $.extend({
            receiver_id: userReceiver[0]
        }, baseData);
    } else if(state === 'multi') {
    	// single messages && multiple receiver/group as receiver
    
        if(groupReceiver.length === 0) {
        	// only users, no group
            data = $.extend({
                receiver_id: userReceiver.join(',')
            }, baseData);
        } else if(userReceiver.length === 0) {
        	// only groups, no user
            data = $.extend({
                receiver_group_id: groupReceiver.join(',')
            }, baseData);
        } else if(userReceiver.length > 0 && groupReceiver.length > 0) {
        	// both
            data = $.extend({
                receiver_id: userReceiver.join(','),
                receiver_group_id: groupReceiver.join(',')
            }, baseData);
        }
    
    } else if(state === 'group') {
    	// group chat
        var groupName = $(this.getOption('group', 'selector')).find(this.getOption('groupName', 'selector')).val();
    
        if(groupReceiver.length === 0) {
        	// only users, no group
            data = $.extend({
                receiver_id: userReceiver.join(','),
                new_group: groupName
            }, baseData);
        } else if(userReceiver.length === 0) {
        	// no users, only groups
            data = $.extend({
                receiver_group_id: groupReceiver.join(','),
                new_group: groupName
            }, baseData);
        } else if(userReceiver.length > 0 && groupReceiver.length > 0) {
        	// both
            data = $.extend({
                receiver_id: userReceiver.join(','),
                receiver_group_id: groupReceiver.join(','),
                new_group: groupName
            }, baseData);
        }
    }
    
    
    if(data) {
    	/** @uses `@@ajax-messages?action=post_message` */
        $.ajax({
            url: this.settings.ajax.remote + '/@@ajax-messages' + this.settings.ajax.callback,
            data: data,
            dataType: 'json',
            // event handler success
            success: $.proxy(function(response) {
                if(state === 'single') {
                    document.location.href = '/@@messages?sid=' + response.receiver_id;
                } else if(state === 'multi') {
                    $modal.modal();
                } else if(state === 'group') {
                    document.location.href = '/@@messages?rid=' + response.receiver_id;
                }
            }, this),
            // event handler error
            error: $.proxy(function(XMLHttpRequest, textStatus, errorThrown) {
                this.saveError(button, XMLHttpRequest, textStatus, errorThrown);
            }, this)
        });
    } else {
        this.saveError(button);
    }
        
};


/**
 * helper function if sending the message failed
 * 
 * @TODO error modal instead of alert
 */
IMessageCleanNewMessage.prototype.saveError = function(button, xml, status, error) {
    alert('Send message failed, please try again');
    
    button.button.removeProp('disabled');
    button.button.text(button.text);
};

