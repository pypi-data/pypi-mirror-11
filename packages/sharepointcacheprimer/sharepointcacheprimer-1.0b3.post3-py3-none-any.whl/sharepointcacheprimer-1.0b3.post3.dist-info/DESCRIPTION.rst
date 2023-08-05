Sharepoint Cache Primer
========================

Overview
--------
The first time a browser hits a sharepoint site after a restart, the caches are
empty, so the page can take a while to load. One can script something to
silently hit a sharepoint web-frontend, causing it to build caches
and preventing any real people from experiencing that. 

This tool does this for a specific circumstance where it's kind of hard to
script it without better tools - where normal NTML authentication doesn't work,
because there is ADFSv3 authentication configured, and where there may be
a number of web-frontends behind a load balancer. 

*I don't know why this is required. I'm not a sharepoint admin. Maybe it's
an artifact of a particular setup.*

Installation
------------
This may work in Python 2, but many distributions of Python 2 do not include
urllib that has SNI support. Since this is a sysadmin tool, you probably want
it to "just work", so "just use Python 3.4".

Simple install:
    pip install sharepointcacheprimer

Usage
-----
The pypi package installs an executable in the standard python location, called
'**sharepointcacheprimer**'.

    usage: sharepointcacheprimer [-h] config site [site ...]
    example: sharepointcacheprimer myconfig.ini mysite.com mysite2.com

This will connect to a sharepoint site, authenticate and load a page silently. 
It is suited to running as a cronjob/scheduled task.

The configuration file is formatted as a .ini. The packages ships with an
example file that is installed in PYTHONROOT/doc/, and described below.


Configuration
-------------
>From the included `doc/example.ini`

Each section is either a site definition or a cookieset definition.

### A Site Definition
This is a sharepoint site, with ADFS credentials and an optional reference
to a cookieset to use.

    [example.com]               ; Site: example.com
    username = domain\user1     ; ADFS username
    password = password1        ; ADFS password
    url = http://example.com    ; URL that for site to prime
    cookielist = examplecookies ; Optional sectionname for Cookie Sets    

### A Cookieset Definition
Every line is a cookie, as "COOKIENAME = value1,value2,value3". For each value 
of each cookie, the site will be primed once. This allows a site pool that uses
a cookie-based load balancer to force iterating through every web frontend via 
cookies.

In the below example, the cookie "LB-COOKIE" will be set for each of
three attempts, using the values abc1, abc2, and abc3 respectively. If more than
one list of cookies is below, that will just be an additional iteration. For 
example, another line with 2 more values would cause a total of 5 priming 
attempts with 5 unique cookie values.

    [examplecookies]            ; The label referenced above
    LB-COOKIE = abc1,abc2,abc3  ; A cookie list, comma-delimited 

