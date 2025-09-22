CREATE TABLE IF NOT EXISTS book_copies (
    uuid CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    is_available BOOLEAN DEFAULT TRUE,
    book_condition VARCHAR(50)
);

INSERT INTO book_copies (uuid, title, author, genre, is_available, book_condition) VALUES
('book-001', 'Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 'Fantasy', TRUE, 'Good'),
('book-002', 'Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 'Fantasy', FALSE, 'Excellent'),
('book-003', 'Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 'Fantasy', TRUE, 'Worn'),
('book-004', 'To Kill a Mockingbird', 'Harper Lee', 'Fiction', TRUE, 'Excellent'),
('book-005', 'To Kill a Mockingbird', 'Harper Lee', 'Fiction', FALSE, 'Good'),
('book-006', '1984', 'George Orwell', 'Dystopian Fiction', TRUE, 'Fair'),
('book-007', '1984', 'George Orwell', 'Dystopian Fiction', TRUE, 'Good'),
('book-008', 'The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', TRUE, 'Good'),
('book-009', 'Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', TRUE, 'Excellent'),
('book-010', 'Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', FALSE, 'Worn'),
('book-011', 'Dune', 'Frank Herbert', 'Science Fiction', TRUE, 'Fair'),
('book-012', 'The Art of War', 'Sun Tzu', 'Philosophy', TRUE, 'Good');