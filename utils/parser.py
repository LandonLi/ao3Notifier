import logging
import re
from datetime import datetime

from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)


class AO3Parser:
    base_url = 'https://archiveofourown.org'

    def parse_works(self, content):
        logger.debug('Parsing works')
        works = dict()
        soup = BeautifulSoup(content, 'html.parser')
        lis = soup.find_all('li', id=re.compile('^work_.+'))
        for li in lis:
            work_id = li.get('id').split('_')[1]
            tag_a_title = li.find('a')
            title = tag_a_title.text.strip()
            url = f'{self.base_url}{tag_a_title.get("href")}'
            date_str = li.select_one('div p').text.strip()
            date = datetime.strptime(date_str, "%d %b %Y")  # TODO ao3返回的时间是否和客户端的时区有关？
            fandoms = [tag_a.text.strip() for tag_a in li.select('div h5 a')]
            symbols = [tag_a.text.strip() for tag_a in li.find('ul', {'class': 'required-tags'})
                       if tag_a.text.strip() != '']
            stats = li.find('dl', {'class': 'stats'})
            language = stats.find('dd', {'class': 'language'}).text.strip()
            words = int(stats.find('dd', {'class': 'words'}).text.strip().replace(',', ''))
            chapters = stats.find('dd', {'class': 'chapters'}).text.strip()
            kudos = int(stats.find('dd', {'class': 'kudos'}).text.strip().replace(',', ''))
            hits = int(stats.find('dd', {'class': 'hits'}).text.strip().replace(',', ''))
            work = {
                'title': title,
                'url': url,
                'date': date,
                'fandoms': fandoms,
                'symbols': symbols,
                'language': language,
                'words': words,
                'chapters': chapters,
                'kudos': kudos,
                'hits': hits
            }
            works[work_id] = work
        return works

    def parse_index(self, content):
        logger.debug('Parsing index')
        chapters = dict()
        soup = BeautifulSoup(content, 'html.parser')
        lis = soup.find(id='main').select('li')
        for li in lis:
            tag_a_title = li.select_one('a')
            title = tag_a_title.text.strip()
            date_str = li.select_one('span').text.strip().replace('(', '').replace(')', '')
            date = datetime.strptime(date_str, '%Y-%m-%d')
            url = f'{self.base_url}{tag_a_title.get("href")}'
            chapter_id = url.split('/')[-1]
            chapter = {
                'title': title,
                'url': url,
                'date': date
            }
            chapters[chapter_id] = chapter
        return chapters

    def parse_chapter(self, content):
        logger.debug('Parsing chapter')
        chapter = dict()
        soup = BeautifulSoup(content, 'html.parser')
        tag_div_chapter = soup.find('div', {'class': 'chapter'})
        tag_h3_title = tag_div_chapter.find('h3', {'class': 'title'})
        title = tag_h3_title.text.strip()
        chapter['title'] = title
        tag_div_summary = soup.find('div', {'class': re.compile('^summary.*')})
        if tag_div_summary:
            summary = '\n'.join([p.text.strip() for p in tag_div_summary.select('blockquote p')])
            chapter['summary'] = summary
        article = '\n'.join([p.text.strip() for p in tag_div_chapter.find('div', role='article').select('p')])
        chapter['article'] = article
        return chapter
