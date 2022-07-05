from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.graph_traversal import GraphTraversalSource
from gremlin_python.structure.graph import Graph

from config import GRAPH_CONNECTION_URL


def get_traversal() -> GraphTraversalSource:
    connection = DriverRemoteConnection(GRAPH_CONNECTION_URL, 'g')
    graph = Graph().traversal().withRemote(connection)
    return graph
