import logging
import os

import requests
from requests import Session

logger = logging.getLogger(__name__)


def do_get(url: str, params: dict = None, exist_session: Session = None, need_json: bool = False,
           expected_status_code: int = requests.codes.ok):
    if exist_session is None:
        session = requests.Session()
    else:
        session = exist_session

    proxies = dict()
    http_proxy = os.getenv('HTTP_PROXY')
    https_proxy = os.getenv('HTTPS_PROXY')
    if http_proxy:
        proxies['http'] = http_proxy
    if https_proxy:
        proxies['https'] = https_proxy
    logger.debug(f'proxies: {proxies}')

    resp = session.get(url, params=params, proxies=proxies)

    if exist_session is None:
        session.close()
    # TODO 太丑了，得整理

    if not resp.status_code == expected_status_code:
        logger.error(f'[{resp.status_code}] GET {url} error')
        return

    if need_json:
        return resp.json()
    else:
        return resp.text
