# make this a module

from zope.interface import implementer, provider
from collective.transmogrifier.interfaces import (
    ISectionBlueprint, ISection)


@provider(ISectionBlueprint)
@implementer(ISection)
class Store(object):

    def __init__(self, transmogrifier, name, options, previous):
        """missing docstring."""
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context

        # keys for sections further down the chain
        self.key = options.get('key', '').strip()
        if not hasattr(self.context, 'items'):
            self.context.items = []

    def __iter__(self):
        """missing docstring."""        # exhaust previous iterator
        for item in self.previous:
            self.context.items.append(item.get(self.key, None))
            yield item
