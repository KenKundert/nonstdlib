from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class Info(object):
    """
    A class used to quickly create a utility object. Any named argument to the 
    constructor are made attributes, and it returns None if you request an 
    attribute that was not set.

    Examples:
    >>> class Penguins(Info):
    ...     pass
    >>> penguins = Penguins(chinstrap=2, magellanic=1)
    >>> print(penguins.chinstrap)
    2
    >>> print(penguins.gentoo)
    None
    >>> repr(penguins)
    'Penguins<chinstrap=2, magellanic=1>'
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError
        return None

    def __repr__(self):
        return '%s<%s>' % (
            self.__class__.__name__,
            ', '.join([
                '%s=%s' % (k, self.__dict__[k])
                for k in sorted(self.__dict__.keys())
            ])
        )
