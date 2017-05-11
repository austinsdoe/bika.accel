from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.interfaces import IClient
from bika.accel.interfaces import IBikaAccel
from bika.lims.browser.widgets import AddressWidget
from archetypes.schemaextender.interfaces import ISchemaExtender
from bika.lims import PMF, bikaMessageFactory as _
from archetypes.schemaextender.field import ExtensionField
from Products.ATExtensions.ateapi import AddressField


class ClientSchemaExtender(object):
    """
    Tried to extend PhysicalAddress using SchemaExtender too, but it seemed
    only widget changes were applied here...
    """
    adapts(IClient)
    implements(ISchemaExtender)

    fields = [
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


class ClientSchemaModifier(object):
    """
    Tried to modify Schema but validator of PhysicalAddress field didn't work,
    where required attribute changes. Validator of Lims's Client Schema was
    not called as well. So it is an interesting point here.
    """
    adapts(IClient)
    implements(ISchemaModifier)
    layer = IBikaAccel

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        # PhysicalAddress is required in order to generate Client ID with
        # Province and District codes
        schema['PhysicalAddress'].required = 0
        schema['PhysicalAddress'].inline_field_validator = "_validate_address"
        return schema

    def _validate_address(self, request, field, data):
        """ Validates the Physical Address Fields
        Province and district fields are required to generate Client ID.
        :returns: (str) message if validation fails, otherwise (bool) True
        """
        country = data.get("country", None)
        province = data.get("state", None)
        district = data.get("district", None)
        if country == "Liberia" and not all([province, district]):
            return "Province and district fields are mandatory"
        return True


class ExtAddressField(ExtensionField, AddressField):
    """
    It has to be under bika.accel.browser.fields module (__init__.py)
    """
    "Field extender"
