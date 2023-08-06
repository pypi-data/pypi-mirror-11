# cliquery

## a command-line browsing interface
cliquery bundles the more important features of a browser and the quickness of the command-line, supporting web searches, page previewing, bookmarking, and other useful features. An interactive interface allows users to make successive queries, eliminating the need to reinvoke the program each time. Simply typing help within the prompt lists all possibilities available to the user. When a link is finally chosen to be open, cliquery simply invokes the browser listed in its configuration file (or will attempt to find a default browser if none listed).

cliquery reduces needless clicking thus giving faster results, all without eliminating the use of a conventional browser!

## Installation
    pip install cliquery

or

    pip install git+https://github.com/huntrar/cliquery.git#egg=cliquery

or

    git clone https://github.com/huntrar/cliquery
    cd cliquery
    python setup.py install

It is recommended to [sign up](https://developer.wolframalpha.com/portal/apisignup.html) for a WolframAlpha API key and enter that and your preferred browser in .cliqrc (cygwin users *MUST* enter `cygwin` as their browser to avoid cross-platform conflicts).

It is also recommended to create a .local.cliqrc file to use in place of .cliqrc, as .cliqrc is overwritten when updating the program. Do the following to copy .cliqrc to .local.cliqrc:

    cd "$(dirname "$(cliquery -c)")"
    cp .cliqrc .local.cliqrc

## Usage
    usage: cliquery.py [-h] [-b] [-c] [-C] [-d] [-f] [-o] [-p] [-s] [-v] [-w]
                       [QUERY [QUERY ...]]

    a command-line browsing interface

    positional arguments:
      QUERY              keywords to search

    optional arguments:
      -h, --help         show this help message and exit
      -b, --bookmark     view and modify bookmarks
      -c, --config       print location of config file
      -C, --clear-cache  clear the cache
      -d, --describe     display page snippet
      -f, --first        open first link
      -o, --open         open link or browser manually
      -p, --print        print link to stdout
      -s, --search       display search links
      -v, --version      display current version
      -w, --wolfram      display wolfram results

## Author
* Hunter Hammond (huntrar@gmail.com)

## Notes
* Supports both Python 2.x and Python 3.x.
* If you receive the following message when trying to add bookmarks:
    ```
    IOError: [Errno 13] Permission denied: '/usr/local/lib/python2.7/dist-packages/cliquery/.cliqrc'
    ```
Enter the following to fix:
    ```
    sudo chmod a+x /usr/local/lib/python2.7/dist-packages/cliquery/.cliqrc
    ```
* A search may return immediate results, such as calculations or facts, or instead a page of search results comprised of descriptive links to follow.
* Interactive use is as easy as passing the regular flag arguments into the link prompt; this overrides any preexisting flags and allows for more even more flexibility. Entering h or help will list all possible prompt commands.
    ```
    + + + + + + + + + + + + + + + + + + + + + + + + + + + +
    1. A Simple Makefile Tutorial
    2. simple sentence - definition and examples of simple ...
    3. HTML Examples - W3Schools
    4. A Simple Guide to HTML - Welcome
    5. What Is Simple Future Tense With Example - Askives Docs
    6. A Simple Example: After Cache - How Caching Works
    7. Basic HTML Sample Page - Sheldon Brown
    8. ENG 1001: Sentences: Simple, Compound, and Complex
    + + + + + + + + + + + + + + + + + + + + + + + + + + + +
    : d 4


    http://www.simplehtmlguide.com/

    A Simple Guide to HTML
    html cheat sheet
    Welcome to my HTML Guide -- I hope you find it useful :)
    This easy guide for beginners covers several topics, with short and basic descriptions of the HTML tags you are likely to need when learning how to make your own website.
    See more? [Press Enter] 
    ```
* To choose multiple links at once, a range may be specified by separating the start and end range with a dash. Leaving one end of the range blank will choose all links until the other end of that range. For example, given 10 links, entering 5- would effectively be the same as entering 5-10.
* Using the bookmarks flag with no arguments will list all current bookmarks in .cliqrc, ordered by time of entry. Adding and deleting bookmarks can be done using add [url] or del [num] or [suburl], where [suburl] is a substring of the url. Opening bookmarks is done through the bookmarks flag and either a [num] or [suburl] argument. Bookmarks may also be added interactively through the link prompt by entering b [num].


News
====

0.7.12
------

 - minor wording changes to installation instructions

0.7.11
------

 - added instructions to create .local.cliqrc file in installation instructions

0.7.10
------

 - fixed bad formatting with README installation instructions

0.7.9
------

 - added urllib getproxies for use with requests
 - replaced url special character encoding (hardcoded symbol_dict) with urllib's quote_plus
 - replaced occurrences of 'link' with 'url' when referring to a web address specifically
 - general function cleanup, including use of format instead of concat'ing strings when conveniently possible

0.7.8
------

 - checks for .local.cliqrc before .cliqrc

0.7.4
------

 - updated usage in README

0.7.3
------

 - changed --CLEAR-CACHE back to --clear-cache, previously thought name conflict is avoided by not allowing to clear cache from link prompt

0.7.2
------

 - added -p, --print flag for printing links to stdout
 - removed bing_open function as open_link does its job already

0.7.1
------

 - removed .testrc file that snuck in

0.7.0
------

 - improvements to documentation

0.6.12
------

 - changed occurence of args['clear_cache'] to args['CLEAR_CACHE'] per the previous update

0.6.11
------

 - changed --clear-cache flag to --CLEAR-CACHE, necessary to avoid a name conflict when resolving link prompt flags (--clear-cache and --config both resolve to 'c')

0.6.10
------

 - updated README

0.6.9
------

 - added requests-cache which caches recent queries in ~/.cache/cliquery

0.6.8
------

 - describe fetches lines with length at least a fifth of avg length, changed from half

0.6.7
------

 - returns bookmarks even if fail to find browser and api key in cliqrc

0.6.6
------

 - dist upload to pypi failed due to permissions error, just a reupload of 6.5

0.6.5
------

 - removed check for 'describe' flag in search() as it is checked in subsequent functions anyways

0.6.4
------

 - removed border printed when describing links

0.6.3
------

 - added package_data field in setup.py to include .cliqrc in the sdist
 - subsequently removed check_config() as .cliqrc will be included
 - added LICENSE.txt to MANIFEST.in
 - now allows empty browser: field in .cliqrc, webbrowser lib can resolve browser itself

0.6.2
------

 - added requests to setup.py install_requires

0.5.8
------

 - reformatting to conform with PEP 8
 - added shebang

0.5.7
------

 - moved a lot of generic functions to utils.py
 - fixed some spacing formatting and changed % to format()

0.5.6
------

 - uncommented version import

0.5.5
------

 - more flag support, 'first' now works in link prompt
 - description flag now allows ranges and multiple numbers

0.5.4
------

 - more improvements to link prompt flags and command line behavior
 - removed ad block regex, too broad

0.5.3
------

 - changed instances of type() to isinstance()

0.5.2
------

 - removed some misplaced lines

0.5.1
------

 - updated link prompt help message

0.5.0
------

 - reworked a lot of logic in bing_search for more flexibility when changing flags
 - bookmarks are read even when bookmark flag isnt specified from command line runner also for flexibility

0.4.9
------

 - fixed UnboundLocalError when api_key not in config
 - made Wolfram API key optional

0.4.8
------

 - uncommented version import

0.4.7
------

 - quick fix for deleting/opening bookmarks using a num

0.4.6
------

 - can add and delete bookmarks using -b add [url] and -b del [url] or [num]
 - can now open and delete bookmarks using a substring of the url

0.4.5
------

 - removed bookmark test code that snuck into commit

0.4.4
------

 - updates to setup.py

0.4.3
------

 - calling -o with no arguments opens browser in current directory

0.4.2
------

 - fixed version import

0.4.1
------

 - python 3 support, switched urllib2 to requests and other minor changes

0.4.0
------

 - rehaul of interactive mode, can now reuse most flags without exiting the prompt

0.3.3
------

 - added -c flag to print location of config

0.3.2
------

 - renamed CLIQuery to cliquery

0.3.1
------

 - improved description output readability 

0.3.0
------

 - fixed desc flag behavior when given standalone

0.2.9
------

 - proper checking for 'cygwin' as browser before writing errors

0.2.8
------

 - updates to .cliqrc creation and error messages

0.2.5
------

 - .cliqrc now created on first run

0.2.4
------

 - Now available on PyPI

0.2.3
------

 - First entry




