import streamlit as st
import os

st.markdown("<style>  .stMainBlockContainer {min-width: 1000px; text-align: center;}</style>", unsafe_allow_html=True)

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    if os.path.exists("ca_tarpinis_atsiskaitymas/assets/logo.jpg"):
        st.image("ca_tarpinis_atsiskaitymas/assets/logo.jpg", caption=None)
    else:
        st.error("ca_tarpinis_atsiskaitymas/assets/logo.jpg failas nerastas.")

st.title("Sveiki atvykę į Mūsų Biblioteką", anchor=False)
col1, col2 = st.columns(2)
with col1:
    if st.button("Aš esu Darbuotojas", key="bibliotek", icon=":material/badge:"):
        st.switch_page("pages/librarian.py")
        
with col2:
    if st.button("Aš esu Skaitytojas", key="skaityt", icon=":material/person:"):
        st.switch_page("pages/visitor.py")
