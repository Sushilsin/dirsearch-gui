<img src="static/logo.png#gh-light-mode-only" alt="dirsearch logo (light)" width="675px">
<img src="static/logo-dark.png#gh-dark-mode-only" alt="dirsearch logo (dark)" width="675px">

Gui based dirsearch - Web path discovery
=========

> An advanced web path brute-forcer

## **dirsearch** is being actively developed by [@maurosoria](https://twitter.com/_maurosoria) and [@shelld3v](https://twitter.com/shells3c_)

## **dirsearch_gui** is being actively developed by [@sushilsin](https://github.com/Sushilsin)

Installation & Usage
------------

**Requirement: python 3.9 or higher**

Choose one of these installation options:

- Install with **git**: `git clone https://github.com/Sushilsin/dirsearch-gui` (**RECOMMENDED**)
- To run
   ```sh
  cd dirsearch-gui
  dirsearch_gui.py
  ```
   

Wordlists (IMPORTANT)
---------------
**Summary:**
  - Wordlist is a text file, each line is a path.
  - About extensions, unlike other tools, dirsearch only replaces the `%EXT%` keyword with extensions from **-e** flag.
  - For wordlists without `%EXT%` (like [SecLists](https://github.com/danielmiessler/SecLists)), **-f | --force-extensions** switch is required to append extensions to every word in wordlist, as well as the `/`.
  - To apply your extensions to wordlist entries that have extensions already, use **-O** | **--overwrite-extensions** (Note: some extensions are excluded from being overwritted such as *.log*, *.json*, *.xml*, ... or media extensions like *.jpg*, *.png*)
  - To use multiple wordlists, you can separate your wordlists with commas. Example: `wordlist1.txt,wordlist2.txt`.

**Examples:**

- *Normal extensions*:
```
index.%EXT%
```

Passing **asp** and **aspx** as extensions will generate the following dictionary:

```
index
index.asp
index.aspx
```

- *Force extensions*:
```
admin
```

Passing **php** and **html** as extensions with **-f**/**--force-extensions** flag will generate the following dictionary:

```
admin
admin.php
admin.html
admin/
```

- *Overwrite extensions*:
```
login.html
```

Passing **jsp** and **jspa** as extensions with **-O**/**--overwrite-extensions** flag will generate the following dictionary:

```
login.html
login.jsp
login.jspa
```


Options
-------

```
Usage: dirsearch_gui.py [-u|--url] target [-e|--extensions] extensions [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit

  Mandatory:
    -u URL, --url=URL   Target URL(s), can use multiple flags
    -l PATH, --urls-file=PATH
                        URL list file
    --stdin             Read URL(s) from STDIN
    --cidr=CIDR         Target CIDR
    --raw=PATH          Load raw HTTP request from file (use '--scheme' flag
                        to set the scheme)
    --nmap-report=PATH  Load targets from nmap report (Ensure the inclusion of
                        the -sV flag during nmap scan for comprehensive
                        results)
    -s SESSION_FILE, --session=SESSION_FILE
                        Session file
    --config=PATH       Path to configuration file (Default:
                        'DIRSEARCH_CONFIG' environment variable, otherwise
                        'config.ini')

  Dictionary Settings:
    -w WORDLISTS, --wordlists=WORDLISTS
                        Wordlist files or directories contain wordlists
                        (separated by commas)
    -e EXTENSIONS, --extensions=EXTENSIONS
                        Extension list separated by commas (e.g. php,asp)
    -f, --force-extensions
                        Add extensions to the end of every wordlist entry. By
                        default dirsearch only replaces the %EXT% keyword with
                        extensions
    -O, --overwrite-extensions
                        Overwrite other extensions in the wordlist with your
                        extensions (selected via `-e`)
    --exclude-extensions=EXTENSIONS
                        Exclude extension list separated by commas (e.g.
                        asp,jsp)
    --remove-extensions
                        Remove extensions in all paths (e.g. admin.php ->
                        admin)
    --prefixes=PREFIXES
                        Add custom prefixes to all wordlist entries (separated
                        by commas)
    --suffixes=SUFFIXES
                        Add custom suffixes to all wordlist entries, ignore
                        directories (separated by commas)
    -U, --uppercase     Uppercase wordlist
    -L, --lowercase     Lowercase wordlist
    -C, --capital       Capital wordlist

  General Settings:
    -t THREADS, --threads=THREADS
                        Number of threads
    --async             Enable asynchronous mode
    -r, --recursive     Brute-force recursively
    --deep-recursive    Perform recursive scan on every directory depth (e.g.
                        api/users -> api/)
    --force-recursive   Do recursive brute-force for every found path, not
                        only directories
    -R DEPTH, --max-recursion-depth=DEPTH
                        Maximum recursion depth
    --recursion-status=CODES
                        Valid status codes to perform recursive scan, support
                        ranges (separated by commas)
    --subdirs=SUBDIRS   Scan sub-directories of the given URL[s] (separated by
                        commas)
    --exclude-subdirs=SUBDIRS
                        Exclude the following subdirectories during recursive
                        scan (separated by commas)
    -i CODES, --include-status=CODES
                        Include status codes, separated by commas, support
                        ranges (e.g. 200,300-399)
    -x CODES, --exclude-status=CODES
                        Exclude status codes, separated by commas, support
                        ranges (e.g. 301,500-599)
    --exclude-sizes=SIZES
                        Exclude responses by sizes, separated by commas (e.g.
                        0B,4KB)
    --exclude-text=TEXTS
                        Exclude responses by text, can use multiple flags
    --exclude-regex=REGEX
                        Exclude responses by regular expression
    --exclude-redirect=STRING
                        Exclude responses if this regex (or text) matches
                        redirect URL (e.g. '/index.html')
    --exclude-response=PATH
                        Exclude responses similar to response of this page,
                        path as input (e.g. 404.html)
    --skip-on-status=CODES
                        Skip target whenever hit one of these status codes,
                        separated by commas, support ranges
    --min-response-size=LENGTH
                        Minimum response length
    --max-response-size=LENGTH
                        Maximum response length
    --max-time=SECONDS  Maximum runtime for the scan
    --exit-on-error     Exit whenever an error occurs

  Request Settings:
    -m METHOD, --http-method=METHOD
                        HTTP method (default: GET)
    -d DATA, --data=DATA
                        HTTP request data
    --data-file=PATH    File contains HTTP request data
    -H HEADERS, --header=HEADERS
                        HTTP request header, can use multiple flags
    --headers-file=PATH
                        File contains HTTP request headers
    -F, --follow-redirects
                        Follow HTTP redirects
    --random-agent      Choose a random User-Agent for each request
    --auth=CREDENTIAL   Authentication credential (e.g. user:password or
                        bearer token)
    --auth-type=TYPE    Authentication type (basic, digest, bearer, ntlm, jwt)
    --cert-file=PATH    File contains client-side certificate
    --key-file=PATH     File contains client-side certificate private key
                        (unencrypted)
    --user-agent=USER_AGENT
    --cookie=COOKIE

  Connection Settings:
    --timeout=TIMEOUT   Connection timeout
    --delay=DELAY       Delay between requests
    -p PROXY, --proxy=PROXY
                        Proxy URL (HTTP/SOCKS), can use multiple flags
    --proxies-file=PATH
                        File contains proxy servers
    --proxy-auth=CREDENTIAL
                        Proxy authentication credential
    --replay-proxy=PROXY
                        Proxy to replay with found paths
    --tor               Use Tor network as proxy
    --scheme=SCHEME     Scheme for raw request or if there is no scheme in the
                        URL (Default: auto-detect)
    --max-rate=RATE     Max requests per second
    --retries=RETRIES   Number of retries for failed requests
    --ip=IP             Server IP address
    --interface=NETWORK_INTERFACE
                        Network interface to use

  Advanced Settings:
    --crawl             Crawl for new paths in responses

  View Settings:
    --full-url          Full URLs in the output (enabled automatically in
                        quiet mode)
    --redirects-history
                        Show redirects history
    --no-color          No colored output
    -q, --quiet-mode    Quiet mode

  Output Settings:
    -o PATH/URL, --output=PATH/URL
                        Output file or MySQL/PostgreSQL URL (Format:
                        scheme://[username:password@]host[:port]/database-
                        name)
    --format=FORMAT     Report format (Available: simple, plain, json, xml,
                        md, csv, html, sqlite, mysql, postgresql)
    --log=PATH          Log file
```


Configuration
---------------

By default, `config.ini` inside your dirsearch directory is used as the configuration file but you can select another file via `--config` flag or `DIRSEARCH_CONFIG` environment variable.

```ini
# If you want to edit dirsearch default configurations, you can
# edit values in this file. Everything after `#` is a comment
# and won't be applied

[general]
threads = 25
async = False
recursive = False
deep-recursive = False
force-recursive = False
recursion-status = 200-399,401,403
max-recursion-depth = 0
exclude-subdirs = %%ff/,.;/,..;/,;/,./,../,%%2e/,%%2e%%2e/
random-user-agents = False
max-time = 0
exit-on-error = False
# subdirs = /,api/
# include-status = 200-299,401
# exclude-status = 400,500-999
# exclude-sizes = 0b,123gb
# exclude-text = "Not found"
# exclude-regex = "^403$"
# exclude-redirect = "*/error.html"
# exclude-response = 404.html
# skip-on-status = 429,999

[dictionary]
default-extensions = php,aspx,jsp,html,js
force-extensions = False
overwrite-extensions = False
lowercase = False
uppercase = False
capitalization = False
# exclude-extensions = old,log
# prefixes = .,admin
# suffixes = ~,.bak
# wordlists = /path/to/wordlist1.txt,/path/to/wordlist2.txt

[request]
http-method = get
follow-redirects = False
# headers-file = /path/to/headers.txt
# user-agent = MyUserAgent
# cookie = SESSIONID=123

[connection]
timeout = 7.5
delay = 0
max-rate = 0
max-retries = 1
## By disabling `scheme` variable, dirsearch will automatically identify the URI scheme
# scheme = http
# proxy = localhost:8080
# proxy-file = /path/to/proxies.txt
# replay-proxy = localhost:8000

[advanced]
crawl = False

[view]
full-url = False
quiet-mode = False
color = True
show-redirects-history = False

[output]
## Support: plain, simple, json, xml, md, csv, html, sqlite
report-format = plain
autosave-report = True
autosave-report-folder = reports/
# log-file = /path/to/dirsearch.log
# log-file-size = 50000000
```





License
---------------
Copyright (C) Mauro Soria (maurosoria@gmail.com)

License: GNU General Public License, version 2
