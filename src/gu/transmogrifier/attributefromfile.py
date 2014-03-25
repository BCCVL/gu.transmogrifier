from zope.interface import implementer, provider
from collective.transmogrifier.interfaces import (
    ISectionBlueprint, ISection)


@provider(ISectionBlueprint)
@implementer(ISection)
class AttributeFromFile(object):
    """use content of _files as attribute value.

    looks for _fileattributes: ["attr1","attr2",...]  if item["attr1"]
    is a dict with a key filename and filename exists in _files dict
    it will put the content into item["attr1"]
    """

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context

        # keys for sections further down the chain
        self.fileskey = options.get('files-key', '_files').strip()
        self.attributeskey = options.get('fileattributes-key',
                                         '_fileattributes').strip()

    def __iter__(self):
        # exhaust previous iterator
        for item in self.previous:
            attributes = item.get(self.attributeskey)
            # no fileattributes .. can't do anything
            if not attributes:
                yield item
                continue

            # replace attributes
            for attr in attributes:
                files = item.setdefault(self.fileskey, {})
                filename = item[attr].get('filename')
                file = files.get(filename)
                if not file:
                    continue
                item[attr] = file['data']
            yield item
