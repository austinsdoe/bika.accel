from Products.CMFCore.utils import getToolByName
from bika.health.browser.analysisrequest.publish import \
    AnalysisRequestPublishView as _AnalysisRequestPublishView
from bika.health import bikaMessageFactory as _h
from bika.lims import bikaMessageFactory as _


class AnalysisRequestPublishView(_AnalysisRequestPublishView):

    def __call__(self):
        return super(AnalysisRequestPublishView, self).__call__()

    def _analyses_data(self, ar, analysis_states=['verified', 'published']):
        analyses = []
        dm = ar.aq_parent.getDecimalMark()
        batch = ar.getBatch()
        workflow = getToolByName(self.context, 'portal_workflow')
        showhidden = self.isHiddenAnalysesVisible()
        for an in ar.getAnalyses(full_objects=True,
                                 review_state=analysis_states,
                                 get_reflexed=False):
            # Omit hidden analyses?
            if not showhidden:
                serv = an.getService()
                asets = ar.getAnalysisServiceSettings(serv.UID())
                if asets.get('hidden'):
                    # Hide analysis
                    continue

            # Build the analysis-specific dict
            andict = self._analysis_data(an, dm)

            # Are there previous results for the same AS and batch?
            andict['previous'] = []
            andict['previous_results'] = ""
            if batch:
                keyword = an.getKeyword()
                bars = [bar for bar in batch.getAnalysisRequests() \
                            if an.aq_parent.UID() != bar.UID() \
                            and keyword in bar]
                for bar in bars:
                    pan = bar[keyword]
                    pan_state = workflow.getInfoFor(pan, 'review_state')
                    if pan.getResult() and pan_state in analysis_states:
                        pandict = self._analysis_data(pan)
                        andict['previous'].append(pandict)

                andict['previous'] = sorted(andict['previous'], key=itemgetter("capture_date"))
                andict['previous_results'] = ", ".join([p['formatted_result'] for p in andict['previous'][-5:]])

            analyses.append(andict)
        return analyses
