from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from bika.accel import logger


def step(tool):
    portal = aq_parent(aq_inner(tool))
    setup = portal.portal_setup
    # reread jsregistry with the new data
    setup.runImportStepFromProfile('profile-bika.accel:default', 'jsregistry')
    setup.runImportStepFromProfile('profile-bika.accel:default', 'skins')
    setup.runImportStepFromProfile('profile-bika.lims:default', 'cssregistry')
    setup.runImportStepFromProfile('profile-bika.lims:default', 'typeinfo')
    # Adding colums and indexes if needed
    pc = getToolByName(portal, 'portal_catalog')
    # Add country/province/district for client navigation
    try:
        pc.addColumn('getCountry')
    except:
        logger.warning(
            "Could not create metadata getCountry in catalog portal_catalog")
    try:
        pc.addColumn('getProvince')
    except:
        logger.warning(
            "Could not create metadata getProvince in catalog portal_catalog")
    try:
        pc.addColumn('getDistrict')
    except:
        logger.warning(
            "Could not create metadata getDistrict in catalog portal_catalog")
    return True
