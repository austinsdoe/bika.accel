from bika.lims.interfaces import IIdServer
from zope.interface import implements
from bika.lims.locales import COUNTRIES, STATES
from Products.CMFCore.utils import getToolByName
import re


class IDGenerator(object):
    """
    This class can be used to generate specific IDs for some content types by
    adding adapters. In LIMS, in case content type has an adapter providing
    IIdServer, it calls generate_id method from that adapter.
    """
    implements(IIdServer)

    def __init__(self, context):
        # Each adapter takes the object itself as the construction
        # parameter and possibly provides other parameters for the
        # interface adaption
        self.context = context

    def generate_id(self, portal_type, batch_size=None):
        """
        Generates unique ID for object.
        In ACCEL Project, ID formats for each conent type that must be
        overriden are shown below:

        Client- <country_code> + <province_code> + <cleint_name_abbreviation>
                E.g: LR33TAPE (Tapeta, from Nimba, Liberia)

        AnalysisRequest- <client_id> + <next_available_number>
                E.g: LR33TAPE001 (first Case registered in Tapeta, Nimba)
        """
        result = ''
        if portal_type == 'Client':
            c_code, p_code = self.getCountryAndProvince()
            name = self.context.getName()
            if len(name) > 3:
                name = name[:4]
            result += c_code+p_code+name
        elif portal_type == 'AnalysisRequest':
            client_id = self.context.getClient().getId()
            result += client_id + self.next_number(client_id).zfill(3)
        return result.upper()

    def next_number(self, prefix):
        """
        Finds next available number, by checking IDs starting by prefix .
        :param prefix: Prefix to search in IDs
        :type prefix: string
        """
        # normalize before anything
        plone = self.context.portal_url.getPortalObject()
        # grab the first catalog we are indexed in.
        at = getToolByName(plone, 'archetype_tool')
        if self.context.portal_type in at.catalog_map:
            catalog_name = at.catalog_map[self.context.portal_type][0]
        else:
            catalog_name = 'portal_catalog'
        catalog = getToolByName(plone, catalog_name)

        # get all IDS that start with prefix
        # this must specifically exclude AR IDs (two -'s)
        rr = re.compile("^"+prefix+"[\d+]+$")
        ids = [int(i.split(prefix)[1]) \
               for i in catalog.Indexes['id'].uniqueValues() \
               if rr.match(i)]
        ids.sort()
        _id = ids and ids[-1] or 0
        new_id = _id + 1
        return str(new_id)

    def getCountryAndProvince(self):
        country = ''
        province = '00'
        for country in COUNTRIES:
            if country['Country'] == self.context.getCountry():
                country = country['ISO']
                break
        for state in STATES:
            if state[0] == country and state[2] == self.context.getProvince():
                province = state[1]
                break
        return country, province
