# Flow Mapping format

Field |	Type |	Required? | Note|
----- | ---- | --------  | -----------|
SourceListName |	string | Y | Name of source flowlist|
SourceListVersion |	string | N | Version number for source list|
SourceFlowName	| string | Y | |
SourceFlowUUID	| string | N | If no UUID present, UUID generated based on olca algorithm|
SourceFlowCategory1 | string | Y | A minimum of one category is required |
SourceFlowCategory2	| string | N | |
SourceFlowCategory3	| string | N | |
SourceProperty	| string |	Y | An openLCA flow property name e.g. 'mass', 'energy' |
SourcePropertyID | string |	N | If not present, assumes openLCA reference UUID for that flow property |
SourceUnit | string | N | If not present, assumes openLCA default unit for that property|
SourceUnitID | string | N | If not present, assumes openLCA reference UUID for that unit |
MatchCondition |	string | N |Single character. '=', '>','<','~'. Meaning 'equal to','a superset of', 'a subset of', ' a proxy for'|
ConversionFactor | double | Y |	Value for multiplying with source flow to equal target flow|
TargetFlowName | string | Y | Name of the Fed Commons flowable|
TargetFlowUUID	| string| Y| UUID for Fed Commons flow |
TargetFlowCategory1 | string | Y| A minimum of one category is required|
TargetFlowCategory2	| string | N| |
TargetFlowCategory3 | string | N| |
TargetProperty | string | Y | An openLCA flow property name e.g. 'mass', 'energy' |
TargetPropertyID | string | N |  If not present, assumes openLCA reference UUID for that flow property |
TargetUnit | string | N | If not present, assumes openLCA default unit for that property|
TargetUnitID | string | N |  If not present, assumes openLCA reference UUID for that unit|
Mapper	|string | N	|Person creating the mapping. Could map to Actor|
Verifier |	string | N |Person verifying the mapping. Could map to Actor.|
LastUpdated |	datetime | N |	Date mapping last updated|

Note that TargetList is not present, because the Fed LCA Commons Elementary Flow List
 is always assumed target, with version number in the file name.