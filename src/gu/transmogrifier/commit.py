import transaction
from zope.interface import implementer, provider
from collective.transmogrifier.interfaces import (
    ISectionBlueprint, ISection)


@provider(ISectionBlueprint)
@implementer(ISection)
class Commit(object):

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.every = int(options.get('every', 0))

    def __iter__(self):
        count = 1
        for item in self.previous:
            yield item
            if self.every and count % self.every == 0:
                transaction.commit()
            count += 1
