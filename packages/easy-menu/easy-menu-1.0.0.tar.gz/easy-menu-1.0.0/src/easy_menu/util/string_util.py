from unicodedata import east_asian_width

__unicode_width_mapping = {'F': 2, 'H': 1, 'W': 2, 'Na': 1, 'A': 2, 'N': 1}


def unicode_width(s):
    if not isinstance(s, unicode):
        return len(s)
    return sum(__unicode_width_mapping[east_asian_width(c)] for c in s)


def to_unicode(s, encoding=None, errors='strict'):
    """
    Make unicode string from any value
    :param s:
    :param encoding:
    :param errors:
    :return: unicode
    """
    encoding = encoding or 'utf-8'

    if isinstance(s, unicode):
        return s
    elif isinstance(s, str):
        return s.decode(encoding, errors)
    else:
        return str(s).decode(encoding, errors)


def edge_just(left, right, width, fillchar=' '):
    padding = fillchar * max(1, width - unicode_width(left + right))
    return left + padding + right
