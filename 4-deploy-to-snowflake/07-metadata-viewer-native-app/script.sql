-- consumer script, automatically triggered after an APPLICATION is created in the deploy script
CREATE APPLICATION ROLE hierarchical_metadata_role;

-- create versioned schema
CREATE OR ALTER VERSIONED SCHEMA app;
GRANT USAGE ON SCHEMA app
  TO APPLICATION ROLE hierarchical_metadata_role;

-- add Streamlit object
CREATE STREAMLIT app.hierarchical_metadata
  FROM '/'
  MAIN_FILE = '/Main.py';
GRANT USAGE ON STREAMLIT app.hierarchical_metadata
  TO APPLICATION ROLE hierarchical_metadata_role;
