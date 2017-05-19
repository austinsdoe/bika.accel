from bika.health.browser.analysisrequests.view import AnalysisRequestsView \
    as BaseView
from bika.lims import bikaMessageFactory as _


class AnalysisRequestsView(BaseView):
    def __init__(self, context, request):
        super(AnalysisRequestsView, self).__init__(context, request)
        self.columns['IDSRCode'] = {
                'title': _('IDSR Code'),
                'sortable': False, }

    def folderitems(self, full_objects=False):
        for rs in self.review_states:
            i = rs['columns'].index('BatchID') + 1
            rs['columns'].insert(i, 'IDSRCode')
        # Setting ip the patient catalog to be used in folderitem()
        # self.patient_catalog = getToolByName(
        #     self.context, CATALOG_PATIENT_LISTING)
        return super(AnalysisRequestsView, self).folderitems(
            full_objects=False)

    def folderitem(self, obj, item, index):
        item = super(AnalysisRequestsView, self)\
            .folderitem(obj, item, index)
        item['IDSRCode'] = ''
        return item
