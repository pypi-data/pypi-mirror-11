(function($, window, document, _, undefined) {
	
	'use strict';
	
	_.libs.editable = {
		name: 'ityou.editable',
		version: '0.1.0',
		
		cache: {
			currentItem: {},
			lastItem: {},
			currentForm: null
		},
		
		settings: {
			selector: '.editable',
			formSelector: '.editable-form'
		},
		
		helper: {
			isEmpty: function(object) {
				var empty = true;
				
				$.each(object, function(k,v) {
					if(object.hasOwnProperty(k) && undefined !== v) {
						empty = false;
						return; // stopy only foreach
					}
				});
				
				return empty;
			},
			toggle: function(object) {
				if(!this.isEmpty(object)) {
					object.span.next().remove();
					object.span.show();
					if(object.span.prev().length > 0 && object.span.prev()[0].hasOwnProperty('nodeName') && obejct.span.prev()[0].nodeName.toLowerCase() === 'i') {
						object.span.prev().show();
					}
				}
			},
			validateField: function(form, item, value) {
				if(item.span.data('required') !== undefnied && item.span.data('required') === true) {
					if(value.length === 0) {
						form.find('.input-group').addClass('has-error');
						return false;
					}
				}
				
				form.find('.input-group').removeClass('has-error');
				return true;
			}
		},
		
		createFormField: function() {
			this.cache.currentForm = null;
			
			var curr = this.cache.currentItem,
				last = this.cache.lastItem;
			
			var form = $('<form class="' + this.settings.formSelector.substr(1) + '" />'),
				inputGroup = $('<div class="input-group" />'),
				inputGroupBtn = $('<span class="input-group-btn" >/'),
				buttonSubmit = $('<button class="btn btn-default" type="submit"><i class="fa fa-check"></i></button>'),
				buttonCancel = $('<button class="btn btn-default" type="button"><i class="fa fa-times"></i></button>'),
				clearValue = $('<i class="fa fa-times-circle clear-value" />'),
				inputGroupAddon = $('<span class="input-group-addon" />'),
				field;
			
			var currentValue = curr.span.hasClass('empty') ? '' : curr.span.text();
			
			form.append(inputGroup);
			inputGroup.append(clearValue).append(inputGroupBtn);
			inputGroupBtn.append(buttonSubmit).append(buttonCancel);
			
			if(curr.hasOwnProperty('type') && (curr.type === 'text' || curr.type === 'date' || curr.type === 'email')) {
				field = $('<input type="' + curr.type + '" value="' + currentValue + '" name="' + curr.name + '" class="form-control">');
			} else if(curr.hasOwnProperty('type') && curr.type === 'textarea') {
				field = $('<textarea class="form-control" name="' + curr.name + '" />');
				field.val(curr.span.text());
			} else {
				return;
			}
			
			// add formField to form
			field.prependTo(inputGroup);
			
			// hide span
			curr.span.hide();
			
			// hide icon if existing
			if(curr.span.prev().length > 0 && curr.span.prev()[0].hasOwnProperty('nodeName') && curr.span.prev()[0].nodeName.toLowerCase() === 'i') {
				// add icon as group addon
				inputGroupAddon.append(curr.span.prev().clone()).prependTo(inputGroup);
				
				// hide icon
				curr.span.prev().hide();
			}
			
			// insert form
			form.insertAfter(curr.span);
			
			// cache form object
			this.cache.currentForm = form;
		},
		
		initForm: function() {
			this.helper.toggle(this.cache.lastItem);
		},
		
		processForm: function() {
			var serializedData = $(this.settings.formSelector).serialize().split('='),
				prop = serializedData[0],
				val = serializedData[1];
			
			if(this.helper.validateField(this.cache.currentForm, this.cache.currentItem, val)) {
				this.saveField(prop, val);
			}
		},
		
		saveField: function(property, value) {
			var _this = this,
				curr = this.cache.currentItem;
			
			if(value !== curr.span.text()) {
				// TODO AJAX Request
				
				// start ajax
				
					if(value.length === 0) {
						value = 'Empty';
						
						curr.span.addClass('empty');
					} else {
						curr.span.removeClass('empty');
					}
					
					// change value
					curr.span.text(value);
					
					// remove input, show content
					_this.helper.toggle(curr);
					
					// animate background if value changed
					curr.span.css('background-color', 'yellow').animate({
						'background-color': 'transparent'
					}, 2000);
					
				// end ajax
			} else {
				_this.helper.toggle(curr);
			}
		},
		
		init: function() {
			var _this = this;
			
			$(this.settings.selector).on('click', function(e) {
				var $this = $(this),
					data = $this.data();
				
				if(Object.size(data) === 0) {
					_.log('!data');
				} else {
					if(_this.cache.currentItem.hasOwnProperty('span')) {
						_this.cache.lastItem.span = _this.cache.currentItem.span;
					}
					
					_this.cache.currentItem.span = $(this);
					
					$.each(data, function(key, value) {
						_this.cache.lastItem[key] = _this.cache.currentItem[key];
						_this.cache.currentItem[key] = value;
					});
					
					_this.initForm();
				}
			});
			
			$(document).on('click', this.settings.formSelector + ' .clear-value', function(e) {
				$(this).prev().val('').focus();
			});
			
			$(document).on('submit', _this.settings.formSelector, function(e) {
				_this.processForm();
				
				return false;
			}); 
		}
		
	};
	
}(jQuery, this, this.document, this.ITYOU));