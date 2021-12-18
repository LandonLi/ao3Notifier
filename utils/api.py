import logging
import os
import typing

import requests

from utils.decorators import required_arguments
from utils.webclient import do_get

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)


class AO3Api:
    base_url = 'https://archiveofourown.org'
    view_adult = False

    def __init__(self, base_url=None, view_adult=False):
        if base_url:
            self.base_url = base_url
        if view_adult:
            self.view_adult = view_adult

        self.session = requests.Session()
        headers = {
            'User-Agent': os.getenv('User-Agent', 'AO3Notifier')  # TODO 应用名称可配置
        }
        self.session.headers.update(headers)

    @required_arguments('user_id')
    def get_works(self, user_id: str) -> typing.Optional[str]:
        logger.debug(f'Fetching works by user_id: {user_id}')
        url = f'{self.base_url}/users/{user_id}/works'
        result = do_get(url, exist_session=self.session)
        return result

    @required_arguments('work_id')
    def get_index(self, work_id: str) -> typing.Optional[str]:
        logger.debug(f'Fetching index by work_id: {work_id}')
        url = f'{self.base_url}/works/{work_id}/navigate'
        result = do_get(url, exist_session=self.session)
        return result

    @required_arguments('work_id,chapter_id')
    def get_chapter(self, work_id, chapter_id):
        logger.debug(f'Fetching chapter by work_id: {work_id} and chapter_id: {chapter_id}')
        url = f'{self.base_url}/works/{work_id}/chapters/{chapter_id}'
        if self.view_adult:
            url += '?view_adult=true'
        result = do_get(url, exist_session=self.session)
        return result

    def close(self):
        logger.debug('Closing requests session')
        self.session.close()
