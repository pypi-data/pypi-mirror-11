/*
 * Pretty simple Cookie law plugin (not a real jQuery plugin)
 * 
 * Just load this file in your pages and use:
 * 
 *   Cookielaw.accept();
 * 
 * This will create a cookie to not display the banner anymore, then 
 * slide up the banner.
 */
var Cookielaw = {
    accept: function () {
        $.cookie('emencia_cookie_law', 'true', { expires: 10 * 365, path: '/' });

        jQuery('#cookie-law-container').slideUp();
    }
};