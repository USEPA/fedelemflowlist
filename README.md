# Federal-LCA-Commons-Elementary-Flow-List
To generate elementary flow lists that can used for life cycle assessment. This list is being created to support the [Federal LCA Commons](http://www.lcacommons.gov).

_Note: This is work in progress. A finalized flow list has not yet been developed. Until a 'release' is posted, we do not recommend the use of any list produced by this repository._


## Flow List Format
The flow list is a pandas data frame with the following columns:
```
Index   Label                   Note 
-----   -------------------     ----------------------------------------------------------------------------------------
  0     Flowable                - the flow name
  1     CAS No                  - CAS number
  2     Formula                 - chemical formula
  3     Synonyms                - flow synonyms
  4     Unit                    - the reference unit
  5     Class                   - Energy | Fuel | ...
  6     External reference      - e.g. a web link
  7     Preferred               - 1 | 0
  8     Context                 - A path-like set in the form of directionality/environmental media/environmental 
                                  compartment... e.g. 'emission/air/tropophere'  
  9     Flow UUID               - Unique ID for the flow
 10     Context UUID            - Unique ID for the context
```


## Disclaimer
The United States Environmental Protection Agency (EPA) GitHub project code is provided on an "as is" basis and the user assumes responsibility for its use.  EPA has relinquished control of the information and no longer has responsibility to protect the integrity , confidentiality, or availability of the information.  Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by EPA.  The EPA seal and logo shall not be used in any manner to imply endorsement of any commercial product or activity by EPA or the United States Government.
