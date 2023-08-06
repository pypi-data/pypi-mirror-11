function toggleFullScreenMode() {
    $('#portal-column-content').toggleClass('fullscreen')
    $('#portal-column-one, #portal-column-two, #sidepanel').toggleClass('hidden')
}


$(document).ready(function() {

    // ====== ANFANG

    // switch editbar-container  --------------------
	var editbar_container_state;

	if(typeof jQuery.jStorage == 'object') {
	    editbar_container_state = jQuery.jStorage.get("editbar-container-state")
    } else {
        editbar_container_state = false;
    }
    console.info( editbar_container_state )
    if (editbar_container_state == 'hidden') {
        $('#editbar-container').addClass('hide')
    }

    $('#editbar-container-switch').click( function() {
        $('#editbar-container').toggleClass('hide')
        //console.info( jQuery.jStorage.get("editbar-container-state")  )
        if (editbar_container_state == 'hidden') {
		    jQuery.jStorage.set("editbar-container-state", "visible");
        } else {
		    jQuery.jStorage.set("editbar-container-state", "hidden");
        }
    }) 
    // /switch editbar-container -------------------

    // h1 to breadcrump
    var bc = $('.documentFirstHeading.breadcrumb').text()
    $('#site-breadcrumbs').append( '<span id="h1-breadcrumnb">' +   bc + '</span>'  )
    $('.documentFirstHeading.breadcrumb').detach()


    // hide default edit bar
    $('.column-wrapper #edit-bar').remove()

    $('#edit-bar > ul.contentViews > li > a').hover( function () {
        $(this).find('div.text').fadeToggle(200)
    })


    if ( $('#editbar-container').length > 0 &&  $("#editbar-container").html().length < 2   ) {
        $("#editbar-container").detach()
    }

    // HIDE PLONE SPINNER
    $('#ajax-spinner, #ajax-spinner img').css({
        'opacity': 0,
        'filter': 'alpha(opacity=0)',
        '-ms-filter': 'progid:DXImageTransform.Microsoft.Alpha(opacity=0)'
    });

    // --- storage ---------
    //var ityou = window.ITYOU;
    //ityou.storage.get('', true)

    // -------------------------------------------------------------------------
    // -------------------------------------------------------------------------
    // initialize ITYOU JavaScript plugins
	/*var ITYOU = window.ITYOU;
	$(this).ITYOU({
	    // ITYOU Object Settings
	    ajax: {
			//callback: '?callback=?',
			callback: '',
			spinnerClass: 'content-spinner',
			timeout: 5000
	    }
	}, {
		backtotop: {
			min: 50
		},
		mapping: {
			container: $('#content'),
			tmplPath: '++theme++esi_theme/jesi-tmpl/',
			templates: [
			    //'activity-stream'
			]
		}
	});*/
	// -------------------------------------------------------------------------
	// -------------------------------------------------------------------------
	
	
    // --- /storage ---------
	

    // --- topnavi ----------------------------
    $('#portaltab-events').remove()
    $('#portaltab-Members').remove()
    // text durch symbole ersetzen
    /*
    $('#portaltab-web > a').attr('class','fa fa-globe').html('')
    $('#portaltab-dokumente > a').attr('class','fa fa-files-o').html('')
    $('#portaltab-wiki > a').attr('class','fa fa-wiki').html('')
    $('#portaltab-blog > a').attr('class','fa fa-book').html('')
    */
    // --- /topnavi ----------------------------


	// --- sidepanel -----------
	var sidepanel_state;
	
	
	if(typeof jQuery.jStorage == 'object') {
	    sidepanel_state = jQuery.jStorage.get("sidepanel-state")
    } else {
        sidepanel_state = 'small';
    }
	if (sidepanel_state == 'large') {
		$('.column-sidepanel, .content-wrapper')
		.removeClass('small-panel')
		.find('i.pfeil')
		.addClass('fa-arrow-circle-left')		
	} else {
		$('.column-sidepanel, .content-wrapper')
				.addClass('small-panel')
				.find('i.pfeil')
				.addClass('fa-arrow-circle-right')
	}
	$('#sidepanel-switch').click( function(e) {
		e.preventDefault()
		$('.column-sidepanel, .content-wrapper')
				.toggleClass('small-panel')
				.find('i.pfeil')
				.toggleClass('fa-arrow-circle-right')
            /* ZUSTAND ABSPEICHERN AUSGESCHALTET */
			jQuery.jStorage.set("sidepanel-state", "small");
            
			if (sidepanel_state == 'small') {
				jQuery.jStorage.set("sidepanel-state", "large");
			} else {
				jQuery.jStorage.set("sidepanel-state", "small");
			}
            
	})
	// --- icon auch anklickbar machen 
	$('#sidemenu > li').each(function(){
		var icon = $(this).find('i')
		$(this).find('a').prepend( icon )
	})

    // --- links aus JESI-PARAMS lesen und setzen ---
    //$('.profile-url').attr('href','authorxxx')
    // --- /links aus JESI-PARAMS lesen und setzen ---

    var portal_url = $('#ESI_DATA').attr('data-ityou-portal-url')
    var imessage_url = $('#ESI_DATA').attr('data-ityou-imessage-url')
    var profile_url = $('#ESI_DATA').attr('data-ityou-profile-url')
    var homefolder_url = $('#ESI_DATA').attr('data-ityou-homefolder-url')
    var dashboard_url = $('#ESI_DATA').attr('data-ityou-dashboard-url')
    //var events_url = $('#ESI_DATA').attr('data-ityou-events-url')
    //var members_url = $('#ESI_DATA').attr('data-ityou-members-url')

    $('#sidepanel-home').attr({'href': portal_url })
    $('#sidepanel-imessage').attr({'href': imessage_url })
    $('#sidepanel-myprofile').attr({'href': profile_url })
    $('#sidepanel-dashboard').attr({'href': dashboard_url })
    $('#sidepanel-mystuff').attr({'href': homefolder_url })
    //$('#sidepanel-events').attr({'href': events_url })
    //$('#sidepanel-Members').attr({'href': members_url })

	// --- /sidepanel --------------
	
    // --- navigation fuer bootstrap vorbereiten ---
    $('#site-globalnav > li > ul.submenu')
        .addClass('dropdown-menu')
        .parent().addClass('dropdown')
        
    $('#site-globalnav > li > ul.submenu > li  ul.submenu')
        .addClass('dropdown-menu')
        .parent().addClass('dropdown-submenu')
        

    $('li.dropdown > a').each( function() {
        $(this).addClass('dropdown-toggle')
        .attr('data-toggle','dropdown')
        .html($(this).text() + ' <b class="caret"></b>')
    })

    $('li.dropdown > a > ul > li > a').each( function() {
        $(this)
        .attr('data-toggle','dropdown')
        .html($(this).text() + ' <b class="caret"></b>')
    })

//    $('.dropdown-toggle').html()
//        .html($(this).html() + ' <b class="caret"></b>')
    // --- /navigation fuer bootstrap vorbereiten ---


    // --- buttons ----
    $('input.standalone').addClass('btn-primary')
    // --- /buttons ---
    
    
    
    
    
    // QR Code Portlet ausblenden wenn kein Inhalt vorhanden
    if($('.portlet.portlet-qrcode').length > 0) {
        var $portletQrcode = $('.portlet.portlet-qrcode');
    
        if($('.portletItem.qrcode').find('img').length === 0) {
            $portletQrcode.hide();
        }
    }
   
    $('.portalMessage').click( function(e) {
        e.preventDefault()
        $(this).fadeOut(400)
    })
 

    // ====== ENDE
});
