from zope.interface import implementer, provider
from collective.transmogrifier.interfaces import (
    ISectionBlueprint, ISection)
from collective.transmogrifier.utils import defaultMatcher
from plone.dexterity.utils import createContentInContainer


@provider(ISectionBlueprint)
@implementer(ISection)
class NameChoosingConstructor(object):
    """
    Constructs Dexterity content and lets INameChooser pick the id.
    """

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context
        self.typekey = defaultMatcher(options, 'type-key', name, 'type',
                                      ('portal_type', 'Type'))
        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')
        self.contextpathkey = defaultMatcher(options, 'contextpath-key',
                                             name, 'contextpath')

    def __iter__(self):
        for item in self.previous:
            keys = item.keys()
            typekey = self.typekey(*keys)[0]
            pathkey = self.pathkey(*keys)[0]
            contextpathkey = self.contextpathkey(*keys)[0]

            if not typekey:
                # wouldn't know what to construct'
                yield item
                continue

            type_ = item[typekey]

            if pathkey:
                # we have already an id, no need to choose a name
                yield item
                continue
            else:
                # we will generate a path later
                pathkey = '_path'

            context = self.context
            if contextpathkey:
                # if we have a contextpath use that one as contaier
                contextpath = item[contextpathkey]
                context = self.context.unrestrictedTraverse(contextpath)
                if context is None:
                    error = "Can't find Container {}".format(contextpath)
                    raise KeyError(error)

            # use title as hint for id if available
            # TODO: maybe try to set filename upfront, to use
            #       INameFromFilename if possible
            kws = {}
            if 'title' in item:
                kws['title'] = item['title']
            # works only for dexterity based types
            newob = createContentInContainer(context, type_, **kws)
            item[pathkey] = newob.id
            yield item
