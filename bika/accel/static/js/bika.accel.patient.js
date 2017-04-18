/**
 * Controller class for patient content creation/edition
 */
function AccelPatientForm() {

    var that = this;
    that.load = function() {
        // These are not meant to show up in the main patient base_edit form.
        // they are flagged 'visible' though, so they do show up when requested.
        $('.template-base_edit #archetypes-fieldname-LastTest').hide();
        $('.template-base_edit #archetypes-fieldname-LastResults').hide();

    }
}
