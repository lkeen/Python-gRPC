from abc import ABC, abstractmethod
from typing import List
from models.book import Book
from .database import connect_db


SEARCH_BY_TITLE_QUERY = "SELECT uuid, title, author, genre, is_available, book_condition FROM book_copies WHERE title LIKE %s"
SEARCH_BY_AUTHOR_QUERY = "SELECT uuid, title, author, genre, is_available, book_condition FROM book_copies WHERE author LIKE %s"
SEARCH_BY_GENRE_QUERY = "SELECT uuid, title, author, genre, is_available, book_condition FROM book_copies WHERE genre LIKE %s"
GET_BY_UUID_QUERY = "SELECT uuid, title, author, genre, is_available, book_condition FROM book_copies WHERE uuid = %s"
INSERT_BOOK_QUERY = "INSERT INTO book_copies (uuid, title, author, genre, is_available, book_condition) VALUES (%s, %s, %s, %s, %s, %s)"
UPDATE_BOOK_QUERY = "UPDATE book_copies SET title = %s, author = %s, genre = %s, is_available = %s, book_condition = %s WHERE uuid = %s"
CHECKOUT_BOOK_QUERY = "UPDATE book_copies SET is_available = FALSE WHERE uuid = %s AND is_available = TRUE"
RETURN_BOOK_QUERY = "UPDATE book_copies SET is_available = TRUE WHERE uuid = %s AND is_available = FALSE"
DELETE_BOOK_QUERY = "DELETE FROM book_copies WHERE uuid = %s"
GET_ALL_BOOKS_QUERY = "SELECT uuid, title, author, genre, is_available, book_condition FROM book_copies"
INVENTORY_SUMMARY_QUERY = """
    SELECT
        COUNT(*) as total_books,
        SUM(CASE WHEN is_available = TRUE THEN 1 ELSE 0 END) as available_books,
        SUM(CASE WHEN is_available = FALSE THEN 1 ELSE 0 END) as checked_out_books
    FROM book_copies
"""


class IBookRepository(ABC):

    @abstractmethod
    def search_books_by_title(self, title: str) -> List[Book]:
        pass

    @abstractmethod
    def search_books_by_author(self, author: str) -> List[Book]:
        pass

    @abstractmethod
    def search_books_by_genre(self, genre: str) -> List[Book]:
        pass

    @abstractmethod
    def get_book_by_uuid(self, uuid: str) -> Book:
        pass

    @abstractmethod
    def create_book(self, book: Book) -> str:
        pass

    @abstractmethod
    def update_book(self, book: Book) -> bool:
        pass

    @abstractmethod
    def checkout_book(self, uuid: str) -> bool:
        pass

    @abstractmethod
    def return_book(self, uuid: str) -> bool:
        pass

    @abstractmethod
    def delete_book(self, uuid: str) -> bool:
        pass

    @abstractmethod
    def get_all_books(self) -> List[Book]:
        pass

    @abstractmethod
    def get_inventory_summary(self) -> dict:
        pass


class BookRepository(IBookRepository):

    def __init__(self, db):
        self._db = db

    def search_books_by_title(self, title: str) -> List[Book]:
        cursor = self._db.cursor()
        cursor.execute(SEARCH_BY_TITLE_QUERY, (f"%{title}%",))
        rows = cursor.fetchall()
        cursor.close()
        return [Book(*row) for row in rows]

    def search_books_by_author(self, author: str) -> List[Book]:
        cursor = self._db.cursor()
        cursor.execute(SEARCH_BY_AUTHOR_QUERY, (f"%{author}%",))
        rows = cursor.fetchall()
        cursor.close()
        return [Book(*row) for row in rows]

    def search_books_by_genre(self, genre: str) -> List[Book]:
        cursor = self._db.cursor()
        cursor.execute(SEARCH_BY_GENRE_QUERY, (f"%{genre}%",))
        rows = cursor.fetchall()
        cursor.close()
        return [Book(*row) for row in rows]

    def get_book_by_uuid(self, uuid: str) -> Book:
        cursor = self._db.cursor()
        cursor.execute(GET_BY_UUID_QUERY, (uuid,))
        row = cursor.fetchone()
        cursor.close()
        return Book(*row) if row else None

    def create_book(self, book: Book) -> str:
        cursor = self._db.cursor()
        cursor.execute(INSERT_BOOK_QUERY, book.get_tuple())
        self._db.commit()
        cursor.close()
        return book.uuid

    def update_book(self, book: Book) -> bool:
        cursor = self._db.cursor()
        cursor.execute(UPDATE_BOOK_QUERY, (
            book.title,
            book.author,
            book.genre,
            book.is_available,
            book.book_condition,
            book.uuid
        ))
        self._db.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0

    def checkout_book(self, uuid: str) -> bool:
        cursor = self._db.cursor()
        cursor.execute(CHECKOUT_BOOK_QUERY, (uuid,))
        self._db.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0

    def return_book(self, uuid: str) -> bool:
        cursor = self._db.cursor()
        cursor.execute(RETURN_BOOK_QUERY, (uuid,))
        self._db.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0

    def delete_book(self, uuid: str) -> bool:
        cursor = self._db.cursor()
        cursor.execute(DELETE_BOOK_QUERY, (uuid,))
        self._db.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0

    def get_all_books(self) -> List[Book]:
        cursor = self._db.cursor()
        cursor.execute(GET_ALL_BOOKS_QUERY)
        rows = cursor.fetchall()
        cursor.close()
        return [Book(*row) for row in rows]

    def get_inventory_summary(self) -> dict:
        cursor = self._db.cursor()
        cursor.execute(INVENTORY_SUMMARY_QUERY)
        row = cursor.fetchone()
        cursor.close()
        return {
            'total_books': row[0],
            'available_books': row[1],
            'checked_out_books': row[2]
        }
