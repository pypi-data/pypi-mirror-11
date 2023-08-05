"""This is a main marc2bib package file.

Make sure to check out the FAQ [1] for the MARC 21 at the Library of
Congress (LOC) website. There is a lot information located on the main
page [2] -- but first, take a look at a brief description and a summary
of the MARC 21 fields [3]. While hacking on this package, you may also
find useful both the full and concise versions of the "MARC 21 Format
for Bibliographic Data" document [4]. Information regarding the BibTeX
entry types and corresponding fields can be found in Section 3 of the
original manual dated 1988 [5].

[1] http://www.loc.gov/marc/faq.html
[2] http://www.loc.gov/marc/
[3] http://www.loc.gov/marc/umb/
[4] http://www.loc.gov/marc/bibliographic/
[5] http://ctan.uni-altai.ru/biblio/bibtex/base/btxdoc.pdf
"""

__all__ = ['convert']

from functools import reduce

from pymarc import MARCReader


def get_address(record):
    val = record['260']['a']
    return val.replace('[', '').replace(']', '').rstrip(' : ')

def get_author(record):
    val = record['245']['c']
    return val.rstrip('.')

def get_edition(record):
    return record['250']['a']

def get_publisher(record):
    val = record['260']['b']
    return val.strip(',')

def get_title(record):
    val = record['245']['a']
    return val.rstrip('/')

def get_year(record):
    # FIXME
    val = record['260']['c']
    return val.lstrip('c').rstrip('.')

BOOK_REQ_TAGFUNCS = {
    'author': get_author,
    'publisher': get_publisher,
    'title': get_title,
    'year': get_year,
}

BOOK_ADD_TAGFUNCS = {
    'address': get_address,
    'edition': get_edition,
}


def _as_bibtex(bibtype, bibkey, fields, indent):
    bibtex = '@{0}{{{1}'.format(bibtype, bibkey)
    for tag, value in sorted(fields.items()):
        bibtex += ',\n{0}{1} = {{{2}}}'.format(' ' * indent, tag, value)
    bibtex += '\n}\n'
    return bibtex

def convert(record, bibtype='book', bibkey=None, tagfuncs=None, **kw):
    tagfuncs_ = BOOK_REQ_TAGFUNCS.copy()

    include_arg = kw.get('include', 'all')
    if include_arg == 'all':
        tagfuncs_.update(BOOK_ADD_TAGFUNCS)
    elif include_arg != 'required':
        # Check if include argument is iterable and not a string.
        # We are no longer interested in a string because all
        # possible values are already passed.
        try:
            assert not isinstance(include_arg, str)
            iter(include_arg)
        except (AssertionError, TypeError) as e:
            msg = ("include should be an iterable or one of "
                   "('required', 'all'), got {}".format(include_arg))
            e.args += (msg,)
            # XXX ValueError or something like that, actually.
            raise
        else:
            req_tags = list(BOOK_REQ_TAGFUNCS.keys())
            add_tags = list(BOOK_ADD_TAGFUNCS.keys())
            if not set(include_arg).issubset(req_tags + add_tags):
                raise ValueError("include contains unknown tag(s)")

            tagsfuncs_to_include = {tag: BOOK_ADD_TAGFUNCS[tag]
                                    for tag in include_arg}
            tagfuncs_.update(tagsfuncs_to_include)

    if tagfuncs:
        tagfuncs_.update(tagfuncs)

    if bibkey is None:
        surname = get_author(record).split(',')[0].split()[-1]
        bibkey = surname + get_year(record)

    fields = {}
    for tag, func in tagfuncs_.items():
        value = func(record)
        if not isinstance(value, str):
            msg = ("Returned value from {} for {} tag "
                   "should be a string").format(func, tag)
            raise TypeError(msg)
        fields[tag] = func(record)

    field_indent = kw.get('indent', 1)
    return _as_bibtex(bibtype, bibkey, fields, field_indent)
