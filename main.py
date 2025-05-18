import logging
import bs4
import requests
import collections

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wb')


ParseResult = collections.namedtuple(
    'ParseResult',
    (
        'platums',
        'augstums',
        'diametrs',
        'razotajs',
        'url',
    ),
)

class Client:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept-Language': 'lv, en;q=0.9',
        }
        self.result = []

    def load_page(self):
        url = 'https://mmkriepas.lv/riepas/vasaras-riepas/'
        try:
            res = self.session.get(url=url, timeout=10)
            res.raise_for_status()
            return res.text
        except Exception as e:
            logger.error(f"Failed to load page: {e}")
            return None

    def parse_page(self, text: str):
        if not text:
            logger.error("No HTML content to parse")
            return

        try:
            soup = bs4.BeautifulSoup(text, 'html.parser')

            # Save HTML for debugging
            with open('debug.html', 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            logger.info("Saved HTML to debug.html")

            # Find the filter form
            filter_form = soup.select_one('form.mmk-filter')
            if not filter_form:
                logger.error("Could not find filter form")
                return

            # Find all filter blocks
            filter_blocks = filter_form.select('.mmk-product-filter-block')
            logger.info(f"Found {len(filter_blocks)} filter blocks")

            for block in filter_blocks:
                self.parse_block(block=block)

        except Exception as e:
            logger.error(f"Parsing failed: {e}")

    def parse_block(self, block):
        label = block.select_one('.mmk-product-filter-block__label')
        label_text = label.get_text(strip=True) if label else "No label"

        select = block.select_one('select')
        options = []
        if select:
            options = [option.get_text(strip=True) for option in select.find_all('option') if
                       option.get('value') != '0']

        logger.info(f"Filter: {label_text}")
        logger.info(f"Options: {options}")
        logger.info('=' * 50)

        url_block = block.select_one('a.mmk-product-filter-block__label')
        if not url_block:
            logger.error("no url_block")
            return
        url = url_block.get('href')
        if not url:
            logger.error("no href")
            return
        logger.info('%s', url)