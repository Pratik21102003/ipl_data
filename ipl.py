import pandas as pd
import numpy as np
import streamlit as st
from matplotlib import pyplot as plt
data=pd.read_csv("C:/Users/Pratik/Desktop/pratik/panda basic/ipl-matches.csv")
data1=pd.read_csv("C:/Users/Pratik/Desktop/pratik/panda basic/deliveries.csv")
st.sidebar.title('IPL Data Analysis')
option=st.sidebar.selectbox('Select One',['Teams','Batter','Bowler'])
if option == 'Teams':
    st.sidebar.selectbox('Teams',sorted(pd.concat((data['Team1'],data['Team2'])).unique()))
elif option == 'Batter':
    st.sidebar.selectbox('Batter',sorted(pd.concat((data1['batsman'],data1['non_striker'])).unique()))
else:
    st.sidebar.selectbox('Bowler',sorted(data1['bowler'].unique()))