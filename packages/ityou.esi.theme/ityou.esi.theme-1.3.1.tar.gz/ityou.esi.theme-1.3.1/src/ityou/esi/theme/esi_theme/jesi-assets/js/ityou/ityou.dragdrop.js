/**
 * Support easy drag and drop to copy or move files, and for sorting items in thumbnail-view
 * 
 * @module DragDrop
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:DragDrop
 * 
 * @param {Object} ajaxSettings		ajax settings for remote host and callback param
 * @param {Object} ThumbnailView	instance of module:ThumbnailView
 */
function DragDrop(ajaxSettings, ThumbnailView) {
	/** @uses module:ThumbnailView */
	this.thumbnailView = ThumbnailView;
	// ajax settnigs
	this.ajax = $.extend({}, ajaxSettings);
	
	// draggable options for moving items in thumbnail-view (e.g. sorting)
	this.draggableOptions = {
		// helper function
        helper: $.proxy(function(event) {
            var el = $(event.currentTarget),
                currentView;
            
            // define which view is currently activated
            var $currentView = $('#thumbnail-view').find('.thumbnail-listing-size').find('a.state-active');
            
            // implemented views are:
            //	* default-view
            //	* thumbnail-list-view
            //	* thumbnail-1-column-view
            //	* thmubnail-2-columns-view
            //	* thumbnail-3-columns-view
            if($currentView.length === 0) {
                currentView = 'col-xs-6 col-md-4 col-lg-3'; // default-view
            } else {
                if($currentView.attr('id') === 'thumbail-list-view') {
                    currentView = 'list-group'; // thumbnail-list-view
                } else if($currentView.attr('id') === 'thumbnail-1-column-view') {
                    currentView = 'col-xs-12'; // thumbnail-1-column-view
                } else if($currentView.attr('id') === 'thumbnail-2-columns-view') {
                    currentView = 'col-xs-6'; // thumbnail-2-columns-view
                } else if($currentView.attr('id') === 'thumbnail-3-columns-view') {
                    currentView = 'col-xs-4'; // thumbnail-3-columns-view
                } else {
                    currentView = 'col-xs-6 col-md-4 col-lg-3'; // default-view
                }
            }
            
            // each dragged element needs additional data stored
            var data = {
                uid: el.attr('id'),
                portal_type: el.attr('data-portal-type'),
                ahref: el.attr('data-url'),
                imgsrc: el.find('img:not(.loading)').attr('src'),
                icon: el.attr('data-contenticon'),
                title: el.find('.item-title').text(),
                elHeight: this.getMaxHeight($('#thumbnail-view').find('.folder-item'))-20,
                //elHeight: parseInt($('#thumbnail-view').find('div.folder-item').first().find('.thumbnail').css('height')) + 10,
                elWidth: parseInt($('#thumbnail-view').find('div.folder-item').first().css('width')),
                currentView: currentView
            };
            
            // distinguish `folder items` and `file items`
            if(data.portal_type == 'Folder') {
                return $($('#dragdrop-draggableFolder-tmpl').render(data));
            } else {
                return $($('#dragdrop-draggableFile-tmpl').render(data));
            }
        }, this),
        containtment: 'body',
        appendTo: 'body',
        cursor: 'move',
        connectToSortable: '#thumbnail-view form[name="folderContentsForm"]',
        start: function(event, ui) {
            $('#thumbnail-view').find('.folder-item:hidden').fadeIn(600);
        },
        cancel: '.copy-move-item, .delete-item',
    };
	
	// dragging tolerance is build in for people without mouse (e.g. using pen or something similiar)
	this.draggingTolerance = 10;
	
    this.floatFix = 2;
    
    this.sortableSelector = $('#thumbnail-view form[name="folderContentsForm"]');
    this.dragDropContainer = 'dl.portlet-static-drag-drop dd.portletItem p#dragdrop-container div.drag-drop-container';
    
    /**
     * helper function to execute `Twitter Bootstrap` columns out of given `css classes`
     * 
     * @param   {Object} self
     * @returns {String}
     */
    this.getTwbsCol = function(self) {
	    toReturn = '';
	    // select `css class` and split it at whitespaces
	    classes = self.className.split(' ');
	    // loop over `classnames`
	    for(i in classes) {
	    	// if the `classname` has `col-` in it, we think it's a `Twitter Bootstrap`
	    	// column, and so we add it to the string we will return
	        if(/col-/i.exec(classes[i])) {
	            toReturn += classes[i] + ' ';
	        }
	    }
	    
	    return toReturn;
    };
	
    
    /**
     * check the permissions in the current folder
     * if the user has no right to copy something in the folder, we need to
     * hide the drag&drop portlet, because he has only `view` rights
     * 
     * @uses `@@ajax-dragdrop-permissions?action=can_copy` CONTEXTBASED, no remote host may be added!
     */
	this.checkPermission = function() {
		var permission = false,
			copyPermission = false;
		
		// define if an request is still running
		var running1 = true;
		// start ajax request
		/** @uses `@@ajax-dragdrop-permission?action=can_copy` CONTEXTBASED, no remote host may be added! */
		$.getJSON('@@ajax-dragdrop-permissions', {action: 'can_copy'}, $.proxy(function(response) {
			copyPermission = copyPermission || response;
			permission = permission || response;
			
			// request is finished
			running1 = false;
		}, this));
		
		// wait for running requests
		var timing = setInterval($.proxy(function() {
			if(!running1) {
				clearInterval(timing);
				
				// debugging
				//console.log("general: " + permission, ", copy: " + copyPermission);
				
				// check permission
				if(!permission) {
					// no permission -> remove drag&drop portlet from DOM
					$('dl.portlet-static-drag-drop').remove();
				} else {
					// permissions are ok, initialize drag&drop
					this.initDragDrop(copyPermission);
				}
			}
		}, this), 50);
	};
	
	
	/**
	 * Initializes the Drag&Drop module
	 * 
	 * @constructs
	 * @uses `@@ajax-dragdrop?action=get_dragdrop_objects`
	 * @uses `ityou.dragdrop/ityou/dragdrop/portlets/dragdrop.pt:61` @ L184
	 * 
	 * @param {Boolean} canCopy	permissions on `copy` in the current folder
	 */
	this.initDragDrop = function(canCopy) {
		// check if drag&drop portlet is installed
		if($('dl.portlet-static-drag-drop').length > 0) {
			if(!canCopy) {
				$('dl.portlet-static-drag-drop').find('div.copy-move-container').find('.action-bar.copy').prop('disabled', true);
			}
			
			// ajax request for getting objects the user dragged into the portlet
	        $.getJSON(this.ajax.remote + '/@@ajax-dragdrop', {action: 'get_dragdrop_objects'}, $.proxy(function(response) {
	            if(response.length > 0) {
	                $('dl.portlet-static-drag-drop').find('#dragdrop-portlet-text').hide();
	            
	                $.each(response, function(i, val) {
                        val.thumbnail_class = (val.portal_type == 'Folder' ? '' : 'linked-document link-overlay');
	                        
                        // rendering
                        /** @uses `ityou.dragdrop/ityou/dragdrop/portlets/dragdrop.pt:61` */
                        $($('#dragdrop-dragdropcontainer-tmpl').render(val)).appendTo('dl.portlet-static-drag-drop p#dragdrop-container');
	                });
	                
	                // check permissions on each file
	                this.checkFilePermission();
                }
	        }, this));
        }
	};
	
	
	/**
	 * check permissions for each file in the drag&drop portlet
	 */
	this.checkFilePermission = function() {
		// loop through each item
		$('div.drag-drop-container').each($.proxy(function(k, el) {
        	var ddEl = $(el),
        		// copy or move button selected?
                state = $('dl.portlet-static-drag-drop').find('div.copy-move-container').find('.action-bar.move').hasClass('state-active') ? 'can_move' : 'can_copy';
        	
        	this.checkState(ddEl, state);
        }, this));
	};
	
	
	/**
	 * initialize the droppable area in the portlet
	 */
	this.initDropable = function() {
		$('dl.portlet-static-drag-drop #dragdrop-container').droppable({
            //greedy: true,
            accept: '#thumbnail-view div.folder-item',
            activeClass: 'state-active',
            hoverClass: 'state-hover',
            tolerance: 'pointer',
            drop: $.proxy(function(event, ui) {
            	// what to do if the user drops an element on the portlet
                this.droppableDrop(ui.draggable, $('dl.portlet-static-drag-drop #dragdrop-container'));
            }, this)
        });
	};
	
	
	/**
	 * initialize the thumbnail-view as a sortable list
	 * 
	 * @uses `@@ajax-dragdrop?action=copy_object|move_object`
	 * @uses `@@ajax-sorting` CONTEXTBASED, no remote host may be added!
	 * @uses `ityou.dragdrop/ityou/dragdrop/portlets/dragdrop.pt:120` @ L405
	 * @uses `ityou.dragdrop/ityou/dragdrop/portlets/dragdrop.pt:167` @ L408
	 */
	this.initSortable = function() {
		this.sortableSelector.sortable({
            appendTo: 'body',
            cursor: 'move',
            helper: 'clone',
            items: '.folder-item',
            placeholder: 'sorting placeholder',
            containment: 'parent',
            // start function
            start: $.proxy(function(event, ui) {
            	// show all items in the thumbnail list when start sorting
                $('#thumbnail-view').find('.folder-item:hidden').fadeIn(600);
                // hide the selected element, there will be a placeholder visible
                ui.item.hide();
                
                var tmpEl = $('#thumbnail-view').find('.folder-item').first();
                
                if(tmpEl.attr('id') === ui.item.attr('id')) {
                    tmpEl = $('#thumbnail-view').find('.folder-item:eq(1)');
                    
                    if(tmpEl.length === 0) {
                        tmpEl = $('#thumbnail-view').find('.more-item');
                    }
                }
                
                var tmpCol = this.getColumns(tmpEl[0]);
                    
                if(tmpEl.hasClass('list-group')) {
                    tmpCol += ' list-group';
                }
                
                $('#thumbnail-view .sorting.placeholder').addClass(tmpCol).html('<div class="thumbnail"/>');
                
                if($(ui.item).hasClass('drag-drop-container')) {
                    var h = this.getMaxHeight($('#thumbnail-view').find('.folder-item, .more-item'));
                
                    $('#thumbnail-view .sorting.placeholder .thumbnail').height((h - 20));
                    ui.helper.height((h - 20));
                } else {
                    $('#thumbnail-view .sorting.placeholder .thumbnail').height((ui.item.height() - 20));
                    ui.helper.height((ui.item.height() - 20));
                }
                
                setTimeout(function() {
                    $('.folder-item.ui-sortable-helper').find('.additional-information').hide();
                }, 1);
                
                this.sortableSelector.sortable('option', 'cursor', 'move');
            }, this),
            // stop function
            stop: $.proxy(function(event, ui) {
            	// if user has no mouse (e.g. using a pen or something similiar), we need
            	// to give him a tolerance area when clicking on links
                var distanceTop = (ui.position.top-ui.originalPosition.top) < 0 ? (ui.position.top-ui.originalPosition.top)*(-1) : (ui.position.top-ui.originalPosition.top),
                    distanceLeft = (ui.position.left-ui.originalPosition.left) < 0 ? (ui.position.left-ui.originalPosition.left)*(-1) : (ui.position.left-ui.originalPosition.left);
                
                if(ui.position == undefined || (distanceTop < this.draggingTolerance && distanceLeft < this.draggingTolerance)) {
                    var isFolder = $.inArray('Folder', event.originalEvent.target.classList) > -1 ? true : false;
                    
                    if(event.originalEvent.target.nodeName == 'IMG') {
                        if(isFolder) {
                            location.href = ui.item.find('a').attr('href');
                        } else {
                            ui.item.find('a.link-overlay').trigger('click');
                        }
                    } else {
                        if(ui.item.find('a.document-download').length > 0) {
                            location.href = ui.item.find('a.document-download').attr('href');
                        } else {
                            location.href = ui.item.find('a').attr('href');
                        }
                    }
                }
            }, this),
            // update function
            /** @uses `@@ajax-dragdrop?action=copy_object|move_object` CONTEXTBASED, no remote host may be added! */
            /** @uses `@@ajax-sorting` CONTEXTBASED, no remote host may be added! */
            update: $.proxy(function(event, ui) {
                var uids = [],
                    selector = this.sortableSelector;
            
                if(ui.item.hasClass('drag-drop-container')) {
                	//
                	// sorting an item from the drag&drop portlet into the thumbnail-view
                	//
                    var uid = ui.item.attr('data-uid');
                    
                    var h = this.getMaxHeight($('#thumbnail-view').find('.folder-item, .more-item'))-20;
                        
                    var data = {
                        id: null, //ui.item.attr('data-id'),
                        uid: null, //uid,
                        portal_type: ui.item.attr('data-portal-type'),
                        contenttype: ('contenttype-'+ui.item.attr('data-portal-type').toLowerCase()),
                        contenticon: ui.item.attr('data-contenticon'),
                        url: null, //ui.item.attr('data-url'),
                        imgsrc: ui.item.find('img:not(.loading)').attr('src'),
                        title: ui.item.find('.item-title').text(),
                        author: ui.item.attr('data-addinfo-author'),
                        created: ui.item.attr('data-addinfo-date-created'),
                        edited: ui.item.attr('data-addinfo-date-edited'),
                        description: ui.item.attr('data-addinfo-description'),
                        aclass: ui.item.attr('data-portal-type') == 'Folder' ? '' : 'linked-document link-overlay',
                        relpb: ($('#thumbnail-view').find('div.folder-item').length+100),
                        elHeight: h
                    };
                    
                    // define copy or move an item
                    var state = $('dl.portlet-static-drag-drop dd.portletItem div.copy-move-container .action-bar.copy').hasClass('state-active') ? 'copy_object' : 'move_object';

                    $('#dragdrop-container').find('div[data-uid="'+data.uid+'"]').find('.copy-move-item').hide();
                    $('#dragdrop-container').find('div[data-uid="'+data.uid+'"]').find('.delete-item').hide();
                    $('#dragdrop-container').find('div[data-uid="'+data.uid+'"]').find('.loader').show();
                    
                    var $next = $(ui.item).next('.folder-item'),
                        $prev = $(ui.item).prev('.folder-item'),
                        $more = $('#thumbnail-view').find('.more-item');
                        
                    var tmpEl = $next.length > 0 ? $next : ($prev.length > 0 ? $prev : $more),
                        tmpCol = this.getColumns(tmpEl[0]);
                    
                    ui.item.empty().removeClass().addClass('folder-item').addClass(tmpCol);
                    var placeholderLoading = $('#dragdrop-droppablePlaceholder-tmpl').render();
                    $(placeholderLoading)
                        .height(h)
                        .appendTo(ui.item);
                
                    // ajax request
                    /** @uses `@@ajax-dragdrop?action=copy_object|move_object` CONTEXTBASED, no remote host may be added! */
                    $.getJSON('@@ajax-dragdrop', {action: state, uid: uid}, $.proxy(function(response) {
                        var uids = [];
                        if(this.castBool(response) == true) {
                            if(state == 'move_object') {
                                $('#thumbnail-view').find('.folder-item#'+uid).remove();
                            }
                            
                            ui.item
                                .empty()
                                .removeClass()
                                .addClass('folder-item '+data.portal_type+' '+data.id)
                                .attr('id', uid)
                                .removeData()
                                .removeAttr('data-portal-type')
                                .removeAttr('data-url')
                                .removeAttr('data-id')
                                .removeAttr('data-uid')
                                .removeAttr('data-addinfo-author')
                                .removeAttr('data-addinfo-created')
                                .removeAttr('data-addinfo-edited')
                                .removeAttr('data-addinfo-description')
                                .removeAttr('data-thumbnail-class')
                                .removeAttr('data-contenticon')
                                .css('display', 'block');
                                
                            var $next = $(ui.item).next('.folder-item'),
                                $prev = $(ui.item).prev('.folder-item'),
                                $more = $('#thumbnail-view').find('.more-item');
                                
                            var tmpEl = $next.length > 0 ? $next : ($prev.length > 0 ? $prev : $more),
                                tmpCol = this.getColumns(tmpEl[0]);
                                
                            ui.item.addClass(tmpCol);
                            
                            var newName = response.url.split("/");
                            
                            // adding new url to data object
                            data.url = response.url;
                            data.id = newName[newName.length-1];
                            data.uid = response.uid;
                            
                            console.log(data);
                        
                            // rendering
                            if(data.portal_type == 'Folder') {
                            	/** @uses `ityou.dragdrop/ityou/dragdrop/portlets/dragdrop.pt:120` */
                                $($('#dragdrop-droppableFolder-tmpl').render(data)).appendTo(ui.item);
                            } else {
                            	/** @uses `ityou.dragdrop/ityou/dragdrop/portlets/dragdrop.pt:167` */
                                $($('#dragdrop-droppableItem-tmpl').render(data)).appendTo(ui.item);
                            }
       
                            // remove item from drag&drop portlet
                            $('p#dragdrop-container').find('#'+uid).find('span.delete-item').trigger('click');
                            ui.item.attr('id', response);

                            // refresh sortables
                            selector.sortable('refresh');
                            selector.sortable('option', 'containment', 'parent');
                            
                            // collecting uids for saving new order
                            $('.folder-item').each(function() {
                                uids.push($(this).attr('id'));
                            });
                            /** @uses `@@ajax-sorting` CONTEXTBASED, no remote host may be added! */
                            $.getJSON('@@ajax-sorting', {'order': uids.join()});
                            
                            // event handler
                            this.thumbnailView.prepOverlay();
                            this.thumbnailView.hoverIntent();
                        } else {
                        	// inserting failed, remove the inserted item from DOM
                            ui.item.fadeOut(200, function() {
                                ui.item.remove();
                            });
                        }
                    }, this));
                } else {
                	//
                	// sorting items, or pushing an item from thumbnail-view to drag&drop portlet
                	//
                    var dragdrop = $('dl.portlet-static-drag-drop'),
                        portletWrapperLeft = $('#portal-column-one').find('.portletWrapper').length > 0 ? true : false,
                        portletWrapperRight = $('#portal-column-two').find('.portletWrapper').length > 0 ? true : false,
                        portletLeft = $('#portal-column-one').find('.portletWrapper').first(),
                        portletRight = $('#portal-column-two').find('.portletWrapper').first(),
                        footer = $('#portal-footer');
                        
                    // if the item is outside the thumbnail-view and not over the droppable area
                    // of the drag&drop portlet, dont save the new order
                    if((portletWrapperRight && (ui.position.left+ui.item.width()) > portletRight.offset().left) || (portletWrapperLeft && (ui.position.left-ui.item.width()) < portletLeft.offset().left) || (ui.position.top+ui.item.height()) < this.sortableSelector.offset().top || (footer.length > 0 && (ui.position.top) > footer.offset().top)) {
                        this.sortableSelector.sortable('cancel');
                    } else {
                    	// collecting uids for saving new order
                    	$('.folder-item').each(function() {
                    		uids.push($(this).attr('id'));
                    	});
                    	/** @uses `@@ajax-sorting` CONTEXTBASED, no remote host may be added! */
                    	$.getJSON('@@ajax-sorting', {'order': uids.join()});
                	}
            	}
            }, this)
        });
	};
	
	
	/**
	 * initialize the trashcan inside the drag&drop portlet
	 * 
	 * @uses `@@ajax-dragdrop-permissions?action=can_delete` CONTEXTBASED, no remote host may be added!
	 * @uses `@@ajax-dragdrop?action=move_to_trash` CONTEXTBASED, no remote host may be added!
	 * @uses `@@ajax-sorting` CONTEXTBASED, no remote host may be added!
	 */
	this.initTrash = function() {
		// ajax request
		/** @uses `@@ajax-dragdrop-permissions?action=can_delete` CONTEXTBASED, no remote host may be added! */
		$.getJSON('@@ajax-dragdrop-permissions', {action:'can_delete'}, $.proxy(function(response) {
			// if user has the permission to delete items in this folder,
			// initialize the droppable area inside the portlet at the trash icon
			if(this.castBool(response) == true) {
                $('#delete-container').droppable({
                    //greedy: true,
                    accept: '#thumbnail-view div.folder-item',
                    hoverClass: 'state-hover',
                    tolerance: 'pointer',
                    // drop function
                    /** @uses `@@ajax-dragdrop?action=move_to_trash` */
                    /** @uses `@@ajax-sorting` CONTEXTBASED, no remote host may be added! */
                    drop: $.proxy(function(event, ui) {
                        var uid = ui.draggable.attr('id'),
                            uids = [];
                        
                        ui.draggable.remove().html('').remove();
                        
                        // ajax request
                        /** @uses `@@ajax-dragdrop?action=move_to_trash` */
                        $.getJSON('@@ajax-dragdrop', {action:'move_to_trash', uid:uid}, $.proxy(function(response) {
                            if(this.castBool(response) == true) {
                                setTimeout(function() {
                                    $('.folder-item#'+uid).html('');
                                    $('#'+uid+'.folder-item').remove();
                                    
                                    $('.folder-item').each(function() {
                                        uids.push($(this).attr('id'));
                                    });
                                    /** @uses `@@ajax-sorting` CONTEXTBASED, no remote host may be added! */
                                    $.getJSON('@@ajax-sorting', {'order': uids.join()});
                                }, 1);
                            }
                        }, this));
                    }, this)
                });
            } else {
            	// user has no permission to delete items in this folder,
            	// do not initialize droppable area and change visibility
            	// of the trash icon
                $('#delete-container i').css({color: '#000', opacity: '0.2'});
            }
        }, this));
	};
	
	// disable text selection
	$('#thumbnail-view, dl.portlet-static-drag-drop').disableSelection();
	
	// init mouse and keyboard events
	this.mouseEventHandler();
	this.keyboardEventHandler();
};


/**
 * helper function to execute columns out of given `css classes`
 * 
 * @param   {Object} el
 * @returns {String}
 */
DragDrop.prototype.getColumns = function(el) {
    var tmp = new Array(),
        classNames = el.className.split(' ');
    
    for(i in classNames) {
        if(/col-/i.exec(classNames[i])) {
            tmp.push(classNames[i]);
        }
    }
    
    return tmp.join(' ');
};


/**
 * all items need to have the same height for a clean grid, so sometimes we need to
 * extract the maxheight of the items
 * 
 * @param   {Object} element
 * @returns {Number}
 */
DragDrop.prototype.getMaxHeight = function(element) {
    return Math.max.apply(null, element.map(function() {
        return $(this).height();
    }).get());
};


/**
 * check if user can copy/move an item in the drag&drop portlet
 * if he can not copy/move an item, the item gets a red border and a red cross
 * at its left top
 * 
 * @uses `@@ajax-dragdrop-permissions?action=can_copy|can_move`
 * 
 * @param {Object} obj		pointer to the item in the drag&drop portlet
 * @param {String} state	can_copy|can_move
 */
DragDrop.prototype.checkState = function(obj, state) {
	// ajax request
	/** @uses `@@ajax-dragdrop-permission?action=can_copy|can_move` */
	$.getJSON('@@ajax-dragdrop-permissions', {action: state, uid: obj.attr('id')}, $.proxy(function(response) {
		var actionBar = obj.find('.action-bar');
		
		// check the permissions on the item
        if(this.castBool(response) == true) {
        	// user has permissions to copy/move
        	// initialize draggable on this item
        	obj.draggable(this.draggableOptions);
            
            // enable selection, copy/move button and change btn
            actionBar.find('.copy-move-item').addClass('fa-arrow-left').removeClass('fa-times').prop('disabled', false);
            actionBar.find('input[type="checkbox"]').prop('disabled', false);
            
            // change border style
            obj.removeClass('can-not-move-or-copy');
        } else {
        	// user has no permissions to copy/move
        	// destroy draggable on this item (only if exists)
        	if(obj.data('uiDraggable')) {
        		obj.draggable('destroy');
        	}
        	
        	// disable selection, copy/move button and change btn
        	actionBar.find('.copy-move-item').removeClass('fa-arrow-left').addClass('fa-times').prop('disabled', true);
        	actionBar.find('input[type="checkbox"]').prop('checked', false).prop('disabled', true);
        	
        	// change border style
            obj.addClass('can-not-move-or-copy');
        }
    }, this));
};


/**
 * helper function to cast strings to boolean etc.
 * 
 * @param   {Object|Array|String|Number|Boolean}
 * @returns {Boolean}
 */
DragDrop.prototype.castBool = function(val) {
    if(typeof val == 'string' && val.toLowerCase() == 'true' || typeof val == 'boolean' && val == true) {
        return true;
    } else if(typeof val == 'string' && val.toLowerCase() == 'false' || typeof val == 'boolean' && val == false) {
        return false;
    } else {
        return true;
    }
};


/**
 * delete an item from thumbnail-view
 * 
 * @uses `@@ajax-dragdrop?action=move_to_trash` CONTEXTBASED, no remote host may be added!
 * @uses `@@ajax-sorting` CONTEXTBASED, no remote host may be added!
 * 
 * @param {Object} obj
 * @param {String} uid
 */
DragDrop.prototype.moveToTrash = function(obj, uid) {
    var uids = [];
    
    // ajax request
    /** @uses `@@ajax-dragdrop?action=move_to_trash` CONTEXTBASED, no remote host may be added! */
    $.getJSON('@@ajax-dragdrop', {action:'move_to_trash', uid:uid}, $.proxy(function(response) {
        if(this.castBool(response) == true) {
            obj.effect('fade', 200, function() {
                setTimeout(function() {
                    obj.remove();
            
                    // collecting uids for new order
                    $('.folder-item').each(function() {
                        uids.push($(this).attr('id'));
                    });
                    
                    // saving new order
                    /** @uses `@@ajax-sorting` CONTEXTBASED, no remote host may be added! */
                    $.getJSON('@@ajax-sorting', {'order': uids.join()});
                }, 1);
            });
        }
    }, this));
};


/**
 * drop an item into the drag&drop portlet
 * 
 * @uses `@@ajax-dragdrop?action=add_dragdrop_object`
 * @uses `@@ajax-dragdrop-permissions?action=can_copy|can_move` CONTEXTBASED, no remote host may be added!
 * @uses `ityou.dragdrop/ityou/dragdrop/portlets/dragdrop.pt:61` @ L699
 */
DragDrop.prototype.droppableDrop = function(ui, obj) {
    var uid = ui.attr('id'),
    	uids = [];

    // collect present items to avoid duplicates
	$('body').find('dd.portletItem p#dragdrop-container').find('div.drag-drop-container').each(function() {
	    uids.push($(this).attr('id'));
	});
	
	// if the item is alreay present in drag&drop portlet we dont wanna add it again
	if($.inArray(uid, uids) == -1 || uids.length == 0) {
		// ajax request
		/** @uses `@@ajax-dragdrop?action=add_dragdrop_object` */
	    $.getJSON(this.ajax.remote + '/@@ajax-dragdrop', {action: 'add_dragdrop_object', uid: uid}, $.proxy(function(response) {
	        if(this.castBool(response) == true) {
	            $('dl.portlet-static-drag-drop').find('#dragdrop-portlet-text').hide();
	            
	            var data = {
	                uid: uid,
	                portal_type: ui.attr('class').replace(/folder-item /, '').split(' ')[0],
	                id: ui.attr('class').replace(/folder-item /,'').split(' ')[1],
	                url: ui.find('a').attr('href'),
	                icon: ui.find('.item-title').find('img').attr('src'),
	                author: ui.find('.additional-information').find('.author').text(),
	                created: ui.find('.additional-information').find('.date_created').text(),
	                edited: ui.find('.additional-information').find('.date_edited').text(),
	                description: ui.find('.additional-information').find('.item-description').text(),
	                thumbnail_url: ui.find('img.img-responsive').attr('src'),
	                thumbnail_class: ui.find('img').attr('class'),
	                title: ui.find('div.item-title').first().text()
	            };
	            
	            /** @uses `ityou.dragdrop/ityou/dragdrop/portlets/dragdrop.pt:61` */
	            $($('#dragdrop-dragdropcontainer-tmpl').render(data)).appendTo('dl.portlet-static-drag-drop p#dragdrop-container');
	            
	            $('dl.portlet-static-drag-drop').find('dd.portletItem p#dragdrop-container').find('div.drag-drop-container#'+uid).each($.proxy(function(k, el) {
	                if(!$(el).hasClass('ui-draggable')) {
	                    var ddEl = $(el);
	                    
	                    // check permissions on the new inserted item
	                    if($('div.copy-move-container').find('.state-active').hasClass('copy')) {
	                    	// ajax request
	                    	/** @uses `@@ajax-dragdrop-permission?action=can_copy` CONTEXTBASED, no remote host may be added! */
	                        $.getJSON('@@ajax-dragdrop-permissions', {action: 'can_copy'}, $.proxy(function(response) {
	                            if(this.castBool(response) == true) {
	                                ddEl.draggable(this.draggableOptions);
	                            } else {
	                                ddEl.addClass('can-not-move-or-copy');
	                            }
	                        }, this));
	                    } else {
	                    	// ajax request
	                    	/** @uses `@@ajax-dragdrop-permission?action=can_move` CONTEXTBASED, no remote host may be added! */
	                        $.getJSON('@@ajax-dragdrop-permissions', {action: 'can_move', uid: uid}, $.proxy(function(response) {
	                            if(this.castBool(response) == true) {
	                                ddEl.draggable(this.draggableOptions);
	                            } else {
	                                ddEl.addClass('can-not-move-or-copy');
	                            }
	                        }, this));
	                    }
	                }
	            }, this));
	        } else {
	            if($('dl.portlet-static-drag-drop').find('dd.portletItem p#dragdrop-container').find('div.drag-drop-container').length == 0) {
	                $('dl.portlet-static-drag-drop').find('dd.portletItem #dragdrop-portlet-text').show();
	            }
	        }
	    }, this));
	}
};


/**
 * remove an item from the drag&drop portlet
 * 
 * @uses `@@ajax-dragdrop?action=remove_dragdrop_object`
 * 
 * @param {Object} obj
 */
DragDrop.prototype.removeFromDragDrop = function(obj) {
	// ajax request
	/** @uses `@@ajax-dragdrop?action=remove_dragdrop_object` */
    $.getJSON(this.ajax.remote + '/@@ajax-dragdrop', {action: 'remove_dragdrop_object', uid: obj.attr('id')});
        
    // hide object with animation
    obj.effect('fade', 500, function() {
    	// after animation ended, remove it from DOM
        obj.remove();
        
        if($('dl.portlet-static-drag-drop').find('dd.portletItem p#dragdrop-container').find('div.drag-drop-container').length == 0) {
            $('dl.portlet-static-drag-drop').find('#dragdrop-portlet-text').show();
        }
    });
};


/**
 * insert an item into the thumbnail-view
 * 
 * @uses `@@ajax-dragdrop?action=copy_object|move_object` CONTEXTBASED, no remote host may be added!
 * @uses `@@ajax-sorting` CONTEXTBASED, no remote host may be added!
 * @uses `ityou.dragdrop/ityou/dragrop/portlets/dragdrop.pt:222` @ L835
 * @uses `ityou.dragdrop/ityou/dragrop/portlets/dragdrop.pt:258` @ L838
 * 
 * @param {Object} obj
 * @param {String} obj_state	copy_object|move_object
 */
DragDrop.prototype.insertToThumbnailView = function(obj, obj_state) {
	var uid = obj.attr('data-uid'),
		// state: copy_object|move_object
        state = obj_state == undefined ? ($('dl.portlet-static-drag-drop dd.portletItem div.copy-move-container div.action-bar.copy').hasClass('state-active') ? 'copy_object' : 'move_object') : obj_state + '_object';

    obj.find('.action-bar').find('.copy-move-item').hide();
    obj.find('.action-bar').find('.delete-item').hide();
    obj.find('.action-bar').find('.loader').show();
    
    //ajax request
    /** @uses `@@ajax-dragdrop?action=copy_object|move_object` CONTEXTBASED, no remote host may be added! */
    $.getJSON('@@ajax-dragdrop', {action: state, uid: uid}, $.proxy(function(response) {
        var uids = [];
        
        if(!!response) {
        	var newName = response.url.split("/");
        	
            var data = {
                uid: response.uid,
                id: newName[newName.length-1],
                portal_type: obj.attr('data-portal-type'),
                contenttype: ('contenttype-'+obj.attr('data-portal-type').toLowerCase()),
                contenticon: obj.attr('data-contenticon'),
                url: response.url,
                imgsrc: obj.find('img:not(.loading)').attr('src'),
                title: obj.find('.item-title').text(),
                author: obj.attr('data-addinfo-author'),
                created: obj.attr('data-addinfo-date-created'),
                edited: obj.attr('data-addinfo-date-edited'),
                description: obj.attr('data-addinfo-description'),
                aclass: obj.attr('data-portal-type') == 'Folder' ? '' : 'linked-document link-overlay',
                relpb: ($('#thumbnail-view').find('div.folder-item').length+100),
            };
            
            $('#thumbnail-view form[name="folderContentsForm"]')
                .find('.folder-item')
                .each(function() {
                    $(this).show();
                });
                
            if($('#thumbnail-view form').children().length > 1) {
                $('#thumbnail-view').find('.more-item').hide();
            } else {
                $('#thumbnail-view').find('.more-item').show();
            }

            $('html, body').animate({
                scrollTop: $($('#thumbnail-view').find('.folder-item').last()[0] || $('#thumbnail-view').find('.more-item')[0]).offset().top
            }, 800);
            
            
            var $more = $('#thumbnail-view').find('.more-item');
                
            var tmpCol = this.getColumns($more[0]);
            
            if($more.hasClass('list-group')) {
                tmpCol += ' list-group';
            }
            
            if(data.portal_type == 'Folder') {
            	/** @uses `ityou.dragdrop/ityou/dragrop/portlets/dragdrop.pt:222` */
                $($('#dragdrop-droppableFolder-wrapper-tmpl').render(data)).addClass(tmpCol).insertBefore('#thumbnail-view .more-item');
            } else {
            	/** @uses `ityou.dragdrop/ityou/dragdrop/portlets/dragdrop.pt:258` */
                $($('#dragdrop-droppableItem-wrapper-tmpl').render(data)).addClass(tmpCol).insertBefore('#thumbnail-view .more-item');
            }
                    
            // collect uids for new order
            $('.folder-item').each(function() {
                uids.push($(this).attr('id'));
            });
            /** @uses `@@ajax-sorting` CONTEXTBASED, no remote host may be added! */
            $.getJSON('@@ajax-sorting', {'order': uids.join()});
            
            // remove element from drag&drop portlet
            $('p#dragdrop-container').find('#'+uid).find('span.delete-item').trigger('click');
            
            // init event handling
            this.thumbnailView.prepOverlay();
            this.thumbnailView.hoverIntent();
        }
        
        var els = $('#thumbnail-view').find('.folder-item, .more-item');
        
        // acquire same height
        els.equalHeights();
    }, this));
};


/**
 * initialize mouse event handler
 */
DragDrop.prototype.mouseEventHandler = function() {
	/** @events	remove an item from drag&drop portlet */
	$(document).on('click', this.dragDropContainer + ' span.delete-item', $.proxy(function(e) {
		this.removeFromDragDrop($(e.target).parents('.drag-drop-container'));
	}, this));
	
	/** @events	copy or move an item from drag&drop portlet into thumbnail view (also multiple items possible) */
	$(document).on('click', this.dragDropContainer + ' .copy-move-item', $.proxy(function(e) {
		$target = $(e.target);
		
		// check if there are multiple items selected
		if($target.parents('.drag-drop-container').find('input[type="checkbox"]').prop('checked')) {
			// multiple items are selected
			$('dl.portlet-static-drag-drop').find('.drag-drop-container').find('input[type="checkbox"]:checked').each($.proxy(function(k, el) {
				var state = 'move';

				if($('.copy-move-container').find('button.state-active').hasClass('copy')) {
					state = 'copy'
				}
				
				// copy/move items to thumbnail-view
				this.insertToThumbnailView($(el).parents('.drag-drop-container'), state);
			}, this));
		} else {
			// only one item is selected
			var state = 'move';
			
			if($('.copy-move-container').find('button.state-active').hasClass('copy')) {
				state = 'copy';
			}
			
			// copy/move items to thumbnail-view
			this.insertToThumbnailView($target.parents('.drag-drop-container'), state);
		}
	}, this));
	
	/** @events	toogle hover state on drag&drop container */
	$(document).on('hover', this.dragDropContainer, function(e) {
		$(this).toggleClass('state-hover');
	});
	
	/** @events	toggle active/hover state on copy/move buttons */
	$(document).on({
		/** @events click */
		click: $.proxy(function(e) {
			var $btn = $(e.target);
			
			if(!$btn.prop('disabled')) {
				if($btn.hasClass('copy')) {
					if(!$btn.hasClass('state-active')) {
						$btn.addClass('state-active').removeClass('state-hover');
						$btn.next().removeClass('state-active');
					}
				} else if($btn.hasClass('move')) {
					if(!$btn.hasClass('state-active')) {
						$btn.addClass('state-active').removeClass('state-hover');
						$btn.prev().removeClass('state-active');
					}
				}
				
				this.checkFilePermission();
			}
		}, this),
		/** @events hover */
		hover: $.proxy(function(e) {
			var $btn = $(e.target);
			
			if(!$btn.prop('disabled') && !$btn.hasClass('state-active')) {
				$btn.toggleClass('state-hover');
			}
		}, this)
	}, 'dl.portlet-static-drag-drop dd.portletItem div.copy-move-container .action-bar');
	
	/** @events	delete item from thumbnail-view */
	$(document).on('click', '#thumbnail-view .toolbar .delete', $.proxy(function(e) {
		this.moveToTrash($(e.target).parents('.folder-item'), $(e.target).parents('.folder-item').attr('id'));
    }, this));
};


/**
 * initialize keyboard event handler
 */
DragDrop.prototype.keyboardEventHandler = function() {
	var shiftDown = false,
		ctrlDown = false,
		cDown = false,
		vDown = false,
		shiftKey = 16,
		ctrlKey = 17,
		vKey = 86,
		cKey = 67,
		delKey = 46,
		backSpace = 8;
	
	/**
	 * it's possible to use drag&drop with keyboard shortcuts
	 * therefore user has to select items (select the checkbox of one or more items)
	 * 
	 * Shortcuts:
	 * 	* Ctrl + c	= copy items to drag&drop portlet
	 *  * Ctrl + v	= copy items to thumbnail-view
	 *  * Shift + v	= move items to thumbnail-view
	 *  * Del		= delete items from thumbnail-view
	 *  * Backspace = delete items from thumbnail-view
	 * 
	 * @events	keyboard event handling
	 * 
	 * @uses `@@ajax-dragdrop?action=can_delete` CONTEXTBASED, no remote host may be added!
	 * */
	$(document).on({
		keydown: $.proxy(function(e) {
			var keyCode = e.which;
			
			switch(keyCode) {
				case ctrlKey:
					ctrlDown = true;
					
					if(!shiftDown) {
						$('dl.portlet-static-drag-drop dd.portletItem div.copy-move-container .action-bar.copy').trigger('click');
					}
					break;
				case shiftKey:
					shiftDown = true;
					
					if(!$('dl.portlet-static-drag-drop dd.portletItem div.copy-move-container .action-bar.move').prop('disabled')) {
						$('dl.portlet-static-drag-drop dd.portletItem div.copy-move-container .action-bar.move').trigger('click');
					}
					break;
				case cKey:
					if(ctrlDown) {
						cDown = true;
						vDown = false;
					}
					break;
				case vKey:
					if(ctrlDown || shiftDown) {
						vDown = true;
						cDown = false;
					}
					break;
				case delKey:
				case backSpace:
					if(keyCode == delKey || (ctrlDown && keyCode == backSpace)) {
						// ajax request
						/** @uses `@@ajax-dragdrop?action=can_delete` CONTEXTBASED, no remote host may be added! */
						$.getJSON('@@ajax-dragdrop', {action:'can_delete'}, $.proxy(function(response) {
							if(this.castBool(response) == true) {
								$('#thumbnail-view').find('.folder-item').find('input[type="checkbox"]:checked').each($.proxy(function(k, el) {
									this.moveToTrash($(el).parents('.folder-item'), $(el).parents('.folder-item').attr('id'));
								}, this));
							}
						}, this));
					}
					break;
			}
			
			var selEl = $('dl.portlet-static-drag-drop').find('.drag-drop-container').find('input[type="checkbox"]:checked').length <= 0 ? '' : ':checked';
			
			if(shiftDown && vDown && !cDown) {
				// move items
		        $('dl.portlet-static-drag-drop').find('.drag-drop-container').find('input[type="checkbox"]' + selEl).each($.proxy(function(k, el) {
		            this.insertToThumbnailView($(el).parents('.drag-drop-container'), 'move');
		        }, this));
			} else if(ctrlDown && !shiftDown && (cDown || vDown)) {
				if(cDown && !vDown) {
					// move to dragdrop area
		            $('#thumbnail-view').find('.folder-item').find('input[type="checkbox"]:checked').each($.proxy(function(k, el) {
		                this.droppableDrop($(el).parents('.folder-item'), $('dl.portlet-static-drag-drop'));
		            }, this));
				} else if(!cDown && vDown) {
					// copy items
		            $('dl.portlet-static-drag-drop').find('.drag-drop-container').find('input[type="checkbox"]'+selEl).each($.proxy(function(k, el) {
		                this.insertToThumbnailView($(el).parents('.drag-drop-container'), 'copy');
		            }, this));
				}
			}
		}, this),
		keyup: $.proxy(function(e) {
			var keyCode = e.which;
			
			switch(keyCode) {
				case ctrlKey:
					ctrlDown = false;
					break;
				case shiftKey:
					shiftDown = false;
					break;
				case cKey:
					cDown = false;
					break;
				case vKey:
					vDown = false;
					break;
			}
		}, this)
	});
	
	/** @events select items without clicking on checkbox, instead press shift and click on items for selection */
	$('#thumbnail-view').on('click', function(e) {
        var $target = $(e.target);
    
        if($target.parents('.folder-item').length > 0 && shiftDown) {
            e.preventDefault();
            
            var $checkbox = $(e.target).parents('.folder-item').find('input[type="checkbox"]');
            
            if($checkbox.prop('checked') === true) {
                $checkbox.prop('checked', false).trigger('change');
            } else {
                $checkbox.prop('checked', true).trigger('change');
            }
            
            return false;
        }
    });
};


/**
 * @notused
 * @TODO may be not functional due to updates, code needs perhaps rewrite
 * 		 needs documentation
 * 
 * @uses `@@ajax-dragdrop-permissions?can_copy|can_move`
 * @uses `@@ajax-dragdrop?action=copy_object|move_object
 */
DragDrop.prototype.initEview = function() {
	var self = this;
	
	var options = {
		accept: '#thumbnail-view .folder-item',
		tolerance: 'pointer',
		over: function(event, ui) {
			var container = $(this),
				uid = ui.draggable.attr('id'),
				content_path = $.trim(container.find('span.content_path').text()),
				content_url = $.trim(container.find('span.content_url').text()),
				state = $('dl.portlet-static-drag-drop').find('.copy-move-container').find('.action-bar.state-active').hasClass('move') ? 'move' : 'copy';
			
			/** @uses `@@ajax-dragdrop-permissions?action=can_copy|can_move` */
			$.getJSON(content_url + '/@@ajax-dragdrop-permissions', {action: 'can_' + state, uid: uid}, function(response) {
				if(self.castBool(response) == true) {
					container.removeClass('state-error').addClass('state-hover');
				} else {
					container.addClass('state-error').removeClass('state-hover');
				}
			});
		},
		out: function(event, ui) {
			$('dl.portletAjaxNavigation').find('.ui-droppable').each(function() {
                $(this).removeClass('state-error state-hover');
            });
		},
		drop: function(event, ui) {
			var self = this;
			
            var container = $(this),
                uid = ui.draggable.attr('id'),
                content_path = $.trim(container.find('span.content_path').text()),
                content_url = $.trim(container.find('span.content_url').text()),
                state = $('dl.portlet-static-drag-drop').find('.copy-move-container').find('.action-bar.state-active').hasClass('move') ? 'move' : 'copy';
            
            /** @uses `@@ajax-dragdrop-permissions?action=can_copy|can_move` */
            $.getJSON('@@ajax-dragdrop-permissions', {action: 'can_' + state, uid: uid}, function(response) {
                if(self.castBool(response) == true) {
                	/** @uses `@@ajax-dragdrop?action=copy_object|move_object` */
                    $.getJSON(content_url + '/@@ajax-dragdrop', {action: state + '_object', uid: uid}, function(response) {
                        container.removeClass('state-error state-hover', 250);
                        
                        if(state == 'move') {
                            ui.draggable.fadeOut(600, function() {
                                ui.draggable.remove();
                            });
                        }
                    });
                } else {
                    container.removeClass('state-error state-hover', 250);
                }
                
                container.removeClass('state-error state-hover', 250);
            });
        }
	};
    
    // init droppables
    if($('dl.portletAjaxNavigation').length > 0) {
        $('dl.portletAjaxNavigation').find('ul#subfolder_listing li').each(function() {
            if($(this).hasClass('is_folderish')) {
                $(this).droppable(options);
            }
        });
    }
};



/**
 * @constructs
 */
DragDrop.prototype.init = function() {
	this.checkPermission(); // check permission in current folder
	this.initSortable();	// initialise sortable on current thumbnail view
	this.initTrash();		// initialise trash portlet
	this.initDropable();	// initialise dragdrop portlet
	//this.initEview();		// initialise eview
};
