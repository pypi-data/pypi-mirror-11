// function to fit all items with the same height
(function($) {
    $.fn.equalHeights = function(minHeight, maxHeight) {
        this.find('.thumbnail').each(function() {
            $(this).height('auto');
        });
    
        tallest = (minHeight) ? minHeight : 0;
        
        //console.log('min: ' + minHeight, 'max: ' + maxHeight, 'tallest: ' + tallest);
        
        setTimeout($.proxy(function() {
            this.each(function() {
                if($(this).height() > tallest) {
                    tallest = $(this).height();
                }
            });
            
            if((maxHeight) && tallest > maxHeight) {
                tallest = maxHeight;
            }
            
            if(tallest % 10 !== 0) {
                 var r = tallest % 10;
                 
                 tallest += (10 - r);
            }
            
            return this.each(function() {
            	$(this).find('.thumbnail').css({
            		'height': tallest,
            		'overflow': 'hidden'
            	});
                //$(this).find('.thumbnail').animate({'height': tallest}, 100).css('overflow', 'hidden');
            });
        }, this), 100);
    }
})(jQuery);




/**
 * controls for Thumbnail View
 * 
 * @module ThumbnailView
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:ThumbnailView
 */
function ThumbnailView(options) {
	this.name = 'ityou.thumbnail.view';
	this.version = '0.5.260814';
	
	// options
	this.options = $.extend({}, {
        currentView: 'thumbnail-standard-view'
    }, options);

	/**
	 * @returns {Object}
	 */
    this.getOptions = function() {
        return this.options;
    };
    
    /**
     * @param   {String} option
     * @returns {Object|Array|String|Number|Boolean}
     */
    this.getOption = function(option) {
        if(this.options.hasOwnProperty(option)) {
            return this.options[option];
        }
        
        return false;
    };
 
    /**
     * @param {String} option
     * @param {Object|Array|String|Number|Boolean} value
     */
    this.setOption = function(option, value) {
        this.options[option] = value;
    };
};

// inherits functionality of `module:Utilities`
/** @uses module:Utilities */
ThumbnailView.prototype = new Utilities();


/**
 * initialize thumbnail-view
 */
ThumbnailView.prototype.init = function() {
	// register event handler
    this.EventHandler();
    
    // fixing runtime issues
    setTimeout($.proxy(function() {    	
    	if(this.storage.local.get('thumbnail-view', true) !== null) {
    		// set last activated view
    		this.setOption('currentView', this.storage.local.get('thumbnail-view', true));
    	}
    	
    	// trigger listing size
        this.ListingSize(this.getOption('currentView'));
		
        // insert image src path
        this.getThumbnail($('.caption .document-download, .caption a'), 0);
    	
    	// show some items
    	$('#thumbnail-view').find('.folder-item').slice(0, (Math.ceil($('#portal-column-content').width() / ($('.folder-item').width() + 14)) * 2)).show();
    	
    	// hide 'more item' element if all items are visible
    	if(($('#thumbnail-view').find('.folder-item:visible').length === $('#thumbnail-view').find('.folder-item').length && $('#thumbnail-view').find('.folder-item').length > 0) || $('#thumbnail-view').find('.folder-item').length == 0) {
    	    $('.more-item').hide();
    	}
    }, this), 1);
};


/**
 * initalizer for different views
 * 
 * thumbnail-list-view		: showing one item per row (list) and show additional information
 * thumbnail-1-column-view	: showing one item per row and hide additional information
 * thumbnail-2-columns-view	: showing two items per row and hide additional information
 * thumbnail-3-columns-view	: showing three items per row and hide additional information
 * thumbnail-standard-view	: count of items per row is flexible, hide additional information 
 * 
 *  @param {String} view	thumbnail-list-view|thumbnail-1-column-view|thumbnail-2-columns-view|thumbnail-3-columns-view|thumbnail-standard-view
 */
ThumbnailView.prototype.ListingSize = function(view) {
	// collect items
    var els = $('#thumbnail-view').find('.folder-item, .more-item');
    
    // feedback state @ listing size controls
    if(!$('#' + view).hasClass('state-active') && !$('#' + view).prop('disabled')) {
    	$('#' + view)
    		.addClass('state-active')
    		.prop('disabled', true);
    }
    
    // save selected view, so we can rebuild other views
    this.storage.local.set('thumbnail-view', view, true);

    // check which view should be built
    switch(view) {
        case 'thumbail-list-view':
            this.initListView(els);
            break;
        case 'thumbnail-1-column-view':
            this.initGridView(els, 'col-xs-12');
            break;
        case 'thumbnail-2-columns-view':
            this.initGridView(els, 'col-xs-6');
            break;
        case 'thumbnail-3-columns-view':
            this.initGridView(els, 'col-xs-4');
            break;
        case 'thumbnail-standard-view':
            this.initGridView(els, 'col-xs-6 col-md-4 col-lg-3');
            break;
    }
    
    // make items same height
    els.equalHeights();
};


/**
 * grid view builder
 * 
 * @param {Array} items
 * @param {String} column
 */
ThumbnailView.prototype.initGridView = function(items, column) {
	// destroy old view
    this.destroyListView(items);

    // build selected view
    items.each($.proxy(function(k, el) {
        $(el).removeClass(this.removeColumn(el)).addClass(column);
    }, this));
};


/**
 * list-view builder
 * 
 * @param {Array} els
 */
ThumbnailView.prototype.initListView = function(els) {
	// loop through elements and build up list view
    els.each($.proxy(function(k, el) {
        $(el).removeClass(this.removeColumn(el)).addClass('col-xs-12 list-group');
        
        $(el).find('.thumbnail').addClass('clearfix');
        $(el).find('.thumbnail > a').first().addClass('col-xs-6 col-sm-4 col-md-2');
        $(el).find('.thumbnail > .caption').addClass('col-xs-6 col-sm-8 col-md-10');
        $(el).find('.thumbnail > .additional-information').addClass('col-xs-6 col-sm-8 col-md-10');
    }, this));
};


/**
 * helper function to destroy list-view
 * 
 * @pram {Array} els
 */
ThumbnailView.prototype.destroyListView = function(els) {
	// loop through elements and destroy list-view
	// means: remove unnecessary css class etc
    els.each($.proxy(function(k, el) {
        var $thumbnail = $(el).find('.thumbnail'),
            $a = $thumbnail.find('> a').first(),
            $caption = $thumbnail.find('.caption'),
            $addInfo = $thumbnail.find('.additional-information');
    
        $(el).removeClass('col-xs-12 list-group');
        $thumbnail.removeClass('clearfix');
        $a.removeClass(this.removeColumn($a[0]));
        
        if($caption.length > 0) {
            $caption.removeClass(this.removeColumn($caption[0]));
        }
        
        if($addInfo.length > 0) {
            $addInfo.removeClass(this.removeColumn($addInfo[0]));
        }
    }, this));
};


/**
 * helper function to destroy grid-view
 * 
 * @param {Object} el
 */
ThumbnailView.prototype.removeColumn = function(el) {
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
 * @events {Click} toggle additional information on click
 * @events {Hover} toggle toolbar on hover
 */
ThumbnailView.prototype.hoverIntent = function() {
	$('#thumbnail-view div.folder-item:not(.list-group) div.thumbnail').off('click', '.additional-information-trigger');
	$('#thumbnail-view div.folder-item:not(.list-group) div.thumbnail').on('click', '.additional-information-trigger', $.proxy(function(e) {
        e.preventDefault();
        
        this.toggleAdditionalInformation(e);
    }, this));
	
	$('#thumbnail-view div.folder-item:not(.list-group) div.thumbnail').hoverIntent($.proxy(this.hoverIntentOverToolbar, this), $.proxy(this.hoverIntentOutToolbar, this));
};


/**
 * register event handler
 * 
 * @events
 */
ThumbnailView.prototype.EventHandler = function() {
	// each thumbnail that is not a folder has a big thumbnail preview
	this.prepOverlay();
	// event handler for additional information and toolbar
	this.hoverIntent();
	
	/** @events if viewport got resized (landscape,portrait etc), we need to recalculate the size of the thumbnails */ 
    $(window).on('resize', $.proxy(function(e) {
        $('#thumbnail-view .folder-item, #thumbnail-view .more-item').equalHeights();
    }, this));

    /** @events handle click on thumbnail listings */
    $('#thumbnail-view .thumbnail-listing-size').on('click', 'button', $.proxy(function(e) {
        e.preventDefault();
        
        // close all opened additional informations
        this.hideAdditionalInformations();
        
        var $target = $(e.target),
        	size = (e.target.nodeName.toLowerCase() === 'button' ? $target.attr('id') : $target.parents('button').attr('id')),
            $eventTrigger = $('#' + size);
        
        // define if button was clicked twice
        if(!$eventTrigger.hasClass('state-active')) {
        	// remove state-active and disabled attribute on all other buttons
            $('#thumbnail-view .thumbnail-listing-size').find('button').each($.proxy(function(k, el) {
                $(el).removeClass('state-active');
                
        		if($(el).prop('disabled')) {
        			$(el).removeProp('disabled');
        		}
            }, this));
            
            return this.ListingSize(size);
        }
        
        return false;
    }, this));
    
    /** @events change checkbox, if checked, toolbar stays visible and border-color changes */
    $('#thumbnail-view').on('change', 'input[type="checkbox"]', $.proxy(function(e) {
        var $target = $(e.currentTarget),
            $el = $target.parents('.folder-item');
            
        if($target.prop('checked') === true) {
            $el.addClass('state-checked');
        } else {
            $el.removeClass('state-checked');
        }
	}, this));
	
	/** @events load other thumbnail if last item is visible in viewport */
	$('#thumbnail-view').find(".folder-item:visible").last().one('inview', $.proxy(function(event, visible) {
		if(visible) {
		    this.getMoreThumbs();
		}
	}, this));
	
	/** @events load other thumbnail is user clicked `more-item` */
	$('#thumbnail-view').on('click', '.more-item', $.proxy(function(e) {
	    e.preventDefault();
	    
	    this.getMoreThumbs();
	}, this));
    
    /** @events sorting */
    $('#thumbnail-view').on('click', '.thumbnail-listing-sort a, #thumbnail-listing-sort-method', $.proxy(function(e) {
        e.preventDefault();
        
        var $el = $(e.target),
        	// action: creation_date|modification_date|thumb_list_title
            action = $el.data('sortby'),
            // direction: asc|desc
            direction = $('#thumbnail-listing-sort-method').data('sort-direction') || 'asc';
        
        if(!$el.hasClass('btn')) {
        	var btn = $('#thumbnail-listing-sort-method');
        	var btnText = $el.text();
        	
        	// rename btn with current sort-action and show current sort-direction
        	btn.text(btnText).data('sortby', action);
        }

        $('#thumbnail-view').find('.folder-item').show();

        switch(action) {
        // action: creation_date|modification_date
        case 'creation_date':
        case 'modification_date':
            var timestamps = [];
            
            var sortingRule = action === 'creation_date' ? 'date_created' : 'date_edited';

            // extract creation-/modification-date
            $('#thumbnail-view').find('.additional-information').find('span.' + sortingRule).each($.proxy(function(k, el) {
                var key = $(el).parents('.folder-item').attr('id');
            
                timestamps.push([key, $.trim($(el).data('unix'))]);
            }, this));
            
            // visual user feedback for sorting direction
            this.sortDirection($('#thumbnail-listing-sort-method'), direction);

            // sort collected timestamps
            timestamps = this.sortNumeric(timestamps, direction);
            
            // prepare items for sorting
            var items = this.prepareSortedItems(timestamps);
            
            // sort items and append them into DOM
            this.tableSort($('#thumbnail-view').find('form'), items);
            
            break;
        // action: title
        case 'title':
            var titles = [];
            
            // extract titles
            $('#thumbnail-view').find('.thumbnail .caption').each($.proxy(function(k, el) {
                var key = $(el).parents('.folder-item').attr('id');
                
                titles.push([key, $.trim($(el).text())]);
            }, this));
            
            // visual user feedback for sorting direction
            this.sortDirection($('#thumbnail-listing-sort-method'), direction);
            
            // sort collected titles
            titles = this.sortAlphabetic(titles, direction);
            
            // prepare items for sorting
            var items = this.prepareSortedItems(titles);
            
            // sort items and append them into DOM
            this.tableSort($('#thumbnail-view').find('form'), items);
        
            break;
        }
    }, this));
};


/**
 * helper function to show visual user feedback for current sorting direction
 * 
 * @param {Object} el
 * @param {String} direction
 */
ThumbnailView.prototype.sortDirection = function(el, direction) {
    if(direction === 'asc') {
        el.data('sort-direction', 'desc').removeClass('sort-desc').addClass('sort-asc');
    } else {
        el.data('sort-direction', 'asc').removeClass('sort-asc').addClass('sort-desc');
    }
};


/**
 * helper function to prepare the pre sorted items
 * 
 * @param   {Array} data
 * @returns {Array}
 */
ThumbnailView.prototype.prepareSortedItems = function(data) {
    var items = [];
    
    $.each(data, $.proxy(function(k, v) {
        var $item = $('#thumbnail-view').find('#' + v[0]);
        
        items.push($item);
    }, this));
    
    return items;
};


/**
 * hide additional information
 */
ThumbnailView.prototype.hideAdditionalInformations = function() {
    $('#thumbnail-view .folder-item').find('.thumbnail').find('.additional-information').find('.holder').each(function() {
        if($(this).is(':visible')) {
            $(this).slideToggle({
                direction: 'down',
                duration: 100
            });
        }
    });
};


/**
 * toggle additional information
 */
ThumbnailView.prototype.toggleAdditionalInformation = function(e) {
    var $wrapper = $(e.currentTarget).parents('.thumbnail'),
        $addInfo = $wrapper.find('.additional-information'),
        $holder = $addInfo.find('.holder');
        
    var wasVisible = $holder.is(':visible');
        
    this.hideAdditionalInformations();
        
    if(!wasVisible) {
        $holder.slideToggle({
            direction: 'up',
            duration: 300
        });
    }
};


/**
 * show additional information
 * 
 * @deprecated
 */
ThumbnailView.prototype.showAdditionalInformation = function(event) {
    var $el = $(event.currentTarget).parents('.thumbnail'),
        $addInfo = $el.find('div.additional-information'),
        $holder = $addInfo.find('.holder');
        
    $holder.slideToggle({
        direction: 'up',
        duration: 300
    });
};


/**
 * hide additional information
 * 
 * @deprecated
 */
ThumbnailView.prototype.hideAdditionalInformation = function(event) {
    var $el = $(event.currentTarget).parents('.thumbnail'),
        $addInfo = $el.find('div.additional-information'),
        $holder = $addInfo.find('.holder');

    $holder.slideToggle({
        direction: 'down',
        duration: 300
    });
};


/**
 * mouseover event
 * 
 * @param {Object} event
 */
ThumbnailView.prototype.hoverIntentOverToolbar = function(event) {
    var $el = $(event.currentTarget),
        $toolbar = $el.find('.toolbar'),
        $toolbarHolder = $toolbar.find('.holder');
        
    if(!$toolbar.find('input[type="checkbox"]').is(':checked')) {
        $toolbarHolder.fadeIn(100);
    }
};


/**
 * mouseout event
 * 
 * @param {Object} event
 */
ThumbnailView.prototype.hoverIntentOutToolbar = function(event) {
    var $el = $(event.currentTarget),
        $toolbar = $el.find('.toolbar'),
        $toolbarHolder = $toolbar.find('.holder');
        
    if(!$toolbar.find('input[type="checkbox"]').is(':checked')) {
        $toolbarHolder.fadeOut(100);
    }
};


/**
 * helper function to show more thumbnails
 * triggered by scroll and click
 */
ThumbnailView.prototype.getMoreThumbs = function() {
	// show loading animation
    this.showSpinner();
    
    // find all items that were not visible yet
    var hiddenItems = $('#thumbnail-view').find('.folder-item:hidden');
    
    // prepare how many items should be shown in addition (based on current view)
    if(this.getOption('currentView') === 'thumbnail-standard-view') {
        hiddenItems.slice(0, (Math.ceil($('#portal-column-content').width() / ($('.folder-item').width() + 14)) * 2)).fadeIn(600);
    } else if(this.getOption('currentView') === 'thumbnail-1-column-view' || this.getOption('currentView') === 'thumbail-list-view') {
    	hiddenItems.slice(0, 2).fadeIn(600);
    } else {
        hiddenItems.slice(0, (Math.ceil($('#portal-column-content').width() / ($('.folder-item').width() + 14)) - 1)).fadeIn(600);
    }
    
    if($('#thumbnail-view').find('.folder-item:hidden').length > 0) {
    	// register inview event
        $('#thumbnail-view').find('.folder-item:visible').last().one('inview', $.proxy(function(e, visible) {
            if(visible) {
                this.getMoreThumbs();
            }
        }, this));
    }
    
    // hide loading animation
    this.hideSpinner();
    
    if($('#thumbnail-view form').children().length > 1 && $('#thumbnail-view').find('.folder-item:visible').length === $('#thumbnail-view').find('.folder-item').length) {
        $('#thumbnail-view').find('.more-item').hide();
    }
    
    this.ListingSize(this.getOption('currentView'));
};


/**
 * show loading animation
 */
ThumbnailView.prototype.showSpinner = function() {
    var $spinner = $('<div id="mr-spinner" style="text-align: center; position: absolute; left: 0; right: 0; bottom: 50px; z-index: 99999;"/>');
    
    $spinner.html('<i class="fa fa-spinner fa-spin" style="font-size: 72px;"/>');
    $spinner.appendTo('#thumbnail-view');
};


/**
 * hide loading animation
 */
ThumbnailView.prototype.hideSpinner = function() {
    $('#mr-spinner').remove();
};


/**
 * helper function to get thumbnails, they're loaded later because of otherwise they
 * would be blocking the loaded progress
 * 
 * @uses `@@ajax-get-thumbnail` @ L631
 * 
 * @param {Array} items
 * @param {Number} offset
 */
ThumbnailView.prototype.getThumbnail = function(items, offset) {
	// select item at offset position
	var item = $(items[offset]);
	// define array length
	var length = items.length;

	// check if items array is not empty
	// if the selected item at the position `offset` is an image 
	if(item.length > 0 && item.parents('.folder-item').find('.contenttype-image').length == 0) {
		/** @uses `@@ajax-get-thumbnail` */
		$.getJSON(item.attr('href') + '/@@ajax-get-thumbnail', $.proxy(function(response) {
	        if(response) {
	        	// replace image source
	            var path = response.replace(/size=(.*)/g, 'size=large');
	            item.parents('.folder-item').find('img.img-responsive').attr('src', path);
	        }
	        
	        // resizing here, rest is not visible
	        if((offset > 1 && !item.is(':visible') && $(items[offset-1]).is(':visible')) || (offset == length-1 && item.is(':visible'))) {
	    		this.ListingSize(this.getOption('currentView'));
	    	}
	    	
	        // get next thumbnail if array has more items left
	    	if(offset < length-1) {
	        	this.getThumbnail(items, ++offset);
	        }
	    }, this));
	} else if(item.length > 0) {
		// selected item at position `offset` is not an image
		// simply add `/image_large` to image source
		item.parents('.folder-item').find('img.img-responsive').attr('src', item.attr('href') + '/image_large');
		
		// resizing here, rest is not visible
        if((offset > 1 && !item.is(':visible') && $(items[offset-1]).is(':visible')) || (offset == length-1 && item.is(':visible'))) {
    		this.ListingSize(this.getOption('currentView'));
    	}
		
        // get next thumbnail if array has more items left
		if(offset < length-1) {
			this.getThumbnail(items, ++offset);
		}
	}
};


/**
 * register prep overlay on thumbnails
 * 
 * prepOverlay is a build-in function of Plone (`plone.app.jquerytools/overlayhelpers.js#L56`)
 */
ThumbnailView.prototype.prepOverlay = function() {
	$('.linked-document, .Image .linked-document').prepOverlay({
		// data will be loaded via ajax request
        subtype: 'ajax',
        config: {
            onLoad: $.proxy(function(e) {
            	// build content
                this.prepContentView();
                // initialize gallery slider
                this.gallery.init($(e.target));
                // make images responsive
                $(e.target).find('img.preview-image').addClass('img-responsive');
            }, this)
        }
    });
};


/**
 * build content for prepoverlay
 */
ThumbnailView.prototype.prepContentView = function() {
    var $contentViews = $('.show-preview #content-views').children(),
        color = 'text-primary';

    /** @events register click event handler */
    $contentViews.on('click', function(e) {
        var url = $(this).find('a').attr('href');
        
        if(undefined !== url) {
            window.location = url;
        }
    });
    
    // loop through list elements in editbar
    // and rebuild the editbar
    $contentViews.each(function() {
        var menu_context = $(this).find('a').html();
        
        $(this).prepend('<div class="content-view-box"/>');
        $(this).find('.content-view-box').html(menu_context);
        $(this).find('a').html('');
        
        if(!$(this).hasClass('selected')) {
            $(this).find('.content-view-box').addClass(color);
        }
    });
    
    /** @events hover */
    $contentViews.hover(function() {
    	/** @events hover.mouseover */
        if($(this).find('.content-view-box').html().length > 1) {
            var $contentViewBox = $(this).find('.content-view-box');
            
            $contentViewBox
                .removeClass(color)
                .find('.text').show();
        }
    }, function() {
    	/** @events hover.mouseout */
        var $contentViewBox = $(this).find('.content-view-box');
    
        if(!$(this).hasClass('selected')) {
            $contentViewBox.addClass(color);
        }
    
        $contentViewBox.find('.text').hide();
    });
};


/**
 * helper function to add an unix timestamp
 * 
 * @notinuse
 */
ThumbnailView.prototype.addUnixTimestamp = function() {
    $('#thumbnail-view').find('.folder-item').find('.additional-information').find('span.date_created').each($.proxy(function(k, el) {
        $(el).data('unix', this.convertToUNIXTimestamp($(el).text()));
    }, this));
};


/**
 * convert a js date into an unix timestamp
 */
ThumbnailView.prototype.convertToUNIXTimestamp = function(timestamp) {
    var tmp = timestamp.split('.');
    var tmpDate = new Date();
    tmpDate.setDate(tmp[0]);
    tmpDate.setMonth((tmp[1]-1));
    tmpDate.setFullYear(tmp[2]);

    return Math.floor(Date.parse(tmpDate) / 1000);
};


/**
 * helper function for sorting the thumbnail-view
 * this function gets pointer to thumbnail-list wrapper
 * and a pre sorted array with all thmubnail items, so we
 * just have to insert them
 * 
 * @param {Array} pointer to thumbnail-view wrapper
 * @param {Array} rows  presorted array with all thumbnail items
 */
ThumbnailView.prototype.tableSort = function(table, rows) {
    var $moreItem = $('<div>').append(table.find('.more-item').clone()).html();

    // empty thumbnail-view
    table.empty();
    
    // loop through pre sorted data and append it to the thumbnail-view
    $.each(rows, $.proxy(function(k, row) {
        table.append(row);
    }, this));
    
    // append the more item
    table.append($moreItem);
    
    // each thumbnail that is not a folder has a big thumbnail preview
	this.prepOverlay();
	// event handler for additional information and toolbar
	this.hoverIntent();
};


/**
 * helper function to sort an array by numbers
 * this function is only for this case, for other cases see `module:Utilities`
 * 
 * @param   {Array} data
 * @param   {String} direction
 * @returns {Array}
 */
ThumbnailView.prototype.sortNumeric = function(data, direction) {
    var tmp = data.sort(function(a, b) {
        a = a[1];
        b = b[1];
    
        return a-b;
    });
    
    if('desc' === direction) {
        tmp.reverse();
    }
    
    return tmp;
};


/**
 * helper function to sort an array by alphanumeric characters
 * this fnuction is only for this case, for other cases see `module:Utilities`
 * 
 * @param   {Array} data
 * @param   {String} direction
 * @returns {Array}
 */
ThumbnailView.prototype.sortAlphabetic = function(data, direction) {
    var tmp = data.sort(function(a, b) {
        var a = a[1].toLowerCase(),
            b = b[1].toLowerCase();
        
        return a.localeCompare(b);
    });
    
    if('desc' === direction) {
        tmp.reverse();
    }
    
    return tmp;
};


/**
 * helper function to get the max height of elements
 * 
 * @param {Array} element
 */
ThumbnailView.prototype.getMaxHeight = function(element) {
    return Math.max.apply(null, element.map(function() {
        return $(this).height();
    }).get());
};


/** @uses module:ThumbnailGallery */
ThumbnailView.prototype.gallery = new ThumbnailGallery();




/**
 * Gallery Slider for Thumbnail-View
 * 
 * @module ThumbnailGallery
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:ThumbnailGallery
 */
function ThumbnailGallery() {
	this.name = 'ityou.thumbnail.slider';
	this.version = '0.1.260814';
	
	// settings
	this.settings = {
		gal: {
			img: '.preview-image',
			control: '.thumbnail-gallery-controls'
		},
		view: {
			wrapper: '#thumbnail-view',
			item: '.folder-item',
			thumb: '.thumbnail-holder'
		},
		cssNamespace: {
			folder: 'Folder',
			more: 'more-item'
		}
	};
	
	/**
	 * helper function to check if current element in slider has `next/previous` element
	 * 
	 * @param   {Object} el
	 * @param   {String} state	next|prev
	 * @returns {Boolean}
	 */
	this.has = function(el, state) {
		// get next/prev element by state
		var possible = state === 'next' ? el.next() : (state === 'prev' ? el.prev() : false);
		
		// if next/prev item is `show-more` button or a folder, try again
		if(possible && (possible.hasClass(this.settings.cssNamespace.more) || possible.hasClass(this.settings.cssNamespace.folder))) {
			return this.has(possible, state);
		}
		
		return possible && possible.length > 0;
	};
	
	/**
	 * get the successor/predecessor of the current element
	 * 
	 * @param   {Object} el
	 * @param   {String} state	next|prev
	 * @returns {Object}
	 */
	this.spElem = function(el, state) {
		// get next/prev element by state
		var item = state === 'next' ? el.next() : el.prev();
		
		// if next/prev item is `show-more` button or a foler, try again
		if(item && (item.hasClass(this.settings.cssNamespace.more) || item.hasClass(this.settings.cssNamespace.folder))) {
			return this.spElem(item, state);
		}
		
		return item;
	};
	
	/**
	 * get the link of the successor/predecessor of the current element
	 * 
	 * @param   {Object} el
	 * @param   {String} state	next|prev
	 * @returns {String|Boolean}
	 */
	this.spLink = function(el, state) {
		// get next/prev element by state
		var item = state === 'next' ? el.next() : el.prev();
		
		// if next/prev item is `show-more` button or a folder, try again
		if(item && (item.hasClass(this.settings.cssNamespace.more) || item.hasClass(this.settings.cssNamespace.folder))) {
			return this.spLink(item, state);
		}
		
		return item ? item.find(this.settings.view.thumb).attr('href') : false;
	};
	
	/**
	 * shorthand to find a folder-item by an image source
	 * 
	 * @param   {Object} el
	 * @returns {Object}
	 */
	this.findItem = function(el) {
		return $(this.settings.view.item).find('img[src="' + el.find(this.settings.gal.img).attr('src') + '"]').parents(this.settings.view.item);
	};
	
	/**
	 * shorthand to check if current element has a successor
	 * 
	 * @param   {Object} el
	 * @returns {Boolean}
	 */
	this.hasNext = function(el) {
		return this.has(this.findItem(el), 'next');
	};
	
	/**
	 * shorthand to check if current element has a predecessor
	 * 
	 * @param   {Object} el
	 * @returns {Boolean}
	 */
	this.hasPrev = function(el) {
		return this.has(this.findItem(el), 'prev');
	};
	
	/**
	 * shorthand to get the link of the successor of the current element
	 * 
	 * @param   {Object} el
	 * @returns {String}
	 */
	this.next = function(el) {
		return this.spLink(this.findItem(el), 'next');
	};
	
	/**
	 * shorthand to get the link of the predecessor of the current element
	 * 
	 * @param   {Object} el
	 * @returns {String}
	 */
	this.prev = function(el) {
		return this.spLink(this.findItem(el), 'prev');
	};
	
	/**
	 * helper function to create the navigation buttons
	 * 
	 * @param   {Object} overlay
	 * @returns {ThumbnailGallery}
	 */
	this.initBtns = function(overlay) {
		// create button wrapper as jquery object
		var $btnWrapper = $('<div class="' + this.settings.gal.control.substr(1) + '"></div>'),
			// default button
			btn = '<button class="btn btn-default"><i class="fa"></i></button>';
		
		// append wrapper to overlay
		overlay.find('.pb-ajax > div').append($btnWrapper);
		
		// check if current element has a successor
		if(this.hasNext(overlay)) {
			// create a button object
			$next = $(btn);
			// append it to our wrapper
			$btnWrapper.append($next);
			// pull it to the right side, give it `next` css class and an icon
			$next.addClass('pull-right next').find('.fa').addClass('fa-arrow-right');
		}
		
		// check if current element has a predecessor
		if(this.hasPrev(overlay)) {
			// create a button object
			$prev = $(btn);
			// prepend it to our wrapper
			$btnWrapper.prepend($prev);
			// pull it to the left side, give it `prev` css class and an icon
			$prev.addClass('pull-left prev').find('.fa').addClass('fa-arrow-left');
		}
		
		return this;
	};
	
	/**
	 * helper function to remove navigation buttons
	 * they will be recreated on each navigation event
	 * 
	 * @param   {Object} overlay
	 * @returns {ThumbnailGallery}
	 */
	this.removeBtns = function(overlay) {
		// check if the button wrapper exists
		if(overlay.find(this.settings.gal.control).length > 0) {
			// remove it from the DOM
			overlay.find(this.settings.gal.control).remove();
		}
		
		return this;
	};
	
	/**
	 * helper function to toggle a loading sign (visual user feedback)
	 * 
	 * @param   {Object} overlay
	 * @returns {ThumbnailGallery}
	 */
	this.toggleLoading = function(overlay) {
		// pointer to a div in the overlay
		var t = overlay.find('.pb-ajax > div');
		
		// check if spinner exists
		if(t.find('.spinner').length > 0) {
			// it exists, so remove it from DOM
			t.find('.spinner').remove();
		} else {
			// it doesnt exists, append it to the DOM
			t.append('<div class="spinner"><i class="fa fa-spinner fa-spin"></i></div>');
		}
		
		return this;
	};
	
	/**
	 * helper function to get the content of the next element
	 * 
	 * @param   {Object} overlay
	 * @param   {String} state	next|prev
	 */
	this.getContent = function(overlay, state) {
		// pointer to a div in the overlay
		var $contentHolder = overlay.find('.pb-ajax > div');
		
		// show the loading animation
		this.toggleLoading(overlay);
		
		// start an ajax request
		$.ajax({
			dataType: 'html',
			url: state === 'next' ? this.next(overlay) : this.prev(overlay),
			success: $.proxy(function(response) {
				// append the response to an empty div, so we can
				// handle the its content
				var html = $('<div/>').append(response);
				// extract the information we need
				var content = html.find('.show-preview');
				
				// remove the old element from DOM
				$contentHolder.find('.show-preview').remove();
				// and append the new element
				$contentHolder.append(content);
				
				// recreate navigation buttons,
				// hide the loading animation
				// and do some styling for content controls
				this.initBtns(overlay)
					.toggleLoading(overlay)
					.prepContentView();
			}, this)
		});
	};
	
	/**
	 * helper function to initialize click events for navigation buttons
	 * 
	 * @events
	 * 
	 * @param   {Object} overlay
	 * @returns {ThumbnailGallery}
	 */
	this.EventHandler = function(overlay) {
		// try to avoid multiple event listeners on the same object
		overlay.off('click');
		
		/** @events handle click on buttons */
		overlay.on('click', this.settings.gal.control + ' button', $.proxy(function(e) {
			e.preventDefault();
			
			// get state (next|prev)
			var state = $(e.currentTarget).hasClass('next') ? 'next' : 'prev';
			
			// remove the buttons, they will be recreated later
			this.removeBtns(overlay);
			
			// get the content of the next/prev element
			this.getContent(overlay, state);
		}, this));
		
		/** @events show/hide buttons on hover */
		overlay.on('hover', this.settings.gal.control, $.proxy(function(e) {
			$(e.currentTarget).find('.btn').stop().fadeToggle();
		}, this));
		
		/** @events show buttons on click */
		overlay.on('click', this.settings.gal.control, $.proxy(function(e) {
			$(e.currentTarget).find('.btn').stop().fadeIn();
		}, this));
		
		return this;
	};
	
	/**
	 * @constructs
	 * @param {Object} overlay
	 */
	this.init = function(overlay) {
		// create navigation buttons and register click event
		this.initBtns(overlay)
			.EventHandler(overlay);
	};
}

/** @uses ThumbnailView.prepContentView */
ThumbnailGallery.prototype.prepContentView = (new ThumbnailView()).prepContentView;
