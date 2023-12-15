import requests
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit, SplitResult
import lxml.html
import lxml.html.clean
import lxml.etree
import codecs
import pickle
import os
import time
import shutil
import html
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


with open(os.path.join('settings', 'global.toml'), 'rb') as f:
    config = tomllib.load(f)
debug = config['debug']['debug']
logging_level = logging.DEBUG if debug else logging.INFO
console = config['debug']['console']
if console:
    logging.basicConfig(handlers=[logging.StreamHandler(), logging.FileHandler('fallout_quests.log', 'w', 'utf-8')], format='%(asctime)s %(levelname)s %(message)s [%(funcName)s]', datefmt='%Y.%m.%d %H:%M:%S', level=logging_level)
else:
    logging.basicConfig(handlers=[logging.FileHandler('fallout_quests.log', 'w', 'utf-8')], format='%(asctime)s %(levelname)s %(message)s [%(funcName)s]', datefmt='%Y.%m.%d %H:%M:%S', level=logging_level)


def filename_check(filename): return ''.join(list(map(lambda x: '' if x in r'\/:*?"<>|' or x == '\n' else x, filename)))[:128]
def files_list(path, ext='.html'): return list(map(lambda x: str(x) + ext, sorted([int(f.strip(ext)) for f in os.listdir(path) if f.endswith(ext)])))



def __lxm2str(element):
    result = ''
    try:
        result = unquote(lxml.html.tostring(element, encoding='utf-8', pretty_print=True)).strip()
    except Exception as e:
        logging.error(f'!ERROR: __lxm2str {element} not converted: {e})')
    return result


def __str2lxm(element):
    result = None
    try:
        result = lxml.html.fromstring(element)
    except Exception as e:
        logging.error(f'!ERROR: __str2lxm {element} not converted: {e})')
    return result


def sample(items, terms_required, terms_removed, terms_negatives, terms_positives, terms_patches):
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
    logging.debug(f'''\n{80*"-"}
    items:\n{items}\n
    required: {terms_required} =>\n{items_required}\n
    removed: {terms_removed} =>\n{items_removed}\n
    negatives: {terms_negatives} =>\n{items_negatives}\n
    positives: {terms_positives} =>\n{items_positives}\n
    result:\n{items_result}\n
    {80*"-"}\n''')
    return items_result


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
        logging.error(f'!ERROR: image {src} not converted: {e})')
    return img


def download(filename, protocol, domain, base, name, query='', fragment=''):
    path = 'raw'
    os.makedirs(path, exist_ok=True)
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
    html = __lxm2str(source)
    with codecs.open(filename, 'w', 'utf-8') as f:
        f.write(html)
    logging.info(f'{url} => {filename}')
    return filename


def extract(filename, page_block, meta_block, title_block, summary_block, content_block, cut_blocks, links_required, links_removed, links_negatives, links_positives, links_patches):
    if not os.path.isfile(filename):
        return None
    raw = ''
    with codecs.open(filename, 'r', 'utf-8') as f:
        raw = f.read()
    source = __str2lxm(raw)
    page = data_extract(source, page_block)
    if page is None:
        logging.debug(f'{filename} is None')
        return None, None, None, None, None, None
    meta = data_extract(page, meta_block)
    title = data_extract(page, title_block)
    summary = data_extract(page, summary_block)
    content = data_extract(page, content_block)
    if content is None:
        return page, meta, title, summary, None, None
    else:
        for block in list(filter(None, cut_blocks.split('\n'))):
            for instance in content.xpath(block):
                instance.getparent().remove(instance)
        for instance in page.getiterator():
            if isinstance(instance, lxml.html.HtmlComment):
                instance.getparent().remove(instance)
    logging.debug(f'''\n{80*"-"}
    page_block:\n{page_block}\nmeta_block:\n{meta_block}\ntitle_block:\n{title_block}\nsummary_block:\n{summary_block}\ncontent_block:\n{content_block}\n
    page:\n{page}\nmeta:\n{meta}\ntitle:\n{title}\nsummary:\n{summary}\ncontent:\n{content}\n
    {80*"-"}\n''')
    content_links = [unquote(content_link[2]) for content_link in content.iterlinks() if content_link[1]=='href']
    # if netloc.strip() != '':
    #     content_links = [urlunsplit(SplitResult(scheme, netloc, link, '', '')) if not urlsplit(link).netloc else link for link in content_links]
    links = sample(content_links, links_required, links_removed, links_negatives, links_positives, links_patches)
    logging.debug(f'''\n{80*"-"}
    links:\n{content_links}\n
    links_result:\n{links}\n
    {80*"-"}\n''')
    if len(links) == 0:
        logging.warning(f'{filename} links to other pages not found')
    return page, meta, title, summary, content, links


def data_extract(source, block, index=0):
    data = None
    try:
        if index >= 0:
            data = source.xpath(block)[index]
        else:
            data = source.xpath(block)
    except Exception as e:
        logging.debug(f'{source} by {block} ectraction error ({e})')
        return None
    logging.debug(f'{source} by {block} exctracted:\n{data}\n')
    return data


def attribute_extract(source, block):
    attrib = ''
    try:
        attrib = unquote(source.attrib[block])
    except Exception as e:
        logging.debug(f'{source} by {block} ectraction error ({e})')
        return ''
    logging.debug(f'{source} by {block} exctracted:\n{attrib}\n')
    return attrib


def text_extract(element):
    content_filter = lxml.html.clean.Cleaner(scripts=True, javascript=True, comments=True, style=True, inline_style=True, links=True, meta=True, page_structure=True, processing_instructions=True, embedded=True, frames=True, forms=True, annoying_tags=[], remove_tags=[], kill_tags=[], allow_tags=['a', 'img'], remove_unknown_tags=False, safe_attrs_only=True, safe_attrs=['href', 'src', 'id'], add_nofollow=False, host_whitelist=[], whitelist_tags=[])
    text = ''
    media = ''
    # try:
    # for subitem in element.iter():
    #     if subitem.tag == 'img':
    #         media += '<p>' + unquote(lxml.etree.tostring(subitem, encoding='utf-8', pretty_print=True).decode('utf-8')) + '</p>'
    src = __lxm2str(element)
    text = content_filter.clean_html(src).strip()
    text = ' '.join(item.strip() for item in list(filter(None, text.split('\n')))).strip()
    text = text.replace('[ ]', '').replace('[]', '')
    text = text[5:-6]
    # except Exception as e:
    #     logging.debug(f'{element} text not extracted ({e})')
    #     return ''
    logging.debug(f'{element} text exctracted:\n{text}\n')
    return f'{media}\n{text}'

# def expand(content):
#     expaned_tags = ['div', 'section', 'span']
#     check_inline_blocks = lambda item: len(set(filter(lambda subitem: subitem.tag in expaned_tags, item.getiterator())))
#     for item in content.getchildren():
#         tag = item.tag
#         if tag in expaned_tags:
#             if check_inline_blocks(content) > 0:
#                 index = content.index(item)
#                 index_delta = 1
#                 for subitem in item:
#                     content.insert(index+index_delta, subitem)
#                     index_delta += 1
#             item.getparent().remove(item)
#     return content



def transform(title, content):
    result = ''
    for item in content.xpath('//p[@title]'):
        item.tag = 'a'
        item.set('href', item.get("title", '!!!'))    
    element_counter = 0
    # span, div, section, ect => p
    # content = expand(content)
    # content = __lxm2str(__str2lxm(content))
    # safe_attrs=['src', 'href']
    # allow_tags=['h1', 'h2', 'h3', 'h4', 'h5', 'table', 'tbody', 'tr', 'th', 'td', 'img', 'a', 'p', 'ul', 'ol', 'li']
    # allow_tags=['a']

    content_filter = lxml.html.clean.Cleaner()
    content = __str2lxm(content_filter.clean_html(__lxm2str(content))[5:-6])


    result = __lxm2str(content)
    title = text_extract(title)
    head = f'<head>\n<meta http-equiv="content-type" content="text/result; charset=utf-8" />\n<title>{title}</title>\n<link rel="stylesheet" href="../style.css">\n</head>\n'
    body = f'<body>\n{result}\n</body>'
    result = f'{head}\n{body}\n'
    # result = __lxm2str(__str2lxm(result))
    logging.debug(f'title:{title}\n{result[:2048]}\n')
    return result


def index_create(main_filter, print_filters):
    captions_filter = sorted(list(filter(None, main_filter.split('\n'))))
    links_list = dict()
    for file in os.listdir('html'):
        if file.endswith('.html'):
            caption = os.path.splitext(os.path.basename(file))[0].strip()
            if captions_filter and not any(set(map(lambda caption_filter: (caption_filter == caption or caption_filter.replace(' ', '_') == caption), captions_filter))):
                continue
            for print_filter in list(filter(None, print_filters.split('\n'))):
                caption = caption.replace(print_filter, ' ')
            caption = caption.strip()
            if caption == '':
                caption = os.path.splitext(os.path.basename(file))[0].replace('_', ' ').strip()
            link = os.path.join('html', file).replace('#', r'%23')
            links_list[caption] = link
    logging.debug(f'links_list:\n{links_list}\n')
    return links_list


def run():
    logging.info(f'PROGRAM STARTED')
    root_path = os.getcwd()
    configfiles = [file for file in os.listdir('settings') if file.endswith('.py') and not file.startswith('!')]
    for configfile in configfiles:
        project = os.path.splitext(os.path.basename(configfile))[0]
        logging.info(f'PROJECT {project} STARTED')
        try:
            settings = importlib.import_module(f'settings.{project}')
            project_path = os.path.join(root_path, project)
            os.makedirs(project_path, exist_ok=True)
            shutil.copyfile('style.css', os.path.join(project_path, 'style.css'))
            os.chdir(project_path)
            os.makedirs('raw', exist_ok=True)
            os.makedirs('html', exist_ok=True)
        except Exception as e:
            logging.critical(f'Cannot starts this project ({e})')
        if config['download']['enabled']:
            logging.info(f'DOWNLOAD STARTED')
            filename = os.path.join(project_path, 'raw', f'index.html')
            if not config['download']['overwrite'] and os.path.isfile(filename):
                logging.warning(f'{filename} exist => passed')
            else:
                download(filename, settings.protocol, settings.domain, settings.root_path, settings.root_page)
            page, meta, title, summary, content, links  = extract(filename, settings.page_block, settings.meta_block, settings.title_block, settings.summary_block, settings.root_page_links_block, settings.cut_blocks, settings.links_required, settings.links_removed, settings.links_negatives, settings.links_positives, settings.links_patches)
            all_links = links
            for level in range(1, settings.pages_level_max+1):
                logging.info(f'DOWNLOAD LEVEL: {level}')
                for link in tqdm(sorted(all_links), desc=f'DOWNLOAD LEVEL {level}'):
                    filename = os.path.join(project_path, 'raw', f'{filename_check(link.split(r"/")[-1])}.html')
                    if not config['download']['overwrite'] and os.path.isfile(filename):
                        logging.warning(f'{filename} exist => passed')
                    else:                    
                        download(filename, settings.protocol, settings.domain, settings.root_path, link)
                    page, meta, title, summary, content, links  = extract(filename, settings.page_block, settings.meta_block, settings.title_block, settings.summary_block, settings.content_block, settings.cut_blocks, settings.links_required, settings.links_removed, settings.links_negatives, settings.links_positives, settings.links_patches)
                    if links is not None:
                        all_links.update(links)
            logging.info(f'DOWNLOAD COMPLETED')
        else:
            logging.info(f'DOWNLOAD PASSED')
        if config['parse']['enabled']:
            logging.info(f'PARSING STARTED')
            name_filter = config['parse']['name_filter']
            for file in tqdm(os.listdir('raw'), desc=f'PARSE RAW'):
                if len(name_filter) > 0 and filename_check(name_filter.replace(' ', '_')) not in file:
                    continue
                filename = os.path.join('raw', file)
                title = os.path.splitext(os.path.basename(filename))[0]
                filename_out = os.path.join('html', f'{filename_check(title)}.html')
                if not config['parse']['overwrite'] and os.path.isfile(filename_out):
                    logging.warning(f'{filename} alreadedy parsed => passed')
                    continue
                page, meta, title, summary, content, links  = extract(filename, settings.page_block, settings.meta_block, settings.title_block, settings.summary_block, settings.content_block, settings.cut_blocks, settings.links_required, settings.links_removed, settings.links_negatives, settings.links_positives, settings.links_patches)
                if page is None:
                    logging.warning(f'{filename} does not match page => passed')
                    continue
                elif meta is not None and not len(sample([text_extract(meta)], settings.meta_required, settings.meta_removed, settings.meta_negatives, settings.meta_positives, settings.meta_patches)):
                    logging.warning(f'{filename} does not match meta => passed')
                    continue
                elif title is not None and not len(sample([text_extract(title)], settings.title_required, settings.title_removed, settings.title_negatives, settings.title_positives, settings.title_patches)):
                    logging.warning(f'{filename} does not match title => passed')
                    continue
                elif summary is not None and not len(sample([text_extract(summary)], settings.summary_required, settings.summary_removed, settings.summary_negatives, settings.summary_positives, settings.summary_patches)):
                    logging.warning(f'{filename} does not match summary => passed')
                    continue
                elif content is not None and not len(sample([text_extract(content)], settings.content_required, settings.content_removed, settings.content_negatives, settings.content_positives, settings.content_patches)):
                    logging.warning(f'{filename} does not match content => passed')
                    continue
                base_url = urlunsplit(SplitResult(settings.protocol, settings.domain, settings.root_path, '', '')) + r'/'
                content.make_links_absolute(base_url)
                raw_files_list = os.listdir('raw')
                href_filter = lambda url: filename_check(f'{unquote(url.replace(base_url, ""))}.html') if (filename_check(f'{unquote(url.replace(base_url, ""))}.html') in os.listdir('raw')) else '<REMOVED>'
                for link in content.iterlinks():
                    instance, type, value, _ = link
                    if type == 'href':
                        value_new = href_filter(value)
                        if value_new == '<REMOVED>':
                            instance.attrib.pop('href', None)
                            instance.tag = 'p'
                        else:
                            instance.set('href', value_new)
                        logging.debug(f'{value}\n=>\n{value_new[:256]}')
                html = transform(title, content)
                if not len(html):
                    logging.error(f'{filename} transforming error')
                    continue
                with codecs.open(filename_out, 'w', 'utf-8') as f:
                    f.write(html)
                logging.info(f'{filename} => {filename_out}')
            logging.info(f'PARSING COMPLETED')
        else:
            logging.info(f'PARSING PASSED')
        if config['build']['enabled']:
            logging.info(f'BUILDING STARTED')
            title = f'Краткий справочник {project}'.replace('_', ' ')
            content = ''
            content += f'<h2>Обзор</h2>\n'
            links = "".join(f'<li><a href="{link}">{caption}</a></li>\n' for caption, link in index_create(settings.main_filter, settings.print_filters).items())
            content += f'<ul>\n{links}</ul>\n'
            content += f'<h2>Индекс</h2>\n'
            links = "".join(f'<li><a href="{link}">{caption}</a></li>\n' for caption, link in index_create('', settings.print_filters).items())
            content += f'<ol>\n{links}</ol>\n'
            head = f'<head>\n<meta http-equiv="content-type" content="text/html; charset=utf-8" />\n<title>{title}</title>\n<link rel="stylesheet" href="style.css">\n</head>\n'
            body = f'<body><h1>\n{title}</h1>\n{content}\n</body>'
            html = f'<html>\n{head}\n{body}\n</html>\n'
            filename = f'{filename_check(title)}.html'
            with codecs.open(filename, 'w', 'utf-8') as f:
                f.write(html)
            logging.info(f'"{title}" => {filename}')
            logging.info(f'BUILDING COMPLETED')
        else:
            logging.info(f'BUILDING PASSED')
        logging.info(f'PROJECT {project} COMPLETED')
    logging.info(f'PROGRAM COMPLETED')


if __name__ == "__main__":
    run()
