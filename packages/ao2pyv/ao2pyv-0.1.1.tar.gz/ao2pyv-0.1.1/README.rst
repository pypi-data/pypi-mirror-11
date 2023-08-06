ao2pyv
======

Converts Archive.org video searches into PyVideo.org API submissions.

Installation
------------

Just ``pip install ao2pyv``.

Examples
--------

The quick and easy way::

    $ ao2pyv --query 'pyconza2014' \
             --category 'PyCon ZA 2014' \
             --language 'English'

The explicit equivalent using a pipeline of commands::

    $ ao2pyv \
        source.archive-org --query 'pyconza2014' \
        transform.ao2pyv --category 'PyCon ZA 2014' --language 'English' \
        sink.json -f -

Read the help for each of the commands in the pipeline::

    $ ao2pyv --help
    $ ao2pyv source.archive-org --help
    $ ao2pyv transform.ao2pyv --help
    $ ao2pyv sink.json --help

Usage
-----

Usage: ao2pyv [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Options:

  --version            Show the version and exit.
  -q, --query TEXT     Archive.org search query
  -c, --category TEXT  Pyvideo category
  -l, --language TEXT  Pyvideo language
  --help               Show this message and exit.

Commands:

  :sink.json:           Output results to a file.
  :source.archive-org:  Search archive.org for a query and return a...
  :source.json:         Return results from a JSON file.
  :transform.ao2pyv:    Transform a video result from archive.org to...
  :transform.none:      Transform a video result not at all.
