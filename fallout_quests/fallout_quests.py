import requests
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit, SplitResult
from lxml import etree, html
from lxml.html.clean import Cleaner
import codecs
import pickle
import os
import time
import shutil
import webbrowser
import copy
import base64
import sys
import importlib
import logging
from tqdm import tqdm


if sys.version_info.major == 3 and sys.version_info.minor >= 11:
    import tomllib
else:
    from pip._vendor import tomli as tomllib


with open('fallout_quests.toml', 'rb') as f:
    config = tomllib.load(f)
DEMO = config['debug']['demo']
DEBUG = config['debug']['debug']
CONSOLE = config['debug']['console']
LOG_STR_LEN = config['debug']['log_str_len']
logging_level = logging.DEBUG if DEBUG else logging.INFO
if CONSOLE:
    logging.basicConfig(handlers=[logging.StreamHandler(), logging.FileHandler('fallout_quests.log', 'w', 'utf-8')], format='%(asctime)s %(levelname)s %(message)s [%(funcName)s]', datefmt='%Y.%m.%d %H:%M:%S', level=logging_level)
else:
    logging.basicConfig(handlers=[logging.FileHandler('fallout_quests.log', 'w', 'utf-8')], format='%(asctime)s %(levelname)s %(message)s [%(funcName)s]', datefmt='%Y.%m.%d %H:%M:%S', level=logging_level)


def filename_check(filename): return ''.join(list(map(lambda x: '' if x in r'\/:*?"<>|' or x == '\n' else x, filename)))[:128]
def files_list(path, ext='.html'): return list(map(lambda x: str(x) + ext, sorted([int(f.strip(ext)) for f in os.listdir(path) if f.endswith(ext)])))


def __lxm2str(element):
    result = ''
    try:
        result = unquote(''.join(etree.tostring(child, encoding='utf-8', pretty_print=True).decode('utf-8').strip() for child in element.iterchildren()))
    except Exception as e:
        logging.warning(f'lxm2str {element} not converted: {e})')
    return result


def __str2lxm(element):
    result = None
    try:
        result = html.fromstring(element)
    except Exception as e:
        logging.warning(f'str2lxm {element} not converted: {e})')
    return result


def sample(name, items, terms_required, terms_removed, terms_negatives, terms_positives, terms_patches):
    items = set(unquote(item) for item in items)
    if terms_patches != []:
        for term_patch in terms_patches:
            items    = set(term_patch(items))
    items_filter_all = lambda items, terms: set(filter(lambda item: item if all(set(map(lambda term: (term in item or term.replace(' ', '_') in item), terms))) else None, items))
    items_filter_any = lambda items, terms: set(filter(lambda item: item if any(set(map(lambda term: (term in item or term.replace(' ', '_') in item), terms))) else None, items))
    terms_filter     = lambda terms: set(filter(None, terms.split('\n'))) if len(set(filter(None, terms.split('\n')))) != 0 else {}
    terms_required   = terms_filter(terms_required); terms_removed = terms_filter(terms_removed); terms_negatives = terms_filter(terms_negatives); terms_positives = terms_filter(terms_positives)
    items_required   = items_filter_any(items, terms_required) if len(terms_required) > 0 else set(items)
    items_removed    = items_filter_any(items, terms_removed)
    items_negatives  = items_filter_any(items, terms_negatives)
    items_positives  = items_filter_any(items, terms_positives)
    items_result     = (items_required - items_removed) - (items_negatives - items_positives)
    logging.debug(f'sample {name} => {" | ".join(item for item in items_result)[:LOG_STR_LEN]}')
    return items_result


def rewrite_link(link, raw_path):
    if 'data:image' in link and 'base64' in link:
        return link
    if any(link.split('/')[-1] in file for file in os.listdir(raw_path)):
        return unquote(link)
    else:
        return None


def __img2base64(src):
    img = ''
    raw = ''
    type = 'png'
    try:
        raw = requests.get(src).content
         # !DEMO
        if '.jpg' or '.jpeg' in raw:
            type = 'jpg'
        else:
            type = 'png'
        img = fr'data:image/{type};base64, ' + base64.b64encode(raw).decode('utf-8')
    except Exception as e:
        logging.warning(f'image {src} not converted: {e})')
    return img


def download(filename, protocol, domain, base, name, query='', fragment=''):
    url = urlunsplit(SplitResult(protocol, domain, urljoin(base, name), query, fragment))
    content = ''
    try:
        content = requests.get(url).text
    except Exception as e:
        logging.error(f'{url} not downloaded ({e})')
        return None
    source = __str2lxm(content)
    for element in source.iter('*'):
        if element.tag == 'img':
            if 'data-src' in element.attrib:
                element.set('src', element.get('data-src'))
            element.set('src', __img2base64(element.get('src')))
            for attrib in element.attrib:
                if attrib != 'src' and attrib != 'alt':
                    element.attrib.pop(attrib)
    content = __lxm2str(source)
    file = os.path.basename(filename)
    with codecs.open(filename, 'w', 'utf-8') as f:
        f.write(content)
    logging.info(f'{url} => {file}')
    return filename


def extract(filename, page_block, meta_block, title_block, summary_block, content_block, cut_blocks, links_required, links_removed, links_negatives, links_positives, links_patches):
    if not os.path.isfile(filename):
        return None
    raw = ''
    file = os.path.basename(filename)
    with codecs.open(filename, 'r', 'utf-8') as f:
        raw = f.read()
    source = __str2lxm(raw)
    page = data_extract(source, page_block, 'page')
    if page is None:
        logging.debug(f'{file} is None')
        return None, None, None, None, None, None
    meta = data_extract(page, meta_block, 'meta')
    title = data_extract(page, title_block, 'title')
    summary = data_extract(page, summary_block, 'summary')
    content = data_extract(page, content_block, 'content')
    if content is None:
        return page, meta, title, summary, None, None
    else:
        for block in list(filter(None, cut_blocks.split('\n'))):
            for instance in content.xpath(block):
                instance.getparent().remove(instance)
        for instance in page.getiterator():
            if isinstance(instance, html.HtmlComment):
                instance.getparent().remove(instance)
    content_links = [unquote(content_link[2]) for content_link in content.iterlinks() if content_link[1]=='href']
    links = sample(file, content_links, links_required, links_removed, links_negatives, links_positives, links_patches)
    if len(links) == 0:
        logging.warning(f'{file} links to other pages not found')
    return page, meta, title, summary, content, links


def data_extract(source, block, name, warning_level_len=10, index=0):
    data = None
    if block == '':
        return data
    text_content_len = 0
    try:
        if index >= 0:
            data = source.xpath(block)[index]
        else:
            data = source.xpath(block)
        text_content_len = len(data.text_content())
        if warning_level_len > 0 and text_content_len < warning_level_len and name != 'summary' and name != 'meta':
            raise Exception('warning_level_len')
    except Exception as e:
        if name != 'summary' and name != 'meta':
            logging.warning(f'{name} by {block} from {source} not extracted: {e}')
        return None
    logging.debug(f'data {name} by {block} from {source} => {data} ({text_content_len})')
    return data


def text_extract(element):
    content_filter = Cleaner(scripts=True, javascript=True, comments=True, style=True, inline_style=True, links=True, meta=True, page_structure=True, processing_instructions=True, embedded=True, frames=True, forms=True, annoying_tags=[], remove_tags=[], kill_tags=[], allow_tags=['a', 'img'], remove_unknown_tags=False, safe_attrs_only=True, safe_attrs=['href', 'src', 'id'], add_nofollow=False, host_whitelist=[], whitelist_tags=[])
    text = ''
    media = ''
    src = __lxm2str(element).strip()
    if len(src) > 0:
        text = content_filter.clean_html(src).strip()    
        text = ' '.join(item.strip() for item in list(filter(None, text.split('\n')))).strip()
        text = text.replace('[ ]', '').replace('[]', '')
        text = text[5:-6]
    else:
        text = ''
    logging.debug(f'text {element} => {text[:LOG_STR_LEN]} ({len(text)})')
    return f'{media}\n{text}'


def transform(title, content):
    result = ''
    for item in content.xpath('//p[@title]'):
        item.tag = 'a'
        item.set('href', item.get("title", '!!!'))    
    element_counter = 0
    content_filter = Cleaner()
    try:
        content = content_filter.clean_html(__lxm2str(content))
        text_content_len = len(content)
        if not text_content_len:
            raise Exception('null content len')
        content_fragment = content[:LOG_STR_LEN].replace('\n', ' ')
        logging.debug(f'title {title} => content {content_fragment} (({text_content_len}))')
    except Exception as e:
        logging.warning(f'title {title} => content not transformed: {e}')
        return result
    title = text_extract(title)
    head = f'<head>\n<meta http-equiv="content-type" content="text/result; charset=utf-8" />\n<title>{title}</title>\n<link rel="stylesheet" href="../style.css">\n</head>\n'
    body = f'<body>\n{content}\n</body>'
    result = f'{head}\n{body}\n'
    return result


def index_create(main_filter, print_filters, project_path):
    captions_filter = sorted(list(filter(None, main_filter.split('\n'))))
    links_list = dict()
    for file in os.listdir(os.path.join(project_path, 'html')):
        if file.endswith('.html'):
            caption = os.path.splitext(os.path.basename(file))[0].strip()
            if captions_filter and not any(set(map(lambda caption_filter: (caption_filter == caption or caption_filter.replace(' ', '_') == caption), captions_filter))):
                continue
            for print_filter in list(filter(None, print_filters.split('\n'))):
                caption = caption.replace(print_filter, ' ')
            caption = caption.strip()
            if caption == '':
                caption = os.path.splitext(os.path.basename(file))[0].replace('_', ' ').strip()
            link = f'html/{file}'.replace('#', r'%23')
            links_list[caption] = link
    logging.debug(f'{links_list=}')
    return links_list

def parse(file, project_path, settings):
    filename = os.path.join(os.path.join(project_path, 'raw'), file)
    title = os.path.splitext(os.path.basename(filename))[0]
    file_out = f'{filename_check(title)}.html'
    filename_out = os.path.join(project_path, 'html', file_out)
    if not config['parse']['overwrite'] and os.path.isfile(filename_out):
        logging.warning(f'{file} alreadedy parsed => passed')
        return -1
    page, meta, title, summary, content, links  = extract(filename, settings['page_block'], settings['meta_block'], settings['title_block'], settings['summary_block'], settings['content_block'], settings['cut_blocks'], settings['links_required'], settings['links_removed'], settings['links_negatives'], settings['links_positives'], settings['links_patches'])
    if page is None or content is None:
        logging.error(f'{file} have no page content')
        return 1
    elif meta is not None and not len(sample('meta', [text_extract(meta)], settings['meta_required'], settings['meta_removed'], settings['meta_negatives'], settings['meta_positives'], settings['meta_patches'])):
        logging.warning(f'{file} does not match meta => passed')
        return 2
    elif title is not None and not len(sample('title', [text_extract(title)], settings['title_required'], settings['title_removed'], settings['title_negatives'], settings['title_positives'], settings['title_patches'])):
        logging.warning(f'{file} does not match title => passed')
        return 3
    elif summary is not None and not len(sample('summary', [text_extract(summary)], settings['summary_required'], settings['summary_removed'], settings['summary_negatives'], settings['summary_positives'], settings['summary_patches'])):
        logging.warning(f'{file} does not match summary => passed')
        return 4
    elif content is not None and not len(sample('content', [text_extract(content)], settings['content_required'], settings['content_removed'], settings['content_negatives'], settings['content_positives'], settings['content_patches'])):
        logging.warning(f'{file} does not match content => passed')
        return 5
    base_url = urlunsplit(SplitResult(settings['protocol'], settings['domain'], settings['root_path'], '', '')) + r'/'
    content.make_links_absolute(base_url)
    content.rewrite_links(lambda x: rewrite_link(x, os.path.join(project_path, 'raw')))
    href_filter = lambda url: filename_check(f'{unquote(url.replace(base_url, ""))}.html') if (filename_check(f'{unquote(url.replace(base_url, ""))}.html') in os.listdir(os.path.join(project_path, 'raw'))) else '<REMOVED>'
    for link in content.iterlinks():
        instance, type, value, _ = link
        if type == 'href':
            value_new = href_filter(value)
            if value_new == '<REMOVED>':
                instance.attrib.pop('href', None)
                instance.tag = 'p'
            else:
                instance.set('href', value_new)
            logging.debug(f'{value} => {value_new[:LOG_STR_LEN]}')
    content = transform(title, content)
    if len(content) == 0:
        logging.error(f'{file} not transformed')
        return 6
    with codecs.open(filename_out, 'w', 'utf-8') as f:
        f.write(content)
    logging.info(f'{file} => {file_out}')
    return 0


def run():
    logging.info(f'PROGRAM STARTED')
    root_path = os.path.join(os.getcwd(), 'output')
    configfiles = [file for file in os.listdir('projects') if file.endswith('.py') and not file.startswith('!')]
    for configfile in configfiles:
        project = os.path.splitext(os.path.basename(configfile))[0]
        logging.info(f'PROJECT {project} STARTED')
        try:
            settings = vars(importlib.import_module(f'projects.{project}'))
            project_path = os.path.join(root_path, project)
            os.makedirs(project_path, exist_ok=True)
            shutil.copyfile('style.css', os.path.join(project_path, 'style.css'))
            # os.chdir(project_path)
            os.makedirs(os.path.join(project_path, 'raw'), exist_ok=True)
            os.makedirs(os.path.join(project_path, 'html'), exist_ok=True)
        except Exception as e:
            logging.critical(f'Cannot starts this project ({e})')
        if config['download']['enabled']:
            logging.info(f'DOWNLOAD STARTED')
            file = 'index.html'
            filename = os.path.join(project_path, 'raw', file)
            if not config['download']['overwrite'] and os.path.isfile(filename):
                logging.warning(f'{file} exist => passed')
            else:
                download(filename, settings['protocol'], settings['domain'], settings['root_path'], settings['root_page'])
            page, meta, title, summary, content, links  = extract(filename, settings['page_block'], settings['meta_block'], settings['title_block'], settings['summary_block'], settings['root_page_links_block'], settings['cut_blocks'], settings['links_required'], settings['links_removed'], settings['links_negatives'], settings['links_positives'], settings['links_patches'])
            all_links = links
            for level in range(1, settings['pages_level_max']+1):
                logging.info(f'DOWNLOAD LEVEL: {level}')
                for link in tqdm(sorted(all_links), desc=f'DOWNLOAD LEVEL {level}'):
                    file = f'{filename_check(link.split(r"/")[-1])}.html'
                    filename = os.path.join(project_path, 'raw', file)
                    if not config['download']['overwrite'] and os.path.isfile(filename):
                        logging.warning(f'{file} exist => passed')
                    else:                    
                        download(filename, settings['protocol'], settings['domain'], settings['root_path'], link)
                    page, meta, title, summary, content, links  = extract(filename, settings['page_block'], settings['meta_block'], settings['title_block'], settings['summary_block'], settings['content_block'], settings['cut_blocks'], settings['links_required'], settings['links_removed'], settings['links_negatives'], settings['links_positives'], settings['links_patches'])
                    if links is not None:
                        all_links.update(links)
                if DEMO:
                    logging.warning(f'INTERRUPTED by DEMO')
                    break           
            logging.info(f'DOWNLOAD COMPLETED')
        else:
            logging.info(f'DOWNLOAD PASSED')
        if config['parse']['enabled']:
            logging.info(f'PARSING STARTED')
            files = os.listdir(os.path.join(project_path, 'raw'))
            for file in tqdm(files, desc=f'PARSE RAW'):
                parse(file, project_path, settings)
                if DEMO:
                    logging.warning(f'INTERRUPTED by DEMO')
                    break
            logging.info(f'PARSING COMPLETED')
        else:
            logging.info(f'PARSING PASSED')
        if config['build']['enabled']:
            logging.info(f'BUILDING STARTED')
            title = f'Краткий справочник {project}'.replace('_', ' ')
            content = ''
            content += f'<h2>Обзор</h2>\n'
            links = "".join(f'<li><a href="{link}">{caption}</a></li>\n' for caption, link in index_create(settings['main_filter'], settings['print_filters'], project_path).items())
            content += f'<ul>\n{links}</ul>\n'
            content += f'<h2>Индекс</h2>\n'
            links = "".join(f'<li><a href="{link}">{caption}</a></li>\n' for caption, link in index_create('', settings['print_filters'], project_path).items())
            content += f'<ol>\n{links}</ol>\n'
            head = f'<head>\n<meta http-equiv="content-type" content="text/html; charset=utf-8" />\n<title>{title}</title>\n<link rel="stylesheet" href="style.css">\n</head>\n'
            body = f'<body><h1>\n{title}</h1>\n{content}\n</body>'
            file = f'{filename_check(title)}.html'
            filename = os.path.join(project_path, file)
            with codecs.open(filename, 'w', 'utf-8') as f:
                f.write(f'<html>\n{head}\n{body}\n</html>\n')
            logging.info(f'"{title}" => {file}')
            logging.info(f'BUILDING COMPLETED')
        else:
            logging.info(f'BUILDING PASSED')
        logging.info(f'PROJECT {project} COMPLETED')
    logging.info(f'PROGRAM COMPLETED')


if __name__ == "__main__":
    run()
