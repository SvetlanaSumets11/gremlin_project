from gremlin_python.structure.graph import Vertex

from config import AUTHOR, BOOK, USER, BORROW, BORROWED, RETURN
from gremlin.interface.base import BaseEntity


class AuthorInterface(BaseEntity):
    label = AUTHOR


class BookInterface(BaseEntity):
    label = BOOK

    @classmethod
    def is_borrow(cls, book_id: str) -> bool:
        book_vertex = BookInterface.get_entity_by_id(book_id)
        return cls.GRAPH.V(book_vertex).outE(BORROWED).hasNext()


class UserInterface(BaseEntity):
    label = USER

    @classmethod
    def is_debtor(cls, user_id: str) -> bool:
        user_vertex = UserInterface.get_entity_by_id(user_id)
        return cls.GRAPH.V(user_vertex).outE(BORROW).hasNext()

    @classmethod
    def get_operation(cls, operation_type: str, user_id: str, book_id: str, properties: dict):
        operations = {
            BORROW: cls.borrow_book,
            RETURN: cls.return_book,
        }
        user_vertex = UserInterface.get_entity_by_id(user_id)
        book_vertex = BookInterface.get_entity_by_id(book_id)

        operation = operations.get(operation_type)
        if operation:
            operation(user_vertex, book_vertex, properties)

    @classmethod
    def borrow_book(cls, user: Vertex, book: Vertex, properties: dict):
        cls.add_edge(BORROW, user, book, properties)
        cls.add_edge(BORROWED, book, user, properties)

    @classmethod
    def return_book(cls, user: Vertex, book: Vertex, *args):
        cls.delete_edge(BORROW, user, book)
        cls.delete_edge(BORROWED, book, user)
