/**
 * Translation Pattern
 * 
 * XYZ has to be the token from <html lang="[XYZ]">,
 * e.g.:
 * 		<html lang="de"> --> var lang_de
 * 		<html lang="fr"> --> var lang_fr
 * 		<html lang="en"> --> var lang_en
 * 
	var lang_XYZ = {
		// ActivityStream
		'comment'		: '',
		'save'			: '',
		'view_all'		: '',
		'last_activity'	: '',
		
		// Clipboard
		'clipboard_copy' : '',
		
		// ExtUserProfile
		'choose_image'		: '',
		'crop_image'		: '',
		'click_to_edit'		: '',
		'date_placeholder'	: '',
		
		// ExtUserProfile DataTables
		'sProcessing'	: '',
		'sLengthMenu'	: '',
		'sZeroRecords'	: '',
	    'sInfo'			: '',
	    'sInfoEmpty'	: '',
	    'sInfoFiltered'	: '',
	    'sInfoPostFix'	: '',
	    'sSearch'		: '',
	    'sUrl'			: '',
	    'oPaginate' : {
		    'sFirst'	: '',
		    'sPrevious'	: '',
		    'sNext'		: '',
		    'sLast'		: ''
	    },
	    
        // ExtUserProfile PersonalToolbar
    	'ptProfileUrl'			   : '',
    	'ptHomefolderUrl'		   : '',
    	'ptImessageUrl'			   : '',
    	'ptDashboard'			   : '',
    	'pt@@personal-preferences' : '',
    	'ptLogout'				   : '',
    
	    // Guided Tour
	    'gtBack' : '',
	    'gtNext' : '',
	    'gtEnd'  : '',
	    
	    // Sidepanel
	    'sidepanel-home'      : '',
	    'sidepanel-imessages' : '',
	    'sidepanel-myprofile' : '',
	    'sidepanel-events'	  : '',
	    'sidepanel-members'	  : '',
	    
	    // WhoIsOnline
	    'wioSendMsg'      : '',
	    'wioLastActivity' : ''
	};
 */


// GERMAN TRANSLATION
// ----------------------------------------------------------------------
var lang_de = {
	// ActivityStream
	'comment'		: 'kommentieren',
	'save'			: 'Speichern',
	'view_all'		: 'alle Kommentare anzeigen',
	'last_activity'	: 'Letzte Aktivität am',
	
	// Clipboard
	'clipboard_copy' : 'Text in die Zwischenablage kopiert.',
	
	// ExtUserProfile
	'choose_image'		: 'Bild zum Zuschneiden auswählen',
	'crop_image'		: 'Bild zuschneiden',
	'click_to_edit'		: 'Anklicken zum Bearbeiten',
	'date_placeholder'	: 'TT.MM.JJJJ',
	
	// ExtUserProfile DataTables
	'sProcessing'	: 'Bitte warten ...',
	'sLengthMenu'	: '_MENU_ Einträge anzeigen',
	'sZeroRecords'	: 'Keine Einträge vorhanden.',
    'sInfo'			: '_START_ bis _END_ von _TOTAL_ Einträgen',
    'sInfoEmpty'	: '0 bis 0 von 0 Einträgen',
    'sInfoFiltered'	: '(gefiltert von _MAX_  Einträgen)',
    'sInfoPostFix'	: '',
    'sSearch'		: 'Suchen',
    'sUrl'			: '',
    'oPaginate' : {
	    'sFirst'	: 'Erste',
	    'sPrevious'	: 'Zurück',
	    'sNext'		: 'Nächste',
	    'sLast'		: 'Letzte'
    },
    
    // ExtUserProfile PersonalToolbar
    'ptProfileUrl'			   : 'Mein Profil',
    'ptHomefolderUrl'		   : 'Mein Ordner',
    'ptImessageUrl'			   : 'neue Nachricht',
    'ptDashboard'			   : 'Persönliche Seite',
    'pt@@personal-preferences' : 'Meine Enistellungen',
    'ptLogout'				   : 'Abmelden',
    
    // Guided Tour
    'gtBack' : 'zurück',
    'gtNext' : 'weiter',
    'gtEnd'  : 'Beenden',
    
    // Guided Tour: Steps
    'activities' : {
    	'step_1' : {
    		'title'   : 'Persönliche Werkzeuge',
			'content' : 'Hier finden Sie Verweise zu Ihren wichtigsten Seiten (Profil etc.).'
    	},
    	'step_2' : {
    		'title'   : 'Persönliche Mitteilungen',
    		'content' : 'Erfahren Sie in Echtzeit sobald Ihnen jemanden eine neue Mitteilungen geschrieben hat.'
    	},
    	'step_3' : {
    		'title'   : 'Letzte Aktivitäten',
            'content' : 'Sobald jemand ein Dokument erstellt oder bearbeitet hat werden Sie in Echtzeit darüber informiert.'
    	},
    	'step_4' : {
    		'title'   : 'Neuen Inhalt bereitstellen',
    		'content' : 'Erstellen Sie mit geringstem Aufwand neuen Inhalt und teilen diesen bei Bedarf mit den anderen Benutzer.'
    	},
    	'step_5' : {
    		'title'   : 'Auswahl letzter Aktivitäten',
            'content' : 'Wechseln Sie zwischen den letzten Aktivitäten aller Benutzer oder denen Ihrer Favoriten.'
    	}
    },
    
    // Sidepanel
    'sidepanel-home'      : 'Start',
    'sidepanel-imessages' : 'Mitteilungen',
    'sidepanel-myprofile' : 'Mein Profil',
    'sidepanel-events'	  : 'Termine',
    'sidepanel-members'	  : 'Benutzer',
    
    // WhoIsOnline
    'wioSendMsg'      : 'Mitteilung versenden',
    'wioLastActivity' : 'Letzte Aktivität am'
};
//----------------------------------------------------------------------


// ENGLISH TRANSLATION
//----------------------------------------------------------------------
var lang_en = {
	// ActivityStream
	'comment'		: 'comment',
	'save'			: 'save',
	'view_all'		: 'show all comments',
	'last_activity'	: 'last activity:',
	
	// Clipboard
	'clipboard_copy' : 'Text copied to clipboard.',
	
	// ExtUserProfile
	'choose_image'		: 'choose image to crop',
	'crop_image'		: 'crop image',
	'click_to_edit'		: 'click to edit',
	'date_placeholder'	: 'DD.MM.YYYY',
	
	// ExtUserProfile DataTables
	'sProcessing'	: 'Processing ...',
	'sLengthMenu'	: 'Show _MENU_ entries',
	'sZeroRecords'	: 'No matching records found.',
    'sInfo'			: 'Showing _START_ to _END_ of _TOTAL_ entries',
    'sInfoEmpty'	: 'Showing 0 to 0 of 0 entries',
    'sInfoFiltered'	: '(filtered from _MAX_ total entries)',
    'sInfoPostFix'	: '',
    'sSearch'		: 'Search',
    'sUrl'			: '',
    'oPaginate' : {
	    'sFirst'	: 'First',
	    'sPrevious'	: 'Previous',
	    'sNext'		: 'Next',
	    'sLast'		: 'Last'
    },
    
    // ExtUserProfile PersonalToolbar
    'ptProfileUrl'			   : 'My Profile',
    'ptHomefolderUrl'		   : 'My Folder',
    'ptImessageUrl'			   : 'new Message',
    'ptDashboard'			   : 'Personal Dashboard',
    'pt@@personal-preferences' : 'My Preferences',
    'ptLogout'				   : 'Logout',
    
    // Guided Tour
    'gtBack' : 'back',
    'gtNext' : 'next',
    'gtEnd'  : 'end',
    
    // Guided Tour: Steps
    'activities' : {
    	'step_1' : {
    		'title'   : 'Personal Tools',
			'content' : 'You can find important links in here, e.g. to your profile.'
    	},
    	'step_2' : {
    		'title'   : 'Personal Messages',
			'content' : 'Experience in real-time when somebody sent you a new messages.'
    	},
    	'step_3' : {
    		'title'   : 'Recent Activities',
        	'content' : 'As soon somebody created or edited a document you will be informed in real-time.'
    	},
    	'step_4' : {
    		'title'   : 'Neuen Inhalt bereitstellen',
			'content' : 'Create with smallest effort new content and share it with your community as needed.'
    	},
    	'step_5' : {
    		'title'   : 'Select recent Activities',
            'content' : 'Exchange between recent activites of the community or your favourite users.'
    	}
    },
    
    // Sidepanel
    'sidepanel-home'      : 'Home',
    'sidepanel-imessages' : 'Messages',
    'sidepanel-myprofile' : 'My Profile',
    'sidepanel-events'	  : 'Events',
    'sidepanel-members'	  : 'Member',
    
    // WhoIsOnline
    'wioSendMsg'      : 'Send Message',
    'wioLastActivity' : 'Last Activity'
};
//----------------------------------------------------------------------
