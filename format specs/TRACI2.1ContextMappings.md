## TRACI 2.1 Context Mapping Input File Format

The TRACI 2.1 context mapping input file is in the form of CSV data with the following fields.

 Field | Type | Required |  Note |
----------- |  ---- | ---------| -----  |
 SourceFlowContext | string | Y | TRACI2.1 context |
 TargetFlowContext | string | N | FEDEFL context, path-like set in the form of directionality/environmental media/environmental compartment... e.g. 'emission/air/tropophere' |
