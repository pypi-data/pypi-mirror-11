/**
 * Converter for Timezone issues, e.g. Germany <-> USA
 * 
 * @module ClientTimezone
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:ClientTimezone
 */
function ClientTimezone() {
	this.name = 'ityou.timezone.converter';
	this.version = '0.2.260814';
	
	// client timezone
	this.client_timezone = (new Date()).getTimezoneOffset() * 60 * -1;
	// server timezone
	this.server_timezone = $('#ESI_DATA').data('ityou-server-time-offset');
	// date format
	this.dateFormat = $('#ESI_DATA').data('ityou-time-format');
	// selector where dates should be changed
	this.selector = '.client-time';
	
	/**
	 * @param {String} key
	 */
	this.get = function(key) {
		if(this.hasOwnProperty(key)) {
			return this[key];
		}
		
		return undefined;
	};
}


/**
 * read a given timestamp and extract everything so we can build a JS DateTimeObject
 * 
 * @param   {String} timestamp
 * @returns {DateTimeObject}
 */
ClientTimezone.prototype.dateSetter = function(timestamp) {
	if(undefined === timestamp || timestamp.length === 0) {
		return false;
	}
	
	var x = timestamp.split('T');
	var dmy = x[0].split('-');
	var hmsms = x[1].split(':');
	var sms = hmsms[2].split('.');
	
	return new Date(dmy[0], dmy[1]-1, dmy[2], hmsms[0], hmsms[1], sms[0], 0); 
};


/**
 * convert a timestamp into another timezone
 * 
 * @TODO Sommerzeit, Winterzeit -> derzeit keine Möglichkeit der Umsetzung
 * 
 * @param   {String} timestamp
 * @returns {String}
 */
ClientTimezone.prototype.convertTime = function(timestamp) {
	// older Android Browsers (Android 2.1) are not formatting ISO correctly
	//var d = new Date('2014-04-04T21:17:20.303876Z');
	//var d = new Date(timestamp);
	var d = this.dateSetter(timestamp);
	
	if(d === false) {
		return '-';
	}
	
	d.setHours(d.getHours() - d.getTimezoneOffset()/60 - this.server_timezone/3600);
	// TODO: Sommer- und Winterzeit => impossible
	
	// parse date to given format
	var x = this.parseFormat(d);
	
	return x;
};


/**
 * parse a date to a given format
 * 
 * @param   {DateTimeObject} date
 * @returns {String}
 */
ClientTimezone.prototype.parseFormat = function(date) {
	var format = this.dateFormat;
	var tmp = new Date();
	
	if(tmp.getDate() === date.getDate() && tmp.getDay() === date.getDay() && tmp.getFullYear() === date.getFullYear()) {
		return this.zeroize(date.getHours()) + ':' + this.zeroize(date.getMinutes());
	}
	
	return format
				.replace(/\%d/, this.zeroize(date.getDate()))
				.replace(/\%m/, this.zeroize((date.getMonth()+1)))
				.replace(/\%Y/, date.getFullYear())
				.replace(/\%H/, this.zeroize(date.getHours()))
				.replace(/\%M/, this.zeroize(date.getMinutes()));
};


/**
 * helper function to add zero in front of 0-9
 * 
 * @param   {Number} number
 * @returns {Number|String}
 */
ClientTimezone.prototype.zeroize = function(number) {
	number = parseInt(number);
	
	if(number < 10) {
		return '0' + number;
	}
	
	return number;
}