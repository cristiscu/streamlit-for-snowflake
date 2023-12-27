import os, sys, configparser
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import udf, col
from snowflake.snowpark.types import Variant
from snowflake.snowpark import functions as fn
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
import sklearn.feature_extraction.text as txt
from sklearn import svm
from joblib import dump
import joblib
import cachetools

st.set_page_config(
    page_title="Snowflake Sentiment Analysis Demo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")
st.title("Sentiment Analysis")

# customize with your own local connection parameters
@st.cache_resource(show_spinner="Connecting to Snowflake...")
def getSession():
    parser = configparser.ConfigParser()
    parser.read(os.path.join(os.path.expanduser('~'), ".snowsql/config"))
    section = "connections.demo_conn"
    pars = {
        "account": parser.get(section, "accountname"),
        "user": parser.get(section, "username"),
        "password": os.environ['SNOWSQL_PWD'],
        "database": 'IMDB',
        "schema": 'PUBLIC'
    }
    session = Session.builder.configs(pars).create()
    session.clear_imports()
    session.clear_packages()
    session.add_packages("snowflake-snowpark-python",
        "scikit-learn", "pandas", "numpy", "nltk", "joblib", "cachetools")
    return session

#session = getSession()

##################################################################
# ML
##################################################################

# #### Train function
def train_model_review_pipline(session: Session, train_dataset_name: str) -> Variant:
    
    train_dataset = session.table(train_dataset_name)
    train_dataset_flag = train_dataset.withColumn("SENTIMENT_FLAG", 
        fn.when(train_dataset.SENTIMENT == "positive", 1).otherwise(2))
    train_x = train_dataset_flag.toPandas().REVIEW.values
    train_y = train_dataset_flag.toPandas().SENTIMENT_FLAG.values
    print('Taille train x : ', len(train_x))
    print('Taille train y : ', len(train_y))
    
    print('Configuring parameters ...')
    # bags of words: parametrage
    analyzer = u'word' # {‘word’, ‘char’, ‘char_wb’}
    ngram_range = (1,2) # unigrammes
    token = u"[\\w']+\\w\\b" #
    max_df=0.02    #50. * 1./len(train_x)  #default
    min_df=0.01
    if len(train_x) > 0: min_df = 1 * 1./len(train_x) # on enleve les mots qui apparaissent moins de 1 fois
    binary=True # presence coding
    svm_max_iter = 100
    svm_c = 1.8
    
    print('Building Sparse Matrix ...')
    vec = txt.CountVectorizer(
        token_pattern=token,
        ngram_range=ngram_range,
        analyzer=analyzer,
        max_df=max_df,
        min_df=min_df,
        vocabulary=None, 
        binary=binary)

    # pres => normalisation
    bow = vec.fit_transform(train_x)
    print('Taille vocabulaire : ', len(vec.get_feature_names_out()))
    
    print('Fitting model ...')
    model = svm.LinearSVC(C=svm_c, max_iter=svm_max_iter)
    print(model.fit(bow, train_y))
    
    # Upload the Vectorizer (BOW) to a stage
    print('Upload the Vectorizer (BOW) to a stage')
    model_output_dire = '/tmp'
    model_file = os.path.join(model_output_dire, 'vect_review.joblib')
    dump(vec, model_file, compress=True)
    session.file.put(model_file, "@stage_models", auto_compress=False, overwrite=True)
    
    # Upload trained model to a stage
    print('Upload trained model to a stage')
    model_output_dire = '/tmp'
    model_file = os.path.join(model_output_dire, 'model_review.joblib')
    dump(model, model_file, compress=True)
    session.file.put(model_file, "@stage_models", auto_compress=False, overwrite=True)
    
    return {"STATUS": "SUCCESS", "R2 Score Train": str(model.score(bow, train_y))}


# Function to load the model from the Internal Stage (Snowflake)
@cachetools.cached(cache={})
def load_file(filename):
    import_dir = sys._xoptions.get("snowflake_import_directory")
    if import_dir:
        with open(os.path.join(import_dir, filename), 'rb') as file:
            return joblib.load(file)


##################################################################
# FUNCTIONS
##################################################################

schema_name = "PUBLIC"
target_column_name = "SENTIMENT"

def train_model(table):

    session = getSession()
    session.sproc.register(
        func=train_model_review_pipline,
        name="train_model_review_pipline",
        replace=True)
    session.call("train_model_review_pipline", table)
    
    # Import the needed files from the stage
    session.add_import("@stage_models/model_review.joblib")
    session.add_import("@stage_models/vect_review.joblib")

    # Deploy an UDF for prediction
    @udf(name='predict_review', session=session,
        stage_location='@stage_models', is_permanent=False, replace=True)
    def predict_review(args: list) -> float:
        import pandas as pd

        model = load_file("model_review.joblib")
        vec = load_file("vect_review.joblib")
            
        features = list(["REVIEW", "SENTIMENT_FLAG"])
        row = pd.DataFrame([args], columns=features)
        bowTest = vec.transform(row.REVIEW.values)
        
        return model.predict(bowTest)

def assess_performance(y_pred, y_test):

    Accuracy = accuracy_score(y_test, y_pred) * 100
    Recall = recall_score(y_test, y_pred, average='weighted') * 100
    Precision = precision_score(y_test, y_pred, average='weighted') * 100
    F1_Score = f1_score(y_test, y_pred, average='weighted') * 100
    return Accuracy, Recall, Precision, F1_Score

def assess_performance_df(y_pred, y_test):

    print("Accuracy: ", accuracy_score(y_test, y_pred))
    print("Recall: ", recall_score(y_test, y_pred, average='weighted'))
    print("Precision: ", precision_score(y_test, y_pred, average='weighted'))
    print("F1 Score: ", f1_score(y_test, y_pred, average='weighted'))
    d = {
        'Metric': ['Accuracy', 'Recall', 'Precision', 'F1 Score'],
        'Score (%)': [
            accuracy_score(y_test, y_pred) * 100, \
            recall_score(y_test, y_pred, average='weighted') * 100, \
            precision_score(y_test, y_pred, average='weighted') * 100, \
            f1_score(y_test, y_pred, average='weighted') * 100
        ]}
    df = pd.DataFrame(data=d)
    return df

##################################################################
# STREAMLIT APP
##################################################################

with st.sidebar:
    option = option_menu("Menu", ["Load Data", "Analyze", "Train Model", "Model Monitoring",
            "Model Catalog", "Inference", "Inference Runs", "Clean up"],
        icons=['download', 'graph-up', 'play-circle', '', 'list-task', 'boxes', 'speedometer2', ''],
        menu_icon="menu-button-wide", default_index=0, styles={
            "container": {"padding": "5!important", "background-color": "white","font-color": "#249dda"},
            "icon": {"color": "#31c0e7", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "white"},
            "nav-link-selected": {"background-color": "7734f9"}})

if option == "Load Data":
    
    if st.button(' ▶️  Setup Database & Upload Files'):
        with open("deploy.sql", "r") as f:
            content = f.read().split(";")
            for statement in content:
                if statement and statement != "":
                    st.code(statement)            
                    getSession().sql(statement).collect()

elif option == "Analyze":

    st.subheader('Tables available')
    session = getSession()
    df_tables = (session.table('information_schema.tables')
        .filter(col("table_schema") == schema_name)
        .select("table_name", "row_count", "created"))
    pd_tables = df_tables.to_pandas()
    st.dataframe(pd_tables)
        
    st.subheader('Analyze Dataset')
    list_tables_names = pd_tables["TABLE_NAME"].values.tolist()
    table_to_print = st.selectbox(
        "Select table to describe statistics:",
        list_tables_names)
    table_to_print = schema_name + "." + table_to_print
    df_table = session.table(table_to_print)
    pd_table = df_table.limit(10).to_pandas()
    pd_describe = df_table.describe().to_pandas()
    
    with st.expander("Statistics", True):
        col0, col1, col2 = st.columns(3)
        with col0:
            total = df_table.count()
            st.metric(label="Total", value=total)
        with col1:
            positive = df_table.filter(col(target_column_name) == 'positive').count()
            st.metric(label="Positive", value=positive)
        with col2:                
            negative = df_table.filter(col(target_column_name) == 'negative').count()
            st.metric(label="Negative", value=negative)

    with st.expander("Sample Data", True):
        st.subheader(table_to_print)
        st.dataframe(pd_table)

    with st.expander("Data Description", True):
        st.subheader('Data Description')
        st.dataframe(pd_describe)
        
elif option == "Train Model":

    st.subheader("Train Dataset")
    df_tables = (getSession()
        .table('information_schema.tables')
        .filter(col("table_schema") == schema_name)
        .select("table_name"))
    pd_tables = df_tables.to_pandas()
    
    list_tables_names = pd_tables["TABLE_NAME"].values.tolist()
    table_to_train = st.selectbox("Select table to train model:", list_tables_names)
    table_to_train = schema_name + "." + table_to_train

    with st.expander("Configuration", True):
        col1, col2 = st.columns(2)
        with col1:
            st.write ('Table selected :')
            st.write ('Algorithm used :')
        with col2:
            st.write(table_to_train)
            st.write ('SVM')
            
    st.button('▶️  Train Model', on_click=train_model, args=(table_to_train,))
                        
elif option == 'Model Monitoring':

    st.subheader('Monitoring')
    df_query_history = (getSession()
        .sql("SELECT * FROM table(information_schema.query_history())")
        .to_pandas())
    st.dataframe(df_query_history, use_container_width=True)

    if st.button('▶️  Refresh'):
        st.experimental_rerun()

elif option == "Model Catalog":
    
    st.subheader('Models')
    data = getSession().sql("LIST @stage_models").collect()
    st.dataframe(data, use_container_width=True)

elif option == "Inference":

    subtab_test_dataset, subtab_accuracy = st.tabs(['Test Dataset', 'Accuracy'])
    with subtab_test_dataset:
        st.subheader('Statistics')
        test_dataset = getSession().table("TEST_DATASET")
        new_df = test_dataset.withColumn("SENTIMENT_FLAG",
            fn.when(test_dataset.SENTIMENT == "positive", 1).otherwise(2))        
        df_predict = (new_df
            .select(new_df.REVIEW, new_df.SENTIMENT, new_df.SENTIMENT_FLAG,
                fn.call_udf("predict_review",
                    fn.array_construct(col("REVIEW"), col("SENTIMENT_FLAG")))
                        .alias('PREDICTED_REVIEW')))
        df_predict.write.mode('overwrite').saveAsTable('REVIEW_PREDICTION')
        
        col0, col1, col2 = st.columns(3)
        with st.container():
            with col0 :
                total = new_df.count()
                st.metric(label="Total", value=total)
            with col1:
                positive = df_predict.filter(col(target_column_name) == 'positive').count()
                st.metric(label="Positive", value=positive)
            with col2:                
                negative = df_predict.filter(col(target_column_name) == 'negative').count()
                st.metric(label="Negative", value=negative)

        st.subheader('Sample Data')
        st.dataframe(new_df.to_pandas())

    with subtab_accuracy:

        st.subheader('Score')        
        df_predict = getSession().table("REVIEW_PREDICTION")
        Accuracy, Recall, Precision, F1_Score = assess_performance(
            df_predict.toPandas().PREDICTED_REVIEW,
            df_predict.toPandas().SENTIMENT_FLAG)

        col0, col1, col2, col3 = st.columns(4)
        with st.container():
            with col0: st.metric(label="Accuracy", value=Accuracy)
            with col1: st.metric(label="Recall", value=Recall)
            with col2: st.metric(label="Precision", value=Precision)
            with col3: st.metric(label="F1_Score", value=F1_Score)

elif option == "Inference Runs":

    st.subheader('Prediction')
    with st.container():
        df_tables = (getSession()
            .table('information_schema.tables')
            .filter(col("table_schema") == schema_name)
            .select("table_name"))
        pd_tables = df_tables.to_pandas()
        list_tables_names = pd_tables["TABLE_NAME"].values.tolist()

        table_to_predict = st.selectbox(
            "Select your new dataset to predict :",
            list_tables_names)
        table_to_print = schema_name + "." + table_to_predict
        test_dataset = getSession().table(table_to_predict)
        new_df = (test_dataset.withColumn("SENTIMENT_FLAG",
            fn.when(test_dataset.SENTIMENT == "positive", 1).otherwise(2)))
        
        df_predict = (new_df
            .select(new_df.REVIEW, new_df.SENTIMENT, new_df.SENTIMENT_FLAG,
                fn.call_udf("predict_review", 
                    fn.array_construct(col("REVIEW"), col("SENTIMENT_FLAG")))
                .alias('PREDICTED_REVIEW')))
        df_predict = (df_predict
            .withColumn("PREDICTED_REVIEW_LABEL",
                fn.when(df_predict.PREDICTED_REVIEW == 1, "positive").otherwise("negative")))
        df_predict.write.mode('overwrite').saveAsTable('NEW_REVIEW_PREDICTION')            
        st.dataframe(df_predict.select("REVIEW", "PREDICTED_REVIEW_LABEL").to_pandas())

elif option == "Clean up":

    if st.button(' ▶️  Clean database'):
        getSession().sql("DROP DATABASE IF EXISTS IMDB").collect()
        st.write("Database and all related objects are properly cleaned")
