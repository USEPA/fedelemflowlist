"""
Methods for UUID generation.

For flows, contexts, uses UUID3 function from UUID package to generate IDs from
strings.
"""

import uuid
from fedelemflowlist.globals import as_path


def make_uuid(*args: str) -> str:
    """
    Generic wrapper of uuid.uuid3 method for uuid generation
    :param args: variable list of strings
    :return: string uuid
    """
    path = as_path(*args)
    return str(uuid.uuid3(uuid.NAMESPACE_OID, path))
