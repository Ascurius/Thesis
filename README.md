# Master Thesis: Secure Collaborative Analysis using Multi Party Computation

This repository contains the code base used for my thesis around multi party computation. This document provides guidance for setup and installation and is not a complete documentation.

## Setup and Installation

This project is based upon the MP-SPDZ framework and its inherent dependencies. For full details please visit the documentation of MP-SPDZ at this location: https://mp-spdz.readthedocs.io/en/latest/. You can use the following scripts and adjust them if needed.

1. Install the dependecies using `install.sh`. 
2. Setup the project structure using `setup.sh`.

## Project Structure

This repo is structured as follows. It is comprised of three main directories: `code`, `duckdb` and `measurements`.

```
.
├── code
│   ├── plot
│   │   ├── group_a.py
│   │   ├── group_b.py
│   │   ├── join_types.py
│   │   ├── operators_group_a.py
│   │   ├── operators_group_b.py
│   │   └── parse.py
│   ├── operators_plain.py
│   ├── operators_secure.py
│   ├── populate.py
│   └── util.py
├── duckdb
│   ├── duckdb
│   ├── setup_reference_table.sh
│   └── thesis.duckdb
└── measurements
    ├── measure_db.sh
    ├── measure_domain.sh
    ├── measure_operators_plain.sh
    ├── measure_secure.sh
```


### Code
The directory `code`contains every program used in this project. It is subdivided into the following two directories `queries` and `plot`.

1. `queries`: This folder is itself divided into four directories and additional scripts. The subfolders `duckdb`, `plain` and `secure` for each query variant, containing corresponding implemntations of all queries. The folder `smcql` contains the original refernce queries used to derive the implementations of the other three query variants.
2. `plot`: This folder contains scripts to plot the data measured from the execution of the queries. There are scripts to plot the total time and the porportional time of the operators, for Group A and B.

Further, this folder contains the file `populate.py` which is callable from the command line and can be used to generate sample data for queries to be used. 

The files `operators_plain.py` and `operators_secure.py` contains the implementations of all algorithms used within the queries. If you are missing a specific implementation for your Python and MP-SPDZ queries you can use the implementation in these files.

### DuckDB

This directory contains the reference DuckDB databases and the script `setup_reference_table.sh` to fill the database with the sample data in the MP-SPDZ player input files.

### Measurements

This directory contains script to automatically evaluate the queries for all three variants for given number of rows which are specified within the respective scripts. Each query takes as an argument the name of the query to be evaluated, and automatically generates the sample data needed. Furthermore, each script 