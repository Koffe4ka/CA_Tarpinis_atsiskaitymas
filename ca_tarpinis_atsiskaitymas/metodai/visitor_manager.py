import pickle
import os
from classes.visitor_data import Visitor
class VisitorManager:
    def __init__(self, visitors_file_path):
        self.visitors_file_path = visitors_file_path
        self.visitors = self.load_visitors()
        
    def create_visitor(self, name):
        if not name:
            raise ValueError("Skaitytojo vardas negali būti tuščias.")
        visitor_id = len(self.visitors) + 1
        new_visitor = Visitor(name=name, visitor_id=visitor_id)
        self.visitors.append(new_visitor)
        self.save_visitors()
        return new_visitor
    
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
    
    def get_visitor_by_id(self, visitor_id):
        for visitor in self.visitors:
            if visitor.visitor_id == visitor_id:
                return visitor
        return None
    
    def get_visitor_by_name(self, name):
        for visitor in self.visitors:
            if visitor.name == name:
                return visitor
        return None