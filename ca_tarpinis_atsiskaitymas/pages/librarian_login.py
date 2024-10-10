import streamlit as st
from metodai.librarian_data import Librarian
from time import sleep

lib_admin = Librarian()

st.subheader("Darbuotojo prisijungimas", anchor=False)

with st.form(key= 'my_form'):
    ent_lib_user_name = st.text_input("Prisijungimo vardas", autocomplete=None)
    ent_lib_password = st.text_input("Slaptažodis", type='password', autocomplete=None)
    if st.form_submit_button("Prisijungti"):
        if (ent_lib_user_name == lib_admin.lib_user_name and ent_lib_password == lib_admin.lib_password):
            st.success(f"Sėkmingai prisijungėte {lib_admin.lib_name}")
            sleep(0.5)
            st.switch_page("pages/librarian.py") 
        else:
            st.warning("Netinkami prisijungimo duomenys! Bandykite dar kartą.")
            
if st.button("Atgal į pagrindinį", key="back_to_main", icon=":material/undo:"):
    st.switch_page("main.py")