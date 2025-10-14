from abc import ABC, abstractmethod
from typing import List
from datetime import datetime, timedelta
from models.book import Book
from repository.book_repository import IBookRepository
import uuid as uuid_lib


class ILibraryController(ABC):

    @abstractmethod
    def search_books(self, title: str = None, author: str = None, genre: str = None) -> List[Book]:
        pass

    @abstractmethod
    def checkout_book(self, user_id: str, copy_uuid: str, loan_time_days: int) -> dict:
        pass

    @abstractmethod
    def return_book(self, copy_uuid: str) -> bool:
        pass

    @abstractmethod
    def add_book(self, title: str, author: str, genre: str, condition: str) -> str:
        pass

    @abstractmethod
    def update_book(self, uuid: str, title: str = None, author: str = None, genre: str = None, condition: str = None) -> bool:
        pass

    @abstractmethod
    def remove_book(self, uuid: str) -> bool:
        pass

    @abstractmethod
    def get_book_details(self, uuid: str) -> Book:
        pass

    @abstractmethod
    def get_inventory_summary(self) -> dict:
        pass

    @abstractmethod
    def get_all_books(self) -> List[Book]:
        pass


class LibraryController(ILibraryController):

    def __init__(self, book_repository: IBookRepository):
        self._book_repository = book_repository

    def search_books(self, title: str = None, author: str = None, genre: str = None) -> List[Book]:
        if not title and not author and not genre:
            return []

        results = []

        if title:
            results.extend(self._book_repository.search_books_by_title(title))

        if author:
            author_results = self._book_repository.search_books_by_author(author)
            results.extend(author_results)

        if genre:
            genre_results = self._book_repository.search_books_by_genre(genre)
            results.extend(genre_results)

        seen = set()
        unique_results = []
        for book in results:
            if book.uuid not in seen:
                seen.add(book.uuid)
                unique_results.append(book)

        return unique_results

    def checkout_book(self, user_id: str, copy_uuid: str, loan_time_days: int) -> dict:
        if not user_id or not copy_uuid:
            raise ValueError("user_id and copy_uuid are required")

        if loan_time_days <= 0:
            raise ValueError("loan_time_days must be positive")

        book = self._book_repository.get_book_by_uuid(copy_uuid)
        if not book:
            raise ValueError(f"Book with uuid {copy_uuid} not found")

        if not book.is_available:
            raise ValueError(f"Book {copy_uuid} is not available for checkout")

        success = self._book_repository.checkout_book(copy_uuid)
        if not success:
            raise ValueError(f"Failed to checkout book {copy_uuid}")

        loan_id = str(uuid_lib.uuid4())
        due_date = datetime.now() + timedelta(days=loan_time_days)
        due_date_str = due_date.strftime("%Y-%m-%d")

        return {
            'loan_id': loan_id,
            'due_date': due_date_str,
            'book_title': book.title,
            'book_author': book.author
        }

    def return_book(self, copy_uuid: str) -> bool:
        if not copy_uuid:
            raise ValueError("copy_uuid is required")

        book = self._book_repository.get_book_by_uuid(copy_uuid)
        if not book:
            raise ValueError(f"Book with uuid {copy_uuid} not found")

        if book.is_available:
            raise ValueError(f"Book {copy_uuid} is already available")

        return self._book_repository.return_book(copy_uuid)

    def add_book(self, title: str, author: str, genre: str, condition: str) -> str:
        if not title or not author:
            raise ValueError("title and author are required")

        if not condition:
            condition = "Good"

        book_uuid = str(uuid_lib.uuid4())
        book = Book(
            uuid=book_uuid,
            title=title,
            author=author,
            genre=genre or "",
            is_available=True,
            book_condition=condition
        )

        return self._book_repository.create_book(book)

    def update_book(self, uuid: str, title: str = None, author: str = None, genre: str = None, condition: str = None) -> bool:
        if not uuid:
            raise ValueError("uuid is required")

        existing_book = self._book_repository.get_book_by_uuid(uuid)
        if not existing_book:
            raise ValueError(f"Book with uuid {uuid} not found")

        updated_book = Book(
            uuid=uuid,
            title=title if title else existing_book.title,
            author=author if author else existing_book.author,
            genre=genre if genre else existing_book.genre,
            is_available=existing_book.is_available,
            book_condition=condition if condition else existing_book.book_condition
        )

        return self._book_repository.update_book(updated_book)

    def remove_book(self, uuid: str) -> bool:
        if not uuid:
            raise ValueError("uuid is required")

        book = self._book_repository.get_book_by_uuid(uuid)
        if not book:
            raise ValueError(f"Book with uuid {uuid} not found")

        return self._book_repository.delete_book(uuid)

    def get_book_details(self, uuid: str) -> Book:
        if not uuid:
            raise ValueError("uuid is required")

        book = self._book_repository.get_book_by_uuid(uuid)
        if not book:
            raise ValueError(f"Book with uuid {uuid} not found")

        return book

    def get_inventory_summary(self) -> dict:
        return self._book_repository.get_inventory_summary()

    def get_all_books(self) -> List[Book]:
        return self._book_repository.get_all_books()
