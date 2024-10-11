import streamlit as st
import pandas as pd
from metodai.book import Book
from metodai.library_manager import LibraryManager
from metodai.librarian_data import Librarian
st.markdown("<style> .stMainBlockContainer {min-width: 1000px; text-align: center;}</style>", unsafe_allow_html=True)
library_manager = LibraryManager()
lib_admin = Librarian()   
def run(library_manager):
    st.subheader("Darbuotojo Paskyra", anchor=False)
    st.success(f"Sėkmingai prisijungėte {lib_admin.lib_name}")
    menu = ["Pridėti knygą", "Peržiūrėti visas knygas", "Rasti knygą", "Ištrinti knygą"]
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
            
                if library_manager.add_book(new_book):
                    st.success(f"Knyga '{name}' : {genre}, {author}, {release_date} m. buvo pridėta!")
                else:
                    st.warning(f"Knyga '{name}' : {genre}, {author}, {release_date} m. jau yra mūsų bibliotekoje!")

    elif choice == "Peržiūrėti visas knygas":
        st.subheader("Knygų sąrašas", anchor=False)
        books = library_manager.list_books()

        if books: 
            book_data = {
                "Pavadinimas": [book.name for book in books],
                "Autorius": [book.author for book in books],
                "Žanras": [book.genre for book in books],
                "Leidybos metai": [book.release_date for book in books],
                "Būklė": [book.status for book in books],
                "Skaitytojo vardas": [book.visitor_name for book in books],
                "Paėmimo data": [book.start_date for book in books]
            }
            df_books = pd.DataFrame(book_data)
            st.table(df_books)
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

run(library_manager)
if st.button("Atgal į pagrindinį", key="63158617_knvnkvnklankv", icon=":material/undo:"):
        st.switch_page("main.py")