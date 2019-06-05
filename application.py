#importing required modules (install via requirements.txt)
import csv, easypost, sys, json, psycopg2

#input data file name declaton & assignment
#(Change here if needed)
DATA_FILE = 'sample-data.csv'

#database details declaration & assignment
#(Change here if needed)
DB_HOST = 'candidate-test-2.cg4nxczsn7yj.us-east-1.rds.amazonaws.com'
DB_PORT = '5432'
DB_USER = 'candidate_test_2'
DB_PASSWORD = 'sj7ZWaC9'
DB_NAME = 'candidate_test'

#declaring and assigning API key
easypost.api_key = 'EZTKb4661e503603421d8dd125dc8e383aa4hY4mwPbdKTnhsCy2CwfUYA'

#surrounding databse connection attempt with try-catch
#in case the table already exists resulting in error
try:
    #attempting to connect to database
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    #Surrounding table creation call with try catch. 
    try:
        #executing query to create database table
        cursor.execute("""CREATE TABLE rates(
            id SERIAL PRIMARY KEY,
            address_line1 VARCHAR NOT NULL,
            address_line2 VARCHAR,
            city VARCHAR NOT NULL,
            state VARCHAR,
            zip INTEGER NOT NULL,
            country VARCHAR NOT NULL, 
            height DECIMAL NOT NULL,
            length DECIMAL NOT NULL,
            width DECIMAL NOT NULL,
            weight DECIMAL NOT NULL,
            CALI_CARRIER VARCHAR NOT NULL,
            CALI_SERVICE VARCHAR NOT NULL,
            CALI_POSTAGE_FEE MONEY NOT NULL,
            OHIO_CARRIER VARCHAR NOT NULL,
            OHIO_SERVICE VARCHAR NOT NULL,
            OHIO_POSTAGE_FEE MONEY NOT NULL
        )""") 
        connection.commit()
    except:
        print("Table already exists. Skipping recreation...")
#error handling block for database connection attempt call
except:
    print("Database Connection/Table Creation Error. Exiting application...")
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
            if index%2 == 0:
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
            
            #Commented out code to create order
            '''
            order_california = easypost.Order.create(
                to_address = to_address,
                from_address = origin_california,
                shipments = [shipment_california]
            )
            '''

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

            print("------------------------")

            
            #print(index_cheapest_california)
            print('California')
            print(cheapest_california_rate)
            print(cheapest_carrier_california)
            print(cheapest_service_california)
            print('------')
            print('Ohio')
            #print(index_cheapest_ohio)
            print(cheapest_ohio_rate)
            print(cheapest_carrier_ohio)
            print(cheapest_service_ohio)
            print('------')

            #declaring, calculating and assigning cost difference
            #between shipping from CALIFORNIA and OHIO
            cost_difference = max(cheapest_california_rate, cheapest_ohio_rate) - min(cheapest_california_rate, cheapest_ohio_rate)

            print('Cost Difference: {}'.format(cost_difference))

            #declaring, calculating and assigning whether it is
            #cheaper from CALIFORNIA or OHIO
            if(cheapest_california_rate < cheapest_ohio_rate):
                cheaper = 'California'
            elif(cheapest_california_rate > cheapest_ohio_rate):
                cheaper = 'Ohio'
            else:
                cheaper = 'Either'

            print(cheaper)

            query = """INSERT INTO rates(address_line1, address_line2, city,
                                         state, zip, country, height, width, length,
                                         weight, cali_carrier, cali_service, 
                                         cali_postage_fee, ohio_carrier, ohio_service,
                                         ohio_postage_fee) VALUES ({},{},{},{},{},{},
                                         {},{},{},{},{},{},{},{},{},{})""".format(to_address.street1, 
                                         to_address.street2, to_address.city, to_address.state, 
                                         to_address.zip, to_address.country, parcel.height, 
                                         parcel.width, parcel.length, parcel.weight, 
                                         cheapest_carrier_california, cheapest_service_california,
                                         cheapest_california_rate, cheapest_carrier_ohio, 
                                         cheapest_service_ohio, cheapest_ohio_rate)

            cursor = connection.cursor()

            try:
                cursor.execute("""INSERT INTO rates(address_line1, address_line2, city,
                                         state, zip, country, height, width, length,
                                         weight, cali_carrier, cali_service, 
                                         cali_postage_fee, ohio_carrier, ohio_service,
                                         ohio_postage_fee) VALUES ({},{},{},{},{},{},
                                         {},{},{},{},{},{},{},{},{},{})""".format(to_address.street1, 
                                         to_address.street2, to_address.city, to_address.state, 
                                         to_address.zip, to_address.country, parcel.height, 
                                         parcel.width, parcel.length, parcel.weight, 
                                         cheapest_carrier_california, cheapest_service_california,
                                         cheapest_california_rate, cheapest_carrier_ohio, 
                                         cheapest_service_ohio, cheapest_ohio_rate))
                connection.commit()
            except:
                print("Database insert failed for index: {}".format(index))
            
            
            print("------------------------")

            print('success {}'.format(index))

            if index > 5:
                break

#error handling block for data file opening try call
except:
    print('Error opening/reading data file. Exiting application...')
    sys.exit(1)

print('-------------------------------')
print('PROGRAM TERMINATED SUCCESSFULLY')
print('-------------------------------')

     
