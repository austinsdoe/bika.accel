""" Bika setup handlers. """

from Products.CMFCore.utils import getToolByName
from bika.accel import logger
from bika.lims.catalog import CATALOG_ANALYSIS_REQUEST_LISTING


class Empty:
    pass


class BikaAccelGenerator:
    def setupCatalogs(self, portal):

        def addIndex(cat, *args):
            try:
                cat.addIndex(*args)
            except:
                logger.warning("Could not create index %s in catalog %s" %
                               (args, cat))

        def addColumn(cat, col):
            try:
                cat.addColumn(col)
            except:
                logger.warning("Could not create metadata %s in catalog %s" %
                               (col, cat))

        pc = getToolByName(portal, 'portal_catalog')

        # Add country/province/district for client navigation
        addColumn(pc, 'getCountry')
        addColumn(pc, 'getProvince')
        addColumn(pc, 'getDistrict')

        # Add IDSRCode to AR Listing Catalog
        arc = getToolByName(portal, CATALOG_ANALYSIS_REQUEST_LISTING)
        addIndex(arc, 'getIDSRCode', 'FieldIndex')
        addColumn(arc, 'getIDSRCode')


def setupAccelVarious(context):
    """ Setup Bika site structure """

    if context.readDataFile('bika.accel.txt') is None:
        return

    portal = context.getSite()

    gen = BikaAccelGenerator()
    gen.setupCatalogs(portal)
