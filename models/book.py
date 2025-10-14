from dataclasses import dataclass
from typing import Tuple


@dataclass
class Book:
    uuid: str
    title: str
    author: str
    genre: str
    is_available: bool
    book_condition: str

    def get_tuple(self) -> Tuple:
        return (
            self.uuid,
            self.title,
            self.author,
            self.genre,
            self.is_available,
            self.book_condition
        )
