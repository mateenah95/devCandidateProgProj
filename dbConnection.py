import psycopg2

connection = psycopg2.connect(
    host='candidate-test-2.cg4nxczsn7yj.us-east-1.rds.amazonaws.com',
    port='5432',
    user='candidate_test_2',
    password='sj7ZWaC9',
    database='candidate_test'
)

cursor = connection.cursor()

cursor.execute("""CREATE TABLE test_table(
        id SERIAL PRIMARY KEY,
        address_line1 VARCHAR NOT NULL,
        address_line2 VARCHAR NOT NULL,
        city VARCHAR NOT NULL,
        state VARCHAR NOT NULL,
        country VARCHAR NOT NULL, 
        height DECIMAL NOT NULL,
        length DECIMAL NOT NULL,
        width DECIMAL NOT NULL,
        CALI_CARRIER VARCHAR NOT NULL,
        CALI_SERVICE VARCHAR NOT NULL,
        CALI_POSTAGE_FEE MONEY NOT NULL,
        OHIO_CARRIER VARCHAR NOT NULL,
        OHIO_SERVICE VARCHAR NOT NULL,
        OHIO_POSTAGE_FEE MONEY NOT NULL
    )""") 


cursor.execute("""SELECT * 
                    FROM information_schema.tables 
                    WHERE table_name='test_table'
                    ORDER BY table_name;""")

for table in cursor.fetchall():
    print(table)

print('Success')