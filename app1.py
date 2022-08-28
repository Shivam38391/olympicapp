from multiprocessing import Event
from select import select
import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.athlete(df,region_df)

st.sidebar.title("SUMMER Olympics Analysis")

st.sidebar.image("https://t4.ftcdn.net/jpg/03/16/84/69/240_F_316846937_dIF7KHIcrnC7JUBAI8Dtd0uOTbR6BvZe.jpg")
user = st.sidebar.radio(
    'Select an Options ',
    ('Medal Tally', 'Overall Analysis', 'Country-wise analysis','Athlete wise Analysis')
)

# st.dataframe(df)

if user == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select year', years)
    selected_country = st.sidebar.selectbox('Select country', country)


    medal_tally = helper.fetch_medal(df,selected_year,selected_country)
    if selected_year == 'overall' and selected_country == 'overall':
        st.title("Overall tally")

    if selected_year != 'overall' and selected_country == 'overall':
        st.title('Medal Tally in' + str(selected_year))

    if selected_year == 'overall' and selected_country != 'overall':
        st.title(selected_country + ' overall performance')

    if selected_year != 'overall' and selected_country != 'overall':
        st.title(selected_country  + ' performance in ' + str(selected_year) + ' olympics')   

    st.table(medal_tally)


# overall analysis

if user == 'Overall Analysis':
    editions = df.Year.nunique()
    Cities = df.City.nunique()
    Sports = df.Sport.nunique()
    Athletes = df.Name.nunique()
    Nations = df.region.nunique()
    Event = df.Event.nunique()

    st.title('TOP STATISTICS')

    col1, col2, col3 = st.columns(3)  #its display horizontly
    with col1:
        st.header('EDITIONS')
        st.title(editions)

    with col2:
        st.header('HOSTS')
        st.title(Cities)

    with col3:
        st.header('SPORTS')
        st.title(Sports)


    col1, col2, col3 = st.columns(3)  #its display horizontly in 2nd row
    with col1:
        st.header('EVENTS')
        st.title(Event)

    with col2:
        st.header('ATHLETES')
        st.title(Athletes)

    with col3:
        st.header('NATIONS')
        st.title(Nations)
    
    nation_overtime = helper.dataovertime(df, 'region')
    fig = px.line(nation_overtime , x='Editions', y ='region')
    st.title("PARTICIPATING NATIONS OVER THE YEAR")
    st.plotly_chart(fig)


    event_overtime = helper.dataovertime(df,'Event')
    fig = px.line(event_overtime , x='Editions', y ='Event')
    st.title("EVENTS OVER THE YEAR")
    st.plotly_chart(fig)

    athlete_overtime = helper.dataovertime(df,'Name')
    fig = px.line(athlete_overtime , x='Editions', y ='Name')
    st.title("ATHLETE OVER THE YEAR")
    st.plotly_chart(fig)

    st.title('No. of events over time (evry year)')
    fig,ax = plt.subplots(figsize=(10,8))

    x=df.drop_duplicates(['Year', 'Sport' , 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year',values= "Event",aggfunc='count').fillna(0) ,annot=True) 
    st.pyplot(fig)


    st.title("MOST SUCCESFUL ATHLETES")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'overall')

    selected_sport = st.selectbox('Select a sport', sport_list)
    x = helper.most_succes(df,selected_sport)
    st.table(x)

if user == 'Country-wise analysis':

    st.title("Country-wise analysis")



    years,country = helper.country_year_list(df)

    # selected_year = st.selectbox('Select year', years)
    selected_country = st.selectbox('Select country', country)




    country_df= helper.yearwise(df, selected_country)

    fig = px.line(country_df , x='Year', y ='Medal')
    st.title(selected_country + " MEDAL OVER THE YEAR")
    st.plotly_chart(fig)



    st.title(selected_country + " EXCEL IN THE FOLLOWING SPORTS")
    pt = helper.country_heat(df , selected_country)

    fig,ax = plt.subplots(figsize=(9,6))

    ax = sns.heatmap(pt,annot=True) 
    st.pyplot(fig)

    st.title("TOP 10 ATHLETES OF "+ selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)


if user == 'Athlete wise Analysis':
    athletes_df = df.drop_duplicates(subset=['Name', 'region'])
    x1= athletes_df["Age"].dropna()

    x2 = athletes_df[athletes_df["Medal"]=='Gold']['Age'].dropna()
    x3 = athletes_df[athletes_df["Medal"]=='Silver']['Age'].dropna()
    x4 = athletes_df[athletes_df["Medal"]=='Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4 ], 'overall_age Gold_medalist Silver Bronze'.split() ,show_hist= False, show_rug = False)


    fig.update_layout(autosize= False, width = 1000, height= 600)

    st.title("Distribution of age")
    st.plotly_chart(fig)


    x= []
    name = []
    famous = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
        'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
        'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
        'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Equestrianism',
        'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
        'Tennis', 'Modern Pentathlon', 'Golf', 'Softball', 'Archery',
        'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
        'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining',
        'Beach Volleyball', 'Triathlon', 'Rugby', 'Lacrosse', 'Polo',
        'Cricket', 'Ice Hockey']


    for i in famous:
        temp_df = athletes_df[athletes_df['Sport'] == i]
        x.append(temp_df[temp_df["Medal"]=='Gold']['Age'].dropna())
        name.append(i)

    fig = ff.create_distplot(x,name ,show_hist= False, show_rug = False)

    fig.update_layout(autosize= False, width = 1200, height= 600)
    st.title("Distribution of age  wrt Sports only Gold medalist")
    st.plotly_chart(fig)

    st.title("HEIGHT VS WEIGHT")

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'overall')

    selected_sport = st.selectbox('Select a sport', sport_list)
    temp_df = helper.weight_vs_height(df, selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'] , hue = temp_df["Medal"] , style=temp_df["Sex"])

    st.pyplot(fig)

    st.title("  Men vs Women participaton over the year ")

    final= helper.men_vs_women(df)
    fig = px.line(final , x = "Year" , y = ['Male','femal'])
    fig.update_layout(autosize= False, width = 1200, height= 600)

    st.plotly_chart(fig)


st.sidebar.write("MY FIRST DATA PROJECTS")
st.sidebar.write("created by SHIVAM SHARMA")
st.sidebar.write("GUIDED by NITISH SIR (youtuber('CAMPUS X') )")