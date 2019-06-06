# ShippingTree Developer Candidate Project

## Pre-Reqs/Requirements
Please install the requirements (globally or in a virtual environment) before using the application. 
Requirements are saved in requirements.txt
Can be installed by simply entering: 'pip install -r requirements.txt'
Please also ensure that the input data file is in the project directory and is named correctly. 
The name of the input file can be changed to whatever is desired in 'DATA_FILE' variable in the application.

## Usage instructions
Application can be run by simply entering: 'python application.py'
The application will print out feedback and details to STDOUT (screen) as it executes.
The application will also insert the results into the remote database provided. 

## Table Manager
The table manager package/module contains helper methods which handle dealing with the database/table.
It is required for application to run.
However, the package/module can be used in isolation by importing and using directly from the CLI. It can be used to test table creation, table deletion, insertion as well printing out the savings. 

Example: 

import tableManager

tableManager.showSavings()


  
