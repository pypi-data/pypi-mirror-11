# scrape

## a web scraping tool
scrape is a command-line tool for extracting webpages as text or pdf files. The crawling mechanism allows for entire websites to be scraped and also offers regexp support for filtering links and text content. scrape is especially useful for converting online documentation to pdf or just as a faster alternative to wget and grep!

## Installation
* `pip install scrape`
* [Installing wkhtmltopdf](https://github.com/pdfkit/pdfkit/wiki/Installing-WKHTMLTOPDF)

## Usage
    usage: scrape.py [-h] [-c [CRAWL [CRAWL ...]]] [-ca]
                     [-f [FILTER [FILTER ...]]] [-fl] [-l LIMIT] [-p] [-s] [-v]
                     [-vb]
                     [urls [urls ...]]

    a web scraping tool

    positional arguments:
      urls                  urls to scrape

    optional arguments:
      -h, --help            show this help message and exit
      -c [CRAWL [CRAWL ...]], --crawl [CRAWL [CRAWL ...]]
                            url keywords to crawl links by
      -ca, --crawl-all      crawl all links
      -f [FILTER [FILTER ...]], --filter [FILTER [FILTER ...]]
                            filter lines of text by keywords
      -fl, --files          keep .html files instead of writing to text
      -l LIMIT, --limit LIMIT
                            set crawl page limit
      -p, --pdf             write to pdf instead of text
      -s, --strict          restrict crawling to domain of seed url
      -v, --version         display current version
      -vb, --verbose        print log and error messages

## Author
* Hunter Hammond (huntrar@gmail.com)

## Notes
* Conversion to text occurs by default, use --pdf or --files to save to pdf or .html files, respectively.

* Text can be filtered by passing one or more regexps to --filter.

* Pages are saved temporarily as PART.html files and removed after they are written to pdf or text. Using --files not only preserves these files but also creates subdirectories for them, named after their seed domain.

* To crawl subsequent pages, enter --crawl followed by one or more regexps which match part of the url. To crawl all links regardless of the url, use --crawl-all.

* To restrict the domain to the seed url's domain, use --strict, otherwise any domain may be followed.

* There is no limit to the number of pages to be crawled unless one is set with --limit, thus to cancel crawling and begin processing simply press Ctrl-C.



News
====

0.2.0
------

 - pages are now saved as they are crawled to PART.html files and processed/removed as necessary, this greatly saves on program memory
 - added a page cache with a limit of 10 for greater duplicate protection
 - added --files option for keeping webpages as PART.html instead of saving as text or pdf, this also organizes them into a subdirectory named after the seed url's domain
 - changed --restrict flag to --strict for restricting the domain to the seed domain while crawling
 - more --verbose messages being printed

0.1.10
------

 - now compares urls scheme-less before updating links to prevent http:// and https:// duplicates and replaced set_scheme with remove_scheme in utils.py
 - renamed write_pages to write_links

0.1.9
------

 - added behavior for --crawl keywords in crawl method
 - added a domain check before outputting crawled message or adding to crawled links
 - domain key in args is now set to base domain for proper --restrict behavior
 - clean_url now rstrips / character for proper link crawling
 - resolve_url now rstrips / character for proper out_file writing
 - updated description of --crawl flag

0.1.8
------

 - removed url fragments
 - replaced set_base with urlparse method urljoin
 - out_file name construction now uses urlparse 'path' member
 - raw_links is now an OrderedSet to try to eliminate as much processing as possible
 - added clear method to OrderedSet in utils.py

0.1.7
------

 - removed validate_domain and replaced it with a lambda instead
 - replaced domain with base_url in set_base as should have been done before
 - crawled message no longer prints if url was a duplicate

0.1.6
------

 - uncommented import __version__

0.1.5
------

 - set_domain was replaced by set_base, proper solution for links that are relative
 - fixed verbose behavior
 - updated description in README

0.1.4
------

 - fixed output file generation, was using domain instead of base_url
 - minor code cleanup

0.1.3
------

 - blank lines are no longer written to text unless as a page separator
 - style tags now ignored alongside script tags when getting text

0.1.2
------

 - added shebang

0.1.1
------

 - uncommented import __version__

0.1.0
------

 - reformatting to conform with PEP 8
 - added regexp support for matching crawl keywords and filter text keywords
 - improved url resolution by correcting domains and schemes
 - added --restrict option to restrict crawler links to only those with seed domain
 - made text the default write option rather than pdf, can now use --pdf to change that
 - removed page number being written to text, separator is now just a single blank line
 - improved construction of output file name

0.0.11
------

 - fixed missing comma in install_requires in setup.py
 - also labeled now as beta as there are still some kinks with crawling

0.0.10
------

 - now ignoring pdfkit load errors only if more than one link to try to prevent an empty pdf being created in case of error

0.0.9
------

 - pdfkit now ignores load errors and writes as many pages as possible

0.0.8
------

 - better implementation of crawler, can now scrape entire websites
 - added OrderedSet class to utils.py

0.0.7
------

 - changed --keywords to --filter and positional arg url to urls

0.0.6
------

 - use --keywords flag for filtering text
 - can pass multiple links now
 - will not write empty files anymore

0.0.5
------

 - added --verbose argument for use with pdfkit
 - improved output file name processing

0.0.4
------

 - accepts 0 or 1 url's, allowing a call with just --version

0.0.3
------

 - Moved utils.py to scrape/

0.0.2
------

 - First entry




