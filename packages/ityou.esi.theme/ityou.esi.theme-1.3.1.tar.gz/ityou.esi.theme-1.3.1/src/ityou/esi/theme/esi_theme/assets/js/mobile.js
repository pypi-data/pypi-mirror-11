$(document).ready(function() {

    // ====== ANFANG


    // --- links aus JESI-PARAMS lesen und setzen ---
    //$('.profile-url').attr('href','authorxxx')
    // --- /links aus JESI-PARAMS lesen und setzen ---

    var portal_url = $('#ESI_DATA').attr('data-ityou-portal-url')
    var imessage_url = $('#ESI_DATA').attr('data-ityou-imessage-url')
    var profile_url = $('#ESI_DATA').attr('data-ityou-profile-url')
    var homefolder_url = $('#ESI_DATA').attr('data-ityou-homefolder-url')
    var dashboard_url = $('#ESI_DATA').attr('data-ityou-dashboard-url')
    var events_url = $('#ESI_DATA').attr('data-ityou-events-url')
    var members_url = $('#ESI_DATA').attr('data-ityou-members-url')

    $('#btn-help').attr({'href': portal_url })
    $('#btn-imessage').attr({'href': imessage_url })
    $('#btn-myprofile').attr({'href': profile_url })
    $('#btn-mystuff').attr({'href': homefolder_url })
    $('#btn-Members').attr({'href': members_url })


    // datatables paginate -> @MR: TODO
    //$('.paginate_disabled_previous').append('<i class="fa fa-caret-square-o-left"')
    //$('.paginate_disabled_next').append('<i class="fa fa-caret-square-o-right"')

    // change img with java -> @MR: wie kann ich dafür sorgen, dass Bilder, die später +ber ajax geladen werden
    // auch geändert werden?
    //$('.sender-portrait').each( function() {
    //    $(this).attr('src','./assets/img/asco/group_icon.png')        
    //})  
    //<img src="/++resource++ityou.esi.theme.img/group_icon.png" class="img-thumbnail sender-portrait" alt="Gaga">    

    // abmelden 
    //<a id="logout" href="/++theme++esi_theme/logout" alt="Abmelden">Abmelden</a>
    $('#logout').attr('href','/logout')
    // ====== ENDE
});
