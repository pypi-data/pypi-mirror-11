# -*- coding: utf-8 -*-
from plone.rest.interfaces import IAPIRequest
from plone.rest.events import mark_as_api_request
from plone.dexterity.content import DexterityContent
from Products.CMFPlone.Portal import PloneSite
from zope.component.interfaces import ComponentLookupError
from zope.event import notify
from zope.traversing.interfaces import BeforeTraverseEvent


def PloneSite__before_publishing_traverse__(self, arg1, arg2=None):
    """Pre-traversal hook that stops traversal to prevent the default view
       to be appended. Appending the default view will break REST calls.
    """
    REQUEST = arg2 or arg1

    goon = True

    if IAPIRequest.providedBy(REQUEST):
        goon = False

    if goon and REQUEST.getHeader('Accept') == 'application/json':
        mark_as_api_request(REQUEST)
        goon = False

    if not goon:
        # Copied of CMFCore PortalObject
        try:
            notify(BeforeTraverseEvent(self, REQUEST))
        except ComponentLookupError:
            # allow ZMI access, even if the portal's site manager is missing
            pass
        return

    super(PloneSite, self).__before_publishing_traverse__(
        arg1, arg2)


def DexterityContent__before_publishing_traverse__(self, arg1, arg2=None):
        """Pre-traversal hook that stops traversal to prevent the default view
           to be appended. Appending the default view will break REST calls.
        """
        REQUEST = arg2 or arg1

        from plone.rest.interfaces import IAPIRequest
        if IAPIRequest.providedBy(REQUEST):
            # Copied of CMFCore PortalObject
            try:
                notify(BeforeTraverseEvent(self, REQUEST))
            except ComponentLookupError:
                # allow ZMI access, even if the portal's site manager is
                # missing
                pass
            return
        super(DexterityContent, self).__before_publishing_traverse__(
            arg1, arg2)


def ArchetypesContent__before_publishing_traverse__(self, arg1, arg2=None):
        """Pre-traversal hook that stops traversal to prevent the default view
           to be appended. Appending the default view will break REST calls.
        """
        REQUEST = arg2 or arg1

        from plone.rest.interfaces import IAPIRequest
        if IAPIRequest.providedBy(REQUEST):
            # Copied of CMFCore PortalObject
            try:
                notify(BeforeTraverseEvent(self, REQUEST))
            except ComponentLookupError:
                # allow ZMI access, even if the portal's site manager is
                # missing
                pass
            return

        super(DexterityContent, self).__before_publishing_traverse__(
            arg1, arg2)
