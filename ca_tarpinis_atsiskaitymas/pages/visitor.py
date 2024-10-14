import streamlit as st
import pandas as pd
from classes.book import Book
from metodai.library_manager import LibraryManager
from metodai.visitor_manager import VisitorManager
from datetime import datetime
from time import sleep

st.markdown("<style> .stMainBlockContainer {min-width: 1000px; text-align: center;}</style>", unsafe_allow_html=True)
library_manager = LibraryManager()
visitor_manager = VisitorManager('ca_tarpinis_atsiskaitymas/data/visitor_list.pkl')   

 
def run_visitor(library_manager):
    st.subheader("Skaitytojo Paskyra", anchor=False)
    menu = ["📖 Peržiūrėti visas knygas", "🔍 Rasti knygą", "📅 Pasiimti knygą", "🔙 Grąžinti knygą"]
    choice = st.selectbox("Pasirinkite veiksmą", menu, index=None, placeholder="Pasirinkite veiksmą...")
    
    if choice == "📖 Peržiūrėti visas knygas":
        st.subheader("📖 Knygų sąrašas", anchor=False)
        books = library_manager.list_books()
        current_visitor = st.session_state.get('current_visitor', None)
        overdue_taken_books = [book for book in books if book.visitor_name == current_visitor.name and book.status == 'vėluojama']
        if overdue_taken_books:
            st.warning(f"Turite vėluojančių knygų: {', '.join([book.name for book in overdue_taken_books])}")
        menu1 = st.radio("Kokį veiksmą norite atlikti?", ["Visos knygos", "Paimtos knygos", "Vėluojančios knygos"], horizontal=True)
        if menu1 == "Visos knygos":           
            st.subheader("Visos knygos", anchor=False)
            free_books = [book for book in books if book.status == 'laisva' or (book.status == 'paimta' and book.visitor_name == current_visitor.name) or (book.status == 'vėluojama' and book.visitor_name == current_visitor.name)]
            if free_books: 
                book_data = {
                    "Pavadinimas": [book.name for book in free_books],
                    "Autorius": [book.author for book in free_books],
                    "Žanras": [book.genre for book in free_books],
                    "Leidybos metai": [book.release_date for book in free_books],
                    "Būklė": [book.status for book in free_books],
                    "Skaitytojo vardas": [book.visitor_name for book in free_books],
                    "Paėmimo data": [book.start_date for book in free_books]
                }
                df_books = pd.DataFrame(book_data)
                def color_status(val):
                    color = ''
                    if val == 'laisva':
                        color = 'green'
                    elif val == 'paimta':
                        color = 'blue'
                    elif val == 'vėluojama':
                        color = 'red'
                    return f'color: {color}'
                styled_table = df_books.style.map(color_status, subset=['Būklė']).set_properties(**{'text-align': 'center'})
                st.dataframe(styled_table) # st.table(df_books) 
            else:
                st.write("Jūsų knygų sąrašas tuščias :(")
        if menu1 == "Paimtos knygos":
            st.subheader("Paimtos knygos", anchor=False)
            taken_books = [book for book in books if book.visitor_name == current_visitor.name and book.status == 'paimta']
            if taken_books:
                book_data = {
                    "Pavadinimas": [book.name for book in taken_books],
                    "Autorius": [book.author for book in taken_books],
                    "Žanras": [book.genre for book in taken_books],
                    "Leidybos metai": [book.release_date for book in taken_books],
                    "Būklė": [book.status for book in taken_books],
                    "Skaitytojo vardas": [book.visitor_name for book in taken_books],
                    "Paėmimo data": [book.start_date for book in taken_books]
                }
                df_books = pd.DataFrame(book_data)
                def color_status(val):
                    color = ''
                    if val == 'paimta':
                        color = 'blue'
                    return f'color: {color}'
                styled_table = df_books.style.map(color_status, subset=['Būklė']).set_properties(**{'text-align': 'center'})
                st.dataframe(styled_table) # st.table(df_books) 
            else:
                st.write("Jūsų knygų sąrašas tuščias :(")
        if menu1 == "Vėluojančios knygos":
            st.subheader("Vėluojančios knygos", anchor=False)
            
            if overdue_taken_books:
                book_data = {
                    "Pavadinimas": [book.name for book in overdue_taken_books],
                    "Autorius": [book.author for book in overdue_taken_books],
                    "Žanras": [book.genre for book in overdue_taken_books],
                    "Leidybos metai": [book.release_date for book in overdue_taken_books],
                    "Būklė": [book.status for book in overdue_taken_books],
                    "Skaitytojo vardas": [book.visitor_name for book in overdue_taken_books],
                    "Paėmimo data": [book.start_date for book in overdue_taken_books]
                }
                df_books = pd.DataFrame(book_data)
                def color_status(val):
                    color = ''
                    if val == 'vėluojama':
                        color = 'red'
                    return f'color: {color}'
                styled_table = df_books.style.map(color_status, subset=['Būklė']).set_properties(**{'text-align': 'center'})
                st.dataframe(styled_table) # st.table(df_books) 
            else:
                st.write("Jūsų knygų sąrašas tuščias :(")
    
    elif choice == "🔍 Rasti knygą":
        st.subheader("🔍 Ieškoti knygos", anchor=False)

        search_by = st.radio("Ieškoti pagal", ["Pavadinimas", "Autorius"],horizontal=True)
        paieska = st.text_input(f"Įveskite {search_by.lower()}")

        if st.button("🔍Ieškoti", key="search_book_button"):
            if not paieska:
                st.warning("Įveskite paieškos užklausą!")
            else:
                if search_by == "Pavadinimas":
                    results = library_manager.rasti_pagal_pavadinima(paieska)
                else:
                    results = library_manager.rasti_pagal_autoriu(paieska)
                free_books_search = [book for book in results if book.status == 'laisva']
                if free_books_search:
                    st.write(f"Rastos {len(free_books_search)} knygos:")
                    book_data = {
                        "Pavadinimas": [book.name for book in free_books_search],
                        "Autorius": [book.author for book in free_books_search],
                        "Žanras": [book.genre for book in free_books_search],
                        "Leidybos metai": [int(book.release_date) for book in free_books_search],
                        "Būklė": [book.status for book in free_books_search],
                    }
                    df_books = pd.DataFrame(book_data)
                    def color_status(val):
                        color = ''
                        if val == 'laisva':
                            color = 'green'
                        elif val == 'paimta':
                            color = 'blue'
                        elif val == 'vėluojama':
                            color = 'red'
                        return f'color: {color}'
                    styled_table = df_books.style.map(color_status, subset=['Būklė']).set_properties(**{'text-align': 'center'})
                    st.dataframe(styled_table) # st.table(df_books)
                else:
                    st.write("Nerasta jokių knygų.")

    elif choice == "🔙 Grąžinti knygą":
        st.subheader("Knygų grąžinimas", anchor=False)
        if 'current_visitor' in st.session_state and st.session_state['current_visitor']:
            current_visitor = st.session_state['current_visitor']
        books = library_manager.list_books()
        st.subheader("Paimtos knygos", anchor=False)
        not_returned_books = not_returned_books = [book for book in books if book.status in ['paimta', 'vėluojama'] and book.visitor_name == current_visitor.name]
        if not_returned_books:
                book_data = {
                    "ID": [str(book.id) for book in not_returned_books],
                    "Pavadinimas": [book.name for book in not_returned_books],
                    "Autorius": [book.author for book in not_returned_books],
                    "Leidybos metai": [str(book.release_date) for book in not_returned_books],
                    "Būklė": [book.status for book in not_returned_books],
                    "Skaitytojo vardas": [book.visitor_name for book in not_returned_books],
                    "Paėmimo data": [book.start_date for book in not_returned_books],
                    "Grąžinti": [False for _ in not_returned_books]
                }
                df_books = pd.DataFrame(book_data)
                edited_df_books = st.data_editor(df_books, num_rows="fixed")
                if st.button("Patvirtinti grąžinimą"):
                    for idx, row in edited_df_books.iterrows():
                        if row["Grąžinti"]:
                            book_id = int(row["ID"])
                            book = next((b for b in books if b.id == book_id), None)
                            if book:
                                book.status = 'laisva'
                                visitor_name = book.visitor_name 
                                book.visitor_name = None
                                book.start_date = None
                                visitor = library_manager.visitor_manager.get_visitor_by_name(visitor_name)

                                if visitor:
                                    visitor.books_taken = [bk for bk in visitor.books_taken if bk.id != book_id] 
                                    library_manager.visitor_manager.save_visitors()
                                library_manager.save_books()
                                st.success(f"Knyga (ID: {book_id}) sėkmingai grąžinta!")


        else:
            st.write("Nėra knygų, kurios būtų paimtos ar vėluojančios :(") 

    elif choice == "📅 Pasiimti knygą":
        st.subheader("📅 Pasiimti knygą", anchor=False)
        selected_visitor = st.session_state.get('current_visitor', None)

        available_books = [book for book in library_manager.list_books() if book.status == 'laisva']
        if available_books:
            book_options = {f"{book.name} ({book.author}, {book.release_date})": book.id for book in available_books}
            selected_book_option = st.selectbox("Pasirinkite knygą", list(book_options.keys()))
            selected_book_id = book_options[selected_book_option]
            selected_book = next(book for book in available_books if book.id == selected_book_id)
        else:
            st.warning("Šiuo metu nėra laisvų knygų.")

        start_date = st.date_input("Pradžios data", value=datetime.today(),min_value=datetime.today(), max_value=datetime.today())

        if st.button("Priskirti knygą", key="assign_book"):
            if selected_visitor and selected_book_id and start_date:
                selected_book = next((book for book in library_manager.list_books() if book.id == selected_book_id), None)
                if selected_book:
                    if any(book.name == selected_book.name and book.author == selected_book.author and book.release_date == selected_book.release_date for book in selected_visitor.books_taken):
                        st.warning("Jus jau pasiėmte šią knygą")
                    elif any(book.status == 'vėluojama' for book in selected_visitor.books_taken):
                        st.error("Jus turite veluojančių knygų, knygų išdavimas negalimas")
                    else:
                        success = library_manager.assign_book_to_visitor(selected_visitor.visitor_id, selected_book_id, start_date.strftime('%Y-%m-%d'))
                        if success:
                            st.success(f"Knyga '{selected_book.name}' priskirta lankytojui '{selected_visitor.name}'!")
                        else:
                            st.warning("Nepavyko priskirti knygos! Patikrinkite lankytojo vardą ir knygos būklę.")
                else:
                    st.warning("Pasirinkta knyga nerasta!")
            else:
                st.warning("Visi laukai yra privalomi!")

       
if 'visitor_login' not in st.session_state:
    st.session_state['visitor_login'] = False

if st.session_state['visitor_login'] == True:
    current_visitor = st.session_state.get('current_visitor', None)
    if current_visitor:
        st.success(f"Sėkmingai prisijungėte, {current_visitor.name} Jūsų ID:{current_visitor.visitor_id}!")
    run_visitor(library_manager) 
    if st.button("Atsijungti"):
        st.success(f"Sėkmingai atsisijungėte {current_visitor.name}")
        sleep(0.5)
        st.session_state['visitor_login'] = False
        st.rerun()
else:
    if st.button("Atgal į pagrindinį", key="63158617_knvklankv", icon=":material/undo:"):
        st.switch_page("main.py")
    with st.form(key='visitor_login_form'):
        st.subheader("Skaitytojo prisijungimas", anchor=False)
        ent_visitor_id = st.text_input("Skaitytojo ID", placeholder="įveskite skaitytojo ID", autocomplete=None)
        if st.form_submit_button("Prisijungti"):
            try:
                visitor_id = int(ent_visitor_id)
                visitor = visitor_manager.get_visitor_by_id(visitor_id)
                if visitor:
                    st.success(f"Sėkmingai prisijungėte kaip {visitor.name}")
                    sleep(0.5)
                    st.session_state['visitor_login'] = True
                    st.session_state['current_visitor'] = visitor
                    st.rerun()
                else:
                    st.warning("Skaitytojo ID nerastas.")
            except ValueError:
                st.warning("Skaitytojo ID turi būti skaičius!")

  