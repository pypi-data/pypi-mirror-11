$(document).ready(function() {
    var reveal_url = 'jq_reveal_email'
    if (typeof(portal_url) != 'undefined') {
	reveal_url = portal_url + '/' + reveal_url;
    }
    $('a.hidden-email').each(function() {
        $.pyproxy_call(reveal_url, {'uid': $(this).attr('rel')});
    });
});
