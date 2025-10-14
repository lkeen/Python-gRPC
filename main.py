import grpc
from concurrent import futures
from proto import library_pb2_grpc
from handler import LibraryHandler
from controller import LibraryController
from repository import BookRepository, connect_db


def serve():
    db = connect_db()
    book_repository = BookRepository(db)
    library_controller = LibraryController(book_repository)
    library_handler = LibraryHandler(library_controller)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    library_pb2_grpc.add_LibraryServicer_to_server(library_handler, server)

    server.add_insecure_port('[::]:50051')
    print("Library gRPC server starting on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
