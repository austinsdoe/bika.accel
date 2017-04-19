from zope.component import adapts
from zope.interface import implements
from Products.Archetypes.public import DisplayList
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from Products.Archetypes.atapi import StringWidget
from bika.health.interfaces import IPatient
from bika.accel import bikaMessageFactory as _
from bika.accel.interfaces import IBikaAccel
from bika.accel.extenders import ExtRecordsField
from bika.lims.browser.widgets import RecordsWidget


class PatientSchemaModifier(object):
    adapts(IPatient)
    implements(ISchemaModifier, IBrowserLayerAwareExtender)
    layer = IBikaAccel

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        # Hidding not desired fields
        schema['Salutation'].widget.visible = {
                'edit': 'hidden',
                'view': 'hidden'
                }
        schema['Middlename'].widget.visible = {
                'edit': 'hidden',
                'view': 'hidden'
                }
        schema['Middleinitial'].widget.visible = {
                'edit': 'hidden',
                'view': 'hidden'
                }
        return schema
