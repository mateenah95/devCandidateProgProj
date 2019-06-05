import psycopg2

connection = psycopg2.connect(
    host='candidate-test-2.cg4nxczsn7yj.us-east-1.rds.amazonaws.com',
    port='5432',
    user='candidate_test_2',
    password='sj7ZWaC9',
    database='candidate_test'
)

cursor = connection.cursor()
cursor.execute("""SELECT * FROM rates""")
for result in cursor.fetchall():
    print(result)

connection.close()
