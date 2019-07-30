#!/usr/bin/env python
# -*- coding:utf-8 -*-
import codecs
import sys
import time
from argparse import ArgumentParser

import bs4
import feedparser
from jinja2 import Environment, FileSystemLoader


def rss_url(type):
    # dwango reference: https://dwango.github.io/niconico/genre_ranking/ranking_rss/
    return u'http://www.nicovideo.jp/ranking/genre/all?term={0}&rss=2.0&lang=ja-jp'.format(type)


def write_file(path, text=u''):
    with codecs.open(path, 'w', 'utf-8') as f:
        f.write(text)
    return text


def parse_nicoranking_feed(rss):
    # parse rss by feedparser
    feed = rss.feed

    # Header include title and link, etc...
    header = {
        'title': feed.title,
        'link': feed.link,
        'updated': time.strftime('%Y-%m-%d %H:%M:%S', feed.updated_parsed)
    }

    # Video info in ranking
    ranking = []
    for rank, entry in enumerate(rss['entries']):
        thumbnail = bs4.BeautifulSoup(entry.description, "html.parser").img
        video_info = {
            'title': entry.title,
            'link': entry.link,
            'thumbnail': {
                'src': thumbnail['src'],
                'width': thumbnail['width'],
                'height': thumbnail['height'],
                'alt': thumbnail['alt']
            }
        }
        ranking.append(video_info)

    return header, ranking


def make_ranking_html(header, ranking):
    # generate html from template
    env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
    template = env.get_template('ranking.tmpl.html')
    html = template.render({'header': header, 'ranking': ranking})
    return html


def main(argv):
    RANKING_TYPE = ['hour', '24h', 'week', 'month', 'total']

    parser = ArgumentParser()
    parser.add_argument('type', metavar='TYPE', choices=RANKING_TYPE, help=u'Ranking type')
    parser.add_argument('-o', '--output', metavar='OUTPUT_PATH', required=False, help=u'Output file path')
    opt = parser.parse_args(argv)

    rss = feedparser.parse(rss_url(opt.type))
    header, ranking = parse_nicoranking_feed(rss)

    # generate html
    html = make_ranking_html(header, ranking)
    if opt.output:
        write_file(opt.output, html)
        return
    print(html)


if __name__ == '__main__':
    main(sys.argv[1:])
