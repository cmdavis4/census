#!/usr/bin/env bash

# Convenience script to download all of the data used in explore_census_data.ipynb
# Links to download all raw census

mkdir `dirname $0`/data
# Data dictionary for the 2016 ASEC March supplement
wget http://thedataweb.rm.census.gov/pub/cps/march/Asec2016_Data_Dict_Full.txt -O `dirname $0`/data/asec2016_dd.txt
# Actual data for the 2016 ASEC March supplement
wget http://thedataweb.rm.census.gov/pub/cps/march/asec2016_pubuse_v3.dat.gz -O `dirname $0`/data/asec2016_pubuse_v3.dat.gz
# The government's aggregation of census data into an income distribution (for comparison)
wget https://www2.census.gov/programs-surveys/cps/tables/hinc-06/2016/hinc06.xls -O `dirname $0`/data/household_income_distribution.xls
gzip -d `dirname $0`/data/asec2016_pubuse_v3.dat.gz