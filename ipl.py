import pandas as pd
import numpy as np
import streamlit as st
from matplotlib import pyplot as plt
data=pd.read_csv("C:/Users/Pratik/Desktop/pratik/panda basic/ipl-matches.csv")
data1=pd.read_csv("C:/Users/Pratik/Desktop/pratik/panda basic/deliveries.csv")
st.sidebar.title('IPL Data Analysis')
option=st.sidebar.selectbox('Select One',['Teams','Player'])
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
            st.subheader('Highest Team Total')
            d2=data1[data1['batting_team']==select]
            a=d2.groupby(['match_id','bowling_team'])['total_runs'].sum().sort_values(ascending=False).reset_index().set_index('bowling_team')
            st.dataframe(a['total_runs'].head())
        with col2:
            st.subheader('lowest Team Total')
            d2=data1[data1['batting_team']==select]
            a=d2.groupby(['match_id','bowling_team'])['total_runs'].sum().sort_values(ascending=False).reset_index().set_index('bowling_team')
            st.dataframe(a['total_runs'].tail())
elif option == 'Player':
    select=st.sidebar.selectbox('Batter',sorted(pd.concat((data1['batsman'],data1['non_striker'])).unique()))
    btn2=st.sidebar.button('Analysis')
    if btn2:
        st.subheader(select)
        st.subheader("Played for Teams")
        st.markdown(data1[data1['batsman']==select]['batting_team'].drop_duplicates().values)
        col1,col2,col3=st.columns(3)
        with col1:
            st.metric('Matches played',data1[(data1['batsman']==select)|(data1['bowler']==select)]['match_id'].drop_duplicates(keep="first").count())
        with col2:
            st.metric('Total Runs',data1[data1['batsman']==select]['total_runs'].sum())   
        with col3:
            st.metric('Highest Runs',data1[data1['batsman']==select].groupby('match_id')['total_runs'].sum().sort_values().tail(1)) 
        col1,col2,col3=st.columns(3)
        with col1:
            st.metric('Ball Faced',data1[data1['batsman']==select]['ball'].count())
        with col2:
            a=data1[data1['batsman']==select]['match_id'].drop_duplicates(keep="first").count()- data1[data1['player_dismissed']==select].shape[0]
            b=data1[data1['batsman']==select]['total_runs'].sum()
            c=data1[data1['batsman']==select]['match_id'].drop_duplicates(keep="first").count()-a
            st.metric('Batting Avg',round(b/c,2))
        with col3:
            a=data1[data1['batsman']==select]['ball'].count()
            b=data1[data1['batsman']==select]['total_runs'].sum()
            st.metric('Strike Rate',round(b/a*100,2))
        col1,col2,col3=st.columns(3)
        with col1:
            c=0
            a1=data1[data1['batsman']== select]
            s=a1.groupby('match_id')['total_runs'].sum()
            for i in s.values:
             if i>=100:
              c=c+1
            st.metric('No. of Centuries',c)
        with col2:
             c=0
             a1=data1[data1['batsman']== select]
             s=a1.groupby('match_id')['total_runs'].sum()
             for i in s.values:
              if i>=50 and i<100:
               c=c+1
             st.metric('No. of Half-Centuries',c)
        with col3:
            a=data1[data1['batsman']== select]
            c=a[(a['batsman_runs']==4)|(a['batsman_runs']==6)].shape[0]
            st.metric('No. of Boundaries',c)
        col1,col2=st.columns(2)
        with col1:
         show1=data1[data1['batsman']==select].groupby('bowling_team')['total_runs'].sum().sort_values(ascending=False)
         st.subheader('Runs against teams')
         fig,ax=plt.subplots()
         ax.plot(show1.index,show1.values,marker='.',linewidth=2,markersize=10)
         plt.xticks(rotation='vertical')
         plt.grid()
         st.pyplot(fig)
        with col2:
            st.subheader('Strike Rate againts teams')
            a=data1[data1['batsman']==select].groupby('bowling_team')['ball'].count()
            b=data1[data1['batsman']==select].groupby('bowling_team')['total_runs'].sum()
            show1=round(b/a*100,2)
            fig,ax=plt.subplots()
            ax.scatter(show1.index,show1.values)
            plt.xticks(rotation='vertical')
            plt.grid()
            st.pyplot(fig)