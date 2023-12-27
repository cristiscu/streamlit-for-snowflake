import os
import snowflake.connector

def getConnection():
    return snowflake.connector.connect(
        account='hdb90888',
        user='cristiscu',
        password=os.environ['SNOWSQL_PWD'],
        database='TESTS',
        schema='PUBLIC'
    )
