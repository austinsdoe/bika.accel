from zope.component import adapts
from zope.interface import implements
from bika.lims.interfaces import IAnalysisRequest
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from bika.lims.interfaces import IBikaCatalogAnalysisRequestListing
from bika.lims.fields import *
from Products.Archetypes.Widget import StringWidget
from bika.lims import bikaMessageFactory as _
from plone.indexer.decorator import indexer


@indexer(IAnalysisRequest, IBikaCatalogAnalysisRequestListing)
def getIDSRCode(instance):
    value = instance.Schema()['IDSRCode'].get(instance)
    return value


class AnalysisRequestSchemaExtender(object):
    adapts(IAnalysisRequest)
    implements(IOrderableSchemaExtender)

    # This column will be set when AR is created via JSON API by Sync App
    # of ACCEL IDSR. IDSCR Code will contain Client ID and Case ID
    fields = [
        ExtStringField('IDSRCode', default=''),
        ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, schematas):
        return schematas
