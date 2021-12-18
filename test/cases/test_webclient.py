import logging
import typing
import unittest

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def call_do_get(url, session=None, need_json=False) -> typing.Union[str, dict]:
    from utils.webclient import do_get
    result = do_get(url, exist_session=session, need_json=need_json)
    return result


def parse_response_json(case: unittest.TestCase, content: dict, check_items: dict):
    import json
    logger.debug('json content')
    logger.debug(json.dumps(content, indent=2, ensure_ascii=False))
    # check content is dict
    case.assertIsInstance(content, dict)
    # check all items
    for key, value in check_items.items():
        case.assertEqual(content.get(key), value)


class TestWebClient(unittest.TestCase):
    url_get = 'http://httpbin.org/get'

    def test_do_get(self):
        logger.debug('testing do_get method')
        result = call_do_get(self.url_get, need_json=True)
        parse_response_json(self, result, {'url': self.url_get})

    def test_do_get_with_existed_session(self):
        logger.debug('testing do_get method with existed requests session')
        import requests
        with requests.Session() as session:
            session.headers.update({'User-Agent': 'AO3Notifier'})
            result = call_do_get(self.url_get, session=session, need_json=True)
            parse_response_json(self, result, {'url': self.url_get})


if __name__ == '__main__':
    unittest.main()
