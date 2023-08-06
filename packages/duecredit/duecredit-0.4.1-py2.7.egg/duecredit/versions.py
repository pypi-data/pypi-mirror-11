# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the duecredit package for the
#   copyright and license terms.   Originates from datalad package distributed
#   under MIT license
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Module to help maintain a registry of versions for external modules etc
"""
import sys
from six import string_types

from distutils.version import StrictVersion, LooseVersion

# To depict an unknown version, which can't be compared by mistake etc
class UnknownVersion:
    """For internal use
    """

    def __str__(self):
        return "UNKNOWN"

    def __cmp__(self, other):
        if other is self:
            return 0
        raise TypeError("UNKNOWN version is not comparable")


class ExternalVersions(object):
    """Helper to figure out/use versions of the external modules.

    It maintains a dictionary of `distuil.version.StrictVersion`s to make
    comparisons easy.  If version string doesn't conform the StrictVersion
    LooseVersion will be used.  If version can't be deduced for the module,
    'None' is assigned
    """

    UNKNOWN = UnknownVersion()

    def __init__(self):
        self._versions = {}

    @classmethod
    def _deduce_version(klass, module):
        version = None
        for attr in ('__version__', 'version'):
            if hasattr(module, attr):
                version = getattr(module, attr)
                break

        if isinstance(version, tuple) or isinstance(version, list):
            #  Generate string representation
            version = ".".join(str(x) for x in version)

        if version:
            try:
                return StrictVersion(version)
            except ValueError:
                # let's then go with Loose one
                return LooseVersion(version)
        else:
            return klass.UNKNOWN

    def __getitem__(self, module):
        if not isinstance(module, string_types):
            modname = module.__name__
        else:
            modname = module
            module = None

        if modname not in self._versions:
            if module is None:
                if modname not in sys.modules:
                    try:
                        module = __import__(modname)
                    except ImportError:
                        return None
                else:
                    module = sys.modules[modname]

            self._versions[modname] = self._deduce_version(module)

        return self._versions.get(modname, self.UNKNOWN)

external_versions = ExternalVersions()
