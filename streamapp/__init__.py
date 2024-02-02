from streamlit import connection
from .snow_class import SnowConnection


class Conn:

    @property
    def connection(cls):
        return connection('snow', type=SnowConnection)
    
    @property
    def query(cls):
        return connection('snow', type=SnowConnection).query

conn = Conn()