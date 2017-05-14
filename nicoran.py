#!/usr/bin/env python
# -*- coding:utf-8 -*-
import codecs
import time
from argparse import ArgumentParser

import bs4
import feedparser
from jinja2 import Environment, FileSystemLoader


def rss_url(type):
    return u'http://www.nicovideo.jp/ranking/fav/{0}/all?rss=2.0&lang=ja-jp'.format(type)


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


if __name__ == '__main__':
    RANKING_TYPE = ['hourly', 'daily', 'weekly', 'monthly', 'total']

    parser = ArgumentParser()
    parser.add_argument('-o', '--output', metavar='OUTPUT_PATH', required=False, help=u'Output file path')
    parser.add_argument('type', metavar='TYPE', choices=RANKING_TYPE, help=u'ranking type')
    opt = parser.parse_args()

    rss = feedparser.parse(rss_url(opt.type))
    header, ranking = parse_nicoranking_feed(rss)

    # generate html
    html = make_ranking_html(header, ranking)
    if opt.output:
        write_file(opt.output, html)
    else:
        print html
