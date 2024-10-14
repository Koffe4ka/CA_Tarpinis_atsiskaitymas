class Visitor:
    def __init__(self, name, visitor_id, books_taken=None):
        self.name = name
        self.visitor_id = visitor_id
        self.books_taken = books_taken if books_taken is not None else []
        self.id = visitor_id
    def __repr__(self):
        return f"Visitor(name='{self.name}', visitor_id={self.visitor_id}, books_taken={self.books_taken})"
    
    def add_book(self, book, start_date):
        self.books_taken.append((book, start_date))

    def list_books(self):
        for book, start_date in self.books_taken:
            print(f"Book ID: {book.id}, Name: {book.name}, Status: {book.status}, Borrowed on: {start_date}")