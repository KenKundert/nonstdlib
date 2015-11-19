#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

# wrap and indent both largely duplicate functions of the same name from the 
# standard textwrap module.
#
# -Ken

def wrap(*lines, **options):
    """ Combines the lines given in the list argument into a single string 
    wrapped to fit inside an 80-character (by default) display.  Both the 
    indentation and the terminal width can be controlled using keyword 
    arguments. """

    indent = options.get('indent', 0) * ' '
    columns = options.get('columns', 79)

    input = ''.join(lines)
    words = re.split('( )+', input)

    line = indent
    lines = []

    for word in words:
        if len(line) + len(word) + 1 < columns:
            line += word
        else:
            lines.append(line)
            line = indent + word.strip()

    lines.append(line)

    return '\n'.join(lines)

def plural(count, singular, plural=None):
    if plural is None: plural = singular + 's'
    return singular if count == 1 else plural

def indent(string, indent='  '):
    return indent + string.replace('\n', '\n' + indent)

def conjoin(lst, conj=' and ', sep=', '):
    # Like join, but supports a conjunction
    """
    Conjunction Join
    Return the list joined into a string, where conj is used to join the last
    two items in the list, and sep is used to join the others.

    Examples:
    >>> conjoin([], ' or ')
    u''
    >>> conjoin(['a'], ' or ')
    u'a'
    >>> conjoin(['a', 'b'], ' or ')
    u'a or b'
    >>> conjoin(['a', 'b', 'c'])
    u'a, b and c'
    """
    if type(lst) == set:
        lst = list(lst)
        lst.sort()
    if conj != None and len(lst) > 1:
        lst = lst[0:-2] + [lst[-2] + conj + lst[-1]]
    return sep.join(lst)

def fmt(message, *args, **kwargs):
    r"""
    Convert a message with embedded attributes to a string. The values for the 
    attributes can come from the argument list, as with ''.format(), or they may 
    come from the local scope (found by introspection).

    Examples:
    >>> from logger import fmt
    >>> s = 'str var'
    >>> d = {'msg': 'dict val'}
    >>> class Class:
    ...     a = 'cls attr'

    >>> print(fmt("by order: {0}, {1[msg]}, {2.a}.", s, d, Class))
    by order: str var, dict val, cls attr.
    >>> print(fmt("by name: {S}, {D[msg]}, {C.a}.", S=s, D=d, C=Class))
    by name: str var, dict val, cls attr.

    The following works, but does not work with doctests
    # >>> print(fmt("by magic: {s}, {d[msg]}, {c.a}."))
    # by magic: str var, dict val, cls attr.
    """
    import inspect

    # Inspect variables from the source frame.
    frame = inspect.stack()[-1][0]

    # Collect all the variables in the scope of the calling code, so they 
    # can be substituted into the message.
    attrs = {}
    attrs.update(frame.f_globals)
    attrs.update(frame.f_locals)
    attrs.update(kwargs)

    return message.format(*args, **attrs)

if __name__ == "__main__":

    sig = '\n\n-fuxit'
    print(fmt(wrap(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi ',
            'lobortis posuere rutrum. Nam eu aliquam dolor. Fusce eleifend ',
            'facilisis nisi in blandit. Donec vitae turpis ipsum. In leo ',
            'justo, sollicitudin id tristique at, accumsan vitae nunc. In ',
            'dapibus, lorem sed congue porta, urna enim vulputate nunc, sit ',
            'amet luctus elit lectus vitae ipsum. Maecenas at velit velit. ',
            'Ut dignissim massa sit amet nisl pretium quis pharetra eros ',
            'pharetra. Nulla scelerisque arcu et sapien commodo ac mollis ',
            'turpis facilisis. Aenean ut justo at nibh posuere pulvinar. ',
            'Pellentesque ornare laoreet libero eget vulputate. Fusce ',
            'vehicula, metus ac commodo adipiscing, turpis eros semper ',
            'dolor, vel scelerisque purus tellus quis leo. Donec pulvinar ',
            'ullamcorper arcu, quis scelerisque orci ornare nec. Donec ',
            'vitae urna ac arcu ultricies posuere. Morbi fermentum molestie ',
            'libero, eu ultricies orci placerat eget.{sig}',
            columns=40, indent=4)))
