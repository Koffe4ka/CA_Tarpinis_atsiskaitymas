import pickle
import os
from classes.book import Book
from metodai.visitor_manager import VisitorManager
from datetime import datetime, timedelta

class LibraryManager:
    def __init__(self, file_path='ca_tarpinis_atsiskaitymas/data/books.pkl', 
                 deleted_file_path='ca_tarpinis_atsiskaitymas/data/deleted_books.pkl', 
                 visitors_file_path='ca_tarpinis_atsiskaitymas/data/visitor_list.pkl'):
        self.data_dir = 'ca_tarpinis_atsiskaitymas/data'
        self.file_path = file_path
        self.deleted_file_path = deleted_file_path
        self.visitors_file_path = visitors_file_path
        self.visitor_manager = VisitorManager(visitors_file_path)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.books = self.load_books()
        self.deleted_books = self.load_dlt_books()
        self.start_id = 20240000  # Custom ID number
        self.next_id = self.get_next_id()
        self.max_duplicates = 2
        
    def ensure_data_directory(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def get_next_id(self):
        if not self.books:
            return self.start_id + 1
        max_id = max(book.id for book in self.books)
        return max(max_id + 1, self.start_id + 1)

    def add_book(self, book):
        duplicate_count = self.is_duplicate(book)
        if duplicate_count >= self.max_duplicates:
            return False, duplicate_count
        book.id = self.next_id
        self.next_id += 1
        self.books.append(book)
        self.save_books()
        return True, duplicate_count + 1

    def is_duplicate(self, book):
        return sum(1 for b in self.books if b.name == book.name 
                   and b.author == book.author 
                   and b.genre == book.genre 
                   and b.release_date == book.release_date)

    def save_books(self):
        with open(self.file_path, 'wb') as file:
            pickle.dump([book.i_sarasa() for book in self.books], file)

    def load_books(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'wb') as file:
                pickle.dump([], file)
        try:
            with open(self.file_path, 'rb') as file:
                return [Book.is_saraso(parameter) for parameter in pickle.load(file)]
        except EOFError:
            return []

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

    def load_dlt_books(self):
        if not os.path.exists(self.deleted_file_path):
            with open(self.deleted_file_path, 'wb') as file:
                pickle.dump([], file)
        try:
            with open(self.deleted_file_path, 'rb') as file:
                return [Book.is_saraso(parameter) for parameter in pickle.load(file)]
        except EOFError:
            return []

    def save_dlt_books(self):
        with open(self.deleted_file_path, 'wb') as file:
            pickle.dump([book.i_sarasa() for book in self.deleted_books], file)

    def dlt_list_books(self):
        return self.deleted_books

    def restore_dlt_books(self):
        restored_count = len(self.deleted_books)
        self.books.extend(self.deleted_books)
        self.deleted_books = []
        self.save_books()
        self.save_dlt_books()
        return restored_count
    
    def check_overdue_books(self):
        overdue_books = []
        for book in self.books:
            if book.status == 'paimta':
                loan_duration = (datetime.today() - datetime.strptime(book.start_date, '%Y-%m-%d')).days
                if loan_duration > 20:
                    book.status = 'vėluojama'
                    overdue_books.append(book)
        self.save_books()
        return overdue_books
    
    # HUGE PROBLEM --- > SOLVED :))))))

    def assign_book_to_visitor(self, visitor_id, book_id, start_date):
        skaitytojas = self.visitor_manager.get_visitor_by_id(visitor_id)
        knyga = next((b for b in self.books if b.id == book_id), None)
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d') 
        if skaitytojas and knyga and knyga.status == 'laisva':
            if start_date < datetime.now():
                knyga.status = 'vėluojama'
            else:
                knyga.status = 'paimta'
            knyga.visitor_name = skaitytojas.name
            knyga.visitor_name = skaitytojas.name
            knyga.start_date = start_date.date()
            skaitytojas.books_taken.append(knyga)
            self.save_books()
            self.visitor_manager.save_visitors()
            return True
        return False

    
    
