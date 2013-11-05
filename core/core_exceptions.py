"""
Exceptions used by core algorithms.
"""

class UnsurePathException(Exception):
    """
    Used when the directory structures may have been messed up. Note that
    depending on how you cloned the repo/local directory structure, you may have
    to edit the package_root and package_directory variables in utils.py to
    avoid this Exception.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Unexpected directory structure. Cannot positively locate: " + repr(self.value)
