import logging
import unittest

from utils.api import AO3Api

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)


class TestApi(unittest.TestCase):
    def setUp(self) -> None:
        self.api = AO3Api(view_adult=True)

    def tearDown(self) -> None:
        self.api.close()

    def test_decorator_required_arguments(self):
        with self.assertLogs('utils.decorators', level='ERROR') as cm:
            self.api.get_index(None)
            self.assertEqual(cm.output, ['ERROR:utils.decorators:<Func: get_index>: work_id is None!'])

    def test_get_works(self):
        content = self.api.get_works('guipaoding')
        self.assertIn('guipaoding', content)

    def test_get_index(self):
        content = self.api.get_index('35618773')
        self.assertIn('白昼骑士', content)

    def test_get_chapter(self):
        content = self.api.get_chapter('35618773', '88801411')
        self.assertIn('白昼骑士 1-2', content)


if __name__ == '__main__':
    unittest.main()
