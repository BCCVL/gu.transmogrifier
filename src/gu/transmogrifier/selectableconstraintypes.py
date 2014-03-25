from zope.interface import implementer, provider
from collective.transmogrifier.interfaces import (
    ISectionBlueprint, ISection)
from collective.transmogrifier.utils import defaultMatcher
from plone.app.dexterity.behaviors import constrains
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes


@provider(ISectionBlueprint)
@implementer(ISection)
class SelectableConstrainTypes(object):
    """Configure ISelectableConstrainTypes on content objects.
    """

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context

        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')
        self.constrainkey = defaultMatcher(options, 'constraintypes-key', name,
                                           'constraintypes')

    def __iter__(self):
        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]
            constrainkey = self.constrainkey(*item.keys())[0]

            if not pathkey or not constrainkey or \
               constrainkey not in item:    # not enough info
                yield item
                continue

            obj = self.context.unrestrictedTraverse(item[pathkey].lstrip('/'),
                                                    None)
            if obj is None:  # path doesn't exist
                yield item
                continue

            constr = ISelectableConstrainTypes(obj, None)
            if constr is not None:
                constrain_dict = item[constrainkey]
                mode = constrain_dict['mode']
                allowedtypes = constrain_dict['locallyallowedtypes']
                addabletypes = constrain_dict['immediatelyaddabletypes']
                if mode not in (constrains.ACQUIRE, constrains.DISABLED,
                                constrains.ENABLED):
                    # mode not valid [-1, 0, 1]
                    yield item
                    continue
                constr.setConstrainTypesMode(mode)
                if allowedtypes:
                    constr.setLocallyAllowedTypes(allowedtypes)
                if addabletypes:
                    constr.setImmediatelyAddableTypes(addabletypes)

            yield item
