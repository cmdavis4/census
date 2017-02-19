# Ingestion Tools for U.S. Census ASEC Data

This repo contains tools for ingesting the Annual Social and Economic Supplement (ASEC) to the U.S. Current Populaion Survey (CPS) for March 2016.

* **download_data.sh**: A shell script to download the data and data dictionary for the March 2016 ASEC. Requires wget.
* **ingestion.py**: Functions to access the files downloaded by download_data.sh. Functionality for parsing the data dictionary, and using the parsed data dictionar to programatically access the data, with some convenience features added.
* **explore_census_data.ipynb**: An example of how the functions in ingestion.py can be used, as well as a very preliminary exploration of the income distribution of the United States, as taken from the ASEC.

## References
All files related to the ASEC can be found at the [Census' FTP page](http://thedataweb.rm.census.gov/ftp/cps_ftp.html). More information about the ASEC can be found at the [U.S. Census website](https://www.census.gov/did/www/saipe/data/model/info/cpsasec.html). The ASEC tech documentation can also be found [on the census' website](https://www2.census.gov/programs-surveys/cps/techdocs/cpsmar15.pdf).