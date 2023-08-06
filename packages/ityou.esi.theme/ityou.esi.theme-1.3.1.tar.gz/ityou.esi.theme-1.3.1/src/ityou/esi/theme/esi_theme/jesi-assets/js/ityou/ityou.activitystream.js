/**
 * Activity Stream
 * 
 * @module ActivityStream
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:ActivityStream
 */
function ActivityStream() {
	this.name = 'ityou.activitystream';
	this.version = '0.3.260814';
	
	// temp storage
	this.cache = {
        // own userid
        userId: undefined,
    
        registered: false,
        activityStream: null,
        
        // follow
        onlyFollowing: false,
        followInstalled: false,
        
        // handle view
        currentView: undefined,
        userprofileId: undefined,
        initUserprofile: false,
        
        // block requests if there are any others running
        runningRequest: false
    };
    
	// settings
    this.settings = {
		moderatable: false
    };
    
    // animations
    this.animation = {
        speedDown: 400,
        speedUp: 200,
        removeHighlight: 1500
    };
    
    // id & class selectors
    this.selector = {
        wrapper: '#activity-stream',
        getMore: '.get-more-activities',
        activityList: '#activity-stream-list',
        commentList: '.activity-comment-list',
        followContainer: '#astream-tabs'
    };
    
    // jsrender templates
    this.template = {
        activity: '#activity-stream-template',
        comment: '#comment-stream-template'
    };
}

// inherits functionality of `module:Utilities`
/** @uses module:Utilities */
ActivityStream.prototype = new Utilities();

/** @uses module:ClientTimezone */
ActivityStream.prototype.TimeConverter = new ClientTimezone();

/** @uses module:Clipboard */
ActivityStream.prototype.Clipboard = new Clipboard();


/**
 * initialise activity stream
 */
ActivityStream.prototype.init = function() {
	// memorize userid to cache
    this.setCache('userId', $('#ESI_DATA').data('ityou-uid'));

    // check if follow is installed
    if($(this.getOption('followContainer', 'selector')).length > 0) {
        this.setCache('followInstalled', true);
    }
    
    // define in which template we are
    this.defineView();
    
    // check if current view is activity stream or userprofile
    if(this.isActivityStream('astream')) {
    	// initialize mouse and key events
        this.initEventHandler();
    
        //this.getActivities('get_latest_activities', true);
        // why get more ?
        this.getActivities('get_more_activities');
    } else if(this.isActivityStream('userprofile')) {
    	// initialize mouse and key events
        this.initEventHandler();
    }
};


/**
 * define which page is currently viewed
 */
ActivityStream.prototype.defineView = function() {
    var pathname = document.location.pathname,
        matchAgainst = /author\/(\w.+)/i;

    // check if we're currently viewing a profile
    if(matchAgainst.exec(pathname)) {
        this.setCache('currentView', 'userprofile');
        this.setCache('userprofileId', RegExp.$1);
    
        // we're viewing a profile, need to end function here
        return ;
    }
    
    // check if we're viewing the astream
    if($('#activity-stream').length > 0) {
        this.setCache('currentView', 'astream');
        this.setCache('userprofileId', undefined);
        
        // we're viewing the astream, need to end function here
        return ;
    }
    
    // not viewing any of the options above
    this.setCache('currentView', undefined);
    this.setCache('userprofileId', undefined);
};


/**
 * simple helper to ask if we can build an astream
 *
 * @param   {String} state	astream|userprofile
 * @returns {Boolean}
 */
ActivityStream.prototype.isActivityStream = function(state) {
    if(state && this.getCache('currentView') === state) {
    	// state given and current view = state
        return true;
    } else if(state && this.getCache('currentView') !== state) {
    	// state given and current view != state
        return false;
    } else if(this.getCache('currentView') === 'astream' || this.getCache('currentView') === 'userprofile') {
    	// state not given, current view = astream or userprofile
        return true;
    }
    
    // otherwise
    return false;
};


/**
 * get the current content uid
 * 
 * @returns {String}
 */
ActivityStream.prototype.getContentUid = function() {
	return $('#ESI_DATA').data('ityou-content-uid') === undefined ? "" : $('#ESI_DATA').data('ityou-content-uid'); 
};


/**
 * ajax request in here for getting activities
 * 
 * @uses `@@ajax-activities?action=get_latest_activities|get_more_activities`
 * 
 * @param {String} state	get_latest_activities|get_more_activities
 * @param {Object|Array|String|Number|Boolean} initial	representing if activity stream is started for the first time (e.g. on page load)
 */
ActivityStream.prototype.getActivities = function(state, initial) {
    var timestamp,
        $wrapper = $(this.getOption('wrapper', 'selector')),
        $activityList = $wrapper.find(this.getOption('activityList', 'selector'));

    // define which timestamp is needed to get new/old activities
    if(state === 'get_latest_activities') {
        timestamp = $activityList.find('li.activity').first().data('timestamp');
    } else if(state === 'get_more_activities') {
        timestamp = $activityList.find('li.activity').last().data('timestamp');
        
        // if there's no timestamp set, go with current time
        //if(!timestamp) {
        	//timestamp = (new Date()).toISOString();
        //}
        
        this.showSpinner();
    } else {
        return ;
    }
    
    // hide the get more trigger
    $wrapper.find(this.getOption('getMore', 'selector')).hide();
    
    // if there's still a running ajax request, don't open another
    if(this.cache.runningRequest == false) {
    	// block other ajax requests from being started
	    this.cache.runningRequest = true;
	    
	    // ajax request
    	$.ajax({
    		url: this.settings.ajax.remote + '/@@ajax-activities' + this.settings.ajax.callback,
	        data: {
	            action: state,
	            timestamp: timestamp,
	            uid: this.getCache('userprofileId'),
	            content_uid: this.getContentUid()
	        },
	        dataType: 'json',
	        // event handler success
	        success: $.proxy(function(response) {
	            if(response.length > 0) {
	            	// sort the response descending
	            	response = this.sort(response, 'desc');
	            
	            	// convert dates
	                $.each(response, $.proxy(function(i, val) {
	                	// need to change response[i][timestr]
	                	response[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
	                	
	                	// if there's no revision given, set it to 0
	                	if(typeof response[i]['revision'] !== 'number') {
	                		response[i]['revision'] = 0;
	                	}
	                	
	                	// replace \n with <br> and convert dates
	                    $.each(val.comments, $.proxy(function(j, com) {
	                        response[i].comments[j].comment = response[i].comments[j].comment.replace(/\n/g, '<br>');
	                        
	                        // need to change response[i]['comments'][j]['timestr']
	                        response[i]['comments'][j]['timestr'] = this.TimeConverter.convertTime(com.timestamp);
	                        
	                        if(typeof response[i]['comments'][j]['revision'] !== 'number') {
	                        	response[i]['comments'][j]['revision'] = 0;
	                        }
	                        
	                        // moderation
	                        if(this.getOption('moderatable', 'settings') && response[i]['content_creator'] === this.getCache('userId')) {
	                        	response[i]['comments'][j]['can_delete'] = true;
	                    		response[i]['comments'][j]['can_moderate'] = true;
	                        }
	                        
	                    	response[i]['comments'][j]['revision_old'] = response[i]['revision'] > response[i]['comments'][j]['revision'];
	                    }, this));
	                }, this));
	                
	                // render
	                this.renderActivities(response, state, initial);
	            } else {
	                // remove get more activities trigger if there is no more to load
	                $(this.getOption('wrapper', 'selector')).find(this.getOption('getMore', 'selector')).remove();
	                
	                this.hideSpinner();
	            }
	        }, this),
	        complete: $.proxy(function() {
	        	// free the pipeline
	        	this.cache.runningRequest = false;
	        }, this)
	    });
    }
};


/**
 * ajax request in here for getting new comments
 * 
 * @uses `@@ajax-activities?action=get_latest_comments`
 */
ActivityStream.prototype.getComments = function() {
    var timestamp,
        commentTimestamps = [];
        
    var $wrapper = $(this.getOption('wrapper', 'selector')),
        $commentList = $wrapper.find(this.getOption('commentList', 'selector'));
        
    // collect comment timestamps
    $commentList.each($.proxy(function(i, el) {
        $(el).find('li').each(function() {
            commentTimestamps.push($(this).data('timestamp'));
        });
    }, this));
    
    // sort timestamp and get first = latest
    timestamp = commentTimestamps.sort().reverse()[0];
    // if there is no comment yet, get the timestamp of the latest activity, streaming comments cannot be older then the latest activity
    if(!timestamp) {
        timestamp = $wrapper.find(this.getOption('activityList', 'selector')).find('li.activity').first().data('timestamp');
    }
    
    // ajax request
    $.ajax({
        url: this.settings.ajax.remote + '/@@ajax-activities' + this.settings.ajax.callback,
        data: {
            action: 'get_latest_comments',
            timestamp: timestamp
        },
        dataType: 'json',
        // event handler success
        success: $.proxy(function(response) {
            if(response.length > 0) {
            	$.each(response, $.proxy(function(i, val) {
            		// get the assigned activity
            		var $assignedActivity = $('#' + val.activity_id);
            		
            		// convert date
            		response[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
            		
            		// add revision number
            		if(typeof response[i]['revision'] !== 'number') {
                    	response[i]['revision'] = 0;
                    }
            		
            		if(this.getOption('moderatable', 'settings') && $assignedActivity.data('content-creator') === this.getCache('userId')) {
            			response[i]['can_delete'] = true;
            			response[i]['can_moderate'] = true;
            		}
            		
            		response[i]['revision_old'] = parseInt($('#' + response[i]['activitiy_id']).data('revision')) > response[i]['revision'];
            	}, this));
            	
                // render
                this.renderComments(response);
            }
        }, this)
    });
};


/**
 * rendering activities
 *
 * @uses `ityou.astream/ityou/astream/browser/templates/tmpl-macros.pt:45` @ L367, L379, L400
 *
 * @param {Object} data		representing an object filled with activities
 * @param {String} state	get_latest_activities|get_more_activities
 * @param {Object|Array|String|Number|Boolean} initial	representing if activity stream is started for the first time (e.g. on page load)
 */
ActivityStream.prototype.renderActivities = function(data, state, initial) {
    var activityList = this.getOption('activityList', 'selector'),
        $activityTmpl = $(this.getOption('activity', 'template'));
        
    var speedDown = this.getOption('speedDown', 'animation'),
        speedUp = this.getOption('speedUp', 'animation');
    
    // loop through data
    $.each(data, $.proxy(function(i, val) {
    	if($('#' + val.id).length > 0) {
    		// remove an existing activity from stream to avoid duplicates
    		$('#' + val.id).remove();
    	}
    	
    	// mark clients own comments
    	$.each(val.comments, $.proxy(function(k, comment) {
    		comment.ownComment = comment.user_id === this.getCache('userId');
    	}, this));
    }, this));

    // render latest activities
    if(state === 'get_latest_activities') {
        if(initial) {
            // no animations if it's an initial call (first time call)
        	/** @uses `ityou.astream/ityou/astream/browser/templates/tmpl-macros.pt:45` */
            $($activityTmpl.render(data)).prependTo(activityList);
            
            // loop over activities
            $(activityList).find('li.activity').each($.proxy(function(k, el) {
            	// find comment list in each activity and check for old revisions
            	if($(el).find(this.getOption('commentList', 'selector')).find('li.older_revision').length) {
            		$(el).find('.comment-show').removeClass('hidden').show();
            	}
            }, this));
        } else {
            // add animations if live stream
        	/** @uses `ityou.astream/ityou/astream/browser/templates/tmpl-macros.pt:45` */
            $($activityTmpl.render(data)).prependTo(activityList).hide().addClass('new');
            
            if(this.getCache('followInstalled') && this.getCache('onlyFollowing')) {
                // follow IS installed and i want to show only the items of authors whom i follow
                $(activityList).find('li.activity.following').slideDown(speedDown, this.removeHighlight(this.getOption('removeHighlight', 'animation')));
            } else {
                // follow IS NOT installed, so show all
                $(activityList).find('li.activity').slideDown(speedDown, this.removeHighlight(this.getOption('removeHighlight', 'animation')));
            }
            
            // loop over activities
            $(activityList).find('li.activity').each($.proxy(function(k, el) {
            	// find comment list in each activity and check for old revisions
            	if($(el).find(this.getOption('commentList', 'selector')).find('li.older_revision').length) {
            		$(el).find('.comment-show').removeClass('hidden').show();
            	}
            }, this));
        }
    } else {
        // get_more_activities
    	/** @uses `ityou.astream/ityou/astream/browser/templates/tmpl-macros.pt:45` */
        $($activityTmpl.render(data)).appendTo(activityList).hide();
        
        if(this.getCache('followInstalled') && this.getCache('onlyFollowing')) {
            // follow IS installed and i want to show only the items of authors whom i follow
            $(activityList).find('li.activity.following').slideDown(speedDown);
        } else {
            // follow IS NOT installed, -> show all
            $(activityList).find('li.activity').slideDown(speedDown);
        }
    }
    
    // set latest activity timestamp (localStorage or cookie)
    this.storage.local.set('activitiesTimestamp', $(activityList).find('li.activity').first().data('timestamp'));
    
    // make textarea autogrowing
    $('.comment-textarea').autoGrow();
    
    // show 'get more' container
    $(this.getOption('wrapper', 'selector')).find(this.getOption('getMore', 'selector')).show();
    
    // our own comments are right sided, the comments of others are left sided
    /** @deprecated as of 17.06.14, this is now handled directly via tmpl */
    //this.markUsersComments();
    
    // bug fix
    $(this.getOption('wrapper', 'selector')).find(activityList).find('li').each(function() {
        $(this).css('overflow', '');
    });
    
    // inherit Plone's build-in functionality for viewing thumbnails in a preview dialog
    this.prepOverlay();
    
    this.hideSpinner();
    
    // translation
    $('.activity').find('.btn.comment-write').text($.i18n._('comment'));
    $('.activity').find('.btn.comment-show').text($.i18n._('view_all'));
};


/**
 * render comments and paste them to their assigned activities
 * 
 * @uses `ityou.astream/ityou/astream/browser/templates/tmpl-macros.pt:147` @ L478
 *
 * @param {Object} data		representing an object filled with comments
 */
ActivityStream.prototype.renderComments = function(data) {
    var commentList = this.getOption('commentList', 'selector'),
        $commentTmpl = $(this.getOption('comment', 'template'));
        
    var $wrapper = $(this.getOption('wrapper', 'selector')),
        $activityList = $wrapper.find(this.getOption('activityList', 'selector'));
        
    var speedDown = this.getOption('speedDown', 'animation');
    
    // loop over comment data
    $.each(data, $.proxy(function(index, value) {
    	// find assigned activity
        var $assignedActivity = $activityList.find('#' + value.activity_id);
        
        // if the assigned activity doesn't exist (e.g. it's not yet visible), we do not render this comment
        if($assignedActivity.length > 0) {
        	// look up if the comment already exists, e.g. someone wrote 2 comments in a short interval
        	// the comment is put together
            var $assignedComment = $assignedActivity.find(commentList).find('#' + value.id);
            
            value.ownComment = value.user_id === this.getCache('userId');
            
            if($assignedComment.length > 0) {
                // comment already exists, just change date and text
                $assignedComment.data('timestamp', value.timestamp);
                $assignedComment.find('p.user-comment').html(value.comment.replace(/\n/g, '<br>'));
                $assignedComment.find('.user-information small').text(value.timestr);
                $assignedComment.addClass('new', this.removeHighlight(this.getOption('removeHighlight', 'animation'), $assignedComment));
            } else {
            	// the comment did not exist, so we have to render it
            	/** @uses `ityou.astream/ityou/astream/browser/templates/tmpl-macros.pt:147` */
                var renderedElement = $commentTmpl.render(value),
                    id = $(renderedElement).attr('id');
            
                // paste the rendered comment into the comment list of it's assigned activity
                $(renderedElement)
                    .appendTo(this.getOption('activityList', 'selector') + ' #' + value.activity_id + ' ' + commentList)
                    .hide()
                    .addClass('new')
                    .slideDown(speedDown, this.removeHighlight(this.getOption('removeHighlight', 'animation'), $('#' + value.id)));
            }
            
            /** @deprecated as of 17.06.14, now handled directly via template */ 
            //if(value.user_id === this.getCache('userId')) {
                //$('#' + value.id).addClass('self');
            //}
        }
    }, this));
};


/**
 * helper function to remove the `new` css class on activities and comments
 */
ActivityStream.prototype.removeHighlight = function(delay, el) {
	if(undefined === el) {
		el = $(this.getOption('wrapper', 'selector')).find('.new');
	}
	
    setTimeout(function() {
        el.removeClass('new');
    }, delay);
};


/**
 * helper function for positioning client's comments
 * 
 * @deprecated as of 17.06.14, now handled directly via template
 */
ActivityStream.prototype.markUsersComments = function() {
    $(this.getOption('wrapper', 'selector')).find('.activity-comment').each($.proxy(function(i, el) {
        if($(el).find('a[data-uid]').data('uid') === this.getCache('userId')) {
            //$('#' + $(el).attr('id')).addClass('self');
        	$(el).addClass('self');
        }
    }, this));
};


/**
 * save a written comment server-side
 * 
 * @uses `@@ajax-post-comment`
 *
 * @param {String} comment		content of written comment 
 * @param {String} parentId		assigned activity
 */
ActivityStream.prototype.saveComment = function(comment, parentId) {
	// if comment has no content or no parentid is given, do not save the comment
    if(!comment || !parentId || $.trim(comment) === '') {
        return ;
    }
    
    var $el = $('#' + parentId),
        $button = $el.find('span.input-group-btn > button.comment-save');
    
    // disable button
    $button.removeClass('comment-save').addClass('disabled').find('i')
        .removeClass('fa-save')
        .addClass('fa-spin fa-spinner');
        
    // send request to server
    $.ajax({
        url: this.settings.ajax.remote + '/@@ajax-post-comment' + this.settings.ajax.callback,
        data: {
            comment: $.trim(comment),
            id: parentId
        },
        dataType: 'json',
        // event handler success
        success: $.proxy(function(response) {
            if(response instanceof Object) {
                $el.find('.comment-textarea').val('');
                $el.find('.new-comment-container').hide();
                $el.find('.comment-controls').show();
                
                $button.addClass('comment-save').removeClass('disabled').find('i')
                    .addClass('fa-save')
                    .removeClass('fa-spin fa-spinner');
                    
                this.getComments();
            }
        }, this)
    });
};


//
// Event Handler Functions below
// -----------------------------------------------------------------------------

/**
 * event handler for switchting activity control buttons
 *
 * @param {String} state	activity-hide|acitivity-hide-all|activity-show|activity-show-all
 */
ActivityStream.prototype.activityControls = function(state) {
    var $wrapper = $(this.getOption('wrapper', 'selector')),
        controls = '.activity-controls',
        $controls = $wrapper.find(controls).length > 0 ? $wrapper.find(controls) : $(controls),
        $activity = $wrapper.find(this.getOption('activityList', 'selector')),
        $getMore = $wrapper.find(this.getOption('getMore', 'selector'));
        
    switch(state) {
        case 'activity-hide':
            $controls.find('.show-all').removeClass('hidden').show();
            if($activity.find('li.activity:visible').length <= 1) {
                $controls.find('.hide-all').hide();
                $getMore.hide();
            }
            break;
        case 'activity-hide-all':
            $getMore.hide();
            
            $controls.find('.show-all').removeClass('hidden').show();
            $controls.find('.hide-all').hide();
            break;
        case 'activity-show':
            $controls.find('.hide-all').show();
            if($activity.find('li.activity:not(:visible)').length <= 0) {
                $controls.find('.show-all').hide();
            }
            break;
        case 'activity-show-all':
            $getMore.show();
            
            $controls.find('.hide-all').show();
            $controls.find('.show-all').hide();
            break;
    }
};


/**
 * Plone build-in modal dialog and image preview
 */
ActivityStream.prototype.prepOverlay = function() {
    $('.Image .linked-document, .linked-document').prepOverlay({
        subtype: 'ajax',
        width: '500px',
        height: '50px',
        config: {
            onLoad: $.proxy(function(e) {
                this.prepContentViews();
            }, this)
        }
    });
};


/**
 * Event Handler and Content for Plone build-in modal dialog and image preview
 */
ActivityStream.prototype.prepContentViews = function() {
    var $el = $('.show-preview #content-views').children(),
        color = 'text-primary';

    /** @events */
    $el.on('click', function(e) {
        var url = $(this).find('a').attr('href');
        
        if(url) {
            window.location = url;
        }
    });
    
    $el.each(function() {
        var menu_context = $(this).find('a').html();
        
        $(this).prepend('<div class="content-view-box"/>');
        $(this).find('.content-view-box').html(menu_context);
        $(this).find('a').html('');
        
        if(!$(this).hasClass('selected')) {
            $(this).find('.content-view-box').addClass(color);
        }
    });
    
    /** @events */
    $el.hover(function() {
        if($(this).find('.content-view-box').html().length > 1) {
            var $contentViewBox = $(this).find('.content-view-box');
        
            $contentViewBox
                .removeClass(color)
                .find('.text').show();
        }
    }, function() {
        var $contentViewBox = $(this).find('.content-view-box');
        
        if(!$(this).hasClass('selected')) {
            $contentViewBox.addClass(color);
        }
        
        $contentViewBox.find('.text').hide();
    });
};





//
// Event Handler Functions below
// -----------------------------------------------------------------------------


/**
 * Mouse and Keyboard event handling
 * 
 * @uses `@@ajax-activities?action=delete_comment|activate_comment|deactivate_comment`
 */
ActivityStream.prototype.initEventHandler = function() {
    var speedDown = this.getOption('speedDown', 'animation'),
        speedUp = this.getOption('speedUp', 'animation');

    var wrapper = this.getOption('wrapper', 'selector'),
        $activityList = $(wrapper).find(this.getOption('activityList', 'selector'));

    // hide a single activity
    /** @events */
    $(wrapper).on('click', 'li.activity .activity-hide', $.proxy(function(e) {
        e.preventDefault();
        
        var $el = $(e.currentTarget);
        
        $activityList.find($el.data('parent-id'))
            .slideUp(speedUp, this.activityControls('activity-hide'));
    }, this));
    
    
    // hide all activities
    /** @events */
    $('.activity-controls').on('click', '.hide-all', $.proxy(function(e) {
        e.preventDefault();
        
        $activityList.find('li.activity').slideUp(speedUp);
        
        this.activityControls('activity-hide-all');
    }, this));
    
    
    // show all activities
    /** @events */
    $('.activity-controls').on('click', '.show-all', $.proxy(function(e) {
        e.preventDefault();
        
        $activityList.find('li.activity').slideDown(speedDown);
        
        this.activityControls('activity-show-all');
    }, this));
    
    
    // show textarea writing comment
    /** @events */
    $(wrapper).on('click', 'li.activity .comment-write', $.proxy(function(e) {
        e.preventDefault();
        
        var $el = $(e.currentTarget),
            $parentEl = $($el.data('parent-id'));
        
        $activityList.find('li.activity').each(function() {
            $(this).find('.comment-input-group').hide();
            $(this).find('.comment-textarea').val('');
            $(this).find('.comment-write').show();
        });
        
        $parentEl.find('.comment-write').hide();
        $parentEl.find('.comment-input-group').removeClass('hidden').show();
        
        this.Clipboard.addPasteControls();
    }, this));
    
    
    // save comment
    /** @events */
    $(wrapper).on('click', 'li.activity .comment-save', $.proxy(function(e) {
        e.preventDefault();
        
        var $el = $(e.currentTarget),
            $li = $($el.data('parent-id'));
            
        this.saveComment($li.find('textarea').val(), $el.data('parent-id').split('#')[1]);
    }, this));
    
    
    // hide comment
    /** @events */
    $(wrapper).on('click', 'li.activity .comment-hide', $.proxy(function(e) {
        e.preventDefault();
        
        var $el = $(e.currentTarget)
            $li = $($el.data('parent-id')),
            $assignedActivity = $li.parents('li.activity');
            
        $li.slideUp(speedUp);
        
        $assignedActivity.find('.comment-show').removeClass('hidden').show();
    }, this));
    
    
    // show comments
    /** @events */
    $(wrapper).on('click', 'li.activity .comment-show', $.proxy(function(e) {
        e.preventDefault();
        
        var $activity = $(e.currentTarget).parents('li.activity');
        
        $activity.find(this.getOption('commentList', 'selector')).find('li').slideDown(speedDown, function() {
        	$(this).css('display', 'list-item'); // TODO: unschoen...
        });
        
        $(e.currentTarget).hide();
    }, this));
    
    // delete a comment
    /** @uses `@@ajax-activities?action=delete_comment` */
    /** @events */
    $(wrapper).on('click', 'li.activity .comment-delete', $.proxy(function(e) {
    	e.preventDefault();
    	
    	var $el = $(e.currentTarget),
    		$li = $($el.data('parent-id')),
    		$activity = $(e.currentTarget).parents('li.activity'),
    		activity_id = $activity.attr('id'),
    		comment_id = $li.attr('id');
    	
    	// server request
    	$.ajax({
    		url: this.settings.ajax.remote + '/@@ajax-activities' + this.settings.ajax.callback,
    		data: {
    			action: 'delete_comment',
    			comment_id: comment_id,
    			content_uid: activity_id
    		},
    		dataType: 'json',
    		success: $.proxy(function(response) {
    			// hide element with an animation 
    			$li.slideUp(speedUp, function() {
    				// after animation has ended, remove it from DOM
    				$li.remove();
    			});
    		}, this)
    	});
    }, this));
    
    // moderate a comment
    /** @uses `@@ajax-activities?action=activate_comment|deactivate_comment */
    /** @events */
    $(wrapper).on('click', 'li.activity .comment-moderate', $.proxy(function(e) {
    	e.preventDefault();
    	
    	var $el = $(e.currentTarget),
    		$li = $($el.data('parent-id')),
    		$activity = $(e.currentTarget).parents('li.activity'),
    		activity_id = $activity.attr('id'),
    		comment_id = $li.attr('id');
    	
    	// what should happen with the selected comment
    	var state = $el.hasClass('activate') ? 'activate' : 'deactivate';
    	
    	// add spinner
    	$el.addClass('disabled').find('i').removeClass().addClass('fa fa-spinner fa-spin');
    	
    	// server request
    	$.ajax({
    		url: this.settings.ajax.remote + '/@@ajax-activities' + this.settings.ajax.callback,
    		data: {
    			action: state + '_comment',
    			comment_id: comment_id,
    			content_uid: activity_id
    		},
    		dataType: 'json',
    		success: $.proxy(function(response) {
				if(response === true) {
					// server answered with `true`, everything was ok, change state
					if(state === 'activate') {
						// comment activation
						$el.removeClass('activate').addClass('deactivate');
						$li.removeClass('not-activated').addClass('activated');
						
						$el.removeClass('disabled').find('i').removeClass().addClass('fa fa-eye-slash');
					} else {
						// comment deactivation
						$el.removeClass('deactivate').addClass('activate');
						$li.removeClass('activated').addClass('not-activated');
						
						$el.removeClass('disabled').find('i').removeClass().addClass('fa fa-eye');
					}
				} else {
					// server answered with `false`, so something went wrong, do not change the state
					$el.removeClass('disabled').find('i').removeClass().addClass('fa fa-eye' + (state === 'activate' ? '' : '-slash'));
				}
    		}, this),
    		error: $.proxy(function(a,b,c) {
    			this.log('Comment De-/Activiation', a,b,c);
    			
    			$el.removeClass('disabled').find('i').removeClass().addClass('fa fa-eye' + (state === 'activate' ? '' : '-slash'));
    		}, this)
    	});
    }, this));
    
    
    
    // Thumbnail preview mouse handler
    //$(wrapper).find('li.activity a.user-message').hoverIntent($.proxy(this.showThumbnailPreview, this), $.proxy(this.hideThumbnailPreview, this));
    /** @events */
    $(wrapper).on({
    	mouseenter: $.proxy(function(e) {
    		this.showThumbnailPreview(e);
    	}, this),
    	mouseleave: $.proxy(function(e) {
    		this.hideThumbnailPreview(e);
    	}, this)
    }, 'li.activity a.user-message');
    
    
    // follow -- only if follow is intalled
    if(this.getCache('followInstalled')) {
        var container = this.getOption('followContainer', 'selector');
    
        /** @events */
        $(container).on('click', 'a', $.proxy(function(e) {
            e.preventDefault();
        
            var $el = $(e.currentTarget);
            
            $(container).find('li').removeClass('active');
            $el.parents('li').addClass('active');
            
            if($el.hasClass('astream-tab-all')) {
                $('li.activity').slideDown(speedDown);
                
                this.setCache('onlyFollowing', false);
            } else {
                $('li.activity.not-following').slideUp(speedUp);
                $('li.activity.following').slideDown(speedDown);
                
                this.setCache('onlyFollowing', true);
                
                if($('li.activity.following').length < 5) {
                    this.getActivities('get_more_activities');
                }
            }
        }, this));
    }
    
    
    // loading on scroll
    /** @events */
    $(window).on('scroll', $.proxy(function(e) {
        var $wrapper = $(this.getOption('wrapper', 'selector')),
            $lastActivity = $wrapper.find(this.getOption('activityList', 'selector')).find('li.activity:last'),
            $getMoreActivities = $wrapper.find(this.getOption('getMore', 'selector'));
            
        if($lastActivity.length > 0 && $getMoreActivities.is(':in-viewport') && $getMoreActivities.is(':visible')) {
            $getMoreActivities.hide();
            
            this.getActivities('get_more_activities');
        } else if($getMoreActivities.is(':in-viewport') && $getMoreActivities.is(':visible') && this.getCache('currentView') === 'userprofile' && this.getCache('initUserprofile') === false) {
            this.setCache('initUserprofile', true);
            
            this.getActivities('get_more_activities', true);
        }
    }, this));
};


/**
 * show thumbnail preview on mouseover (link)
 *
 * @param {Object} e	mouseover event
 */
ActivityStream.prototype.showThumbnailPreview = function(e) {
    var $el = $(e.currentTarget);
    
    var $thumbnailPreview = $el.parents('.well').find('.thumbnail-preview'),
        $thumbnail = $thumbnailPreview.find('img.lazy');
        
    if($thumbnail.attr('src') === undefined || $thumbnail.attr('src') !== $thumbnail.data('original')) {
        $thumbnail.attr('src', $thumbnail.data('original'));
    }
    
    $thumbnailPreview.fadeIn(10);
};


/**
 * hide thumbnail preview on mouseleave link or mouseleave thumbnailpreview
 *
 * @param {Object} e	mouseout event
 */
ActivityStream.prototype.hideThumbnailPreview = function(e) {
    var $el = $(e.currentTarget);
    
    var $thumbnailPreview = $el.parents('.well').find('.thumbnail-preview'),
        $thumbnail = $thumbnailPreview.find('img.lazy');

    setTimeout(function() {
        if(!$thumbnailPreview.is(':hover')) {
            $thumbnailPreview.fadeOut(100);
            
            return ;
        }
    
        $thumbnailPreview.mouseleave(function() {
            $thumbnailPreview.fadeOut(100);
        });
    }, 100);
};



/**
 * helper function to sort activities by timestamp
 * 
 * @param   {Object} data		object filled with activities
 * @param   {String} direction	asc|desc
 * @returns {Object}
 */
ActivityStream.prototype.sort = function(data, direction) {
    var tmp = data.sort(function(a, b) {
        a = (new Date(a['timestamp'])).getTime();
        b = (new Date(b['timestamp'])).getTime();
    
        return a-b;
    });
    
    if('desc' === direction) {
        tmp.reverse();
    }
    
    return tmp;
};