"""Writes flow list and mapping files to a JSON-LD zip archive using olca library."""
import datetime
import logging as log
import math
import uuid
from pathlib import Path
from typing import Optional
import pandas as pd
import json

try:
    import olca_schema as o
    import olca_schema.units as units
    import olca_schema.zipio as zipio
except ImportError:
    raise ImportError("fedelemflowlist now requires olca-schema to align with "
                      "openLCA v2.0. Use pip install olca-schema")

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
        flow_ref = o.Ref()
        flow_ref.name = self.name
        if self.category is not None:
            flow_ref.category = self.category

        # set the UUID or generate it from the attributes
        if self.uid is None:
            flow_ref.id = make_uuid("Flow", self.category, self.name)
        else:
            flow_ref.id = self.uid

        json = {
            'flow': flow_ref.to_dict()
        }
        if self.unit is not None:
            unit_ref = units.unit_ref(self.unit)
            if unit_ref is not None:
                json['unit'] = unit_ref.to_dict()
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

    def write_to(self, path: Path, zw: zipio.ZipWriter = None):
        """
        Writes json dictionaries to files
        :param path: string path to file
        :param zw: optional zipio.ZipWriter
        :return: None
        """
        if (path and path.exists()):
            log.warning(f'File {path} already exists and will be overwritten')
            path.unlink()
        if not zw:
            passed_zw = False
            zw = zipio.ZipWriter(path)
        else:
            passed_zw = True
        self._write_flows(zw)
        if self.flow_mapping is not None:
            self._write_mappings(zw)
        if not passed_zw:
            zw.close()

    def _write_flows(self, zw: zipio.ZipWriter):
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

            flow = o.Flow()
            flow.description = description
            flow.id = row["Flow UUID"]
            flow.name = row["Flowable"]
            flow.cas = row.get("CAS No", None)
            flow.formula = row.get("Formula", None)
            flow.version = flow_list_specs['list_version']
            flow.synonyms = row.get("Synonyms")
            flow.last_change = datetime.datetime.now().isoformat()
            flow.flow_type = o.FlowType.ELEMENTARY_FLOW
            flow.category = "Elementary flows/" + row['Context'].lower()

            fp = o.FlowPropertyFactor()
            fp.is_ref_flow_property = True
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
                    altfp = o.FlowPropertyFactor()
                    altfp.is_ref_flow_property = False
                    altfp.conversion_factor = alternate['AltUnitConversionFactor']
                    altfp.flow_property = units.property_ref(alternate["AltUnit"])
                    if altfp.flow_property is None:
                        log.warning("unknown altunit %s in flow %s",
                                    alternate["AltUnit"], row["Flow UUID"])
                    else:
                        flow.flow_properties.append(altfp)
            zw.write(flow)

    def _write_mappings(self, zw: zipio.ZipWriter):
        maps = {}
        for i, row in self.flow_mapping.iterrows():
            me = _MapEntry(row)
            m = maps.get(me.source_list)
            if m is None:
                m = []
                maps[me.source_list] = m
            m.append(me)

        for source_list, entries in maps.items():
            list_ref = o.Ref()
            list_ref.ref_type = o.RefType.FlowMap
            list_ref.name = source_list
            mappings = []
            flow_map = {
                '@id': str(uuid.uuid4()),
                'name': '%s -> Fed.LCA Commons' % source_list,
                'source': list_ref.to_dict(),
                'mappings': mappings
            }
            for e in entries:
                mappings.append(e.to_json())

            # an ugly hack to write the flow maps directly to the zip-file
            # as there are currenty only methods for writing RootEntity
            # objects in the ZipWriter
            zw._ZipWriter__zip.writestr(
                "flow_mappings/" + flow_map["@id"] + ".json",
                json.dumps(flow_map))
