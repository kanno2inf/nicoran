# nicoran
"nicoran" script get rss and generate a simple html of "niconico video ranking".

## Install
Please install python.
* python 3.7.x

This script needs these modules.
```
# pip install feedparser beautifulsoup4 jinja2
```

## Usage
Next command generate hourly ranking to "ranking-hourly.html".
```
$ python nicoran.py hourly -o ranking-hourly.html
```

Support these ranking.
* hour
* 24h
* week
* month
* total
