from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from bika.accel import logger
from bika.lims.upgrade.utils import UpgradeUtils
from bika.lims.catalog import CATALOG_ANALYSIS_REQUEST_LISTING


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
    ut = UpgradeUtils(portal)
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

    # Add IDSRCode to AR Listing Catalog
    try:
        arc = getToolByName(portal, CATALOG_ANALYSIS_REQUEST_LISTING)
        ut.addIndex(arc, 'getIDSRCode', 'FieldIndex')
        ut.addColumn(arc, 'getIDSRCode')
    except:
        logger.warning("Could not add getIDSRCode to %s" %
                       CATALOG_ANALYSIS_REQUEST_LISTING)
    # Refresh affected catalogs
    ut.refreshCatalogs()
    return True
