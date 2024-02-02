from pathlib import Path
from datetime import timedelta
from snowflake import connector
from cryptography.fernet import Fernet
from jinja2 import Environment, FileSystemLoader, BaseLoader
from pandas import read_sql_query, DataFrame
from streamlit.connections import BaseConnection
from streamlit import cache_data, session_state, secrets
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


class SnowConnection(BaseConnection[connector.connect]):
    def _connect(self) -> connector.connect:
        connection = connector.connect(
            **self.__check_tocken(
                dict(secrets.SNOW_SERVER)
            )
        )
        return connection
    
    def __check_tocken(self, credentials: dict):
        try:
            if secrets.get('key') and not credentials.get('authenticator') == 'externalbrowser':
                token = Fernet(secrets.key.encode()).decrypt(secrets.SNOW_SERVER.password.encode()).decode()
                credentials.pop('password')
                credentials.update(password=token)
        except:
            credentials.pop('user')
            credentials.update(user=session_state.name)
        return credentials 

    
    @classmethod
    def render(cls, query, params, direct:bool = True, sub_folder:str = ''):
        if not direct:
            
            query_path = Path(secrets.queries_path, sub_folder, query +'.sql').as_posix()
            query_rendered = Environment(
                loader=FileSystemLoader('')
            ).get_template(query_path).render(**params)
        else:
            query_rendered = Environment(
                loader=BaseLoader
            ).from_string(query).render(**params) 
        return query_rendered

    def query(self, query:str, params:dict = {}, direct:bool = True, logic:str = None, ttl:timedelta = timedelta(minutes=30), set_index:str = None):
        """
        query: if saved it must be in the queries folder, otherwise it must be an sql statement
        params = dict: {country : 'br', ally:'as'}
        direct: if the query is a string True, if must be loaded a query file False

        """
        query_rendered = SnowConnection.render(query, params, direct, logic)

        @cache_data(ttl=ttl, show_spinner=True)
        def _query(query_rendered):
            try:
                frm = read_sql_query(query_rendered, self._instance)
                frm.rename(columns=str.upper, inplace = True)
                if set_index:
                    frm.set_index(set_index.upper())
                print('success query ', session_state.get('name', 'No log!'))
                return frm
            except Exception as e:
                return DataFrame(data={'Error Reason': [e]})

        return _query(query_rendered)
