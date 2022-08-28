import streamlit as st
import pandas as pd


@st.cache
def athlete(df,region_df):
    
    # filtering for summer olympics
    df = df[df['Season']=='Summer']
    #merge with region_df
    df =df.merge(region_df,on='NOC', how='left')
    # dropping duplicated
    df.drop_duplicates(inplace=True)
    # one hot encoding medal
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis =1)
    
    return df