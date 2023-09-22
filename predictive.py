import numpy as np
import pandas as pd
import warnings
from datetime import datetime as dt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
warnings.filterwarnings('ignore')
import streamlit as st
from snowflake.snowpark import Session

def predict():
   CONNECTION_PARAMETERS = {
      "account": "od21480.ap-southeast-1",
      "user": "JADE",
      "password": "Welcome@123",
       "database": "FINANCIALS",
      "schema": "PROD",
      "warehouse": "COMPUTE_WH",
   }
   sql_query='SELECT * FROM FINANCIALS.PROD.FINANCE_PREDICT'
   session = Session.builder.configs(CONNECTION_PARAMETERS).create()
   df = session.sql(sql_query).collect()
   df = pd.DataFrame(df, columns=['DATE','REVENUE','RND'])
   df["DATE"] = df['DATE'].apply(lambda x: dt.strptime(x, '%b-%y'))
   ts_sales = df['REVENUE']
   ts_rnd = df['RND']
   X_train, X_test, y_train, y_test = train_test_split(ts_rnd, ts_sales, train_size=0.8, random_state=50)
   lr = LinearRegression()
   lr.fit(np.array(X_train.values).reshape(-1,1), np.array(y_train.values).reshape(-1,1))
   
   #y_pred = lr.predict(np.array([7240, 7310]).reshape(-1,1))
   #y_pred
   
   