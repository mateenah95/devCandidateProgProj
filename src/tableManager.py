#importing package
import psycopg2

#database details declaration & assignment
#(Change here if needed)
DB_HOST = 'candidate-test-2.cg4nxczsn7yj.us-east-1.rds.amazonaws.com'
DB_PORT = '5432'
DB_USER = 'candidate_test_2'
DB_PASSWORD = 'sj7ZWaC9'
DB_NAME = 'candidate_test'

#connection details
connection = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

#postgres cursor 
cursor = connection.cursor()

#helper method used to check if rates table
#exists by returning 0 or 1+
def tableCheck():
    cursor.execute("""SELECT table_name FROM information_schema.tables
        WHERE table_name = 'rates'""")

    counter = 0
    for table in cursor.fetchall():
        counter+=1

    return counter

#helper method used to create the rates table
def createTable():
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
        cali_carrier VARCHAR NOT NULL,
        cali_service VARCHAR NOT NULL,
        cali_postage_fee MONEY NOT NULL,
        ohio_carrier VARCHAR NOT NULL,
        ohio_service VARCHAR NOT NULL,
        ohio_postage_fee MONEY NOT NULL           
    )""") 
    connection.commit()
    print('Rates table created successfully...')

#helper method used to delete the rates table
def deleteTable():
    cursor.execute("""DROP TABLE rates""")
    connection.commit()
    print('Rates table deleted successfully...')

#helper method used to test inserting entry into rates table
def insertTestEntry():
    x = 8.0
    y = 3.3
    if x >= y:
        z = 'x'
        d = x - y
    else:
        z = 'y'
        d = y - x

    query = """INSERT INTO rates(address_line1, address_line2, city,
                                            state, zip, country, height, width, length,
                                            weight, cali_carrier, cali_service, 
                                            cali_postage_fee, ohio_carrier, ohio_service,
                                            ohio_postage_fee, choice, saving) VALUES ('{}','{}','{}','{}',{},'{}',
                                            {},{},{},{},'{}','{}',{},'{}','{}',{},'{}',{})""".format('7 Walmer Road', 
                                            'Unit 304', 'Toronto', 'ON', 
                                            120118, 'Canada', 4.3, 
                                            3.2, 1.4, 4.2, 
                                            'Fedex', 'Ground',
                                            x, 'DHL', 
                                            'Express', y, z, d)

    cursor.execute(query)
    connection.commit()
    print('Entry inserted into rates table successfully...')

def buildInsertQuery(street1, street2, city, state, zip, country, height, width, length, weight,
                    cheapest_carrier_california, cheapest_service_california, cheapest_california_rate,
                    cheapest_carrier_ohio, cheapest_service_ohio, cheapest_ohio_rate):
    #building insert query
    query = """INSERT INTO rates(address_line1, address_line2, city,
                                    state, zip, country, height, width, length,
                                    weight, cali_carrier, cali_service, 
                                    cali_postage_fee, ohio_carrier, ohio_service,
                                    ohio_postage_fee) VALUES ('{}','{}','{}','{}',{},'{}',
                                    {},{},{},{},'{}','{}',{},'{}','{}',{})""".format(street1, 
                                    street2, city, state, 
                                    zip, country, height, 
                                    width, length, weight, 
                                    cheapest_carrier_california, cheapest_service_california,
                                    cheapest_california_rate, cheapest_carrier_ohio, 
                                    cheapest_service_ohio, cheapest_ohio_rate)
    
    return query

#helper method to show all rates table entries
def showEntries():
    cursor.execute("""SELECT * FROM rates""")
    for result in cursor.fetchall():
        print(result)

#helper method printing all table entries & records including savings & cheaper option
def showSavings():
    cursor.execute("""SELECT id, 
    'California',
    cali_postage_fee,
    'Ohio',
    ohio_postage_fee,
    'Saving',
    CAST(GREATEST(cali_postage_fee, ohio_postage_fee) -  
    LEAST(cali_postage_fee, ohio_postage_fee) AS MONEY)
    FROM rates""")

    for result in cursor.fetchall():
        print(result)

#helper method printing only entry id, savings & cheaper option 
def showOnlySavings():
    cursor.execute("""SELECT id, 
    'California',
    cali_postage_fee,
    'Ohio',
    ohio_postage_fee,
    'Saving',
    CAST(GREATEST(cali_postage_fee, ohio_postage_fee) -  
    LEAST(cali_postage_fee, ohio_postage_fee) AS MONEY)
    FROM rates""")

    for result in cursor.fetchall():
        print(result)

#helper method used by the front end 
def getData():
    cursor.execute("""SELECT id, 
    cali_postage_fee,
    ohio_postage_fee,
    CAST(GREATEST(cali_postage_fee, ohio_postage_fee) -  
    LEAST(cali_postage_fee, ohio_postage_fee) AS MONEY)
    FROM rates""")

    return cursor.fetchall()

#helper method for printing line details to console/stdout
def printDetailsToScreen(index, cheapest_california_rate, cheapest_carrier_california, cheapest_service_california, cheapest_ohio_rate, cheapest_carrier_ohio, cheapest_service_ohio, saving, choice):
    print('--------------------------')
    print("--------------------------")
    print('LINE INDEX: {}'.format(index))
    print('------')
    print('California')
    print('California Cheapest Rate: {}'.format(cheapest_california_rate))
    print('California Cheapest Carrier: {}'.format(cheapest_carrier_california))
    print('California Cheapest Service Level: {}'.format(cheapest_service_california))
    print('------')
    print('Ohio')
    print('Ohio Cheapest Rate: {}'.format(cheapest_ohio_rate))
    print('Ohio Cheapest Carrier: {}'.format(cheapest_carrier_ohio))
    print('Ohio Cheapest Service Level: {}'.format(cheapest_service_ohio))
    print('------')
    print('Cost Difference: {}'.format(saving))
    print('Cheaper choice: {}'.format(choice))
    print('------')