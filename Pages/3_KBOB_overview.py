import streamlit as st
import pandas as pd

KBOB = pd.read_excel('C:/Users/simon/Dropbox/01_Master_Thesis/06_KBOB/KBOB_clean.xlsx', sheet_name='Material')

KBOB_over = KBOB.iloc[:, 0:2]

def KBOB_overview():

    st.title("KBOB overview:")
    st.write(KBOB_over)


KBOB_overview()   
