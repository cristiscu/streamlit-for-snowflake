# Enrich IP Address Data with a Snowflake Native App

Simplified version of the [**Data Mapping in Snowflake Native Apps using Streamlit**](https://quickstarts.snowflake.com/guide/data_mapping_in_native_apps/index.html?index=..%2F..index#0) quickstart tutorial.

It uses the [**IP2Location**](https://www.ip2location.com/database/ip2location) external Internet service, with [a free version here](https://lite.ip2location.com/database/db11-ip-country-region-city-latitude-longitude-zipcode-timezone). I kept just 100 rows of sample data in the *data/ip2location-small.csv* file.

* **manifest.yml** - required by the Snowflake Native App Framework.
* **script.sql** - required by the Snowflake Native App Framework.
* **app.py** - single-page native app Python code.
* **deploy.sql** - deployment script, as a native app.