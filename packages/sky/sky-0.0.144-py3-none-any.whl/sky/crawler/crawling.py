"""A simple web crawler -- class implementing crawling logic."""

import asyncio
import cgi
import os
from collections import namedtuple
import logging
import re
import time
import urllib.parse
import tldextract
import json
import shutil

from sky.scraper import Scraper
from sky.helper import makeTree

try:
    # Python 3.4.
    from asyncio import JoinableQueue as Queue
except ImportError:
    # Python 3.5.
    from asyncio import Queue

from asyncio import PriorityQueue


class JoinablePriorityQueue(Queue, PriorityQueue):
    pass

import aiohttp  # Install with "pip install aiohttp".

LOGGER = logging.getLogger(__name__)


def lenient_host(host):
    parts = host.split('.')[-2:]
    return ''.join(parts)


def is_redirect(response):
    return response.status in (300, 301, 302, 303, 307)


def slugify(value):
    url = re.sub(r'[^\w\s-]', '', re.sub(r'[-\s]+', '-', value)).strip().lower()
    return url[:-1] if url.endswith('/') else url


def extractDomain(url):
    tld = ".".join([x for x in tldextract.extract(url) if x])
    protocol = url.split('//', 1)[0]
    if 'file:' == protocol:
        protocol += '///'
    else:
        protocol += '//'
    return protocol + tld

FetchStatistic = namedtuple('FetchStatistic',
                            ['url',
                             'next_url',
                             'status',
                             'exception',
                             'size',
                             'content_type',
                             'encoding',
                             'num_urls',
                             'num_new_urls'])


class Crawler:
    """Crawl a set of URLs.

    This manages two sets of URLs: 'urls' and 'done'.  'urls' is a set of
    URLs seen, and 'done' is a list of FetchStatistics.
    """

    def __init__(self, config):
        self.loop = None
        self.seed_urls = None
        self.collections_path = None
        self.collection_name = None
        self.max_redirects_per_url = None
        self.max_saved_responses = 10000000
        self.max_tries_per_url = None
        self.max_workers = None
        self.crawl_required_regexps = []
        self.crawl_filter_regexps = []
        self.index_required_regexps = []
        self.index_filter_regexps = []
        self.login_data = {}
        self.login_url = None
        self.seen_urls = set()
        self.headers = {'User-Agent': 'My User Agent 1.0',
                        'From': 'youremail@domain.com'}
        for k, v in config.items():
            setattr(self, k, v)
        self.seen_urls = set(self.seen_urls)
        self.max_saved_responses = int(self.max_saved_responses)
        self.max_workers = min(int(self.max_workers), self.max_saved_responses)
        self.max_tries_per_url = int(self.max_tries_per_url)
        self.max_redirects_per_url = int(self.max_redirects_per_url)
        self.max_hops = int(self.max_hops)
        self.q = JoinablePriorityQueue(loop=self.loop)
        self.done = []
        self.root_domains = self.handle_root_of_seeds()
        self.t0 = time.time()
        self.t1 = None
        self.num_saved_responses = 0
        self.domain = extractDomain(self.seed_urls[0])
        self.file_storage_place = os.path.join(self.collections_path, self.collection_name)
        delete = False
        if delete and os.path.isdir(self.file_storage_place):
            shutil.rmtree(self.file_storage_place)
        if self.file_storage_place and not os.path.isdir(self.file_storage_place):
            os.makedirs(self.file_storage_place)

        self.session = aiohttp.ClientSession(headers=self.headers)

    @asyncio.coroutine
    def login(self):
        resp = yield from self.session.post(self.login_url, data=aiohttp.FormData(self.login_data))
        LOGGER.info('login in to url %r', self.login_url)
        print(resp.status)
        yield from resp.release()

    def handle_root_of_seeds(self):
        root_domains = set()
        for root in self.seed_urls:
            parts = urllib.parse.urlparse(root)
            host, _ = urllib.parse.splitport(parts.netloc)
            if host:
                if re.match(r'\A[\d\.]*\Z', host):
                    root_domains.add(host)
                else:
                    host = host.lower()
                    root_domains.add(lenient_host(host))
                self.add_url(0, root)
        if len(root_domains) > 1:
            raise Exception('Multiple Domains')
        return root_domains

    def close(self):
        """Close resources."""
        self.session.close()

    def host_okay(self, host):
        """Check if a host should be crawled.
        """
        host = host.lower()
        if host in self.root_domains:
            return True
        if re.match(r'\A[\d\.]*\Z', host):
            return False
        return self._host_okay_lenient(host)

    def _host_okay_lenient(self, host):
        """Check if a host should be crawled, lenient version.

        This compares the last two components of the host.
        """
        return lenient_host(host) in self.root_domains

    def record_statistic(self, fetch_statistic):
        """Record the FetchStatistic for completed / failed URL."""
        self.done.append(fetch_statistic)

    @asyncio.coroutine
    def save_response(self, text, response):
        with open(os.path.join(self.file_storage_place, slugify(response.url)), 'w') as f:
            json.dump({'url': response.url, 'html': text, 'headers': dict(response.headers)}, f)

    def should_crawl(self, url):
        if all([not re.search(x, url) for x in self.crawl_filter_regexps]):
            if (not self.crawl_required_regexps or
                    any([re.search(x, url) for x in self.crawl_required_regexps])):
                return True
        return False

    def should_save(self, url):
        if (not self.index_required_regexps or
                any([re.search(condition, url) for condition in self.index_required_regexps])):
            if all([not re.search(x, url) for x in self.index_filter_regexps]):
                return True
        return False

    @asyncio.coroutine
    def handle_response(self, response):
        """Return a FetchStatistic and list of links."""
        links = set()
        content_type = None
        encoding = None
        body = yield from response.read()

        if response.status == 200:
            num_allowed_urls = 0

            content_type = response.headers.get('content-type')
            pdict = {}

            if content_type:
                content_type, pdict = cgi.parse_header(content_type)

            encoding = pdict.get('charset', 'utf-8')
            if content_type in ('text/html', 'application/xml'):
                text = yield from response.text()

                if self.should_save(response.url):
                    _ = yield from self.save_response(text, response)
                    LOGGER.info('url %r will be converted to document, ', response.url)
                    self.num_saved_responses += 1

                # Replace href with (?:href|src) to follow image links.
                urls = set(re.findall(r'''(?i)href=["']?([^\s"'<>]+)''',
                                      text))

                for url in urls:
                    normalized = urllib.parse.urljoin(response.url, url)
                    defragmented, _ = urllib.parse.urldefrag(normalized)
                    if self.url_allowed(defragmented) and self.should_crawl(normalized):
                        if defragmented not in links and defragmented not in self.seen_urls:
                            num_allowed_urls += 1
                            links.add(defragmented)

                # visitable means: "urls that may be visit according to config"
                LOGGER.info('queue: %r, got ~%r visitable urls from %r, ',
                            self.q.qsize(), num_allowed_urls, response.url)

        stat = FetchStatistic(
            url=response.url,
            next_url=None,
            status=response.status,
            exception=None,
            size=len(body),
            content_type=content_type,
            encoding=encoding,
            num_urls=len(links),
            num_new_urls=len(links - self.seen_urls))

        return stat, links

    @asyncio.coroutine
    def fetch(self, prio, url, max_redirects_per_url):
        """Fetch one URL."""
        # Using max_workers since they are not being quit
        if self.num_saved_responses >= self.max_saved_responses:
            # NOT SURE IF THIS IS NEEDED
            self.q.task_done()
            return
        tries = 0
        exception = None
        while tries < self.max_tries_per_url:
            try:
                LOGGER.debug('getting url: ' + url)
                response = yield from asyncio.wait_for(
                    self.session.get(url, allow_redirects=False), 20)
                if tries > 1:
                    LOGGER.info('try %r for %r success', tries, url)
                break
            except aiohttp.ClientError as client_error:
                LOGGER.info('try %r for %r raised %r', tries, url, client_error)
                exception = client_error
            except asyncio.TimeoutError as e:
                LOGGER.error('asyncio.TimeoutError for %r raised %r', url, e)
            except Exception as e:
                LOGGER.error('General error for %r raised %r', url, e)
            tries += 1
        else:
            # We never broke out of the loop: all tries failed.
            if self.max_tries_per_url > 1:
                LOGGER.error('%r failed after %r tries', url, self.max_tries_per_url)

            self.record_statistic(FetchStatistic(url=url,
                                                 next_url=None,
                                                 status=None,
                                                 exception=exception,
                                                 size=0,
                                                 content_type=None,
                                                 encoding=None,
                                                 num_urls=0,
                                                 num_new_urls=0))
            return

        if is_redirect(response):
            location = response.headers['location']
            next_url = urllib.parse.urljoin(url, location)
            self.record_statistic(FetchStatistic(url=url,
                                                 next_url=next_url,
                                                 status=response.status,
                                                 exception=None,
                                                 size=0,
                                                 content_type=None,
                                                 encoding=None,
                                                 num_urls=0,
                                                 num_new_urls=0))

            if next_url in self.seen_urls:
                yield from response.release()
                return
            if max_redirects_per_url > 0:
                LOGGER.info('redirect to %r from %r', next_url, url)
                self.add_url(prio, next_url, max_redirects_per_url - 1)
            else:
                LOGGER.error('redirect limit reached for %r from %r',
                             next_url, url)
        else:
            stat, links = yield from self.handle_response(response)
            self.record_statistic(stat)
            for link in links.difference(self.seen_urls):
                good = sum([x in link for x in self.index_required_regexps])
                bad = 10 * any([x in link for x in self.index_filter_regexps])
                prio = bad - good  # lower is better
                self.q.put_nowait((prio, link, self.max_redirects_per_url))

            self.seen_urls.update(links)
        yield from response.release()

    @asyncio.coroutine
    def work(self):
        """Process queue items forever."""
        while True:
            prio, url, max_redirects_per_url = yield from self.q.get()
            assert url in self.seen_urls
            yield from self.fetch(prio, url, max_redirects_per_url)
            self.q.task_done()

    def url_allowed(self, url):
        if url.endswith('.jpg') or url.endswith('.png'):
            return False
        parts = urllib.parse.urlparse(url)
        if parts.scheme not in ('http', 'https'):
            LOGGER.debug('skipping non-http scheme in %r', url)
            return False
        host, _ = urllib.parse.splitport(parts.netloc)
        if not self.host_okay(host):
            LOGGER.debug('skipping non-root host in %r', url)
            return False
        return True

    def add_url(self, prio, url, max_redirects_per_url=None):
        """Add a URL to the queue if not seen before."""
        if max_redirects_per_url is None:
            max_redirects_per_url = self.max_redirects_per_url
        LOGGER.debug('adding %r %r', url, max_redirects_per_url)
        self.seen_urls.add(url)
        self.q.put_nowait((prio, url, max_redirects_per_url))

    @asyncio.coroutine
    def crawl(self):
        """Run the crawler until all finished."""
        workers = [asyncio.Task(self.work(), loop=self.loop)
                   for _ in range(self.max_workers)]
        self.t0 = time.time()
        yield from self.q.join()
        print('seen urls {} done urls {}'.format(len(self.seen_urls), len(self.done)))
        self.t1 = time.time()
        for w in workers:
            w.cancel()

    def finish_leftovers(self):
        return False


class NewsCrawler(Crawler):

    def __init__(self, config):
        super(NewsCrawler, self).__init__(config)
        self.scraper = Scraper(config)
        self.template_complete = False
        self.data = {}
        self.templates_done = 0

    @asyncio.coroutine
    def save_response(self, text, response):
        # just let the indexer save the files as normal and also create a Template
        url = response.url
        tree = makeTree(text, self.scraper.domain)
        if self.templates_done < self.scraper.config['max_templates']:
            self.templates_done += 1
            self.scraper.domain_nodes_dict.add_template_elements(tree)
            self.scraper.url_to_headers_mapping[url] = dict(response.headers)
            self.data[url] = self.scraper.process(url, tree, False, ['cleaned'])
        else:
            # Let's try to do it in a tasked manner to remove existing ones and new ones
            # new one
            self.data[url] = self.scraper.process(url, tree, False, ['cleaned'])
        return

    def save_data(self, data):
        raise NotImplementedError('save_data has to be implemented')

    def save_bulk_data(self, data):
        raise NotImplementedError('save_bulk_data has to be implemented')

    def finish_leftovers(self):
        LOGGER.info('finish leftovers')
        if self.data:
            LOGGER.info('saving: ' + str([url for url in self.data]))
            self.save_bulk_data(self.data)
            for url in self.data:
                LOGGER.info('saved url ' + url)
        return dict(self.scraper.domain_nodes_dict)
