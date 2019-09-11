## Flowable Alternate Units Input File Format

The flowable alternate units input files are in the form of CSV data with the following fields.

 Field | Type | Required |  Note |
----------- |  ---- | ---------| -----  |
 Flowable | string | Y | The flowable name |
 Alternate Unit | string | Y | Unit of measure, different than the preferred unit |
 Reference Unit | string | Y | Unit of measure, original preferred unit |
 Conversion Factor | float | Y | Factor for unit conversion, in the form of alternate units/reference unit|
 External Reference | string | Y | Description or link to reference for conversion values |
