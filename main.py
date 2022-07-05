from fastapi import FastAPI

from gremlin.interface.entities import AuthorInterface, BookInterface, UserInterface
from models import Author, Book, User

app = FastAPI()


@app.get('/books')
def read_books() -> list:
    return BookInterface.get_all()


@app.get('/authors')
def read_authors() -> list:
    return AuthorInterface.get_all()


@app.get('/users')
def read_users() -> list:
    return UserInterface.get_all()


@app.get('/book{book_id}')
def read_book(book_id: str) -> dict:
    return BookInterface.get_by_id(book_id)


@app.get('/author{author_id}')
def read_author(author_id: str) -> dict:
    return AuthorInterface.get_by_id(author_id)


@app.get('/user{user_id}')
def read_user(user_id: str) -> dict:
    return UserInterface.get_by_id(user_id)


@app.put('/book')
def put_book(book: Book) -> dict:
    if not AuthorInterface.is_exist(search_field='id', search_value=book.author_id):
        raise ValueError(f'Author does not exist')
    return BookInterface.add_or_update_vertex(book)


@app.put('/author')
def put_author(author: Author) -> dict:
    return AuthorInterface.add_or_update_vertex(author)


@app.put('/user')
def put_user(user: User) -> dict:
    return UserInterface.add_or_update_vertex(user)


@app.post('/book')
def add_book(book: Book) -> dict:
    if not AuthorInterface.is_exist('id', book.author_id):
        raise ValueError(f'Author does not exist')
    return BookInterface.add_or_update_vertex(book)


@app.post('/author')
def add_author(author: Author) -> dict:
    return AuthorInterface.add_or_update_vertex(author)


@app.post('/user')
def add_user(user: User) -> dict:
    return UserInterface.add_or_update_vertex(user)


@app.delete('/book{book_id}')
def delete_book(book_id: str):
    if BookInterface.is_borrow(book_id):
        raise ValueError(f'Book can not be deleted')
    BookInterface.delete_vertex(book_id)


@app.delete('/author{author_id}')
def delete_author(author_id: str):
    if not AuthorInterface.is_exist('id', author_id):
        raise ValueError(f'Author does not exist')
    if BookInterface.is_exist('author_id', author_id):
        books = BookInterface.get_all_by_field('author_id', author_id)
        for book in books:
            book_id = book['id'].pop()
            if BookInterface.is_borrow(book_id):
                raise ValueError(f'Author can not be deleted')
            BookInterface.delete_vertex(book_id)
    AuthorInterface.delete_vertex(author_id)


@app.delete('/user{user_id}')
def delete_user(user_id: str):
    if not UserInterface.is_exist('id', user_id):
        raise ValueError(f'User does not exist')
    if UserInterface.is_debtor(user_id):
        raise ValueError(f'User can not be deleted')
    UserInterface.delete_vertex(user_id)


@app.get('/books/{author_id}')
def get_books_by_author(author_id: str) -> list:
    return BookInterface.get_all_by_field('author_id', author_id)


@app.post("/actions")
def form_user_actions(relation: str, user_id: str, book_id: str, days: int = None):
    if not UserInterface.is_exist(search_field='id', search_value=user_id):
        raise ValueError(f'User does not exist')
    UserInterface.get_operation(relation, user_id, book_id, properties={'days': days} if days else {})
