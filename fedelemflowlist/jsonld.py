import datetime
import logging as log
import math
import os
import uuid

import fedelemflowlist as fedfl
import pandas as pd
import olca
import olca.units as units
import olca.pack as pack

from typing import Optional


def _uid(*args) -> str:
    """A helper function that creates a name based UUID. """
    path = '/'.join([str(arg).strip() for arg in args]).lower()
    return str(uuid.uuid3(uuid.NAMESPACE_OID, path))


def _isnil(val) -> bool:
    """Returns True when the given value is `None`, `NaN`, or `""`."""
    if val is None:
        return True
    if isinstance(val, float):
        return math.isnan(val)
    if isinstance(val, str):
        return val.strip() == ""
    return False


def _isnum(val) -> bool:
    """Returns true when the given value is a number."""
    if isinstance(val, (float, int)):
        return not math.isnan(val)
    return False


def _catpath(*args) -> str:
    p = ''
    for arg in args:
        if _isnil(arg):
            continue
        if p != '':
            p = p + "/"
        p = p + str(arg).strip()

    if p == 'air':
        return 'Elementary flows/emission/air'
    if p == 'ground':
        return 'Elementary flows/resource/ground'
    if p == 'soil':
        return 'Elementary flows/emission/soil'
    if p == 'water':
        return 'Elementary flows/emission/water'
    return p


def _s(val) -> Optional[str]:
    """Returns the string value of the given value or None if the value is
       `None`, `NaN`, or `""`.
    """
    if _isnil(val):
        return None
    return str(val).strip()


class _MapFlow(object):

    def __init__(self):
        self.name = None  # type: Optional[str]
        self.uid = None  # type: Optional[str]
        self.category = None  # type: Optional[str]
        self.unit = None  # type: Optional[str]

    def to_json(self) -> dict:
        flow_ref = olca.FlowRef()
        flow_ref.name = self.name
        if self.category is not None:
            flow_ref.category_path = self.category.split('/')

        # set the UUID or generate it from the attributes
        if self.uid is None:
            flow_ref.id = _uid(olca.ModelType.FLOW,
                               self.category, self.name)
        else:
            flow_ref.id = self.uid

        json = {
            'flow': flow_ref.to_json()
        }
        if self.unit is not None:
            unit_ref = units.unit_ref(self.unit)
            if unit_ref is not None:
                json['unit'] = unit_ref.to_json()
            prop_ref = units.property_ref(self.unit)
            if prop_ref is not None:
                json['flowProperty'] = prop_ref.to_json()

        return json


class _MapEntry(object):
    """ Describes a mapping entry in the Fed.LCA flow list. """

    def __init__(self, row):

        self.source_list = _s(row['SourceListName'])

        # source flow attributes
        s_flow = _MapFlow()
        self.source_flow = s_flow
        s_flow.name = _s(row['SourceFlowName'])
        s_flow.uid = _s(row['SourceFlowUUID'])
        s_flow.category = _catpath(row['SourceFlowContext'])
        s_flow.unit = _s(row['SourceUnit'])

        # traget flow attributs
        t_flow = _MapFlow()
        self.target_flow = t_flow
        t_flow.name = _s(row['TargetFlowName'])
        t_flow.uid = _s(row['TargetFlowUUID'])
        t_flow.category = _catpath(row['TargetFlowContext'])
        t_flow.unit = _s(row['TargetUnit'])

        factor = row['ConversionFactor']
        if _isnum(factor):
            self.factor = factor
        else:
            self.factor = 1.0

    def to_json(self) -> dict:
        return {
            'from': self.source_flow.to_json(),
            'to': self.target_flow.to_json(),
            'conversionFactor': self.factor,
        }


class Writer(object):

    def __init__(self, version="0.1", flow_list: pd.DataFrame = None,
                 flow_mapping: pd.DataFrame = None):
        self.version = version

        if flow_list is None:
            self.flow_list = fedfl.get_flowlist(version)  # type: pd.DataFrame
        else:
            self.flow_list = flow_list

        if flow_mapping is None:
            self.flow_mapping = fedfl.get_flowmapping(  # type: pd.DataFrame
                version)
        else:
            self.flow_mapping = flow_mapping

    def write_to(self, path: str):
        if os.path.exists(path):
            log.warning("File %s already exists and will be overwritten", path)
            os.remove(path)
        pw = pack.Writer(path)
        self._write_top_categories(pw)
        self._write_flow_compartments(pw)
        self._write_flows(pw)
        self._write_mappings(pw)
        pw.close()

    def _write_top_categories(self, pw: pack.Writer):
        # elementary flows
        root = olca.Category()
        root.id = "f318fa60-bae9-361f-ad5a-5066a0e2a9d1"
        root.name = "Elementary flows"
        root.model_type = olca.ModelType.FLOW
        pw.write(root)

        # resources
        res = olca.Category()
        res.id = "3095c63c-7962-4086-a0d7-df4fd38c2e68"
        res.name = "resource"
        res.category = olca.ref(olca.Category, root.id)
        res.model_type = olca.ModelType.FLOW
        pw.write(res)

        # emissions
        emi = olca.Category()
        emi.id = "c2433915-9ca3-3933-a64d-68d67e3e3281"
        emi.name = "emission"
        emi.category = olca.ref(olca.Category, root.id)
        emi.model_type = olca.ModelType.FLOW
        pw.write(emi)

    def _write_flow_compartments(self, pw: pack.Writer):
        handled = set()
        for _, row in self.flow_list.iterrows():
            uid = row["Compartment UUID"]
            if uid in handled:
                continue
            handled.add(uid)
            parent_uid = None
            direction = row["Directionality"].strip()
            if direction == "resource":
                parent_uid = "3095c63c-7962-4086-a0d7-df4fd38c2e68"
            elif direction == "emission":
                parent_uid = "c2433915-9ca3-3933-a64d-68d67e3e3281"
            else:
                log.error("Unknown directionality: %s", direction)
                continue
            comp = olca.Category()
            comp.id = uid
            comp.name = row["Compartment"]
            comp.model_type = olca.ModelType.FLOW
            comp.category = olca.ref(olca.Category, parent_uid)
            pw.write(comp)

    def _write_flows(self, pw: pack.Writer):
        for _, row in self.flow_list.iterrows():

            description = "From FedElemFlowList_%s." % self.version
            flow_class = row.get("Class")
            if flow_class is not None:
                description += " Flow Class: %s." % flow_class

            preferred = row.get("Preferred", 0)
            if preferred == 1 or preferred == "1":
                description += " Preferred flow."
            else:
                description += " Not a preferred flow."

            flow = olca.Flow()
            flow.description = description
            flow.id = row["Flow UUID"]
            flow.name = row["Flowable"]
            flow.cas = row.get("CAS No", None)
            flow.formula = row.get("Formula", None)
            flow.version = self.version
            flow.last_change = datetime.datetime.now().isoformat()
            flow.category = olca.ref(olca.Category, row["Compartment UUID"])
            flow.flow_type = olca.FlowType.ELEMENTARY_FLOW
            fp = olca.FlowPropertyFactor()
            fp.reference_flow_property = True
            fp.conversion_factor = 1.0
            fp.flow_property = olca.ref(
                olca.FlowProperty, row["Quality UUID"])
            flow.flow_properties = [fp]
            pw.write(flow)

    def _write_mappings(self, pw: pack.Writer):
        maps = {}
        for i, row in self.flow_mapping.iterrows():
            me = _MapEntry(row)
            m = maps.get(me.source_list)
            if m is None:
                m = []
                maps[me.source_list] = m
            m.append(me)

        for source_list, entries in maps.items():
            list_ref = olca.Ref()
            list_ref.olca_type = 'FlowMap'
            list_ref.name = source_list
            mappings = []
            flow_map = {
                '@id': str(uuid.uuid4()),
                'name': '%s -> Fed.LCA Commons' % source_list,
                'source': list_ref.to_json(),
                'mappings': mappings
            }
            for e in entries:
                mappings.append(e.to_json())
            pw.write_json(flow_map, 'flow_mappings')
