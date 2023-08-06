$.windowActive = true;

$.isWindowActive = function () {
    return $.windowActive;
};

$(window).focus(function() {
    $.windowActive = true;
});

$(window).blur(function() {
    $.windowActive = false;
});



/**
 * A module representing common methods
 * 
 * @module Utilities
 * @author mreichenbecher
 * @usage
 * 		this.storage.local/session.get(key, noParse)
 * 		this.storage.local/session.set(key, value, noParse)
 * 		this.storage.local/session.unset(key)
 */

/**
 * @constructor
 * @alias module:utilities
 */
function Utilities() {
	this.name = 'ityou.utilities';
	this.version = '0.5.260814';
	
	/** Is the current tab the active tab */
    this.windowActive = true;
    
    /**
     * magic getter
     * 
     * @param   {String} key
     * @param   {String} prop	optional
     * @returns {Object|Array|String|Number|Boolean}
     */
    this.get = function(key, prop) {
    	if(!!key && this.hasOwnProperty(key)) {
    		if(!!prop && this[key].hasOwnProperty(prop)) {
    			return this[key][prop];
    		} else {
    			return this[key];
    		}
    	}
    	
    	return undefined;
    };
    
    /**
     * magic setter
     * 
     * @param   {String} key
     * @param   {String} prop	optional
     * @param   {Object|Array|String|Number|Boolean} value
     * @returns {Utilities}
     */
    this.set = function(key, prop, value) {
    	if(!!prop) {
    		this[key][prop] = value;
    	} else {
    		this[key] = value;
    	}
    	
    	return this;
    };
    
    /**
     * @param   {String} key	get a property named `key` out of cache
     * @returns {Object|Array|String|Number|Boolean}
     */
    this.getCache = function(key) {
    	return this.get('cache', key);
    };
    
    /**
     * @param   {String} key	set a property into cache
     * @param   {Object|Array|String|Number|Boolean} value
     * @returns {Utilities}
     */
    this.setCache = function(key, value) {
    	return this.set('cache', key, value);
    };
    
    /**
     * @param   {String} option	get a property named `option` out of a property named `key`
     * @param   {String} key	get a property named `key` out of `this` 
     * @returns {Object|Array|String|Number|Boolean}
     */
    this.getOption = function(option, key) {
    	return this.get(key, option);
    };
    
    /**
     * @param   {String} option	set a property named `option` into `this`
     * @param   {Object|Array|String|Number|Boolean} value
     * @param   {String} key 	set a property named `key` into a property named `option`
     * @returns {Utilities}
     */
    this.setOption = function(option, value, key) {
    	return this.set(option, key, value);
    };
    
    /**
     * @param   {String} key
     * @returns {Object}
     */
    this.getSettings = function(key) {
    	return this.get('settings');
    };
    
    /**
     * @param   {Object} settings
     * @returns {Utilities}
     */
    this.setSettings = function(settings) {
    	if(settings) {
    		this.settings = $.extend(this.settings ? this.settings : {}, settings);
    	}
    	
    	return this;
    };
}


/**
 * detect the language of platform
 * 
 * @returns {String}
 */
Utilities.prototype.detectLanguage = function() {
	return ($('#ESI_DATA').data('ityou-lang') ? $('#ESI_DATA').data('ityou-lang').slice(0,2) : (navigator.language || navigator.browserLanguage ? (navigator.language ? navigator.language.slice(0,2) : navigator.browserLanguage.slice(0,2)) : $('html').attr('lang').slice(0,2))).toLowerCase();
};


/**
 * Convert a JS Date Object into an unix timestamp
 * 
 * @param {Number} timestamp 
 * @returns {Number} the unix timestamp
 */
Utilities.prototype.convertToUNIXTimestamp = function(timestamp) {
    timestamp = timestamp.replace(/ /g, 'T');
    
    return Math.floor(Date.parse(timestamp) / 1000);
};


/**
 * Sort a numeric Array
 * 
 * @param {Array} data
 * @param {String} direction asc or desc
 * @returns {Array} the sorted array
 */
Utilities.prototype.sortNumeric = function(data, direction) {
    var tmp = data.sort(function(a, b) {
        return a-b;
    });
    
    if('desc' === direction) {
        tmp.reverse();
    }
    
    return tmp;
};


/**
 * Sort a 2D array by a numeric value
 * 
 * @param {Array} data
 * @param {String} direction asc or desc
 * @returns {Array} the sorted array
 */
Utilities.prototype.sortNumericArray = function(data, direction) {
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
 * Sort a 2D array by an alphabetic value 
 * 
 * @param {Array} data
 * @param {String} direction asc or desc
 * @returns {Array} the sorted array
 */
Utilities.prototype.sortAlphabetic = function(data, direction) {
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
 * Sort an HTML table
 * 
 * @param {Object} table
 * @param {Array} rows
 */
Utilities.prototype.tableSort = function(table, rows) {
    table.empty();
    
    $.each(rows, $.proxy(function(k, row) {
        table.append(row);
    }, this));
};


/**
 * convert a given value to a boolean
 * 
 * @param {Object|Array|String|Number|Boolean} value
 * @returns {Boolean}
 */
Utilities.prototype.toBoolean = function(value) {
    if((typeof value === 'string' && value.toLowerCase() === 'true') || (typeof value === 'boolean' && value === true)) {
        return true;
    } else if((typeof value === 'string' && value.toLowerCase() === 'false') || (typeof value === 'boolean' && value === false)) {
        return false;
    }
    
    return true;
};


/**
 * show a self-defined spinner
 */
Utilities.prototype.showSpinner = function() {
    //$('#ajax-spinner').css('opacity', 1).show().find('img').css('opacity', 1);
    
    if($('.jesi-spinner').length > 0) {
        $('.jesi-spinner').removeClass('hidden');
    } else {
        $('<div class="jesi-spinner"><div class="inner"><i class="fa fa-spinner fa-spin"></i></div>').appendTo('body');
    }
};


/**
 * hide a self-defined spinner
 */
Utilities.prototype.hideSpinner = function() {
    //$('#ajax-spinner').css('opacity', 0).show().find('img').css('opacity', 0);
    $('.jesi-spinner').addClass('hidden');
};


/**
 * check either the window is active or not
 * 
 * @returns {Boolean}
 */
Utilities.prototype.isWindowActive = function() {
    return $.isWindowActive();
};


/**
 * a lightweight log function
 */
Utilities.prototype.log = function() {
    this.log.history = this.log.history || []; // store logs to an array for reference
    this.log.history.push(arguments);
    
    if(window.console) {
        console.log(Array.prototype.slice.call(arguments));
    }
};


/**
 * remove some html tags from a given value
 *
 * @param {String} str
 * @param {String} allowed_tag
 * @returns {String}
 */
Utilities.prototype.stripTags = function(str, allowed_tags) {
    var key = '',
        allowed = false;
        
    var matches = [],
        allowed_array = [];
        
    var allowed_tag = '',
        i = 0,
        k = '',
        html = '';
        
    var replacer = function(search, replace, str) {
        return str.split(search).join(replace);
    };
    
    if(allowed_tags) {
        allowed_array = allowed_tags.match(/([a-zA-Z0-9]+)/gi);
    }
    
    str += '';
    
    matches = str.match(/(<\/?[\S][^>]*>)/gi);
    
    for(key in matches) {
        if(isNaN(key)) {
            continue;
        }
        
        html = matches[key].toString();
        allowed = false;
        
        for(k in allowed_array) {
            allowed_tag = allowed_array[k];
            i = -1;
            
            if(i != 0) {
                i = html.toLowerCase().indexOf('<' + allowed_tag + '>');
            }
            
            if(i != 0) {
                i = html.toLowerCase().indexOf('<' + allowed_tag + ' ');
            }
            
            if(i != 0) {
                i = html.toLowerCase().indexOf('</' + allowed_tag);
            }
            
            if(i == 0) {
                allowed = true;
                break;
            }
        }
        
        if(!allowed) {
            str = replacer(html, ' ', str);
        }
    }
    
    return str;
};


/**
 * get the size of an object
 * 
 * @param {Object} object
 * @returns {Number} the size of the object
 */
Utilities.prototype.size = function(object) {
    var count = 0, i;
    
    for(i in object) {
        if(object.hasOwnProperty(i)) {
            count++;
        }
    }
    
    return count;
};


/**
 * set the translation dictionary
 * 
 * @param {Object} dict
 */
Utilities.prototype.loadDictionary = function(dict) {
	$.i18n.setDictionary(dict);
};


/**
 * check if user opened edit/create doc site
 * 
 * @returns {Boolean}
 */
Utilities.prototype.checkTemplate = function() {
	return !!$('body').attr('class').match(/template-[a-zA-Z0-9-_]+edit/);
};


/**
 * capitalize the first letter of a given string
 * 
 * @param   {String} string
 * @returns {String}
 */
Utilities.prototype.capitalizeFirstLetter = function(string) {
	return string.charAt(0).toUpperCase() + string.slice(1);
};


/**
 * create instances of storage to deploy its methods to other classes
 */
Utilities.prototype.storage = {
	session: new Storage('session'), // using `window.sessionStorage`
	local: new Storage('local')		 // using `window.localStorage`
};


/**
 * A module representing the browser storage
 * 
 * @module storage
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:storage
 * @param {String} type session or local
 */
function Storage(type) {
	this.name = 'ityou.storage';
	this.version = '0.4.260814';
	
	// What storage should be used
	this.type = type;
	// a pointer on the used storage
	this.storage = (type === 'session' ? ('sessionStorage' in window && window['sessionStorage'] !== null ? window.sessionStorage : false) : (type === 'local' ? ('localStorage' in window && window['localStorage'] !== null ? window.localStorage : false) : false));
}


/**
 * get a stored value
 * 
 * @param {String} key
 * @param {Boolean} noParse optional, use it if you don't want to parse the value
 * @returns {Object|Array|String|Number|Boolean}
 */
Storage.prototype.get = function(key, noParse) {
	// check if storage can be used, otherwise fallback to cookies
	if(this.storage) {
		if(noParse) {
			// don't parse the value
			return this.storage.getItem(key);
		} else {
			// parse the value, useful, if storing objects
			return JSON.parse(this.storage.getItem(key));
		}
	} else {
		// returning the value from cookie
		var name = key + '=',
			ca = document.cookie.split(';');
		
		var erg = '';
		
		$.each(ca, $.proxy(function(i, val) {
			var c = $.trim(val);
			
			if(c.indexOf(name) === 0) {
				if(noParse) {
					erg = c.substring(name.length, c.length);
					return;
				} else {
					erg = JSON.parse(c.substring(name.length, c.length));
					return;
				}
			}
		}, this));
		
		return erg;
	}
}

/**
 * save a value to the storage
 * use noParse if you don't want the value to be parsed
 * 
 * @param {String} key
 * @param {Object|Array|String|Number|Boolean} value
 * @param {Boolean} noParse
 */
Storage.prototype.set = function(key, value, noParse) {
	// check if storage can be used, otherwise fallback to cookies
	if(this.storage) {
		if(noParse) {
			// save value without parsing
			this.storage.setItem(key, value);
		} else {
			// save value parsed, useful for objects
			this.storage.setItem(key, JSON.stringify(value));
		}
	} else {
		// saving value in cookie
		var date = new Date(),
			expires = "";
		
		if(this.type === 'local') {
			data.setTime(date.getTime() + (365 * 24 * 60 * 60 * 1000));
			expires = '; expires=' + date.toGMTString();
		}
		
		if(noParse) {
			document.cookie = key + '=' + value + expires + '; path=/';
		} else {
			document.cookie = key + '=' + JSON.stringify(value) + expires + '; path=/';
		}
	}
};


/**
 * remove an item from the storage
 * 
 * @param {String} key
 */
Storage.prototype.unset = function(key) {
	// check if storage can be used, otherwise fallback to cookies
	if(this.storage) {
		// delete from storage
		this.storage.removeItem(key);
	} else {
		// delete cookie
		document.cookie = key + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT';
	}
};


/**
 * clear storage if something important changed, e.g. parsing values
 */
Storage.prototype.clear = function() {
	this.storage.clear();
};