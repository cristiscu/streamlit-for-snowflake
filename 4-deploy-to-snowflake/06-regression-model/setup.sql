CREATE OR REPLACE DATABASE financial_regression;

CREATE STAGE stage;
-- LIST @stage;

-- What financial data is available as a time-series from FRED?
SELECT DISTINCT variable_name
FROM FINANCIAL__ECONOMIC_ESSENTIALS.CYBERSYN.FINANCIAL_FRED_TIMESERIES;

-- What is the size of the all the time-series data?
SELECT COUNT(*)
FROM FINANCIAL__ECONOMIC_ESSENTIALS.CYBERSYN.FINANCIAL_FRED_TIMESERIES;

-- What is the US inflation over time (annually)?
SELECT variable_name, date, value, unit
FROM FINANCIAL__ECONOMIC_ESSENTIALS.CYBERSYN.FINANCIAL_FRED_TIMESERIES
WHERE MONTH(date) = 1
AND variable_name = 'Personal Consumption Expenditures: Chain-type Price Index, Seasonally adjusted, Monthly, Index 2017=100'
ORDER BY date;

-- create first the UDF with the Jupyter Notebook!
-- SELECT predict_pce_udf(2024);