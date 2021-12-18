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
            self.api.get_work_index(None)
            self.assertEqual(cm.output, ['ERROR:utils.decorators:<Func: get_work_index>: work_id is None!'])

    def test_get_user_works(self):
        content = self.api.get_user_works('guipaoding')
        self.assertIn('html', content)


if __name__ == '__main__':
    unittest.main()
