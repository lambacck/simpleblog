==========
simpleblog
==========

A simple blog for Django 1.4

Installation of Dependencies
============================

First, make sure you are using virtualenv (http://www.virtualenv.org)::

    $ mkvirtualenv --distribute simpleblog

You will also need to ensure that the virtualenv has the project directory
added to the path. Adding the project directory will allow `django-admin.py` to be able to change settings using the `--settings` flag.

In Linux and Mac OSX, you can install virtualenvwrapper (http://http://virtualenvwrapper.readthedocs.org/en/latest/), which will take care of adding the project path to the `site-directory` for you::

    $ cd icecream && add2virtualenv `pwd`

In Windows, or if you're not comfortable using the command line, you will need
to add a `.pth` file to the `site-packages` of your virtualenv. If you have
been following the book's example for the virtualenv directory (pg. 12), then
you will need to add a python pathfile named `_virtualenv_path_extensions.pth`
to the `site-packages`. If you have been following the book, then your
virtualenv folder will be something like::

`~/.virtualenvs/icecream/lib/python2.7/site-directory/`

In the pathfile, you will want to include the following code (from
virtualenvwrapper):

    import sys; sys.__plen = len(sys.path)
    /home/<youruser>/icecream/icecream/
    import sys; new=sys.path[sys.__plen:]; del sys.path[sys.__plen:]; p=getattr(sys,'__egginsert',0); sys.path[p:p]=new; sys.__egginsert = p+len(new)

Virtualenvwrapper takes care of this for you by creating the exact same file
using the `add2virtualenv` command (see above).

Then, depending on where you are installing dependencies:

In development::

    $ pip install -r requirements/local.txt

For production::

    $ pip install -r requirements.txt

*note: We install production requirements this way because many Platforms as a Services expect a requirements.txt file in the root of projects.*

Acknowledgements
================


