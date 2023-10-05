import pandas as pd
import numpy as np
import streamlit as st
from matplotlib import pyplot as plt
data=pd.read_csv("C:/Users/Pratik/Desktop/pratik/panda basic/IPL_Ball_by_Ball_2008_2022.csv")
data1=pd.read_csv("C:/Users/Pratik/Desktop/pratik/panda basic/ipl-matches.csv")
df=data.merge(data1,how='outer',on='ID')
df.rename(columns={'Team2':'BowlingTeam'},inplace=True)

st.set_page_config(layout='wide')
st.sidebar.title('Select Options')
option=st.sidebar.selectbox('Select One',['Preview','Teams','Players'])
if option=='Preview':
    st.title('IPL Upto Year 2022 Preview')
    col1,col2,col3=st.columns(3)
    with col1:
        st.subheader('Winning Teams')
        st.dataframe(data1[data1['MatchNumber']=='Final'][['Season','WinningTeam']].value_counts('WinningTeam'))
    with col2:
        st.subheader('Orange Cap Holder')
        st.dataframe(df.groupby(['Season','batter'])['batsman_run'].sum().reset_index().sort_values('batsman_run',ascending=False).drop_duplicates(['Season'],keep='first').sort_values('Season').set_index('Season'))
    with col3:
        st.subheader('Purple Cap Holder')
        df.rename(columns={'isWicketDelivery':'WicketsTaken'},inplace=True)
        st.dataframe(df.groupby(['Season','bowler'])['WicketsTaken'].sum().reset_index().sort_values('WicketsTaken',ascending=False).drop_duplicates(['Season'],keep='first').sort_values('Season').set_index('Season'))

    col1,col2=st.columns(2)
    with col1:
        st.subheader('Most Number of Sixes')
        st.dataframe(df[df['batsman_run']==6]['batter'].value_counts().reset_index().set_index('batter').head(10))
    with col2:
        st.subheader('Venue with Most Sixes')
        st.dataframe(df[df['batsman_run']==6][['Venue','City']].value_counts().reset_index().set_index('City')['Venue'].head(10))
        
    st.subheader('Most Runs by a Team')
    st.dataframe(df.groupby(['ID','BattingTeam','BowlingTeam','City','Venue'])['total_run'].sum().reset_index().sort_values('total_run',ascending=False).set_index('BattingTeam').drop(['ID'],axis=1).head(15))

if option == 'Teams':
    select=st.sidebar.selectbox('Teams',sorted(pd.concat((df['BattingTeam'],df['BowlingTeam'])).unique()))
    
    st.title(select)
    f=data1[(data1['Team1']==select)|(data1['Team2']==select)]['Venue'].value_counts().head(1).reset_index()['Venue'][0]
    opt4=st.checkbox('Overall')
    if opt4:
        col1,col2,col3,col4=st.columns(4)
        a=data1[(data1['Team1']==select)|(data1['Team2']==select)]['MatchNumber'].count()
        b=data1[((data1['Team1']==select)|(data1['Team2']==select))&(data1['WinningTeam']==select)]['MatchNumber'].count()
        with col1:
              st.metric('Matches Played',a)
        with col2:
              st.metric('Matches Won',b)
        with col3:
            st.metric('Matches Lost',data1[((data1['Team1']==select)|(data1['Team2']==select))&(data1['WinningTeam']!=select)]['MatchNumber'].count())
        with col4:
              st.metric('WIn %',round(b/a*100,2))   
    opt=st.checkbox('Home')
    if opt:
            st.text(f)
            col1,col2,col3,col4=st.columns(4)
            a=data1[(data1['Venue']==f)&((data1['Team1']==select)|(data1['Team2']==select))]['MatchNumber'].count()
            b=data1[(data1['Venue']==f)&((data1['Team1']==select)|(data1['Team2']==select))&(data1['WinningTeam']==select)]['MatchNumber'].count()
            with col1:
              st.metric('Matches Played',a)
            with col2:
              st.metric('Matches Won',b)
            with col3:
              st.metric('Matches Lost',data1[(data1['Venue']==f)&((data1['Team1']==select)|(data1['Team2']==select))&(data1['WinningTeam']!=select)]['MatchNumber'].count())
            with col4:
              st.metric('WIn %',round(b/a*100,2))
    opt1=st.checkbox('Away')
    if opt1:
            col1,col2,col3,col4=st.columns(4)
            with col1:
              a=data1[(data1['Venue']!=f)&((data1['Team1']==select)|(data1['Team2']==select))]['MatchNumber'].count()
              b=data1[(data1['Venue']!=f)&((data1['Team1']==select)|(data1['Team2']==select))&(data1['WinningTeam']==select)]['MatchNumber'].count()
              st.metric('Matches Played',a)
            with col2:
              st.metric('Matches Won',b)
            with col3:
              st.metric('Matches Lost',data1[(data1['Venue']!=f)&((data1['Team1']==select)|(data1['Team2']==select))&(data1['WinningTeam']!=select)]['MatchNumber'].count())
            with col4:
              st.metric('WIn %',round(b/a*100,2))
    opt2=st.checkbox('Winning the Toss')
    if opt2:
          col1,col2,col3,col4,col5=st.columns(5)
          with col1:
              st.metric('Matches',data1[((data1['Team1']==select)|(data1['Team2']==select))&(data1['TossWinner']==select)]['MatchNumber'].count())
          with col2:
              a=data1[((data1['Team1']==select)|(data1['Team2']==select))&(data1['TossWinner']==select)]
              b=a[a['TossDecision']=='bat']
              st.metric('Choose batting and Won',b[b['WinningTeam']==select]['MatchNumber'].count())
          with col3:
              a=data1[((data1['Team1']==select)|(data1['Team2']==select))&(data1['TossWinner']==select)]
              b=a[a['TossDecision']=='bat']
              st.metric('Choose batting and lost',b[b['WinningTeam']!=select]['MatchNumber'].count())
          with col4:
              a=data1[((data1['Team1']==select)|(data1['Team2']==select))&(data1['TossWinner']==select)]
              b=a[a['TossDecision']=='field']
              st.metric('Choose fielding and Won',b[b['WinningTeam']==select]['MatchNumber'].count())
          with col5:
              a=data1[((data1['Team1']==select)|(data1['Team2']==select))&(data1['TossWinner']==select)]
              b=a[a['TossDecision']=='field']
              st.metric('Choose fielding and lost',b[b['WinningTeam']!=select]['MatchNumber'].count())
    opt3=st.checkbox('Losing the Toss')
    if opt3:
          col1,col2,col3,col4,col5=st.columns(5)
          with col1:
              st.metric('Matches',data1[((data1['Team1']==select)|(data1['Team2']==select))&(data1['TossWinner']!=select)]['MatchNumber'].count())
          with col2:
              a=data1[((data1['Team1']==select)|(data1['Team2']==select))&(data1['TossWinner']!=select)]
              b=a[a['TossDecision']=='bat']
              st.metric('batting first and won',b[b['WinningTeam']==select]['MatchNumber'].count())
          with col3:
              a=data1[((data1['Team1']==select)|(data1['Team2']==select))&(data1['TossWinner']!=select)]
              b=a[a['TossDecision']=='bat']
              st.metric('batting first and lost',b[b['WinningTeam']!=select]['MatchNumber'].count())
          with col4:
              a=data1[((data1['Team1']==select)|(data1['Team2']==select))&(data1['TossWinner']!=select)]
              b=a[a['TossDecision']=='field']
              st.metric('chase and won',b[b['WinningTeam']==select]['MatchNumber'].count())
          with col5:
              a=data1[((data1['Team1']==select)|(data1['Team2']==select))&(data1['TossWinner']!=select)]
              b=a[a['TossDecision']=='field']
              st.metric('Chase and lost',b[b['WinningTeam']!=select]['MatchNumber'].count())
    l=[]
    for i in sorted(pd.concat((df['BattingTeam'],df['BowlingTeam'])).unique()):
        if i==select:
            continue 
        else:
            l.append(i)
    select1=st.selectbox('Against Teams',l)   
    st.dataframe(data1[((data1['Team1']==select)&(data1['Team2']==select1))|((data1['Team2']==select)&(data1['Team1']==select1))][['WinningTeam','TossDecision']].value_counts().reset_index().set_index('WinningTeam').sort_index())
    select2=st.selectbox('Season',data1['Season'].drop_duplicates())
    col1,col2,col3=st.columns(3)
    a=data1[((data1['Team1']==select)|(data1['Team2']==select))]
    with col1:
        st.metric('Matches',a[a['Season']==select2]['MatchNumber'].count())
    with col2:
        st.metric('Matches Won',a[(a['Season']==select2)&(a['WinningTeam']==select)]['MatchNumber'].count())
    with col3:
        st.metric('Matches Lost',a[(a['Season']==select2)&(a['WinningTeam']!=select)]['MatchNumber'].count())
    
elif option == 'Players':
   select=st.sidebar.selectbox('Batter',sorted(pd.concat((data['batter'],data['non-striker'])).unique()))
   btn2=st.sidebar.button("Batter's Analysis")
   select1=st.sidebar.selectbox('Bowler',sorted(data['bowler'].unique()))
   btn3=st.sidebar.button("Bowler's Analysis")
   if btn2:
        st.header(select)
        st.subheader("Played for Teams")
        st.markdown(df[df['batter']==select]['BattingTeam'].drop_duplicates().values)
        col1,col2,col3=st.columns(3)
        with col1:
            st.metric('Matches played',data[(data['batter']==select)|(data['bowler']==select)]['ID'].drop_duplicates(keep="first").count())
        with col2:
            st.metric('Total Runs',data[data['batter']==select]['batsman_run'].sum())   
        with col3:
            st.metric('Highest Runs',data[data['batter']==select].groupby('ID')['batsman_run'].sum().sort_values().tail(1)) 
            
        col1,col2,col3,col4,col5=st.columns(5)
        
        with col3:
            a=data[data['batter']== select]
            c=a[(a['batsman_run']==4)|(a['batsman_run']==6)].shape[0]
            st.metric('No. of Boundaries',c)
        
        with col2:
            c=0
            a1=data[data['batter']== select]
            s=a1.groupby('ID')['batsman_run'].sum()
            for i in s.values:
             if i>=100:
              c=c+1
            st.metric('No. of Centuries',c)
        
        with col1:
             c=0
             a1=data[data['batter']== select]
             s=a1.groupby('ID')['batsman_run'].sum()
             for i in s.values:
              if i>=50 and i<100:
               c=c+1
             st.metric('No. of Half-Centuries',c)
             
        with col4:
            a=data[data['batter']==select]['ID'].drop_duplicates(keep="first").count()- data[data['player_out']==select].shape[0]
            b=data[data['batter']==select]['batsman_run'].sum()
            c=data[data['batter']==select]['ID'].drop_duplicates(keep="first").count()-a
            st.metric('Batting Avg',round(b/c,2))
            
        with col5:
            data=data[data['batter']==select]
            a=data[data['ballnumber']<=6]['ballnumber'].count()
            b=data[data['batter']==select]['batsman_run'].sum()
            st.metric('Strike Rate',round(b/a*100,2))
            
        col1,col2=st.columns(2)
        with col1:
            st.subheader('Runs Every Season')
            df=df[df['batter']==select]
            show=df.groupby('Season')['batsman_run'].sum().sort_values(ascending=False)
            fig,ax=plt.subplots()
            max1= max(show.values)
            explode=[]
            for i in (show.values):
               if i==max1:
                  explode.append(0.1)
               else:
                   explode.append(0)   
            ax.pie(show.values,labels=show.index,autopct='%0.1f%%',explode=explode)
            st.pyplot(fig)
        with col2:
            st.subheader('Strike Rate againts teams')
            a=df[df['batter']==select].groupby('BowlingTeam')['ballnumber'].count()
            b=df[df['batter']==select].groupby('BowlingTeam')['batsman_run'].sum()
            show1=round(b/a*100,2)
            fig,ax=plt.subplots()
            ax.scatter(show1.index,show1.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
    
   if btn3:
        st.header(select1)
        st.subheader("Played for Teams")
        st.markdown(df[df['batter']==select1]['BattingTeam'].drop_duplicates().values)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.metric('Overs Bowled',data[data['bowler']==select][['ID','overs']].drop_duplicates().count().values[1])
        with col2:
            st.metric('Runs concived',data[data['bowler']==select]['total_run'].sum())
        with col3:
            st.metric('Wicket Taken',data[data['bowler']==select][['ID','isWicketDelivery']].sum().values[1])
        with col4:
            st.metric('Economy',round(data[data['bowler']==select]['total_run'].sum()/data[data['bowler']==select][['ID','overs']].drop_duplicates().count().values[1],2))
        st.subheader('Best Bowling Figure')
        a=df[df['bowler']==select].groupby(['ID','BattingTeam','Venue','City'])[['total_run','isWicketDelivery']].sum().sort_values('isWicketDelivery',ascending=False).reset_index().drop(['ID'], axis=1)
        a.rename(columns={'isWicketDelivery':'Wickets'},inplace=True)
        st.dataframe(a.head(10))
    