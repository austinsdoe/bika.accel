"""Archetypes widgets have a .visible property.
By default it may be True or False, or it may contain a dictionary:
            visible={'edit': 'visible',
                     'view': 'visible'}
Values may be 'visible', 'invisible', or 'hidden' depending on how we want
the widget to display in different modes.
The adapters in WidgetVisibility extend the possibilities of this variable.
To define rules for showing/hiding fields at runtime, this is the best way.
For simpler field visibility configuration examine extenders/analysisrequest.py
where the widget.visible flag is used to control adapters in bika.lims.
"""
from bika.lims.interfaces import IATWidgetVisibility
from zope.interface import implements


class AnalysisRequestFieldsVisibility(object):
    """Forces a set of AnalysisRequest fields to be invisible.
    """
    implements(IATWidgetVisibility)

    def __init__(self, context):
        self.context = context
        self.sort = 10

    def __call__(self, context, mode, field, default):
        hidden_fields = ['SamplingRound',
                         'SubGroup',
                         'EnvironmentalConditions',
                         'AdHoc',
                         'Composite',
                         'ReportDryMatter',
                         'InvoiceExclude']
        state = default if default else 'hidden'
        fieldName = field.getName()
        if fieldName in hidden_fields:
            return 'invisible'
        return state


class PatientFieldsVisibility(object):
    """Forces a set of Patient fields to be invisible.
    """
    implements(IATWidgetVisibility)

    def __init__(self, context):
        self.context = context
        self.sort = 10

    def __call__(self, context, mode, field, default):
        hidden_fields = ['TravelHistory', ]
        state = default if default else 'hidden'
        fieldName = field.getName()
        if fieldName in hidden_fields:
            return 'invisible'
        return state
