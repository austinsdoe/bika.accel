from Products.CMFCore.utils import getToolByName
from bika.health.browser.patient.chronicconditions import ChronicConditionsView as CCV
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bika.accel import bikaMessageFactory as _
from bika.lims import PMF as _p
from bika.health.browser.patient.treatmenthistory import TreatmentHistoryView as HealthTHV


class ChronicConditionsView(CCV):
    template = ViewPageTemplateFile("templates/chronicconditions.pt")

    def __call__(self):
        if 'submitted' in self.request:
            self.context.setChronicConditions(self.request.form.get('ChronicConditions', ()))
            self.context.plone_utils.addPortalMessage(_p("Changes saved"))
        return self.template()
