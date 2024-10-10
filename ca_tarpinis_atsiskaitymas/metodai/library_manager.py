import pickle
import os
from ca_tarpinis_atsiskaitymas.metodai.book import Book

class LibraryManager:
    def __init__(self, file_path='ca_tarpinis_atsiskaitymas/data/books.pkl', deleted_file_path='ca_tarpinis_atsiskaitymas/data/deleted_books.pkl'):
        self.file_path = file_path
        self.deleted_file_path = deleted_file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.books = self.load_books()
        self.deleted_books = self.load_dlt_books()

    def load_books(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'wb') as file:
                pickle.dump([], file)
        try:
            with open(self.file_path, 'rb') as file:
                return [Book.is_saraso(parameter) for parameter in pickle.load(file)]
        except EOFError:
            return []
        
    def load_dlt_books(self):
        if not os.path.exists(self.deleted_file_path):
            with open(self.deleted_file_path, 'wb') as file:
                pickle.dump([], file)
        try:
            with open(self.deleted_file_path, 'rb') as file:
                return [Book.is_saraso(parameter) for parameter in pickle.load(file)]
        except EOFError:
            return []
        
    def save_books(self):
        with open(self.file_path, 'wb') as file:
            pickle.dump([book.i_sarasa() for book in self.books], file)
    
    def save_dlt_books(self):
        with open(self.deleted_file_path, 'wb') as file:
            pickle.dump([book.i_sarasa() for book in self.deleted_books], file)

    def add_book(self, book):
        if self.is_duplicate(book):
            return False
        self.books.append(book)
        self.save_books()
        return True

    def is_duplicate(self, book):
        for existing_book in self.books:
            if (existing_book.name == book.name and
                existing_book.author == book.author and
                existing_book.genre == book.genre and
                existing_book.release_date == book.release_date):
                return True
        return False

    def list_books(self):
        return self.books
    
    def rasti_pagal_pavadinima(self, name):
        return [book for book in self.books if name.lower() in book.name.lower()]

    def rasti_pagal_autoriu(self, author):
        return [book for book in self.books if author.lower() in book.author.lower()]
    
    def dlt_books_year(self, year):
        deleted_books = [book for book in self.books if int(book.release_date) <= year]
        self.books = [book for book in self.books if int(book.release_date) > year]
        self.deleted_books.extend(deleted_books)
        self.save_books()
        self.save_dlt_books()
        return len(deleted_books)

    def dlt_books_author(self, author):
        deleted_books = [book for book in self.books if author.lower() in book.author.lower()]
        self.books = [book for book in self.books if author.lower() not in book.author.lower()]
        self.deleted_books.extend(deleted_books)
        self.save_books()
        self.save_dlt_books()
        return len(deleted_books)
    
    def dlt_list_books(self):
        return self.deleted_books
    
    def restore_dlt_books(self):
        restored_count = len(self.deleted_books)  
        self.books.extend(self.deleted_books)      
        self.deleted_books = []                    
        self.save_books()                         
        self.save_dlt_books()                      
        return restored_count 