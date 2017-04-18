# -*- coding: utf-8 -*-

import logging

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.component import getMultiAdapter

from plone.memoize.instance import memoize
from plone.app.portlets.portlets import navigation

from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder

logger = logging.getLogger("bika.accel.browser.portlets.navigation")


class Renderer(navigation.Renderer):
    """Navigation Tree Renderer which allows special handling of nodes

    Note: Inherited methods are `camelCase`, additional `snake_case`
    """

    _template = ViewPageTemplateFile('navigation.pt')
    recurse = ViewPageTemplateFile('navigation_recurse.pt')

    def __init__(self, context, request, view, manager, data):
        navigation.Renderer.__init__(self, context, request, view, manager, data)
        logger.info("BIKA ACCEL Navigation Renderer initialize")

    def get_children(self, tree=dict()):
        """Return the children of the current tree

        :returns: List of child nodes
        :rtype: List
        """
        return tree.get("children", [])

    def find_node_by_id(self, id, tree):
        """Searches the children of the given tree and finds a node by id

        :returns: Index of the found node
        :rtype: Integer
        """
        # tree structure built by `plone.app.layout.navigation.navtree.buildFolderTree`
        children = self.get_children(tree)

        # no nodes in tree, nothing to do
        if not children:
            return -1

        # find the node by the provided id
        for n, node in enumerate(children):
            if node.get("id") == id:
                return n

        return -1

    def prepare_client_folder_navigation(self, tree):
        """Mark the `ClientFolder` node of the navigation tree to allow client
        subnavigation categorized by province/districts

        :returns: Navigation tree
        :rtype: list
        """

        # context should be in this case the `ClientsFolder` itself
        context = aq_inner(self.context)

        # Find the right node in the tree
        node_index = self.find_node_by_id(context.getId(), tree)

        # nothing found -> fail gracefully ()
        if node_index < 0:
            logger.error("Could not find id `%s` node in tree", context.getId())
            return tree

        children = self.get_children(tree)
        node = children[node_index]

        if node.get("children"):
            # stop if existing nodes are already rendered
            # -> happens if `Client` portal types are checked in the Plone
            #    navigation settings
            logger.warning("Client nodes detected, skipping province/district navigation")
            return tree

        # mark the node so that the template can render the categorized nodes
        node["is_client_folder"] = True
        return tree

    def find_clients(self, client_type="Client", depth=1):
        """Scoped search for `Client` objects within the current context
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, "portal_catalog")

        # build the catalog query
        query = {}
        path = "/".join(context.getPhysicalPath())
        query["path"] = {"query": path, "depth": depth}
        query["portal_type"] = client_type

        return catalog(query)

    @memoize
    def build_client_navigation_structure(self):
        """build a client structure
        """
        context = aq_inner(self.context)
        strategy = getMultiAdapter((context, self.data), INavtreeStrategy)

        structure = {}

        for brain in self.find_clients():

            # fetch the needed address parts to build the structure
            country = brain.getCountry or "No Country"
            province = brain.getProvince or "No Province"
            district = brain.getDistrict or "No District"

            # We can assume here, that the country/province/district
            # information is valid, as only valid selections can be made
            # through the address widget in the form.
            if structure.get(country) is None:
                structure[country] = {}
            if structure[country].get(province) is None:
                structure[country][province] = {}
            if structure[country][province].get(district) is None:
                structure[country][province][district] = []

            # build an item and decorate it for the navigation tree
            client_location = "/".join([country, province, district])
            new_item = {
                "item": brain,
                "client_location": client_location,
            }
            item = strategy.decoratorFactory(new_item)

            # create node and append it to the structure
            structure[country][province][district].append(item)

        return structure

    @memoize
    def getNavTree(self, _marker=None):
        if _marker is None:
            _marker = []
        context = aq_inner(self.context)
        queryBuilder = getMultiAdapter((context, self.data), INavigationQueryBuilder)
        strategy = getMultiAdapter((context, self.data), INavtreeStrategy)
        tree = buildFolderTree(context, obj=context, query=queryBuilder(), strategy=strategy)

        # User clicked on a `ClientFolder` in the navigation tree
        if context.portal_type == "ClientFolder":
            logger.debug("Client Folder detected -> prepare subnavigation")
            # mark the node for the "recurse" template
            return self.prepare_client_folder_navigation(tree)

        return tree
