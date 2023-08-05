VERSION = (0, 0, 5)


def get_version():
    """Returns the version as a human-format string."""
    return '.'.join([str(i) for i in VERSION])

__author__ = 'dlancer'
__docformat__ = 'restructuredtext en'
__copyright__ = 'Copyright 2014-2015, dlancer'
__license__ = 'BSD License'
__version__ = get_version()
__maintainer__ = 'dlancer'
__email__ = 'dmdpost@gmail.com'
__status__ = 'Development'
