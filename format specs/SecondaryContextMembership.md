## Secondary Context Membership Input File Format

The secondary context membership input file is in the form of CSV data with the following fields. Binary entries indicate possible compartment combinations resulting in unique contexts.

 Field | Type | Required |  Note |
----------- |  ---- | ---------| -----  |
 FlowCLass | string | Y | the flow name |
 Directionality | string | Y | defines whether flow is emission or resource |
 Environmental Media | string | Y | environmental compartment emission or resource flows to or from, respectively |
 Vertical Strata | int | Y | defines atmospheric or subterranean strata |
 Land Use | int | Y | primary use based on human activity or naturally occurring community of flora and fauna in a habitat |
 Human-Dominated | int | Y  | primary use categories based on ecologically-dominant human activity |
 Terrestrial | int | Y | primary use based on human activity or naturally occurring community of flora and fauna in a habitat |
 Aquatic Feature | int | Y | describing different formations of water bodies |
 Indoor | int |  Y |  defines if release occurs to air inside of a building or enclosed structure |
 Population Density | int | Y | describes the population density of the area of a release. This context can describe air, water or ground emissions |  
 Release Height | int | Y | height at which an air release occurs, ground-level is default |
 ContextPreferred | int | Y | 1 for preferred, 0 for non-preferred |
