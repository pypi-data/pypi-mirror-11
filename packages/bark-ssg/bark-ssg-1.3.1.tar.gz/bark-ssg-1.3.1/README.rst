====
Bark
====

Bark is a single file static site generator. I set out to make it primarily because I got tired of dealing with Jekyll and didn't want to put a bunch of effort into tweaking Pelican to look alright.

I hope to continually improve it so perhaps others might find it useful.

--------
Features
--------

* Single file
* Jinja2 templating language
* Posts support markdown formatting thanks to Hoedown with SmartyPants.

------------
Installation
------------

You can install using the source by simply using::

    python setup.py install --user

or::

    sudo python setup.py install
    
for system wide installation.

-----
Usage
-----

You can get the usage by using ``-h``, ``--help``, or ``bark``.

    Usage:
        bark new <name>
        bark make [<settings>]

    Options:
        -h --help  Show this screen.
        --version  Show version.

------------
Contributing
------------

If something is wrong or could be improved, let me know or submit a pull request.
