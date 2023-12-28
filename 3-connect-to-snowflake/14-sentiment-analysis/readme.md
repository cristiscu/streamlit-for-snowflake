# Create a NLP Sentiment Analysis App with the IMDB Reviews

Simplified version of the [**NLP and ML with Snowpark Python and Streamlit for Sentiment Analysis**](https://quickstarts.snowflake.com/guide/end_to_end_nlp_and_ml_using_snowpark_python_and_streamlit:_sentiments_analysis/index.html?index=..%2F..index#0) quickstart tutorial. Machine Learning Binary Classification problem, with the SVM algorithm, on the IMDB dataset of more than 10K movie reviews. Download and upload the *TEST_DATASET.csv* and *TRAIN_DATASET.csv* (large!) files in the *data* subfolder.

* **deploy.sql** - SQL script to upload the *data/TEST_DATASET.csv* and *data/TRAIN_DATASET.csv* (large!) files into Snowflake tables.
* **app.ipynb** - Jupyter Notebook notebook, to be executed eventually in VSCode or Google Colab. This will push the training sequence into a stored proc in Snowflake, using Snowpark registration functions. And will deploy a UDF for predictions.
* **app.py** - adapted local Streamlit web app, with all the step required to run the experiment and serve the model. This will push the training sequence into a stored proc in Snowflake, using Snowpark registration functions. And will call the deployed UDF for predictions.
* **requirements.txt** - all dependencies, with many data science packages for NLP.