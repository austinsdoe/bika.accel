/**
 * Controller class for all site views
 */
function AccelSiteView() {
    // Geting the doRedirect cookie and obtains the url to redirect
    var that = this;
    that.load = function() {
        var url = readCookie('doRedirect');
        if (url){
            // The page shown before being redirected is not going to be displayed
            $('body').hide();
            // Deleting doRedirect cookie
            document.cookie = "doRedirect=; expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;";
            // Redirecting to case cration page
            window.location.replace(url.replace(/"/g,''));
        }
    }
}
