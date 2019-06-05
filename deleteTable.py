import psycopg2

connection = psycopg2.connect(
    host='candidate-test-2.cg4nxczsn7yj.us-east-1.rds.amazonaws.com',
    port='5432',
    user='candidate_test_2',
    password='sj7ZWaC9',
    database='candidate_test'
)

cursor = connection.cursor()
cursor.execute("""DROP TABLE rates""")
connection.commit()
connection.close()
'''
add1 = '7_Walmer_Road'
add2 = 'Unit_304'
city = 'Toronto'
state = 'ON'
zip = 120118
country = 'CA'
l = 4.2
h = 3.3
w = 1.5
weight = 5.3
c_c = 'UPS'
c_s = 'Standard'
c_r = 13.99
o_c = 'DHL'
o_s = 'Ground'
o_r = 16.50

query = """INSERT INTO rates(address_line1, address_line2, city,
                                        state, zip, country, height, width, length,
                                        weight, cali_carrier, cali_service, 
                                        cali_postage_fee, ohio_carrier, ohio_service,
                                        ohio_postage_fee) VALUES ({},{},{},{},{},{},
                                        {},{},{},{},{},{},{},{},{},{})""".format(add1, 
                                        add2, city, state, 
                                        zip, country, h, 
                                        w, l, weight, 
                                        c_c, c_s,
                                        c_r, o_c, 
                                        o_s, o_r))
'''