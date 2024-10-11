class Visitor:
    def __init__(self, name, visitor_id, books_taken=None):
        self.name = name
        self.visitor_id = visitor_id
        self.books_taken = books_taken if books_taken is not None else []
        self.id = visitor_id

    def add_book(self, book, start_date):
        self.books_taken.append((book, start_date))
