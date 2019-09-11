## Contexts Input File Format

The context input file is in the form of CSV data with the following fields.

 Field | Type | Required |  Note |
----------- |  ---- | ---------| -----  |
 Directionality | string | Y | See [FlowablePrimaryContexts](FlowablePrimaryContexts.md). |
 Environmental Media | string | Y | See [FlowablePrimaryContexts](FlowablePrimaryContexts.md). |
 Vertical Strata | string | N | A secondary context component that defines atmospheric or subterranean strata, like `Troposphere` |
 Land Use | string | N | A secondary context component that indicates if the land use is human-dominated or a primary terrestrial or aquatic natural use. |
 Human-Dominated | string | N  |  A secondary context component for naming human-dominated land use type, like `Urban`. Used if Land Use is `Human-Dominated`.|
 Terrestrial | string | N | A secondary context component that describes various terrestrial habitat types, like `Forest`. Used if Land Use is `Terrestrial`.|
 Aquatic Feature | string | N | A secondary context component that describes different water body types, like `Lake`. Used if Land Use is a broader water body type like `Fresh Water Body`. |
 Indoor | string |  N |  A secondary context component that indicates `Indoor` for releases that occur to air inside of a building or enclosed structure. |
 Population Density | string | N | A secondary context component that describes the population density of the area of an emission or resource, like `Urban`.|  
 Release Height | string | N | A secondary context component that describes the height at which an air release occurs, like `Ground-level` or `Low` |
