""" Bika setup handlers. """

from Products.CMFCore.utils import getToolByName
from bika.accel import logger


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

def setupAccelVarious(context):
    """ Setup Bika site structure """

    if context.readDataFile('bika.accel.txt') is None:
        return

    portal = context.getSite()

    gen = BikaAccelGenerator()
    gen.setupCatalogs(portal)
