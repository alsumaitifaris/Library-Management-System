from datetime import datetime
from typing import List, Dict

class Book:
    def __init__(self, title: str, author: str, genre: str, book_id: str):
        self.title = title
        self.author = author
        self.genre = genre
        self.book_id = book_id
        self.is_borrowed = False
        self.borrow_history: List[Dict] = []
        self.rating: float = 0.0
        self.num_ratings: int = 0

    def __str__(self) -> str:
        status = 'Borrowed' if self.is_borrowed else 'Available'
        rating_info = f", Rating: {self.rating:.1f}/5.0" if self.num_ratings > 0 else ", No ratings yet"
        return f"{self.title} by {self.author} ({status}){rating_info}"

    def add_rating(self, rating: float) -> None:
        if 1 <= rating <= 5:
            self.rating = ((self.rating * self.num_ratings) + rating) / (self.num_ratings + 1)
            self.num_ratings += 1

    def borrow(self, user_id: str) -> bool:
        if not self.is_borrowed:
            self.is_borrowed = True
            self.borrow_history.append({
                'user_id': user_id,
                'borrow_date': datetime.now().isoformat(),
                'return_date': None
            })
            return True
        return False

    def return_book(self) -> bool:
        if self.is_borrowed:
            self.is_borrowed = False
            if self.borrow_history:
                self.borrow_history[-1]['return_date'] = datetime.now().isoformat()
            return True
        return False

    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'book_id': self.book_id,
            'is_borrowed': self.is_borrowed,
            'borrow_history': self.borrow_history,
            'rating': self.rating,
            'num_ratings': self.num_ratings
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Book':
        book = cls(data['title'], data['author'], data['genre'], data['book_id'])
        book.is_borrowed = data['is_borrowed']
        book.borrow_history = data['borrow_history']
        book.rating = data.get('rating', 0.0)
        book.num_ratings = data.get('num_ratings', 0)
        return book
