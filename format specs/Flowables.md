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
 Flowable Preferred | int | Y | Indicates whether or not flowable is preferred.* `1` for preferred, `0` for non-preferred |

\* See the [EPA Report](https://cfpub.epa.gov/si/si_public_search_results.cfm?simpleSearch=0&showCriteria=2&searchAll=elementary+flows&TIMSType=Published+Report&dateBeginPublishedPresented=07%2F31%2F2019)
 for discussion of preferred flowables.