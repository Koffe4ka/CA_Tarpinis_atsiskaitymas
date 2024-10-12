import pickle
import os
from classes.book import Book
from classes.visitor_data import Visitor
from datetime import datetime, timedelta

class LibraryManager:
    def __init__(self, file_path='ca_tarpinis_atsiskaitymas/data/books.pkl', 
                 deleted_file_path='ca_tarpinis_atsiskaitymas/data/deleted_books.pkl', 
                 visitors_file_path='ca_tarpinis_atsiskaitymas/data/visitor_list.pkl'):
        self.file_path = file_path
        self.deleted_file_path = deleted_file_path
        self.visitors_file_path = visitors_file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.books = self.load_books()
        self.deleted_books = self.load_dlt_books()
        self.visitors = self.load_visitors()
        self.start_id = 20240000  # Custom ID number
        self.next_id = self.get_next_id()
        self.max_duplicates = 2
        self.data_dir = 'ca_tarpinis_atsiskaitymas/data'
        self.load_visitors()

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
        return sum(1 for b in self.books if b.name == book.name and b.author == book.author and b.genre == book.genre and b.release_date == book.release_date)

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

    def create_visitor(self, name):
        visitor_id = len(self.visitors) + 1
        new_visitor = Visitor(name=name, visitor_id=visitor_id)
        self.visitors.append(new_visitor)
        self.save_visitors()
        return new_visitor

    def assign_book_to_visitor(self, visitor_id, book_id, start_date):
        visitor = next((v for v in self.visitors if v.visitor_id == visitor_id), None)
        book = next((b for b in self.books if b.id == book_id), None)
        if visitor and book and book.status == 'laisva':
            book.status = 'paimta'
            book.visitor_name = visitor.name
            book.start_date = start_date
            visitor.books_taken.append(book)
            self.save_books()
            self.save_visitors()
            return True
        return False

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

    def load_visitors(self):
        if not os.path.exists(self.visitors_file_path):
            with open(self.visitors_file_path, 'wb') as file:
                pickle.dump([], file)
        try:
            with open(self.visitors_file_path, 'rb') as file:
                return pickle.load(file)
        except EOFError:
            return []

    def save_visitors(self):
        with open(self.visitors_file_path, 'wb') as file:
            pickle.dump(self.visitors, file)

    def list_visitors(self):
        return self.visitors

    def delete_visitor(self, visitor_id):
        visitor = next((v for v in self.visitors if v.visitor_id == visitor_id), None)
        if visitor and not visitor.books_taken:
            self.visitors.remove(visitor)
            self.save_visitors()
            return True
        return False

    def get_next_visitor_id(self):
        return len(self.visitors) + 1
