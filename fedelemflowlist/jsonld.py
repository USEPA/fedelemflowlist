"""Writes flow list and mapping files to a JSON-LD zip archive using olca library."""
import datetime
import logging as log
import math
import os
import uuid
from typing import Optional

import olca
import olca.units as units
import olca.pack as pack
import pandas as pd
from esupy.util import make_uuid

import fedelemflowlist
from fedelemflowlist.globals import flow_list_specs


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


def _s(val) -> Optional[str]:
    """Returns the string value of the given value or None if the value is `None`, `NaN`, or `""`."""
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
        """
        Creates a dictionary for an olca json file
        :return: dictionary
        """
        flow_ref = olca.FlowRef()
        flow_ref.name = self.name
        if self.category is not None:
            flow_ref.category_path = self.category.split('/')

        # set the UUID or generate it from the attributes
        if self.uid is None:
            flow_ref.id = make_uuid("Flow",
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

        return json


class _MapEntry(object):
    """Describes a mapping entry in the Fed.LCA flow list."""

    def __init__(self, row):

        self.source_list = _s(row['SourceListName'])

        # source flow attributes
        s_flow = _MapFlow()
        self.source_flow = s_flow
        s_flow.name = _s(row['SourceFlowName'])
        s_flow.uid = _s(row['SourceFlowUUID'])
        s_flow.category = _s(row['SourceFlowContext'])
        s_flow.unit = _s(row['SourceUnit'])

        # traget flow attributs
        t_flow = _MapFlow()
        self.target_flow = t_flow
        t_flow.name = _s(row['TargetFlowName'])
        t_flow.uid = _s(row['TargetFlowUUID'])
        t_flow.category = _s(row['TargetFlowContext'])
        t_flow.unit = _s(row['TargetUnit'])

        factor = row['ConversionFactor']
        if _isnum(factor):
            self.factor = factor
        else:
            self.factor = 1.0

    def to_json(self) -> dict:
        """
        Create an olca json mapping dictionary
        :return: dictionary
        """
        return {
            'from': self.source_flow.to_json(),
            'to': self.target_flow.to_json(),
            'conversionFactor': self.factor,
        }


class Writer(object):
    """Class for writing flows and mappings to json."""

    def __init__(self, flow_list: pd.DataFrame,
                 flow_mapping: pd.DataFrame = None):
        self.flow_list = flow_list
        self.flow_mapping = flow_mapping
        self._context_uids = {}

    def write_to(self, path: str):
        """
        Writes json dictionaries to files
        :param path: string path to file
        :return: None
        """
        if os.path.exists(path):
            log.warning("File %s already exists and will be overwritten", path)
            os.remove(path)
        pw = pack.Writer(path)
        self._write_categories(pw)
        self._write_flows(pw)
        if self.flow_mapping is not None:
            self._write_mappings(pw)
        pw.close()

    def _write_categories(self, pw: pack.Writer):

        root = olca.Category()
        root.id = "f318fa60-bae9-361f-ad5a-5066a0e2a9d1"
        root.name = "Elementary flows"
        root.model_type = olca.ModelType.FLOW
        self._context_uids[root.name.lower()] = root.id
        pw.write(root)

        for _, row in self.flow_list.iterrows():
            path = row['Context']
            if not isinstance(path, str):
                continue
            path = path.strip()
            if path == '' or path.lower() in self._context_uids:
                continue
            parts = path.split("/")
            parent_id = root.id
            for i in range(0, len(parts)):
                lpath = "/".join(parts[0:i+1]).lower()
                uid = self._context_uids.get(lpath)
                if uid is not None:
                    parent_id = uid
                    continue
                uid = make_uuid("Flow", lpath)
                log.info("create category %s", lpath)
                c = olca.Category()
                c.id = uid
                c.name = parts[i]
                c.category = olca.ref(olca.Category, parent_id)
                c.model_type = olca.ModelType.FLOW
                pw.write(c)
                self._context_uids[lpath] = uid
                parent_id = uid

    def _write_flows(self, pw: pack.Writer):
        altflowlist=fedelemflowlist.get_alt_conversion()
        for _, row in self.flow_list.iterrows():
            description = "From FedElemFlowList_"+flow_list_specs['list_version']+'.'
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
            flow.version = flow_list_specs['list_version']
            flow.synonyms = row.get("Synonyms")
            flow.last_change = datetime.datetime.now().isoformat()
            flow.flow_type = olca.FlowType.ELEMENTARY_FLOW

            context_uid = self._context_uids.get(row['Context'].lower())
            if context_uid is not None:
                flow.category = olca.ref(olca.Category, context_uid)

            fp = olca.FlowPropertyFactor()
            fp.reference_flow_property = True
            fp.conversion_factor = 1.0
            fp.flow_property = units.property_ref(row["Unit"])
            if fp.flow_property is None:
                log.warning("unknown unit %s in flow %s",
                            row["Unit"], row["Flow UUID"])
            flow.flow_properties = [fp]
            #Add in alternate unit flow propert(ies), if an alternate unit exists
            #in the flows list, uses short list of altflowlist to assign one or more
            #alternate units
            if row["AltUnit"] is not None:
                #create dataframe of all alternate units for this flowable
                altunits=altflowlist[altflowlist['Flowable']==row["Flowable"]]
                for i, alternate in altunits.iterrows():
                    altfp = olca.FlowPropertyFactor()
                    altfp.reference_flow_property = False
                    altfp.conversion_factor = alternate['AltUnitConversionFactor']
                    altfp.flow_property = units.property_ref(alternate["AltUnit"])
                    if altfp.flow_property is None:
                        log.warning("unknown altunit %s in flow %s",
                                    alternate["AltUnit"], row["Flow UUID"])
                    else:
                        flow.flow_properties.append(altfp)
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
