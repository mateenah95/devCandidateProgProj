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
The application will also insert the results into the remote database provided as it excutes. Finally, after the processing is complete, it will launch a local webserver at "127.0.0.1:5000" where the results can be viewed via a browser. The tableManager's showSavings() and showOnlySavings() methods can also be used to view the results in addition to writing custom methods with the desired queries. 


## Table Manager
The table manager package/module contains helper methods which handle dealing with the database/table.
It is required for application to run.
However, the package/module can be used in isolation by importing and using directly from a CLI or as a module in other programs. It can be used to test table creation, table deletion, insertion as well displaying the savings. 

Example: 

import tableManager

tableManager.showSavings()

## Front End
The front end module is required for the flask web app to display the results at the end of the processing/calculations. The app can also be imported and used separately without having to run the calculations. 

Example: 

from front_end import app

app.run()

## Time To Complete: 48 hours (approx.)

## Difficulties
1- Understanding the project requirements - needed several readings and design iterations
2- Understanding working with API - some aspects of the API were not clear and needed further clarification

## Considerations
Although this is a good way of deciding whether or not to open a new warehouse, if used in isolation, it could give an incorrect or one dimentional view on the subject. This should be used as a guiding indicator among other indicators and the general economic/financial/business context to come to a final decision. Furthermore, the same data could also be used to extract more details that may be beneficial.  