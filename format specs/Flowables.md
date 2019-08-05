## Flowables Input File Format

Flowable input files are the form of CSV data with the following fields.

 Field | Type | Required |  Note |
----------- |  ---- | ---------| -----  |
 Flowable | string | Y | The flowable name |
 CAS No | string | N | CAS number |
 Formula | string | N | Chemical formula |
 Synonyms | string | N | Flow synonyms |
 Unit | string | Y  | The reference unit. Uses [olca-ipc.py](https://github.com/GreenDelta/olca-ipc.py) units |
 External Reference | string | N | Description or link to definition of flowable |
 Flowable Preferred | int | Y | Indicates whether or not flowable is preferred. `1` for preferred, `0` for non-preferred |
