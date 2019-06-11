# ShippingTree Developer Candidate Project

## Pre-Reqs/Requirements
Please install the requirements (globally or in a virtual environment) before using the application. 
Requirements are saved in requirements.txt
Can be installed by simply entering: 'pip install -r requirements.txt'
Please also ensure that the input data file is in the project directory and is named correctly. 
The name of the input file can be changed to whatever is desired in 'DATA_FILE' variable in the application.

## Usage instructions
Once you have the requirements installed, the application can be run by simply entering: 'python application.py'. 

By default the CALL LIMIT of the application is set to 5 for testing with a smaller number of calls. However, this can be changed in LINE 7 of the application.py file. 

The application will print out feedback and details to STDOUT (screen) as it executes.
The application will also insert the results into the remote database provided as it excutes.

Finally, after the processing is complete, it will launch a local flask webserver at "127.0.0.1:5000" where the results can be viewed via a browser. On the webpage, for each shipment, the webpage will show how much can be saved for that shipment between the two warehouses, the cheaper rate as well as the cheaper option. Furthermore, it will also show how much the total savings from all shipments processed is. [Please check the sampleOutput.jpg to see sample output.]

The tableManager's showSavings() and showOnlySavings() methods can leveraged to view the results. (Note: On each execution the program will add the results from the file to the database so using the same data/data file more than once might duplicate some entries in the database).

## Time To Complete
14-15 hours work (approx.)

## Difficulties
1- Understanding working with API - some aspects of the API were not clear and needed further clarification.

2- Trying to see/figure out how the program could add more value to the business context. What additional calculations/processing could be done to generate useful economic/business information form the data. 

## Considerations
1- Keeping API calls & database calls to a minimum to improve performance/processing time. 

2- Keeping the user informed as to what is happening at each stage of the execution.

3- Checking for runtime errors like fileIO and database/API connections errors and handling them.

4- Giving the user useful error messages. 

5- Giving the user feedback for cheaper option, rate, carrier and service for each line/entry as program executes. 

## Business Context
Although this is a good way of deciding whether or not to open a new warehouse, if used in isolation, it could give an incorrect or one dimentional view on the subject. This should be used as a guiding indicator among other indicators and the general economic/financial/business context to come to a final decision. For example, will the savings from the additional warehouse be enough to justify the additional utility, labor and maintanance costs? 

Furthermore, the same data could also be used to extract more details that may be beneficial. For example, we could use program with sample data to see how many shipments (and by extention time) it would take to recoup the original investment cost towards the additional warehouse. 


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

