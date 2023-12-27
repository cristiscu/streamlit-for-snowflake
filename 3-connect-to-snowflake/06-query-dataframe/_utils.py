import os
from snowflake.snowpark import Session

def getSession():
    return Session.builder.configs({
        "account": 'hdb90888',
        "user": 'cristiscu',
        "password": os.environ['SNOWSQL_PWD'],
        "database": 'TESTS',
        "schema": 'PUBLIC'
    }).create()
