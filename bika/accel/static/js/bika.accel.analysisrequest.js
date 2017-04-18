/**
 * Controller class for Analysis Request Add form
 */
function AccelAddForm() {

    var that = this;
    that.load = function() {
        /** I have to hide "Commercial ID" here because it isn't possible to
            override an overrode class. The beast approach would be to override
            the folderitems() function from
            bika/lims/controlpanel/AnalysisServciesView/folderitems()
            obtaining its result and removing items[x]['ProtocolID'] before
            returning the items to bikalisting. But AnalysisServciesView is also
            overridden in health, so the quickest way to hide the column is
            using our loved JavaScript.
        */
        $('th#foldercontents-CommercialID-column').hide();
        $('td.CommercialID').hide();
    };
}
