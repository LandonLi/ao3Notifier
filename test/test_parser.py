import json
import logging
import os.path
import sys
import unittest
from datetime import datetime

from main.utils.parser import AO3Parser

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def check_items(case: unittest.TestCase, item: dict, check: dict):
    case.assertIsInstance(item, dict)
    case.assertEqual(item.keys(), check.keys())
    for key, _type in check.items():
        case.assertEqual(type(item.get(key)), eval(_type))


class TestApi(unittest.TestCase):
    resources_path = os.path.join(sys.path[0], 'resources')

    def setUp(self) -> None:
        self.parser = AO3Parser()
        datetime.now()  # avoid removing import

    def test_parse_works(self):
        logger.info('Testing method parse_works')

        with open(os.path.join(self.resources_path, 'works.html'), 'r', encoding='utf-8') as f:
            content = f.read()
        works = self.parser.parse_works(content)

        with open(os.path.join(self.resources_path, 'verify', 'works.json'), 'r', encoding='utf-8') as f:
            check = json.load(f)
        for work in works.values():
            check_items(self, work, check)

    def test_parse_index(self):
        logger.info('Testing method parse_index')

        with open(os.path.join(self.resources_path, 'index.html'), 'r', encoding='utf-8') as f:
            content = f.read()
        chapters = self.parser.parse_index(content)

        with open(os.path.join(self.resources_path, 'verify', 'index.json'), 'r', encoding='utf-8') as f:
            check = json.load(f)
        for chapter in chapters.values():
            check_items(self, chapter, check)

    def test_parse_chapter(self):
        logger.info('Testing method parse_chapter')

        with open(os.path.join(self.resources_path, 'chapter.html'), 'r', encoding='utf-8') as f:
            content = f.read()
        chapter = self.parser.parse_chapter(content)

        with open(os.path.join(self.resources_path, 'verify', 'chapter.json'), 'r', encoding='utf-8') as f:
            check = json.load(f)
        check_items(self, chapter, check)


if __name__ == '__main__':
    unittest.main()
