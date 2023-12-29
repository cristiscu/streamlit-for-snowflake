-- consumer script, automatically triggered after an APPLICATION is created in the deploy script
CREATE APPLICATION ROLE ip2location_role;

-- create versioned schema
CREATE OR ALTER VERSIONED SCHEMA app;
GRANT USAGE ON SCHEMA app
  TO APPLICATION ROLE ip2location_role;

-- create secure view
CREATE SECURE VIEW app.litedb11 AS
  SELECT * FROM private.litedb11;
GRANT SELECT ON VIEW app.litedb11
  TO APPLICATION ROLE ip2location_role;

-- create secure UDF
CREATE SECURE FUNCTION app.ip2long(ip_address varchar(16))
  RETURNS string
  LANGUAGE JAVASCRIPT
AS $$
  var result = "";
  var parts = [];
  if (IP_ADDRESS.match(/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/)) {
    parts = IP_ADDRESS.split('.');
    result = (parts[0] * 16777216
      + (parts[1] * 65536)
      + (parts[2] * 256)
      + (parts[3] * 1));
  }
  return result;
$$;

-- accepts an ip address and converts it using the ip2long function above
CREATE SECURE FUNCTION app.ip2data(ip_address varchar(16))
  returns object
as $$
  select object_construct(
    'country_code', MAX(COUNTRY_CODE),
    'country_name', MAX(COUNTRY_NAME),
    'region_name', MAX(REGION_NAME),
    'city_name', MAX(CITY_NAME),
    'latitude', MAX(LATITUDE),
    'longitude', MAX(LONGITUDE),
    'zip_code', MAX(ZIP_CODE),
    'time_zome', MAX(TIME_ZONE))
  from app.litedb11
  where ip_from <= app.ip2long(ip_address)::int
    and ip_to >= app.ip2long(ip_address)::int
$$;

-- permissions callback we saw in the manifest.yml file
create secure procedure app.register_single_callback(
  ref_name string, operation string, ref_or_alias string)
  returns string
  language sql
as
begin
  case (operation)
    when 'ADD' then select system$set_reference(:ref_name, :ref_or_alias);
    when 'REMOVE' then select system$remove_reference(:ref_name);
    when 'CLEAR' then select system$remove_reference(:ref_name);
    else return 'Unknown operation: ' || operation;
  end case;
  system$log('debug', 'register_single_callback: ' || operation || ' succeeded');
  return 'Operation ' || operation || ' succeeded';
end;
grant usage on procedure app.register_single_callback(
  string, string, string) to application role ip2location_role;

-- consumer data is read and enhanced information is written
CREATE SECURE PROCEDURE app.enrich_ip_data(
  inp_field varchar, out_field varchar)
  RETURNS number
AS
DECLARE 
  q VARCHAR DEFAULT
    'UPDATE REFERENCE(''tabletouse'') SET ' || out_field
      || ' = app.ip2data(' || inp_field || ')';
  result INTEGER DEFAULT 0;
BEGIN
  EXECUTE IMMEDIATE q;
  RETURN RESULT;
END; 
GRANT USAGE ON PROCEDURE app.enrich_ip_data(varchar, varchar)
  TO APPLICATION ROLE ip2location_role;

-- test table, w/ test entries for Fuzhou/China + Chanthaburi/Thailand
CREATE TABLE app.test_data (IP VARCHAR(16), IP_DATA VARIANT);
GRANT SELECT, INSERT, UPDATE, REFERENCES ON TABLE app.test_data
  TO APPLICATION ROLE ip2location_role;
INSERT INTO app.test_data(IP) VALUES ('1.0.1.170'), ('1.0.177.230');

-- add Streamlit object
CREATE STREAMLIT app.ip2location
  FROM '/'
  MAIN_FILE = '/app.py';
GRANT USAGE ON STREAMLIT app.ip2location
  TO APPLICATION ROLE ip2location_role;

