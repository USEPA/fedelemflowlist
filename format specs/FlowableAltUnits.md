## Flowable Alternate Units Input File Format

The flowable alternate units input files are in the form of CSV data with the following fields.

 Field | Type | Required |  Note |
----------- |  ---- | ---------| -----  |
 Flowable | string | Y | the flowable name |
 Alternate Unit | string | Y | unit of measure, different than the preferred unit |
 Reference Unit | string | Y | unit of measure, original preferred unit |
 Conversion Factor | float | Y | factor for conversion from reference unit to alternate unit |
 External Reference | string | Y | description or link to reference for conversion values |
