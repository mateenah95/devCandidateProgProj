#importing required packages (sticking to PEP8 guidlines by separating imports on new lines)
import easypost
import psycopg2
#importing core python packages 
import sys, json, csv   
#importing helper methods and constants from tableManager module 
from table_manager import tableCheck, createTable, buildInsertQuery, printDetailsToScreen
from table_manager import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, connection, cursor
#importing flask web app for post processing front_end module
from front_end import app



#declaring and assigning the variables used to limit the number of calls
START = 0
LIMIT = 1000

#input data file name declaton & assignment
#(Change here if needed)
DATA_FILE = 'sample-data.csv'

#declaring and assigning API key
easypost.api_key = 'EZTKb4661e503603421d8dd125dc8e383aa4hY4mwPbdKTnhsCy2CwfUYA'

#surrounding databse connection attempt with try-catch
#in case the table already exists resulting in error
try:
    print('Attempting to connect to database...')
    #checking if table exists. IMPORTED HELPER METHOD: tableCheck()
    tableExists = tableCheck()
    
    if(tableExists == 0 ):
        print('Rates table not found. Attempting to create...')
        #Surrounding table creation call with try catch. 
        try:
            createTable()
        except:
            print('Rates table could not be created. Exiting application...')
            sys.exit(1)
    else:
        print("Table already exists. Skipping recreation...")
#error handling block for database connection attempt call
except:
    print("Database Connection Error. Exiting application...")
    sys.exit(1)

#creating CALIFORNIA (origin) address object
origin_california = easypost.Address.create(
    street1 = '10731 Walker St',
    street2 = '',
    city = 'Cypress',
    state = 'CA',
    zip = '90630',
    country = 'US'
)

#creating OHIO (origin) address object
origin_ohio = easypost.Address.create(
    street1 = '4720 Poth Rd',
    street2 = '',
    city = 'Whitehall',
    state = 'OH',
    zip = '43213',
    country = 'US'
)

#surrounding data file opening call with try-except
try:
    #opening data file file
    with open(DATA_FILE, 'r') as csv_file:
        csv_data = csv.reader(csv_file)

        #reading line by line using for loop, keeping track of index as well
        for index, csv_line in enumerate(csv_data):
           
            #FOR DEV/TESTING PURPOSES
            if index <= (START-1):
                continue
                
            #variable declarations - FOR CLEANER/EASIER CODE    
            street1 = csv_line[0]
            street2 = csv_line[1]
            city = csv_line[2]
            state = csv_line[3]
            zip_code = csv_line[4]
            country = csv_line[5]
            height = csv_line[6]
            length = csv_line[7]
            width = csv_line[8]
            weight = csv_line[9]

            #declaring & the DESTINATION address object
            to_address = easypost.Address.create(
                street1 = street1,
                street2 = street2,
                city = city,
                state = state,
                zip = zip_code,
                country = country,
            )

            #declaring & the parcel object 
            parcel = easypost.Parcel.create(
                length = length,
                width = width,
                height = height,
                weight = weight
            )

            #declaring & creating a shipment object from CALIFORNIA
            shipment_california = easypost.Shipment.create(
                to_address = to_address,
                from_address = origin_california,
                parcel = parcel
            )

            #declaring & creating a shipment object from OHIO 
            shipment_ohio = easypost.Shipment.create(
                to_address = to_address,
                from_address = origin_ohio,
                parcel = parcel
            )

            #declaring lists which will hold the rates retruned
            #from the respective shipment objects
            california_rates = []
            ohio_rates = []

            #looping through the rates in shipment objects and
            #inserting them to the arrays declared above after
            #casting to float type
            for cali_counter in shipment_california.rates:
                california_rates.append(float(cali_counter.rate))

            for ohio_counter in shipment_ohio.rates:
                ohio_rates.append(float(ohio_counter.rate))
            
            if len(california_rates) == 0:
                print('Error with index: [{}]. Skipping entry...'.format(index))
                continue

            if len(ohio_rates) == 0:
                print('Error with index: [{}]. Skipping entry...'.format(index))
                continue

            #finding the minimum rates and their respective
            #carrier and service type for CALIFORNIA and OHIO
            cheapest_california_rate = min(california_rates)
            index_cheapest_california = california_rates.index(cheapest_california_rate)
            cheapest_carrier_california = shipment_california.rates[index_cheapest_california].carrier
            cheapest_service_california = shipment_california.rates[index_cheapest_california].service

            cheapest_ohio_rate = min(ohio_rates)
            index_cheapest_ohio = ohio_rates.index(cheapest_ohio_rate)
            cheapest_carrier_ohio = shipment_ohio.rates[index_cheapest_ohio].carrier
            cheapest_service_ohio = shipment_ohio.rates[index_cheapest_ohio].service

            #declaring, calculating and assigning cost difference
            #between shipping from CALIFORNIA and OHIO
            saving = max(cheapest_california_rate, cheapest_ohio_rate) - min(cheapest_california_rate, cheapest_ohio_rate)
            
            #declaring, calculating and assigning whether it is
            #cheaper from CALIFORNIA or OHIO
            if(cheapest_california_rate < cheapest_ohio_rate):
                choice = 'California'
            elif(cheapest_california_rate > cheapest_ohio_rate):
                choice = 'Ohio'
            else:
                choice = 'Either'
            
            #calling function to print details to screen
            printDetailsToScreen(index, cheapest_california_rate, cheapest_carrier_california, 
                                 cheapest_service_california, cheapest_ohio_rate, cheapest_carrier_ohio, 
                                 cheapest_service_ohio, saving, choice)
            
            #calling helper method from table manager to build insert query
            query = buildInsertQuery(to_address.street1, 
                                         to_address.street2, to_address.city, to_address.state, 
                                         to_address.zip, to_address.country, parcel.height, 
                                         parcel.width, parcel.length, parcel.weight, 
                                         cheapest_carrier_california, cheapest_service_california,
                                         cheapest_california_rate, cheapest_carrier_ohio, 
                                         cheapest_service_ohio, cheapest_ohio_rate)
            
            #surrounding the insert query with try catch 
            try:
                cursor.execute(query)
                connection.commit()
                print("Database insert successfull for line index: [{}] ...".format(index))
            #error handling block for the insert query
            except Exception as e:
                print(e)
                print("Database insert failed for line index: [{}] ...".format(index))


            if index == (LIMIT-1): 
                break
#error handling block for data file opening try call
except Exception as e:
    print(e)
    #print('Error opening/reading data file. Exiting application...')
    sys.exit(1)
    
#running flask app/web server
app.run()
#terminating database
connection.close()

print('-------------------------------')
print('PROGRAM TERMINATED SUCCESSFULLY')
print('-------------------------------')


     
