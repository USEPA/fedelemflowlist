# Secondary Context Membership Input File Format

The secondary context membership input file is in the form of CSV data with the following fields.
Secondary context membership indicates whether or not secondary contexts (see [Contexts](Contexts.md)
for class definitions) should be associated with flows from this FlowClass with listed primary contexts
 (Directionality and Environmental Media).

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
 ContextPreferred* | int | Y | `1` for included and `0` for excluded. See note. |

 \* See the [EPA Report]((https://cfpub.epa.gov/si/si_public_search_results.cfm?simpleSearch=0&showCriteria=2&searchAll=elementary+flows&TIMSType=Published+Report&dateBeginPublishedPresented=07%2F31%2F2019))
  for discussion of preferred secondary contexts.
