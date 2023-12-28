import os
import snowflake.connector

conn = snowflake.connector.connect(
    account='hdb90888',
    user='cristiscu',
    password=os.environ['SNOWSQL_PWD'],
    database='TESTS',
    schema='PUBLIC',
    role='ACCOUNTADMIN',
    warehouse='COMPUTE_WH'
)

# (1) fetching row by row
cur = conn.cursor()
cur.execute('select * from tests.public.employees')
for row in cur: print(row)

# (2) getting the whole set
df = cur.fetch_pandas_all()
print(df)
