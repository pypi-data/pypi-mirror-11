/**
 * DataTables Filling in Extuserprofile
 * 
 * @module UserDatatables
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:UserDatatables
 * 
 * @uses module:WhoIsOnline
 * 
 * @param {Object} settings
 * @param {WhoIsOnline} whoisonline
 */
function UserDatatables(settings, whoisonline) {
	this.name = 'ityou.extuserprofile.datatables';
	this.version = '0.2.260814';
	
	// extend settings
	this.settings = $.extend({
		dataUrl: '/@@ajax-users-datatable'
	}, settings);
	
	this.userTable = $('#user-table');
	this.dataTable = null;
	
	this.whoisonline = whoisonline;
}


/** @uses module:Utilities.detectLanguage() */
UserDatatables.prototype.detectLanguage = (new Utilities()).detectLanguage;


/**
 * Draw Table and mark users which are online right now
 * also sort the table according to who is online
 * 
 * @uses `@@ajax-whoisonline?time_client=...` @ L43
 * @uses `@@ajax-users-datatable?g=...` @ L52
 * 
 * @param {String} group_id
 */
UserDatatables.prototype.drawTable = function(group_id) {
	var ajaxSource = this.settings.remote + this.settings.dataUrl + (!!this.settings.callback ? this.settings.callback + '&' : '?') + 'g=' + group_id;
	
	// check who is online
	/** @uses `@@ajax-whoisonline?time_client=...` */
	$.ajax({
		url: this.settings.remote + '/@@ajax-whoisonline' + this.settings.callback,
		data: {
			time_client: (new Date()).getTime() / 1000
		},
		dataType: 'json',
		timeout: 30000,
		success: $.proxy(function(response) {
			/** @uses `@@ajax-users-datatable?g=...` */
			this.dataTable = this.userTable.dataTable({
				'bProcessing'	: true,
				'bDestroy'		: true,
				'sAjaxSource'	: ajaxSource,
				'aoColumnDefs'	: [{
					'sClass'  	: 'recent_time hidden',
					'aTargets'	: [0],
					'fnRender'	: $.proxy(function(data) {
						return this.inResponse(response, data.aData[8]);
					}, this)
				}, {
					'bSortable' : false,
					'sClass'	: 'portrait',
					'aTargets'	: [1],
					'fnRender'	: $.proxy(function(data) {
						return '<span title=""><a href="' + this.settings.remote + '/author/' + data.aData[8] + '" class="user-portrait" data-uid="' + data.aData[8] + '">' + data.aData[1] + '</a></span>'; 
					}, this)
				}, {
					'aTargets'	: [2],
					'sClass'	: 'fullname'
				}, {
					'aTargets'	: [3],
					'bSortable'	: false,
					'sClass'	: 'send-message',
					'fnRender'	: $.proxy(function(data) {
						return '<a href="' + this.settings.remote + '/@@messages?sid=' + data.aData[8] + '" class="btn btn-default"><i class="fa fa-envelope-o"></i></a>';
					}, this)
				}, {
					'aTargets'	: [4],
          			'sClass'	: 'position'
          		}, {
          			'aTargets'	: [5],
          			'sClass'	: 'mobile'
          		}, {
          			'aTargets'	: [6],
          			'sClass'	: 'location'
          		}, {
          			'aTargets'	: [7],
          			'sClass'	: 'lastlogin',
          			'fnRender'	: $.proxy(function(data) {
          				var t = new ClientTimezone();
          				return '<span class="hiddenStructure">' + data.aData[7][1] + '</span><span>' + t.convertTime(data.aData[7][0]) + '</span>';
          			}, this)
				}],
				'aaSorting'		: [[0, 'desc']],
				'bAutoWidth'	: false,
				'oLanguage'		: eval('lang_' + this.detectLanguage()),//eval('lang_' + $('html').attr('lang')),
				'iDisplayLength': 50
			});
			
			this.dataTable.fnClearTable(true);
		}, this)
	});
};


/**
 * check if currently rendered user is in the `whoisonline` response and return
 * the last recent time; this is for sorting the table
 * 
 * @param   {Array} whoIsOnline
 * @param   {String} value
 * @returns {Number}
 */
UserDatatables.prototype.inResponse = function(whoIsOnline, value) {
	var x = 0;
	
	if($('#ESI_DATA').data('ityou-uid') == value) {
		x = parseInt((new Date()).getTime() / 1000);
	} else {
		var active = true,
			i = 0;
		
		while(active && i < whoIsOnline.length) {
			if(whoIsOnline[i].id === value) {
				x = whoIsOnline[i].recent_time;
				active = false;
			}
			
			i++;
		}
	}
	
	return x;
};


/**
 * mouse event handler registering
 * 
 * @events
 */
UserDatatables.prototype.mouseEvents = function() {
	/** @events toggle groups if user clicks on group portlet */
	$('#group-portlet').on('click', '.group', $.proxy(function(e) {
		var $el = $(e.currentTarget);
		
		if($el.hasClass('active')) {
			$el.removeClass('active');
			this.drawTable('');
		} else {
			$('#group-portlet').find('.group').removeClass('active');
			$el.toggleClass('active');
			this.drawTable($el.attr('id'));
		}
		
		this.whoisonline.getAll();
	}, this));
};


/**
 * @constructs
 */
UserDatatables.prototype.init = function() {
	this.mouseEvents();
	
	if(this.userTable.length > 0) {
		this.drawTable('');
	} 
};
