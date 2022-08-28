import numpy as np
import streamlit as st

# @st.cache
def fetch_medal(df,year,country):
    medal_df = df.drop_duplicates(subset='Team NOC Games Year City Sport Event Medal'.split())    
    
    flag = 0
    if year == 'overall' and country == 'overall':
        temp_df = medal_df
        
    if year == 'overall' and country != 'overall':
        flag = 1
        temp_df = medal_df[medal_df['region']== country ]
        
    if year != 'overall' and country == 'overall':
         temp_df = medal_df[medal_df['Year']== int(year) ]
    
    if year != 'overall' and country != 'overall':
        temp_df = medal_df[(medal_df['Year'] == year) &  (medal_df['region'] == country)]   
        
    if flag == 1:
        x = temp_df.groupby('Year')[['Gold', 'Silver','Bronze']].sum().sort_values('Year').reset_index()

    else:
        x = temp_df.groupby('region')[['Gold', 'Silver','Bronze']].sum().sort_values('Gold',ascending=False).reset_index()
        
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']   
    
    return x


# @st.cache
def medal(df):
    
    medal_tally=df.drop_duplicates(subset='Team NOC Games Year City Sport Event Medal'.split())

    medal_tally = medal_tally.groupby('region')[['Gold', 'Silver','Bronze']].sum().sort_values('Gold',ascending=False).reset_index()

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold']= medal_tally['Gold'].astype('int')
    medal_tally['Silver']= medal_tally['Silver'].astype('int')
    medal_tally['Bronze']= medal_tally['Bronze'].astype('int')
    medal_tally['total']= medal_tally['total'].astype('int')


    return medal_tally


# @st.cache
def country_year_list(df):

    years= df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'overall')

    country= np.unique(df['region'].dropna()).tolist()
    country.insert(0,'overall')

    return years, country


# @st.cache
def dataovertime(df,col):

    nation_overtime = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nation_overtime.rename(columns={'index' : 'Editions' , 'Year': col}, inplace=True)

    return nation_overtime

def most_succes(df,sport):
    temp_df = df.dropna(subset = ['Medal'])
    
    if sport != 'overall':
        temp_df = temp_df[temp_df['Sport']== sport]
        
    x=temp_df["Name"].value_counts().reset_index().head(20).merge(df, left_on = 'index', right_on= 'Name', how = 'left')[['index', 'Name_x','Sport' ,'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name','Name_x': 'Medals'},inplace =True)
    return x

def yearwise(df, country):
    temp_df = df.dropna(subset=['Medal'])    
    temp_df.drop_duplicates(subset='Team NOC Games Year City Sport Event Medal'.split(),inplace=True)
    new_df= temp_df[temp_df['region']== country]
    final_df= new_df.groupby('Year').count()['Medal'].reset_index()
    
    return final_df

# @st.cache
def country_heat(df, country):
    temp_df = df.dropna(subset=['Medal'])    
    temp_df.drop_duplicates(subset='Team NOC Games Year City Sport Event Medal'.split(),inplace=True)
    new_df= temp_df[temp_df['region']== country]

    pt = new_df.pivot_table(index='Sport', columns='Year',values= "Medal",aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df,country):
    temp_df = df.dropna(subset = ['Medal'])
 
    temp_df = temp_df[temp_df['region']== country]
        
    x=temp_df["Name"].value_counts().reset_index().head(10).merge(df, left_on = 'index', right_on= 'Name', how = 'left')[['index', 'Name_x','Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name','Name_x': 'Medals'},inplace =True)
    return x

def weight_vs_height(df,sport):

    athletes_df = df.drop_duplicates(subset=['Name', 'region'])
    athletes_df['Medal'].fillna('No medals',inplace =True)

    temp_df = athletes_df[athletes_df['Sport'] == sport]

    return temp_df
   

def men_vs_women(df):


    athletes_df = df.drop_duplicates(subset=['Name', 'region'])

    men= athletes_df[athletes_df['Sex']== 'M'].groupby("Year").count()['Name'].reset_index()
    women = athletes_df[athletes_df['Sex']== 'F'].groupby("Year").count()['Name'].reset_index()

    final = men.merge(women ,on='Year')

    final.rename(columns={'Name_x': 'Male' , 'Name_y': 'femal'}, inplace = True)

    return final
