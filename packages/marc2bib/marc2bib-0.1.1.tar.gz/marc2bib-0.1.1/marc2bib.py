__all__ = ['convert']

from pymarc import MARCReader


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
    val = record['260']['c']
    return val[1:-1]

BOOK_TAGFUNCS = {
    'author': get_author,
    'edition': get_edition,
    'publisher': get_publisher,
    'title': get_title,
    'year': get_year,
}


def _as_bibtex(bibtype, bibkey, fields):
    bibtex = '@{0}{{{1}'.format(bibtype, bibkey)
    for tag, value in sorted(fields.items()):
        bibtex += ',\n {0} = {{{1}}}'.format(tag, value)
    bibtex += '\n}\n'
    return bibtex

def convert(record, bibtype='book', bibkey=None, tagfuncs=None):
    tagfuncs_ = BOOK_TAGFUNCS.copy()
    if tagfuncs:
        tagfuncs_.update(tagfuncs)

    if bibkey is None:
        surname = get_author(record).split(',')[0].split()[-1]
        bibkey = surname + get_year(record)

    fields = {}
    for tag, func in tagfuncs_.items():
        value = func(record)
        if not isinstance(value, str):
            msg = ("Return value from {} for {} tag "
                   "should be a string").format(func, tag)
            raise TypeError(msg)
        fields[tag] = func(record)

    return _as_bibtex(bibtype, bibkey, fields)
