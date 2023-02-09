import streamlit as st
import pandas as pd

filepath = 'C:/Users/simon/Dropbox/01_Master_Thesis/06_KBOB/Database.xlsx' #change filepath where the database is located
KBOB = pd.read_excel(filepath, sheet_name='Material')

KBOB_over = KBOB.iloc[:, 0:2]

def KBOB_overview():

    st.title("KBOB overview:")
    st.write(KBOB_over)


KBOB_overview()   
