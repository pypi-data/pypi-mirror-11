==============================================
RDS Utils: Utilities for playing with RDS data
==============================================

RDS Utils provide few commands for preprocessing RDS data in text files.

Following commands are aviable:

- `rds_cycle`: replay in cycle set of RDS files in rate 11.4 groups a second (timestamps updated).
- `rds_concat`: concatenates RDS records from set of RDS files
- `rds_sort`: sort names of RDS files according to timestamp in first RDS record

.. contents:: Table of Content

Installation
============

Install using `pip`. Best install into virtualenv.
::

    $ pip install ttr.rdsutils

Format of RDS data
==================
The RDS data are expected to have following format::

    2406846391911698;33;40;92.6 MHz;2015-08-12T10:21:41Z
    24060468E0CD522D;33;40;92.6 MHz;2015-08-12T10:21:41Z
    240624686E6F7374;33;40;92.6 MHz;2015-08-12T10:21:41Z
    24060469E0CD5245;33;40;92.6 MHz;2015-08-12T10:21:41Z
    240634704080CD46;33;40;92.6 MHz;2015-08-12T10:21:41Z
    2406846391911698;33;40;92.6 MHz;2015-08-12T10:21:41Z
    2406046AE0CD4749;33;40;92.6 MHz;2015-08-12T10:21:41Z
    24062469692E2043;33;40;92.6 MHz;2015-08-12T10:21:41Z
    2406046FE0CD4E41;31;40;92.6 MHz;2015-08-12T10:21:42Z
    2406846361A2AC00;31;40;92.6 MHz;2015-08-12T10:21:42Z
    24060468E0CD522D;31;40;92.6 MHz;2015-08-12T10:21:42Z
    2406246A68636574;31;40;92.6 MHz;2015-08-12T10:21:42Z
    2406846361A2AC00;31;40;92.6 MHz;2015-08-12T10:21:42Z
    24060469E0CD5245;31;40;92.6 MHz;2015-08-12T10:21:42Z
    240634700647CD46;31;40;92.6 MHz;2015-08-12T10:21:42Z

The format follows this pattern::
    
    <rds>;<signal>;<par2>;<freq>;<ts>

where:

- `<rds>`: RDS data in hexa. May contain `*` in place, where content cannot be decoded.
- `<signal>`: strength of signal.
- `<par2>`: ??not sure, what is the meaning.
- `<freq>`: Frequency on which we are receiving.
- `<ts>`: Timestamp in ISO format expressed in UTC. Must follow
  `YYYY-MM-DDTHH:MM:SSZ` format. Using precission of whole seconds.

Beside of lines in described format, other lines may appear. Utilities are
usually taking the lines as they are and not doing any transformation of them.

Quick start
===========

Assuming, you have couple of directories with RDS files and you want to create
one large RDS file for processing by RDSTMCCruncher, one would do::

    $ find . -name "*.rds" | rds_sort | rds_concat > big.rds

On MS Windows one would achive the same::

    $ dir -s -b *.rds | rds_sort | rds_concat > big.rds

Would there be any time overlaps, problems would be printed to stderr and
status code 1 would be returned.

Resulting file would contain all lines form all the listed RDS files and if
there are no time overlaps detected, all records woudl be sorted according to
reported timestamp.

One could then process the RDS file, e.g. using command `RDSTMCCruncher` (this
is out of scope of this package documentation).

Commands
========

Accessing help for commands
---------------------------

All provided commands provide help, when using with `--help` switch.


`rds_cycle`: Cycle content of RDS files
---------------------------------------

Having one or more RDS files, with `rds_cycle` one can start replaying the
content in real pace with rate of 11.4 RDS groups a second. Typically, one
pipes the output to `zmqc` command and publish it on ZeroMQ PUB socket
(RDSTMCCruncher is able to consume from such socket remotely).

To show command help::

    $ rds_cycle --help
    rds_cycle
    Usage:
        rds_cycle <rds_file>...

    Reads RDS files in cycle and prints their lines in rate of
    11.4 lines per second.

    All lines following RDS data pattern

        2406046AE0CD4749;33;40;92.6 MHz;2015-08-12T10:36:31Z
        24062469692E2043;33;40;92.6 MHz;2015-08-12T10:36:31Z
        2406046FE0CD4E41;31;40;92.6 MHz;2015-08-12T10:36:32Z

    get timestamp updated to the current one.

    All other lines are printed unchanged.

Assuming you have files `A.rds` and `B.rds`, replay them in following way::

    $ rds_cycle A.rds B.rds
    2406046AE0CD4749;33;40;92.6 MHz;2015-08-12T10:36:31Z
    24062469692E2043;33;40;92.6 MHz;2015-08-12T10:36:31Z
    2406046FE0CD4E41;31;40;92.6 MHz;2015-08-12T10:36:32Z
    ....

The records appeare continually and files are cycled over and over, so to stop
it, one must canceld te command.

If you want to publish the data to ZeroMQ socket on port 5555 on localhost (and
assuming you have `zmqc` command installed), use the command as follows::

    $ rds_cycle A.rds B.rds|zmqc -b -w PUB "tcp://*:5555"

You may consume the stream from another console to see the records flowing::

    $ zmqc -c -r SUB tcp://localhost:5555
    24060468E0CD522D;33;40;92.6 MHz;2015-08-12T19:02:35Z
    240624686E6F7374;33;40;92.6 MHz;2015-08-12T19:02:35Z
    24060469E0CD5245;33;40;92.6 MHz;2015-08-12T19:02:35Z
    240634704080CD46;33;40;92.6 MHz;2015-08-12T19:02:36Z
    2406846391911698;33;40;92.6 MHz;2015-08-12T19:02:36Z
    2406046AE0CD4749;33;40;92.6 MHz;2015-08-12T19:02:36Z
    24062469692E2043;33;40;92.6 MHz;2015-08-12T19:02:36Z
    ....

The timestamp of records shall show current time (expressed in UTC).


`rds_sort`: Sort RDS files by time
----------------------------------

Assuming you have bunch of RDS files in one or more directories, `rds_sort`
allows sorting the file names according to time expressed in first RDS record
in each file. This is often intermediate step in creating larger RDS file (see
`rds_concat` later on).

Check the help::

    $ rds_sort --help
    rds_sort - Sort RDS files by time of first RDS record
    Usage:
        rds_sort

    File names are given on stdin.

    List of sorted file names is printed to stdout.

    "Age" of the file is determined by reading the first valid RDS record in the
    file and using timestamp mentioned there.

    If there are two files having the same timestamp (which are expressed with
    precission of seconds) in the first RDS record, the command returns status 1.


.. note:: File names are not specified as positional arguments, but on stdin.
          This is to allow processing large number of RDS files, where it would
          be easy to reach limits of command line argument number or total
          argument name. Using `stdin` instead allows sorting much more file names.


Assuming you have a directory of RDS files named `rds`::

    $ ls rds/*.rds | rds_sort
    rawrds_2014-01-23T23-28-04Z
    rawrds_2014-01-24T00-28-06Z
    rawrds_2014-01-24T01-28-07Z
    rawrds_2014-01-24T02-28-08Z
    rawrds_2014-01-24T03-28-10Z
    rawrds_2014-01-24T04-28-11Z
    rawrds_2014-01-24T05-28-12Z
    rawrds_2014-01-24T06-28-14Z
    rawrds_2014-01-24T07-28-15Z
    rawrds_2014-01-24T08-28-16Z
    rawrds_2014-01-24T09-28-18Z

Note, that if you have datetime encoded in file name, the task seems easy, but
if you are not sure, `rds_sort` would deal even with randomly named files.

Output of `rds_sort` is usually piped into `rds_concat` or saved into a file to reuse in later calls

Output of `rds_sort` is usually piped into `rds_concat` or saved into a file to
reuse in later calls.


.. warning:: If there multiple files, reporting exactly the same second in
             first record, the command will complain to stderr, return status
             code 1, but will still print the result.

`rds_concat`: Concatenate RDS records from set of RDS files
-----------------------------------------------------------

It reads file names from stdin and prints to stdout all lines from all the files::

    $ rds_concat --help
    rds_concat - Concatenate RDS records from set of RDS files
    Usage:
        rds_concat

    File names are given on stdin.

    It reads file names from stdin and prints to stdout all lines from all the
    files.

    If there are timestamp overlaps (last record of last file reports later datetime
    than fist record in following file), warnings are printed to stderr and the
    command exists with exit code 1

First, create list of files sorted from the olderst to the newest one (in
regards to first RDS record datetime). Good option is using `rds_sort`. Pipe
the file names into `rds_concat` command::

    
    $ ls rds/*.rds | rds_sort | rds_concat
    2406846391911698;33;40;92.6 MHz;2015-08-12T10:21:41Z
    24060468E0CD522D;33;40;92.6 MHz;2015-08-12T10:21:41Z
    240624686E6F7374;33;40;92.6 MHz;2015-08-12T10:21:41Z
    24060469E0CD5245;33;40;92.6 MHz;2015-08-12T10:21:41Z
    240634704080CD46;33;40;92.6 MHz;2015-08-12T10:21:41Z
    2406846391911698;33;40;92.6 MHz;2015-08-12T10:21:41Z
    2406046AE0CD4749;33;40;92.6 MHz;2015-08-12T10:21:41Z
    24062469692E2043;33;40;92.6 MHz;2015-08-12T10:21:41Z
    2406046FE0CD4E41;31;40;92.6 MHz;2015-08-12T10:21:42Z
    2406846361A2AC00;31;40;92.6 MHz;2015-08-12T10:21:42Z
    24060468E0CD522D;31;40;92.6 MHz;2015-08-12T10:21:42Z
    ....continued with records from all the files...

In case, there are time overlaps (typically last record of a file is newer than
the first of next one), program prints to stdout complains, exits with status
code 1, but proceeds with printing the records to stdout.

Records lacking usable timestamp are printed to the output too (without warning).

Time overlaps inside of any RDS file are detected too.
