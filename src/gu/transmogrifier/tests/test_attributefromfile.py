import unittest

from collective.transmogrifier.transmogrifier import Transmogrifier

from gu.transmogrifier.attributefromfile import AttributeFromFile


class AttributeFromFileTest(unittest.TestCase):

    def _makeone(self, name='test', previous=(), **options):
        transmogrifier = Transmogrifier(object())
        return AttributeFromFile(transmogrifier, name, options, previous)

    def test_one(self):

        step = self._makeone(
            previous=[{
                'attr1': {'filename': 'file1'},
                'attr2': {'filename': 'file2'},
                '_files': {
                    'file1': {'data': 'data1'},
                    'file2': {'data': 'data2'}
                },
                '_fileattributes': ['attr1', 'attr2']
            }]
        )
        item = next(iter(step))
        self.assertEqual(item['attr1'], 'data1')
        self.assertEqual(item['attr2'], 'data2')
