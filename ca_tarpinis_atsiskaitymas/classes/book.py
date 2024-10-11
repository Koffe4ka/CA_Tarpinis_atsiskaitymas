class Book:
    def __init__(self, name, author, genre, release_date, status='laisva', visitor_name=None, start_date=None, days_overdue=None, id=None):
        self.id = id
        self.name = name
        self.author = author
        self.genre = genre
        self.release_date = release_date
        self.status = status
        self.visitor_name = visitor_name
        self.start_date = start_date
        self.days_overdue = days_overdue

    def i_sarasa(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'genre': self.genre,
            'release_date': self.release_date,
            'status': self.status,
            'visitor_name': self.visitor_name,
            'start_date': self.start_date,
            'days_overdue': self.days_overdue
        }

    def is_saraso(parameter):
        return Book(
            id=parameter.get('id'),
            name=parameter['name'],
            author=parameter['author'],
            genre=parameter['genre'],
            release_date=parameter['release_date'],
            status=parameter.get('status', 'laisva'),
            visitor_name=parameter.get('visitor_name'),
            start_date=parameter.get('start_date'),
            days_overdue=parameter.get('days_overdue')
        )
