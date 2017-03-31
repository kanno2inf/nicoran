#!/usr/bin/env python
# -*- coding:utf-8 -*-
import codecs
import os
from argparse import ArgumentParser
from datetime import datetime

import bs4
import requests
from jinja2 import Environment, FileSystemLoader


def get_ranking(type):
    # get rss of ranking
    ranking_rss_url = u'http://www.nicovideo.jp/ranking/fav/{0}/all?rss=2.0&lang=ja-jp'.format(type)
    res = requests.get(ranking_rss_url)
    return res.text


def write_file(path, text=u''):
    with codecs.open(path, 'w', 'utf-8') as f:
        f.write(text)
    return text


def read_file(path):
    with codecs.open(path, 'r', 'utf-8') as f:
        return u'\n'.join(f.readlines())


def load_ranking(type, cache=False):
    cache_path = u'ranking-{0}.rss'.format(type)
    # If exists a cache file, read this file.
    if cache and os.path.exists(cache_path):
        return read_file(cache_path)
    # get new rss
    rss = get_ranking(type)
    if cache:
        # save to a cache file
        write_file(cache_path, rss)
    return rss


def parse_datestr(date_str):
    # parse date in rss
    return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S +0900')


def parse_nicoranking(rss):
    # parse rss by bs4
    soup = bs4.BeautifulSoup(rss, "html.parser")
    # Header include title and link, etc...
    channel = soup.find('channel')
    header = {
        'title': channel.title.text,
        'link': channel.link.text,
        'publishDate': parse_datestr(channel.pubdate.text),
        'lastBuildDate': parse_datestr(channel.lastbuilddate.text)
    }

    # Video info in ranking
    ranking = []
    for rank, video in enumerate(soup.find_all('item')):
        cdata = video.description.text
        thumbnail = bs4.BeautifulSoup(cdata, "html.parser").img
        video_info = {
            'title': video.title.text,
            'link': video.link.text,
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
    parser.add_argument('-c', '--cache', action='store_true', help=u'Using ranking cache file')
    parser.add_argument('-o', '--output', metavar='OUTPUT_PATH', required=False, help=u'Output file path')
    parser.add_argument('type', metavar='TYPE', choices=RANKING_TYPE, help=u'ranking type')
    opt = parser.parse_args()

    # get rss and parse
    rss = load_ranking(opt.type, cache=opt.cache)
    header, ranking = parse_nicoranking(rss)

    # generate html
    html = make_ranking_html(header, ranking)
    if opt.output:
        write_file(opt.output, html)
    else:
        print html
