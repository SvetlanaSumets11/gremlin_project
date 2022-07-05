from abc import abstractmethod, ABC
from datetime import datetime
from typing import Any, Union

from gremlin_python.process.graph_traversal import inV, GraphTraversal
from gremlin_python.structure.graph import Vertex

from config import DATATIME_FORMAT
from gremlin.graph import get_traversal
from gremlin.models import Author, Book, User


class BaseEntity(ABC):
    GRAPH = get_traversal()

    @property
    @abstractmethod
    def label(self):
        pass

    @classmethod
    @property
    def _entity(cls) -> GraphTraversal:
        return cls.GRAPH.V().hasLabel(cls.label)

    @classmethod
    def add_or_update_vertex(cls, data: Union[Author, Book, User]) -> dict:
        data = data.dict()
        now = datetime.now().strftime(DATATIME_FORMAT)

        vertex = cls._entity.has('id', data['id'])
        if vertex.hasNext():
            vertex.property('updated_at', now).next()
        else:
            cls.GRAPH.addV(cls.label)\
                .property('id', data['id'])\
                .property('created_at', now)\
                .property('updated_at', now).next()

        vertex_with_property = cls.add_property(
            item=cls._entity.has('id', data['id']),
            data=data,
        )
        vertex_with_property.next()
        return cls._entity.has('id', data['id']).valueMap(True).next()

    @classmethod
    def add_property(cls, item: GraphTraversal, data: dict) -> GraphTraversal:
        for key, value in data.items():
            item.property(key, value)
        return item

    @classmethod
    def delete_vertex(cls, search_value: str):
        if cls.is_exists('id', search_value):
            cls._entity.has('id', search_value).drop().iterate()

    @classmethod
    def is_exists(cls, search_field: str, search_value: Any) -> bool:
        return cls._entity.has(search_field, search_value).hasNext()

    @classmethod
    def get_all(cls) -> list:
        return cls._entity.valueMap(True).toList()

    @classmethod
    def get_all_by_field(cls, search_field: str, search_value: Any) -> list:
        return cls._entity.has(search_field, search_value).valueMap(True).toList()

    @classmethod
    def get_entity_by_id(cls, search_value: str) -> Vertex:
        return cls._entity.has('id', search_value).next()

    @classmethod
    def get_by_id(cls, search_value: str) -> dict:
        return cls._entity.has('id', search_value).valueMap(True).next()

    @classmethod
    def has_edge(cls, relation: str, vertex_from, vertex_to) -> bool:
        return cls.GRAPH.V(vertex_from).outE(relation).filter_(inV().is_(vertex_to)).hasNext()

    @classmethod
    def add_edge(cls, relation: str, vertex_from: Vertex, vertex_to: Vertex, weights: dict):
        if cls.has_edge(relation, vertex_from, vertex_to):
            return
        edge = cls.GRAPH.addE(relation).from_(vertex_from).to(vertex_to)
        cls.add_property(edge, weights).next()

    @classmethod
    def delete_edge(cls, relation: str, vertex_from: Vertex, vertex_to: Vertex):
        if cls.has_edge(relation, vertex_from, vertex_to):
            cls.GRAPH.V(vertex_from).outE(relation).filter_(inV().is_(vertex_to)).drop().iterate()
