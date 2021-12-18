import logging
import os.path
import sys
import unittest

from main.utils.parser import AO3Parser

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)


class TestApi(unittest.TestCase):
    resources_path = os.path.join(sys.path[0], 'resources')

    def setUp(self) -> None:
        self.parser = AO3Parser()

    def test_parse_works(self):
        logger.info('Testing method parse_works')
        with open(os.path.join(self.resources_path, 'works.html'), 'r', encoding='utf-8') as f:
            content = f.read()
        works = self.parser.parse_works(content)
        self.assertIsInstance(works, dict)
        self.assertEqual(len(works.keys()), 19)

    def test_parse_index(self):
        logger.info('Testing method parse_index')
        with open(os.path.join(self.resources_path, 'index.html'), 'r', encoding='utf-8') as f:
            content = f.read()
        chapters = self.parser.parse_index(content)
        self.assertIsInstance(chapters, dict)
        self.assertEqual(len(chapters.keys()), 6)

    def test_parse_chapter(self):
        logger.info('Testing method parse_chapter')
        with open(os.path.join(self.resources_path, 'chapter.html'), 'r', encoding='utf-8') as f:
            content = f.read()
        chapter = self.parser.parse_chapter(content)
        self.assertIsInstance(chapter, dict)
        self.assertEqual(len(chapter.keys()), 3)


if __name__ == '__main__':
    unittest.main()
