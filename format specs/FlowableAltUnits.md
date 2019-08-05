## Flowable Alternative Units Input File Format

The flowable alternative units input files are in the form of CSV data with the following fields.

 Field | Type | Required |  Note |
----------- |  ---- | ---------| -----  |
 Flowable | string | Y | the flow name |
 CAS No | string | N | CAS number |
 Formula | string | N | chemical formula|
 Synonyms | string | N | flow synonyms
 Unit | string | Y  | the reference unit. uses olca units |
 Class | string | Y | The flow class, e.g. 'Energy' or 'Chemical' |
 External Reference | string | N | e.g. a web link |
 Preferred | int |  N |   1 for preferred, 0 for non-preferred
 Context | string | Y | A path-like set in the form of directionality/environmental media/environmental compartment... e.g. 'emission/air/tropophere'|  
 Flow UUID | string | Y | Unique hexadecimal ID for the flow |
 AltUnit | string | N | Alternate unit for the flow |
 AltUnitConversionFactor | double | N | Conversion factor to convert from Unit to AltUnit | 
