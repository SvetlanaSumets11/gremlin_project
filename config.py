from environs import Env

env = Env()
env.read_env('.env')

BOOK = 'BOOK'
AUTHOR = 'AUTHOR'
USER = 'USER'

BORROW = 'borrow'
BORROWED = 'borrowed'
RETURN = 'return'

DATATIME_FORMAT = '%Y-%m-%d %H:%M:%S'

GRAPH_CONNECTION_URL = f'ws://{env("GREMLIN_HOST")}:{env("GREMLIN_PORT")}/gremlin'
