"""
Methods for UUID generation.

For flows, contexts, uses UUID3 function from UUID package to generate IDs from
strings.
"""

import uuid
from fedelemflowlist.globals import as_path


def generate_flow_uuid(flowable, directionality, compartment, unit):
    """
    Generates uuid for a flow
    :param flowable:
    :param directionality:
    :param compartment:
    :param unit:
    :return: string uuid
    """
    flow = flowable + directionality + compartment + unit
    flowid = str(uuid.uuid3(uuid.NAMESPACE_OID, flow))
    return flowid


def generate_context_uuid(*args: str):
    """
    Generates uuid for a context
    :param args: variable list of context elements
    :return: string uuid
    """
    context = as_path(*args)
    contextid = str(uuid.uuid3(uuid.NAMESPACE_OID, context))
    return contextid


def make_uuid(*args: str) -> str:
    """
    Generic wrapper of uuid.uuid3 method for uuid generation
    :param args: variable list of strings
    :return: string uuid
    """
    path = as_path(*args)
    return str(uuid.uuid3(uuid.NAMESPACE_OID, path))
