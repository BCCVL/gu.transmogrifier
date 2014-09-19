import os
import os.path
import json
import logging
from zope.interface import implementer, provider
from collective.transmogrifier.interfaces import (
    ISectionBlueprint, ISection)
from collective.transmogrifier.utils import resolvePackageReferenceOrFile


LOG = logging.getLogger(__name__)


@provider(ISectionBlueprint)
@implementer(ISection)
class JSONSource(object):
    """reads json files from a given folder and passes these on into the
    transmogrifier pipeline

    The json filename will be used as id for the object to create.
    If there is a folder with the same name as the json file, all files within
    not ending in .json will be available in the _files dictionary on the item.

    All .json files in any of the subdirectories, will be loaded and
    passed into the pipeline as well.
    """

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        # TODO: try to get import contextpath if there is no path set
        self.path = resolvePackageReferenceOrFile(options['path'])
        if self.path is None or not os.path.isdir(self.path):
            raise Exception('Path ({}) does not exists.'.format(str(self.path)))
        self.path = self.path.rstrip(os.sep)

        self.enabled = options.get('enabled', "True").lower() in ("true", "1", "on", "yes")
        # add path prefix to imported content
        self.prefix = options.get('prefix', '').strip().strip(os.sep)
        # keys for sections further down the chain
        self.pathkey = options.get('path-key', '_path').strip()
        self.fileskey = options.get('files-key', '_files').strip()

    def __iter__(self):
        # exhaust previous iterator
        for item in self.previous:
            yield item

        if not self.enabled:
            return

        # start our own source
        # 1. iterate through dir files first
        for (root, dirs, files) in os.walk(self.path):
            for filename in files:
                if ((not filename.endswith('.json')
                     or filename.startswith('.'))):
                    # if it's not json it's not an item
                    # if it starts with . we don't want it
                    continue
                # read the json
                f = open(os.path.join(root, filename), 'r')
                # TODO: could put this into _files as well with 'content' key
                try:
                    item = json.loads(f.read())
                except ValueError as e:
                    LOG.error("couldn't parse item %s (%s)", filename, e)
                    # No point to move on
                    continue
                finally:
                    f.close()
                # TODO: need _type?
                # _path
                name, ext = os.path.splitext(filename)
                # TODO: so many split and joins, consider self.prefix as well
                path = root[len(self.path):].strip(os.sep)
                path = '/'.join((path, name))
                item[self.pathkey] = '/'.join(path.split(os.sep))
                # _files
                if name in dirs:
                    # matching dir for entry? then read all the files
                    # within it.
                    _files = item.setdefault(self.fileskey, {})
                    for _filename in os.listdir(os.path.join(root, name)):
                        if ((_filename.startswith('.') or
                             _filename.endswith('.json'))):
                            # TODO: figure out way to allow
                            # attachments with .json ignore . and
                            # .json in case item is a folder
                            continue
                        _absfilename = os.path.join(root, name, _filename)
                        if os.path.isdir(_absfilename):
                            # ignore dirs, in case we generated a folder
                            continue
                        # FIXME: if possible don't load file into ram
                        _files[_filename] = {
                            'name': _filename,
                            'data': open(_absfilename).read()
                            }
                yield item
