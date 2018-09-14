from bs4 import BeautifulSoup as bs
from functools import reduce


def prepare_comics_list(data):
    return list(map(prepare_comic_dict, data))


def prepare_comic_dict(data):
    title = bs(data['title']['rendered'], 'html.parser').string
    links = bs(data['content']['rendered'], 'html.parser').find_all('a') if data.get('content') else []
    paragraphs = bs(data['excerpt']['rendered'], 'html.parser').find_all('p') if data.get('excerpt') else []

    return {
        'id': data['id'],
        'link': data['link'],
        'date': data['date'],
        'excerpt': '\n'.join(map((lambda p: p.getText()), paragraphs)),
        'title': title,
        'image_url': data['_embedded']['wp:featuredmedia'][0]['link'] if data.get('_embedded') else None,
        'download_url': reduce((lambda x, y: y.get('href') if y.get('title') == 'Download Now' else x), links, None)
    }
