import streamlit as st
import pandas as pd
from classes.book import Book
from classes.visitor_data import Visitor
from metodai.library_manager import LibraryManager
from datetime import datetime
from classes.librarian_data import Librarian
lib_admin = Librarian() 
st.markdown("<style> .stMainBlockContainer {min-width: 1000px; text-align: center;}</style>", unsafe_allow_html=True)
library_manager = LibraryManager()
  
def run(library_manager):
    st.subheader("Darbuotojo Paskyra", anchor=False)
    st.success(f"Sėkmingai prisijungėte {lib_admin.lib_name}")
    menu = ["Pridėti knygą", "Peržiūrėti visas knygas", "Rasti knygą", "Ištrinti knygą", "Skaitytojų valdymas", "Priskirti knygą lankytojui"]
    choice = st.selectbox("Pasirinkite veiksmą", menu, index=None, placeholder="Pasirinkite veiksmą...")
    
    if choice == "Pridėti knygą":
        st.subheader("Įveskite naują knygą", anchor=False)

        name = st.text_input("Pavadinimas")
        author = st.text_input("Autorius")
        genre = st.text_input("Žanras")
        release_date = st.number_input("Leidybos metai", min_value=1800, max_value=2024,value=None, placeholder="Įveskite metus nuo 1800 iki 2024", step=None)

        if st.button("Pridėti", key="add_book"):
            if not name or not author or not genre or not release_date:
                st.warning("Visi laukai yra privalomi!")
            else:
                new_book = Book(
                    name=name,
                    author=author,
                    genre=genre,
                    release_date=int(release_date)
                )
            
                success, count = library_manager.add_book(new_book)
                if success:
                    if count == 1:
                        st.success(f"Knyga '{name}' : {genre}, {author}, {release_date} m. buvo pridėta!")
                    else:
                        st.success(f"Knyga '{name}' : {author} buvo pridėta sėkmingai, dabartinis knygos egzempliorių skaičius yra: {count}")
                else:
                    st.warning(f"Knyga '{name}' : {author} jau yra mūsų bibliotekoje! knygos egzempliorių skaičius yra: {count}")

    elif choice == "Peržiūrėti visas knygas":
        st.subheader("Knygų sąrašas", anchor=False)
        books = library_manager.list_books()

        if books: 
            book_data = {
                "ID": [book.id for book in books],
                "Pavadinimas": [book.name for book in books],
                "Autorius": [book.author for book in books],
                "Žanras": [book.genre for book in books],
                "Leidybos metai": [book.release_date for book in books],
                "Būklė": [book.status for book in books],
                "Skaitytojo vardas": [book.visitor_name for book in books],
                "Paėmimo data": [book.start_date for book in books]
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
            st.dataframe(styled_table)
            # st.table(df_books)
        else:
            st.write("Jūsų knygų sąrašas tuščias :(")

    elif choice == "Rasti knygą":
        st.subheader("Ieškoti knygos", anchor=False)

        search_by = st.radio("Ieškoti pagal", ("Pavadinimas", "Autorius"))
        paieska = st.text_input(f"Įveskite {search_by.lower()}")

        if st.button("Ieškoti", key="search_book_button"):
            if not paieska:
                st.warning("Įveskite paieškos užklausą!")
            else:
                if search_by == "Pavadinimas":
                    results = library_manager.rasti_pagal_pavadinima(paieska)
                else:
                    results = library_manager.rasti_pagal_autoriu(paieska)

                if results:
                    st.write(f"Rastos {len(results)} knygos:")
                    book_data = {
                        "Pavadinimas": [book.name for book in results],
                        "Autorius": [book.author for book in results],
                        "Žanras": [book.genre for book in results],
                        "Leidybos metai": [int(book.release_date) for book in results],
                        "Būsena": [book.status for book in results],
                        "Lankytojo vardas": [book.visitor_name for book in results],
                        "Pradžios data": [book.start_date for book in results]
                    }
                    df_books = pd.DataFrame(book_data, dtype=str)
                    st.table(df_books)
                else:
                    st.write("Nerasta jokių knygų.")
    elif choice == "Ištrinti knygą":
        st.subheader("Ištrinti knygą", anchor=False)

        delete_by = st.radio("Ištrinti pagal", ("Leidybos metai", "Autorius"))

        if delete_by == "Leidybos metai":
            year = st.number_input("Įveskite leidybos metus", min_value=1800, max_value=2024,value=None, placeholder="Įveskite metus nuo 1800 iki 2024", step=None)
            if st.button("Ištrinti pagal metus", key="delete_by_year_btn"):
                count = library_manager.dlt_books_year(year)
                st.success(f"Ištrinta {count} knygų, kurios buvo išleistos iki {year} metų.")

        elif delete_by == "Autorius":
            author = st.text_input("Įveskite autorių")
            if st.button("Ištrinti pagal autorių", key="delete_by_author_btn"):
                count = library_manager.dlt_books_author(author)
                st.success(f"Ištrinta {count} knygų autoriaus {author}.")

        st.subheader("Ištrintų knygų sąrašas", anchor=False)
        dlt_books = library_manager.dlt_list_books()

        if dlt_books: 
            book_data = {
                "Pavadinimas": [book.name for book in dlt_books],
                "Autorius": [book.author for book in dlt_books],
                "Žanras": [book.genre for book in dlt_books],
                "Leidybos metai": [book.release_date for book in dlt_books],
            }
            df_books = pd.DataFrame(book_data)
            st.table(df_books)
            if st.button("Atkurti visas ištrintas knygas", key="restore_deleted_books_btn"):
                restored_count = library_manager.restore_dlt_books()
                st.success(f"Atkurta {restored_count} knygų.")
        else:
            st.write("Ištrintų knygų sąrašas tuščias")

    if choice == "Skaitytojų valdymas":
        
        menu2 = st.radio("Kokį veiksmą norite atlikti?", ["Peržiūrėti skaitytojus", "Sukurti skaitytojo kortelę"])
        if menu2 == "Peržiūrėti skaitytojus":
            st.subheader("Skaitytojai", anchor=False)
            visitors = library_manager.list_visitors()
            if visitors:
                visitor_data = {
                    "Vardas": [visitor.name for visitor in visitors],
                    "ID": [visitor.visitor_id for visitor in visitors],
                    "Paimtos knygos": [
                    ',\n '.join([f"{book.name} ({book.status} {book.start_date})" for book in visitor.books_taken]) if visitor.books_taken else 'Nėra' 
                    for visitor in visitors
                ],
            }
                df_visitors = pd.DataFrame(visitor_data)
                st.dataframe(df_visitors)

                # Skaitytojų ištrinimas veikia tik tuo atvėju, kai sąrašas nėra tuščias
                visitor_id_to_delete = st.number_input("Įveskite skaitytojo ID, kurį norite ištrinti", min_value=1, step=1)
                if st.button("Ištrinti skaitytoją"):
                    if library_manager.delete_visitor(visitor_id_to_delete):
                        st.success(f"Skaitytojas ID {visitor_id_to_delete} sėkmingai ištrintas.")
                    else:
                        st.warning("Nepavyko ištrinti skaitytojo! Patikrinkite, ar skaitytojas turi paskolintų knygų.")
            else:
                st.write("Skaitytojų sąrašas tuščias.")
                
        if menu2 == "Sukurti skaitytojo kortelę":
            st.subheader("Sukurti skaitytojo kortelę", anchor=False)

            visitor_name = st.text_input("Lankytojo vardas")

            if st.button("Pridėti lankytoją"):
                if visitor_name:
                    new_visitor = library_manager.create_visitor(visitor_name)
                    st.success(f"Lankytojas '{visitor_name}' buvo pridėtas su ID {new_visitor.visitor_id}!")
                else:
                    st.warning("Visi laukai yra privalomi!")

    if choice == "Priskirti knygą lankytojui":
        st.subheader("Priskirti knygą lankytojui", anchor=False)

        if library_manager.visitors:
            visitor_options = {f"{visitor.name} (ID: {visitor.visitor_id}) - paimtos knygos: {len(visitor.books_taken)}": visitor for visitor in library_manager.visitors}
            selected_visitor_option = st.selectbox("Pasirinkite skaitytoją", list(visitor_options.keys()))
            selected_visitor = visitor_options[selected_visitor_option]
        else:
            st.warning("Skaitytojų sąrašas tuščias")

        available_books = [book for book in library_manager.books if book.status == 'laisva']
        if available_books:
            book_options = {f"{book.name} ({book.author}, {book.release_date})": book.id for book in available_books}
            selected_book_option = st.selectbox("Pasirinkite knygą", list(book_options.keys()))
            selected_book_id = book_options[selected_book_option]
            selected_book = next(book for book in available_books if book.id == selected_book_id)
        else:
            st.warning("Šiuo metu nėra laisvų knygų.")

        start_date = st.date_input("Pradžios data", value=datetime.today(), max_value=datetime.today())

        if st.button("Priskirti knygą", key="assign_book"):
            if selected_visitor and selected_book_id and start_date:
                if any(book.name == selected_book.name and book.author == selected_book.author and book.release_date == selected_book.release_date for book in selected_visitor.books_taken):
                    st.warning("Skaitytojas jau yra pasiėmęs šią knygą")
                elif any(book.status == 'vėluojama' for book in selected_visitor.books_taken):
                    st.warning("Skaitytojas turi veluojančių knygų, knygų išdavimas negalimas")
                else:
                    success = library_manager.assign_book_to_visitor(selected_visitor.visitor_id, selected_book_id, start_date.strftime('%Y-%m-%d'))
                    if success:
                        st.success(f"Knyga '{selected_book_option}' priskirta lankytojui '{selected_visitor.name}'!")
                    else:
                        st.warning("Nepavyko priskirti knygos! Patikrinkite lankytojo vardą ir knygos būklę.")
            else:
                st.warning("Visi laukai yra privalomi!")

    overdue_books = library_manager.check_overdue_books()
    if overdue_books:
        st.warning(f"Šios knygos yra vėluojamos: {[book.name for book in overdue_books]}")

run(library_manager)
if st.button("Atgal į pagrindinį", key="63158617_knvnkvnklankv", icon=":material/undo:"):
        st.switch_page("main.py")