import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")
st.markdown("<style> .stSidebar {display: none;} .stMainBlockContainer {min-width: 1000px; text-align: center;}</style>", unsafe_allow_html=True)

st.title("Sveiki atvykę į Mūsų Biblioteką", anchor=False)
col1, col2 = st.columns(2)
with col1:
    if st.button("Aš esu Bibliotekininkas", key="bibliotek"):
        st.switch_page("pages/librarian.py")
        
with col2:
    if st.button("Aš esu Skaitytojas", key="skaityt"):
        st.switch_page("pages/visitor.py")
