# Listing details parser
Scrape and extract apps' listing details information from the Google Play Store

## Installation

### Installing from PyPI
```
pip install playlistingscraper
```

### Installing from source
```
$ git clone https://github.com/sikuli/sieveable-tools.git
$ cd Play-Listing-Scraper
$ sudo python setup.py install
```

## Usage

```
$ playlistingscraper --help
playlistingscraper [options] packageName-versionCode | google_play_html_page_file

A tool for Scraping an app's listing details data from the Google Play Store
store and saving it in a file in JSON format.

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -o DIR, --out-dir=DIR
                        write out file to a target directory. Default is
                        current directory
  -l FILE, --log=FILE   write logs to FILE.
  -v, --verbose         Increase verbosity.
```

## Example
```
$ playlistingscraper com.evernote-4535
$ ls
com.evernote-4534.listing.json
```

## Disclaimer

This tool is developed and released here for academic purposes only, and we are not responsible for any damage that could be done with it.
Use it at your own risk.

## License
This tool is licensed under the MIT license.

