-- to select and execute all from a SQL Worksheet from your Snowflake web UI
CREATE OR REPLACE DATABASE FROSTY_SAMPLE;
CREATE SCHEMA CYBERSYN_FINANCIAL;

-- Create the limited attributes view
CREATE VIEW FROSTY_SAMPLE.CYBERSYN_FINANCIAL.FINANCIAL_ENTITY_ATTRIBUTES_LIMITED AS
    SELECT * from financial__economic_essentials.cybersyn.financial_institution_attributes
    WHERE VARIABLE IN ('ASSET', 'ESTINS', 'LNRE', 'DEP', 'SC');

-- Confirm the view was created correctly - should show 6 rows with variable name and definition
SELECT *
FROM FROSTY_SAMPLE.CYBERSYN_FINANCIAL.FINANCIAL_ENTITY_ATTRIBUTES_LIMITED;

-- Create the modified time series view
CREATE VIEW IF NOT EXISTS FROSTY_SAMPLE.CYBERSYN_FINANCIAL.FINANCIAL_ENTITY_ANNUAL_TIME_SERIES AS
    SELECT ent.name as entity_name, ent.city, ent.state_abbreviation,
        ts.variable_name, year(ts.date) as "YEAR", to_double(ts.value) as value,
        ts.unit, att.definition
    FROM financial__economic_essentials.cybersyn.financial_institution_timeseries AS ts
        INNER JOIN FROSTY_SAMPLE.CYBERSYN_FINANCIAL.FINANCIAL_ENTITY_ATTRIBUTES_LIMITED att
        ON (ts.variable = att.variable)
        INNER JOIN financial__economic_essentials.cybersyn.financial_institution_entities AS ent
        ON (ts.id_rssd = ent.id_rssd)
    WHERE MONTH(date) = 12 AND DAY(date) = 31;

-- Confirm the view was created correctly and view sample data
select *
from FROSTY_SAMPLE.CYBERSYN_FINANCIAL.FINANCIAL_ENTITY_ANNUAL_TIME_SERIES
limit 10;