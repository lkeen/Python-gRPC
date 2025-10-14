import grpc
from proto import library_pb2, library_pb2_grpc
from controller.library import ILibraryController


class LibraryHandler(library_pb2_grpc.LibraryServicer):

    def __init__(self, library_controller: ILibraryController):
        self._library_controller = library_controller

    def SearchBook(self, request, context):
        try:
            books = self._library_controller.search_books(
                title=request.bookName if request.bookName else None,
                author=request.bookAuthor if request.bookAuthor else None,
                genre=request.bookGenre if request.bookGenre else None
            )

            book_copies = []
            for book in books:
                book_copy = library_pb2.BookCopy(
                    uuid=book.uuid,
                    author=book.author,
                    title=book.title,
                    genre=book.genre,
                    isAvaliable=book.is_available,
                    condition=book.book_condition
                )
                book_copies.append(book_copy)

            return library_pb2.SearchBookResponse(avaliableCopies=book_copies)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return library_pb2.SearchBookResponse()

    def CheckoutBook(self, request, context):
        try:
            result = self._library_controller.checkout_book(
                user_id=request.userId,
                copy_uuid=request.copyUuid,
                loan_time_days=request.loanTime
            )

            return library_pb2.CheckoutBookResponse(
                loanId=result['loan_id'],
                dueDate=result['due_date'],
                bookTitle=result['book_title'],
                bookAuthor=result['book_author']
            )

        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return library_pb2.CheckoutBookResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return library_pb2.CheckoutBookResponse()

    def ReturnBook(self, request, context):
        try:
            success = self._library_controller.return_book(request.copyUuid)
            return library_pb2.ReturnBookResponse(success=success)

        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return library_pb2.ReturnBookResponse(success=False)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return library_pb2.ReturnBookResponse(success=False)

    def CreateBook(self, request, context):
        try:
            uuid = self._library_controller.add_book(
                title=request.title,
                author=request.author,
                genre=request.genre,
                condition=request.condition
            )
            return library_pb2.CreateBookResponse(uuid=uuid)

        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return library_pb2.CreateBookResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return library_pb2.CreateBookResponse()

    def GetBook(self, request, context):
        try:
            book = self._library_controller.get_book_details(request.uuid)

            book_copy = library_pb2.BookCopy(
                uuid=book.uuid,
                author=book.author,
                title=book.title,
                genre=book.genre,
                isAvaliable=book.is_available,
                condition=book.book_condition
            )
            return library_pb2.GetBookResponse(book=book_copy)

        except ValueError as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(str(e))
            return library_pb2.GetBookResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return library_pb2.GetBookResponse()

    def UpdateBook(self, request, context):
        try:
            success = self._library_controller.update_book(
                uuid=request.uuid,
                title=request.title if request.title else None,
                author=request.author if request.author else None,
                genre=request.genre if request.genre else None,
                condition=request.condition if request.condition else None
            )
            return library_pb2.UpdateBookResponse(success=success)

        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return library_pb2.UpdateBookResponse(success=False)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return library_pb2.UpdateBookResponse(success=False)

    def DeleteBook(self, request, context):
        try:
            success = self._library_controller.remove_book(request.uuid)
            return library_pb2.DeleteBookResponse(success=success)

        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return library_pb2.DeleteBookResponse(success=False)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return library_pb2.DeleteBookResponse(success=False)

    def GetAllBooks(self, request, context):
        try:
            books = self._library_controller.get_all_books()

            book_copies = []
            for book in books:
                book_copy = library_pb2.BookCopy(
                    uuid=book.uuid,
                    author=book.author,
                    title=book.title,
                    genre=book.genre,
                    isAvaliable=book.is_available,
                    condition=book.book_condition
                )
                book_copies.append(book_copy)

            return library_pb2.GetAllBooksResponse(books=book_copies)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return library_pb2.GetAllBooksResponse()

    def GetInventorySummary(self, request, context):
        try:
            summary = self._library_controller.get_inventory_summary()

            return library_pb2.GetInventorySummaryResponse(
                totalBooks=summary['total_books'],
                availableBooks=summary['available_books'],
                checkedOutBooks=summary['checked_out_books']
            )

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return library_pb2.GetInventorySummaryResponse()
