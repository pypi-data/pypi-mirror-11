| |version| |downloads| |supported-versions| |supported-implementations|

.. |version| image:: http://img.shields.io/pypi/v/quoter.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/quoter

.. |downloads| image:: http://img.shields.io/pypi/dm/quoter.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/quoter

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/quoter.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/quoter

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/quoter.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/quoter


In dealing with text, one quotes values all the time. Single quotes. Double
quotes. Curly quotes. Backticks. Funny Unicode quotes. HTML or XML markup code.
*Et cetera.*

For simple cases, this isn't hard, and there a *lot* of ways to do it::

    value = 'something'
    print '{x}'.replace('x', value)             # {something}
    print "'{}'".format(value)                  # 'value'
    print "'" + value + "'"                     # 'value'
    print "{}{}{}".format('"', value, '"')      # "value"
    print ''.join(['"', value, '"'])            # "value"

But for such a simple, common task as wrapping values in surrounding text,
it looks pretty ugly, it's very low-level, and it's easy to type the wrong
character here or there. There are also some gotchas, such as when you wrap
values, some of which are strings, but others are integers or other
primtivie types--instant ``TypeError``!

The *ad hoc* nature makes textual quoting tiresome and error-prone. It's
never more so than when you're constructing multi-level quoted strings, such
as Unix command line arguments, SQL commands, or HTML attributes.

So this module provides an clean, consistent, higher-level alternative.
Beyond just a better API, it also provides a mechanism to pre-define quoting
styles that can then be later easily reused.

Usage
=====

::

    from quoter import *

    print single('this')       # 'this'
    print double('that')       # "that"
    print backticks('ls -l')   # `ls -l`
    print braces('curlycue')   # {curlycue}

.. |laquo| unicode:: 0xAB .. left angle quote
    :rtrim:
.. |raquo| unicode:: 0xBB .. right angle quote
    :ltrim:
.. |lsquo| unicode:: 0x2018 .. left angle quote
    :rtrim:
.. |rsquo| unicode:: 0x2019 .. right angle quote
    :ltrim:
.. |ldquo| unicode:: 0x201C .. left angle quote
    :rtrim:
.. |rdquo| unicode:: 0x201D .. right angle quote
    :ltrim:

It pre-defines callable ``Quoters`` for a handful of the most common quoting styles:

 *  ``braces``  {example}
 *  ``brackets`` [example]
 *  ``angles`` <example>
 *  ``parens`` (example)
 *  ``double`` "example"
 *  ``single`` 'example'
 *  ``backticks`` \`example\`
 *  ``anglequote`` |laquo| example |raquo|
 *   ``curlysingle`` |lsquo| example |rsquo|
 *   ``curlydouble`` |ldquo| example |rdquo|

But there are a *huge* number of ways you might want to wrap or quote text. Even
considering just "quotation marks," there are `well over a dozen
<http://en.wikipedia.org/wiki/Quotation_mark_glyphs>`_. There are also `numerous
bracketing symbols in common use <http://en.wikipedia.org/wiki/Bracket>`_.
That's to say nothing of the constructs seen in markup, programming, and
templating languages. So ``quoter`` couldn't possibly provide an option
for every possible quoting style. Instead, it provides a general-purpose
mechanism for defining your own::

    from quoter import Quoter

    bars = Quoter('|')
    print bars('x')                    # |x|

    plus = Quoter('+','')
    print plus('x')                    # +x

    para = Quoter('<p>', '</p>')
    print para('this is a paragraph')  # <p>this is a paragraph</p>

    variable = Quoter('${', '}')
    print variable('x')                # ${x}

Note that ``bars`` is specified with just one symbol. If only one is given,
the prefix and suffix are considered to be identical. If you really only want
a prefix or a suffix, and not both, then instantiate the ``Quoter`` with two, one
of which is an empty string, as in ``plus`` above.

In most cases, it's cleaner and more efficient to define a style, but
there's nothing preventing you from an on-the-fly usage::

    print Quoter('+[ ', ' ]+')('castle')   # +[ castle ]+

Formatting and Encoding
=======================

The Devil, as they say, is in the details. We often don't just want quote
marks wrapped around values. We also want those values set apart from
the rest of the text. ``quoter`` supports this with ``padding`` and ``margin``
settings patterned on the `CSS box model <http://www.w3.org/TR/CSS2/box.html>`_.
In CSS, moving out from content one finds padding, a border, and then a margin.
Padding can be thought of as an internal margin, and
the prefix and suffix strings like the border. With that in mind::

    print braces('this')                      # '{this}'
    print braces('this', padding=1)           # '{ this }'
    print braces('this', margin=1)            # ' {this} '
    print braces('this', padding=1, margin=1) # ' { this } '

If desired, the ``padding`` and ``margin`` can be given as
strings, though usually they will be integers specifying the
number of spaces surrounding the text.

One can also define the ``encoding`` used for each call, per instance, or
globally. If some of your quote symbols use Unicode characters, yet your output
medium doesn't support them directly, this is an easy fix. E.g.::

    Quoter.options.encoding = 'utf-8'
    print curlydouble('something something')

Now ``curlydouble`` will output UTF-8 bytes. But in general, this is not a
great idea; you should work in Unicode strings in Python, encoding or
decoding only at the time of input and output, not as each piece of content
is constructed.

Shortcuts
=========

One often sees very long function calls and expressions as text parts are being
assembled. In order to reduce this problem, ``quoter`` defines aliases for
``single``, ``double``, and ``triple`` quoting, as well as ``backticks``, and
double backticks::

    from quoter import qs, qd, qt, qb, qdb

    print qs('one'), qd('two'), qt('three'), qb('and'), qdb('four')
    # 'one' "two" """three""" `and` ``four``

You can, of course, define your own aliases as well, and/or redefine existing
styles. If, for example, you like ``braces`` but wish it added a padding space
by default, it's simple to redefine::

    braces = Quoter('{', '}', padding=1, name='braces')
    print braces('braces plus spaces!')  # '{ braces plus spaces! }'

You could still get the no-padding variation with::

    print braces('no space braces', padding=0) # '{no space braces}'

Clean Imports
=============

As an organizational assist, quoters are available as
named attributes of a pre-defined ``quote`` object. For those
who like strict, minialist imports, this permits
``from quoter import quote`` without loss of generality. For example::

    from quoter import quote

    quote.double('test')    # "test"
    quote.braces('test')    # {test}
    # ...and so on...

Each of these can also serve like an instance of an enumerated type,
specifying for a later time what kind of quoting you'd like. Then,
at the time that quoter is needed, it can simply be called. E.g.::

    preferred_quoting = quote.brackets

    ...

    print preferred_quoting(data)

HTML
====

There is an extended quoting mode designed for XML and
HTML construction.

Instead of prefix and suffix strings, they use tag names. Or more accurately,
tag specifications in a "CSS selector" style.
like `jQuery <http://jquery.com>`_.
This is a considerable help in Python, which defines and/or reserves some of the
attribute names most used in HTML (to wit, ``class`` and ``id``). Using the CSS
selector style neatly gets around this annoyance--and is more compact
and more consistent with modern web development idioms to boot.:::

    from quoter import *

    print html.p('this is great!', {'class':'emphatic'})
    print html.p('this is great!', '.emphatic')

    print html.p('First para!', '#first')

Note that the order in which attributes appear is not guaranteed. They're
stored in ``dict`` objects, which have different orderings on diferent versions
of Python. This generally isn't a problem, in that ordering isn't significant
in HTML. But it can make testing more annoying.

HTML quoting also understands that some elements are "void" (also called
"self-closing"), meaning they do not need closing tags (and in some cases,
not even content).

So for example::

    >>> print html.br()
    <br>

    >>> print html.img('.big', src='afile')
    <img class='big' src='afile'>

You can also define your own customized quoters which can
be called functionally or, if you name
them, via the ``html.`` front-end.::

    para_e = HTMLQuoter('p.emphatic', name='para_e')
    print para_e('this is great!')
    print html.para_e('this is great?', '.question')
    print html.img(src='somefile')
    print html.br()

yields::

    <p class='emphatic'>this is great!</p>
    <p class='question'>this is great?</p>
    <img src='somefile'>
    <br>


``HTMLQuoter`` quotes attributes by default with single quotes. If you
prefer double quotes, you may set them when the element is defined::

    div = HTMLQuoter('div', attquote=double)

``HTMLQuoter`` basically works (see the tests for verification and
inspiration on how to use it), but buyer beware: It's trying to map to more
complex rules than the rest of the module, and is not as extensively tested.

XML
===

There is also an ``XMLQuoter`` with an ``xml`` front-end. It offers
one additional attribute beyond ``HTMLQuoter``:
``ns`` for namespaces. Thus::

    item = XMLQuoter(tag='item', ns='inv', name='item inv_item')
    print item('an item')
    print xml.item('another')
    print xml.inv_item('yet another')
    print xml.thing('something')

yields::

    <inv:item>an item</inv:item>
    <inv:item>another</inv:item>
    <inv:item>yet another</inv:item>
    <thing>something</thing>

Note that ``item`` was given two names. Multiple aliases are supported.

In general, ``xml.tagname`` auto-generates quoters just like ``html.tagname`` does
on first use. There are also pre-defined utility methods such as
``html.comment()`` and ``xml.comment()`` for commenting
purposes.

Named Styles
============

Quoting via the functional API or the attribute-accessed front-ends
(``quote``, ``html``, and ``xml``) is probably the easiest way to go. But
there's one more way. If you provide the name of a defined style via the
``style`` attribute, that's the style you get. So while
``quote('something')`` gives you single quotes by default (``'something'``),
if you invoke it as ``quote('something', style='double')``, you get double
quoting as though you had used ``quote.double(...)``, ``double(...)``, or
``qd(...)``. This even works through named front.ends;
``quote.braces('something', style='double')`` still gets you
``"something"``. If you don't want to be confused by such double-bucky
forms, don't use them. The best use-case for named styles is probably when
you don't know how something will be quoted (or what tag it will use, in the
HTML or XML case), but that decision is made dynamically. Then
``style=desired_style`` makes good sense.

Style names are stored in the class of the quoter. So all ``Quoter``
instances share the same named styles, as do ``HTMLQuoter``, ``XMLQuoter``,
and ``LambdaQuoter``.

Dynamic Quoters
===============

It is possible to define ``Quoters`` that don't just concatenate text, but
that examine it and provide dynamic rewriting on the fly. For example,
in finance, one often wants to present numbers with a special formatting::

    from quoter import LambdaQuoter

    f = lambda v: ('(', abs(v), ')') if v < 0 else ('', v, '')
    financial = LambdaQuoter(f)
    print financial(-3)            # (3)
    print financial(45)            # 45

    password = LambdaQuoter(lambda v: ('', 'x' * len(v), ''))
    print password('secret!')      # xxxxxxx

    wf = lambda v:  ('**', v, '**') if v < 0 else ('', v, '')
    warning = LambdaQuoter(wf, name='warning')
    print warning(12)              # 12
    print warning(-99)             # **-99**

The trick is instantiating ``LambdaQuoter`` with a callable (e.g. ``lambda``
expression or function) that accepts one value and returns a tuple of three
values: the quote prefix, the value (possibly rewritten), and the suffix.

You can access ``LambdaQuoter`` named instances through ``lambdaq`` (because
``lambda`` is a reserved word). Given the code above, ``lambdaq.warning``
is active, for example.

``LambdaQuoter`` is an edge case, arcing over towards being
a general formatting function. That has the virtue of
providing a consistent mechanism for tactical output transformation
with built-in margin and padding support. It's also able to encapsulate
complex quoting / representation decisions that would otherwise muck
up "business logic," making representation code much more unit-testable.
But, one could argue that
such full transformations are "a bridge too far" for a quoting module.
So use the dynamic component of``quoter``, or not, as you see fit.

Notes
=====

 * Version 1.1 cleans up HTML quoting, esp. re void / self-closing elements.
   Added new double-backtick functions. Changed to Apache License 2.0.
   Updated docs and testing matrix.

 * See ``CHANGES.rst`` for more complete change log.

 * ``quoter`` provides simple transformations that could be alternatively
   implemented as a series of small functions. The problem is that such "little
   functions" tend to be constantly re-implemented, in different ways, and
   spread through many programs. That need to constantly re-implement such
   common and straightforward text formatting has led me to re-think how
   software should format text. ``quoter`` is one facet of a project to
   systematize higher-level formatting operations. See `say <http://pypi.python.org/pypi/say>`_
   and `show <http://pypi.python.org/pypi/show>`_
   for other parts of the larger effort.

 * ``quoter`` is also a test case for `options <http://pypi.python.org/pypi/options>`_,
   a module that supports flexible option handling. In fact, it is one of ``options`` most
   extensive test cases, in terms of subclassing and dealing with named styles.

 * In the future, additional quoting styles such as ones for Markdown or RST format
   styles might appear. It's not hard to subclass ``Quoter`` for new languages.

 *  Automated multi-version testing managed with `pytest
    <http://pypi.python.org/pypi/pytest>`_ and `tox
    <http://pypi.python.org/pypi/tox>`_.
    Packaging linting with `pyroma <https://pypi.python.org/pypi/pyroma>`_.

    Successfully packaged for, and
    tested against, all late-model versions of Python: 2.6, 2.7, 3.2, 3.3,
    3.4, and 3.5 pre-release (3.5.0b3) as well as PyPy 2.6.0 (based on
    2.7.9) and PyPy3 2.4.0 (based on 3.2.5).

 * The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_ or
   `@jeunice on Twitter <http://twitter.com/jeunice>`_ welcomes your comments
   and suggestions.

Installation
============

To install or upgrade to the latest version::

    pip install -U quoter

To ``easy_install`` under a specific Python version (3.3 in this example)::

    python3.3 -m easy_install --upgrade quoter

(You may need to prefix these with ``sudo`` to authorize
installation. In environments without super-user privileges, you may want to
use ``pip``'s ``--user`` option, to install only for a single user, rather
than system-wide.)
