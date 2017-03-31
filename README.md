# nicoran
"nicoran" script get rss and generate a simple html of "niconico video ranking".

## Install
Please install python.
* python 2.7.x

This script needs these modules.
```bash
# pip install requests beautifulsoup4 jinja4
```

## Usage
Next command generate hourly ranking to "ranking-hourly.html".
```bash
$ python nicoran.py hourly -o ranking-hourly.html
```

Support these ranking.
* hourly
* daily
* weekly
* monthly
* total
