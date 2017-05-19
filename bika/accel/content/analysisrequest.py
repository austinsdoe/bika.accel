from zope.component import adapts
from zope.interface import implements
from bika.lims.interfaces import IAnalysisRequest
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender

from bika.lims.fields import *
from Products.Archetypes.Widget import StringWidget
from bika.lims import bikaMessageFactory as _


class AnalysisRequestSchemaExtender(object):
    adapts(IAnalysisRequest)
    implements(IOrderableSchemaExtender)

    fields = [
        ExtStringField('IDSRCode', default=''),
        ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, schematas):
        return schematas
