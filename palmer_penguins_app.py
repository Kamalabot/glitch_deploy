import warnings
warnings.filterwarnings('ignore')
import streamlit as st
import numpy as np 
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

st.write("""
         ## The Great Penguin Classifier
         This app that predicts the type of Penguin from the size data
         """)

st.sidebar.header("User input features")


st.sidebar.markdown("""
The CSV file can be loaded for prediction
                    """)
uploaded_file  = st.sidebar.file_uploader("Upload input csv file ",type=["csv"])

if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    def user_input_data():
        island = st.sidebar.selectbox('Island',('Biscoe','Dream','Torgersen'))
        sex = st.sidebar.selectbox('Sex',('male','female'))
        bill_length = st.sidebar.slider('Bill length (mm)', 32.1,59.6,43.9)
        bill_depth = st.sidebar.slider('Bill depth (mm)', 13.1,21.6,17.2)
        flipper_length = st.sidebar.slider('Flipper Length (mm)', 172.1,231.6,201.2)
        body_mass = st.sidebar.slider('Body Mass (g)',2700, 6800, 4207)

        data = {'island':island,
                'sex':sex,
                'bill_length_mm':bill_length,
                'bill_depth_mm':bill_depth,
                'flipper_length_mm':flipper_length,
                'body_mass_g':body_mass}
        feature = pd.DataFrame(data, index=[0])
        return feature
    input_df = user_input_data()

penguins_raw = pd.read_csv('penguins_cleaned.csv')
penguins = penguins_raw.drop(columns=['species'])
df = pd.concat([input_df, penguins],axis=0)

encode = ['sex','island']
for col in encode:
    dummy = pd.get_dummies(df[col],prefix=col)
    df = pd.concat([df,dummy],axis=1)
    del df[col]

df = df[:1]

st.subheader('User input features')

if uploaded_file is not None:
    st.write(df)
else:
    st.subheader('using example data')
    st.write(df)

load_clf = pickle.load(open('penguinKlassifier.pkl','rb'))

prediction = load_clf.predict(df)
predict_proba = load_clf.predict_proba(df)

penguin_species = np.array(['Adele','Chinstrap','Gentoo'])
st.write(penguin_species[prediction])

st.subheader('Probability')
st.write(predict_proba)
