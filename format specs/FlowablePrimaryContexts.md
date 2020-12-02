# Flowable Primary Context Input File Format

Flowable primary context input files are the form of CSV data with the following fields.

 Field | Type | Required |  Note |
----------- |  ---- | ---------| -----  |
 Flowable | string | Y | The flowable name |
 Directionality | string | Y | A primary context component indicating direction of flow. Currently `emission` or `resource` |
 Environmental Media | string | Y | A primary context component indicating primary environmental compartment that is origin or destination of the flow. Currently `air`, `ground`, `water`, or `biotic` |
