# ML Object Detection with a CNN Data Science Streamlit App

From [**Turn Python Scripts into Beautiful ML Tools**](https://medium.com/towards-data-science/coding-ml-tools-like-you-code-ml-models-ddba3357eace) blog post, by *Adrien Treuille*, co-founder of Streamlit and current Head of Streamlit at Snowflake.

The demo is also open-sourced in GitHub as [**Streamlit Demo: The Udacity Self-driving Car Image Browser**](https://github.com/streamlit/demo-self-driving/tree/master)

The *OpenCV* library is required as well for this experiment (see the **requirements.txt** file). The demo will download two remote files, but always exclude **yolov3.weights** from the GitHub repository, as it is too large.

## Actions

Run **`pip install -r requirements.txt`** to install all new Python dependencies.

From the current subfolder, run from a Terminal **`streamlit run app.py`**. Quit the local Streamlit web app session with CTRL+C.

The app will first install a very large *yolov3.weights* file. To make sure you do not try to push it into GitHub by accident, just delete it after running the experiment.