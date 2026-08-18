"""Helpers for building LCIA mapping files from flowable and context maps."""

import pandas as pd
import fedelemflowlist

SEQ_FLOWABLE = 'Carbon dioxide, to soil or biomass stock'


def attach_air_co2_to_ground_sequestration(df: pd.DataFrame) -> pd.DataFrame:
    """Map method air CO2 onto FEDEFL emission/ground sequestration only.

    This flowable is ground-only. Climate methods characterize CO2 in air, so
    piggyback those air CFs onto emission/ground* without a global air→ground
    context mapping. Existing emission/ground targets (e.g. from soil) are kept.
    """
    seq = df['TargetFlowName'] == SEQ_FLOWABLE
    if not seq.any():
        return df
    air_or_water = df['TargetFlowContext'].fillna('').str.startswith(
        ('emission/air', 'emission/water'))
    to_replace = seq & air_or_water
    keep = df.loc[~to_replace].copy()
    if not to_replace.any():
        return df
    src = (df.loc[to_replace]
           .drop(columns=['TargetFlowContext'])
           .drop_duplicates())
    flows = fedelemflowlist.get_flows()
    ground = (flows[(flows['Flowable'] == SEQ_FLOWABLE)
                    & flows['Context'].fillna('').str.startswith('emission/ground')]
              [['Context']]
              .drop_duplicates()
              .rename(columns={'Context': 'TargetFlowContext'}))
    if src.empty or ground.empty:
        return keep
    extra = src.assign(_k=1).merge(ground.assign(_k=1), on='_k').drop(columns='_k')
    return pd.concat([keep, extra], ignore_index=True)
