# Generic field extensions
from archetypes.schemaextender.field import ExtensionField
from Products.Archetypes.public import StringField
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import ComputedField
from Products.Archetypes.public import ReferenceField
from Products.ATExtensions.ateapi import DateTimeField
from Products.ATExtensions.ateapi import RecordsField


class ExtStringField(ExtensionField, StringField):
    "Field extender"

class ExtBooleanField(ExtensionField, BooleanField):
    "Field extender"

class ExtComputedField(ExtensionField, ComputedField):
    "Field extender"

class ExtDateTimeField(ExtensionField, DateTimeField):
    "Field extender"

class ExtReferenceField(ExtensionField, ReferenceField):
    "Field extender"

class ExtRecordsField(ExtensionField, RecordsField):
    "Field extender"
