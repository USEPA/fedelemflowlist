## Secondary Context Membership Input File Format

The secondary context membership input file is in the form of CSV data with the following fields. 
 
 Field | Type | Required |  Note |
----------- |  ---- | ---------| -----  |
 FlowClass | string | Y | The flow class. Same as 'Class' in [FlowList](FlowList.md). |
 Directionality | string | Y |  A primary context compartment. See definition in [FlowablePrimaryContext](FlowablePrimaryContext.md) |
 Environmental Media | string | Y | A primary context compartment.  See definition in [FlowablePrimaryContext](FlowablePrimaryContext.md) |
 Vertical Strata | int | Y | `1` for included and `0` for excluded. See note.  |
 Land Use | int | Y | `1` for included and `0` for excluded. See note. |
 Human-Dominated | int | Y  | `1` for included and `0` for excluded. See note. |
 Terrestrial | int | Y | `1` for included and `0` for excluded. See note. |
 Aquatic Feature | int | Y | `1` for included and `0` for excluded. See note. |
 Indoor | int |  Y |  `1` for included and `0` for excluded. See note. |
 Population Density | int | Y | `1` for included and `0` for excluded. See note. |  
 Release Height | int | Y | `1` for included and `0` for excluded. See note. |
 ContextPreferred | int | Y | `1` for included and `0` for excluded. See note. |

Note: Indicates whether or not contexts with compartment of this class (see [Contexts](Contexts.md) for class definitions)
 should be associated with flows from this FlowClass and primary contexts (Directionality and Environmental Media). 