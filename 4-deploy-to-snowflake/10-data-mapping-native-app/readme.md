# Enrich IP Address Data with a Snowflake Native App

Simplified version of the [**Data Mapping in Snowflake Native Apps using Streamlit**](https://quickstarts.snowflake.com/guide/data_mapping_in_native_apps/index.html?index=..%2F..index#0) quickstart tutorial.

It uses the [**IP2Location**](https://www.ip2location.com/database/ip2location) external Internet service, with [a free version here](https://lite.ip2location.com/database/db11-ip-country-region-city-latitude-longitude-zipcode-timezone). I kept just 100 rows of sample data in the *data/ip2location-small.csv* file.

* **manifest.yml** - required by the Snowflake Native App Framework.
* **script.sql** - required by the Snowflake Native App Framework.
* **app.py** - single-page native app Python code.
* **deploy.sql** - deployment script, as a native app.

## Actions

To deploy the app as a Native App, run **`snowsql -c my_conn -f deploy.sql`**. Check that there are no errors (i.e. no text in red on screen). Switch to the Snowflake web UI and run/test/edit the app there.

To share it with other accounts from your organization, deploy the APPLICATION PACKAGE in a private listing, and specifying other account names. The consumer can get the shared app from its Apps folder.

The deployment script uploads the **data/ip2location-small.csv** file into a private table, exposed to the consumer through secure views, secure procedures and secure UDFs. A test table - that can be easily replicated on the consumer side - is provided as well. The consumer table is unknown when the native app is deployed, but the process of assigning access rights to the external application is automated.