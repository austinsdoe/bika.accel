window.bika = window.bika || { lims: {}, health: {} };
window.bika.accel={};
window.jarn.i18n.loadCatalog("bika.accel");
var _s = window.jarn.i18n.MessageFactory("bika.accel");

/**
 * Dictionary of JS objects to be loaded at runtime.
 * The key is the DOM element to look for in the current page. The
 * values are the JS objects to be loaded if a match is found in the
 * page for the specified key. The loader initializes the JS objects
 * following the order of the dictionary.
 */
window.bika.accel.controllers =  {
    "body":
        ['AccelSiteView'],
    ".template-ar_add.portaltype-analysisrequest":
        ['AccelAddForm'],
    ".portaltype-client.template-base_edit":
        ['ClientEditForm'],
};

window.bika.accel.initialized = false;

/**
 * Initializes all bika.accel js stuff
 */
window.bika.accel.initialize = function() {
    "use strict";
    if (bika.health.initialized === true) {
        window.bika.lims.controllers = $.extend(window.bika.lims.controllers, window.bika.accel.controllers);
        // We need to force bika.lims.loader to load the bika.health controllers.
        var len = window.bika.lims.initview();
        window.bika.accel.initialized = true;
        return len;
    }
    // We should wait after bika.lims & health being initialized (500+500)
    setTimeout(function() {
        return window.bika.accel.initialize();
    }, 1000);
};

(function( $ ) {
$(document).ready(function(){
    "use strict";
    // Initializes bika.accel
    var length = window.bika.accel.initialize();

});
}(jQuery));
