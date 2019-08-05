## Contexts Input File Format

The context input file is in the form of CSV data with the following fields.

 Field | Type | Required |  Note |
----------- |  ---- | ---------| -----  |
 Directionality | string | Y | defines whether flow is emission or resource |
 Environmental Media | string | Y | environmental compartment emission or resource flows to or from, respectively |
 Vertical Strata | string | N | defines atmospheric or subterranean strata |
 Land Use | string | N | primary use based on human activity or naturally occurring community of flora and fauna in a habitat |
 Human-Dominated | string | N  | primary use categories based on ecologically-dominant human activity |
 Terrestrial | string | N | primary use based on human activity or naturally occurring community of flora and fauna in a habitat |
 Aquatic Feature | string | N | describing different formations of water bodies |
 Indoor | string |  N |  defines if release occurs to air inside of a building or enclosed structure |
 Population Density | string | N | describes the population density of the area of a release. This context can describe air, water or ground emissions |  
 Release Height | string | N | height at which an air release occurs, ground-level is default |
