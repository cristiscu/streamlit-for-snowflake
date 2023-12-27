import os, configparser
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session

# customize with your own local connection parameters
def getSession():
    try:
        return get_active_session()
    except:
        parser = configparser.ConfigParser()
        parser.read(os.path.join(os.path.expanduser('~'), ".snowsql/config"))
        section = "connections.demo_conn"
        pars = {
            "account": parser.get(section, "accountname"),
            "user": parser.get(section, "username"),
            "password": os.environ['SNOWSQL_PWD']
        }
        return Session.builder.configs(pars).create()
