"""Carbon GHG mapping policy and helpers for LCIA mapping files."""

import pandas as pd
import fedelemflowlist

C_TO_CO2 = 44.0 / 12.0  # kg CO2 / kg C

# Net accounting alternate (pass as policy=CARBON_GHG_POLICY). Unmapped: - .
# Elemental Carbon rows commented out for now.
#
# Flowable                         res/ground  res/air  em/air  em/ground
# Carbon dioxide                   0           -1       1       0
# Carbon                           0           -        3.667   0
# Carbon dioxide, biogenic         0           -1       1       0
# Carbon, biogenic                 0           -3.667   3.667   0
# Carbon dioxide, land use change  -           -        1       -
CARBON_GHG_POLICY = [
    {'target': 'Carbon dioxide', 'context': 'emission/air', 'cf': 1.0},
    {'target': 'Carbon dioxide', 'context': 'emission/ground', 'cf': 0.0},
    {'target': 'Carbon dioxide', 'context': 'resource/ground', 'cf': 0.0},
    {'target': 'Carbon dioxide', 'context': 'resource/air', 'cf': -1.0},
    {'target': 'Carbon dioxide, biogenic', 'context': 'emission/air', 'cf': 1.0},
    {'target': 'Carbon dioxide, biogenic', 'context': 'emission/ground', 'cf': 0.0},
    {'target': 'Carbon dioxide, biogenic', 'context': 'resource/air', 'cf': -1.0},
    {'target': 'Carbon dioxide, biogenic', 'context': 'resource/ground', 'cf': 0.0},
    {'target': 'Carbon dioxide, land use change', 'context': 'emission/air',
     'cf': 1.0},
    # {'target': 'Carbon', 'context': 'emission/air', 'cf': C_TO_CO2},
    # {'target': 'Carbon', 'context': 'emission/ground', 'cf': 0.0},
    # {'target': 'Carbon', 'context': 'resource/ground', 'cf': 0.0},
    # {'target': 'Carbon, biogenic', 'context': 'emission/air', 'cf': C_TO_CO2},
    # {'target': 'Carbon, biogenic', 'context': 'emission/ground', 'cf': 0.0},
    # {'target': 'Carbon, biogenic', 'context': 'resource/air', 'cf': -C_TO_CO2},
    # {'target': 'Carbon, biogenic', 'context': 'resource/ground', 'cf': 0.0},
]

# Default policy (used when apply_carbon_ghg_policy policy=None).
# Climate-neutral biogenic air. Fossil CO2 and LUC CO2 match CARBON_GHG_POLICY.
# Only Carbon dioxide, biogenic changes (elemental Carbon rows commented out):
#
# Flowable                         res/ground  res/air  em/air  em/ground
# Carbon dioxide, biogenic         1           0        0       -1
# Carbon, biogenic                 3.667       0        0       -3.667
CARBON_GHG_POLICY_BIOGENIC_STOCK = [
    r for r in CARBON_GHG_POLICY
    if r['target'] not in ('Carbon dioxide, biogenic', 'Carbon, biogenic')
] + [
    {'target': 'Carbon dioxide, biogenic', 'context': 'emission/air', 'cf': 0.0},
    {'target': 'Carbon dioxide, biogenic', 'context': 'emission/ground',
     'cf': -1.0},
    {'target': 'Carbon dioxide, biogenic', 'context': 'resource/air', 'cf': 0.0},
    {'target': 'Carbon dioxide, biogenic', 'context': 'resource/ground',
     'cf': 1.0},
    # {'target': 'Carbon, biogenic', 'context': 'emission/air', 'cf': 0.0},
    # {'target': 'Carbon, biogenic', 'context': 'emission/ground',
    #  'cf': -C_TO_CO2},
    # {'target': 'Carbon, biogenic', 'context': 'resource/air', 'cf': 0.0},
    # {'target': 'Carbon, biogenic', 'context': 'resource/ground',
    #  'cf': C_TO_CO2},
]

CO2_SOURCE_BY_METHOD = {
    'IPCC': 'Carbon dioxide',
    'ReCiPe2016': 'Carbon dioxide',
    'TRACI2.1': 'CARBON DIOXIDE',
    'TRACI2.2': 'CARBON DIOXIDE',
    'ImpactWorld+': 'Carbon dioxide',
}

# Optional per-method patches: list of {target, context, cf} replacing
# matching default rules (or adding new ones).
POLICY_BY_METHOD = {}


def _rules_for_method(method_name, policy=None):
    rules = list(policy if policy is not None else CARBON_GHG_POLICY_BIOGENIC_STOCK)
    overlay = POLICY_BY_METHOD.get(method_name, [])
    if not overlay:
        return rules
    by_key = {(r['target'], r['context']): r for r in rules}
    for item in overlay:
        by_key[(item['target'], item['context'])] = item
    return list(by_key.values())


def apply_carbon_ghg_policy(df, method_name, policy=None):
    """Attach method air CO2 to FEDEFL carbon flows using the shared policy.

    Default policy is CARBON_GHG_POLICY_BIOGENIC_STOCK. Pass CARBON_GHG_POLICY
    for net accounting.

    Contexts the method does not have (resource, ground) are filled from
    FEDEFL without adding global context maps.

    For most methods, existing rows for policy targets are replaced.
    ImpactWorld+ keeps native air source→target mappings (biogenic / land
    transformation / generic CO2) and only appends non-air stock-policy
    contexts using generic Carbon dioxide as the source (method CF = 1).
    """
    source = CO2_SOURCE_BY_METHOD.get(method_name)
    if not source or df.empty:
        return df
    rules = _rules_for_method(method_name, policy)
    if not rules:
        return df

    iw_native_air = method_name == 'ImpactWorld+'
    if iw_native_air:
        # Air CFs come from IW's own sources; do not overwrite them.
        rules = [r for r in rules
                 if not str(r['context']).startswith('emission/air')]
        if not rules:
            return df

    src = df['SourceFlowName'].fillna('') == source
    air = df['TargetFlowContext'].fillna('').str.startswith('emission/air')
    drop_cols = [c for c in ('TargetFlowContext', 'TargetFlowName',
                             'ConversionFactor', 'TargetFlowUUID')
                 if c in df.columns]
    template = (df.loc[src & air]
                .drop(columns=drop_cols)
                .drop_duplicates())
    if template.empty:
        return df

    if iw_native_air:
        keep = df.copy()
    else:
        targets = {r['target'] for r in rules}
        keep = df.loc[~df['TargetFlowName'].isin(targets)].copy()

    flows = fedelemflowlist.get_flows()
    parts = []
    for rule in rules:
        ctxs = (flows[(flows['Flowable'] == rule['target'])
                      & flows['Context'].fillna('').str.startswith(
                          rule['context'])]
                [['Context']]
                .drop_duplicates()
                .rename(columns={'Context': 'TargetFlowContext'}))
        if ctxs.empty:
            continue
        part = (template.assign(_k=1)
                .merge(ctxs.assign(_k=1), on='_k')
                .drop(columns='_k'))
        part['TargetFlowName'] = rule['target']
        part['ConversionFactor'] = float(rule['cf'])
        parts.append(part)
    if not parts:
        return df
    extra = pd.concat(parts, ignore_index=True)
    return pd.concat([keep, extra], ignore_index=True)
