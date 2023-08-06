red
===

Python regex command-line tool, to replace functionality akin to 'perl -ne'.

Installation
------------

From the project root directory::

    $ python setup.py install

Usage
-----

Use --help/-h to view info on the arguments::

    $ red --help

Example usage::

    $ cat test.txt 
    foo 1 bar 2
    fiz 5 baz 10
    funk 10 bunk 9
    funk a bunk b
    a b c d
    aaaaa
    bbbb
    cc

Use it like grep::

    $ cat test.txt | red "\w+ (\d+) \w+ (\d+)" 
    foo 1 bar 2
    fiz 5 baz 10
    funk 10 bunk 9

Use it to evaluate Python code on groups stored in variable `g`::

    $ cat test.txt | red "\w+ (\d+) \w+ (\d+)" -e "int(g[0]) + int(g[1])"
    3
    15
    19

Use it to aggregate across all of stdin, into list `ag`::

    $ cat test.txt | red "\w+ (\d+) \w+ (\d+)" -a "sum([int(x[0]) for x in ag])"
    16

Evaluate on each match, and aggregate against all matches::

    $ cat test.txt | red "\w+ (\d+) \w+ (\d+)" -a "sum([int(x[0]) for x in ag])" -e "'adding {}'.format(g[0])"
    adding 1
    adding 5
    adding 10
    16

You can use named groups as well, stored in variables `d` and aggregated into `ad1`::

    $ cat test.txt | red "\w+ (?P<first>\d+) \w+ \d+" -e "'first value is {first}'.format(**d)"
    first value is 1
    first value is 5
    first value is 10

Release Notes
-------------

:0.1.0:
    Version is available on pypi, with functionality of evaluation and aggregation
:0.0.1:
    Project created
