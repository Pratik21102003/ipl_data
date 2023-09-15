import pandas as pd
import numpy as np
import streamlit as st
from matplotlib import pyplot as plt
data=pd.read_csv("C:/Users/Pratik/Desktop/pratik/panda basic/ipl-matches.csv")
data1=pd.read_csv("C:/Users/Pratik/Desktop/pratik/panda basic/deliveries.csv")
st.sidebar.title('IPL Data Analysis')
option=st.sidebar.selectbox('Select One',['Teams','Batter','Bowler'])
if option == 'Teams':
    select=st.sidebar.selectbox('Teams',sorted(pd.concat((data['Team1'],data['Team2'])).unique()))
    btn1=st.sidebar.button('Analysis')
    if btn1:
        st.title(select)
        d1=data[(data['Team1']==select)|(data['Team2']==select)]
        col1,col2,col3=st.columns(3)
        with col1:
           st.metric('Matches Played',d1['MatchNumber'].count())
        with col2:
            st.metric('Matches Won',d1[d1['WinningTeam']==select]['MatchNumber'].count())
        with col3:
            st.metric('Matches Lost',d1[d1['WinningTeam']!=select]['MatchNumber'].count())
        col1,col2=st.columns(2)
        with col1:
            d2=data1[data1['batting_team']==select]
            a=d2.groupby(['match_id','bowling_team'])['total_runs'].sum().sort_values(ascending=False).reset_index().set_index('bowling_team')
            st.dataframe(a['total_runs'].head())
        with col2:
            d2=data1[data1['batting_team']==select]
            a=d2.groupby(['match_id','bowling_team'])['total_runs'].sum().sort_values(ascending=False).reset_index().set_index('bowling_team')
            st.dataframe(a['total_runs'].tail())
elif option == 'Batter':
    select=st.sidebar.selectbox('Batter',sorted(pd.concat((data1['batsman'],data1['non_striker'])).unique()))
    btn2=st.sidebar.button('Analysis')
    if btn2:
        st.title(select)
else:
    select=st.sidebar.selectbox('Bowler',sorted(data1['bowler'].unique()))
    btn3=st.sidebar.button('Analysis')
    if btn3:
        st.title(select)