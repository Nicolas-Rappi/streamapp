from streamlit_authenticator  import Authenticate
import streamlit as st
from snow_class import SnowConnection
from country_selector import CountrySelector

class Roles:
    no_acces = '## Sorry you don\'t have access to this page ⛔ \n contact your admin for more info **@nicolas.morales**'
    
    def __init__(self, roles: list, current_role: list):
        self.roles = set(roles)
        self.roles.add('admin')
        self.current_role = current_role

    def __call__(self, func):
        print(self.roles.intersection(self.current_role))
        if self.roles.intersection(self.current_role):
            def wrapper(*args, **kargs):
                return func(*args, **kargs)
            return wrapper
        return lambda: st.markdown(Roles.no_acces)
    
    @classmethod
    def allow_acces(cls, roles:list = None):
        if 'dev' in st.session_state.get('roles', []):
            st.error('Be carefull in development speace', icon='🤖')
        elif roles == None or st.session_state.get('roles', ['admin']):
            return
        elif not set(roles).intersection(st.session_state.get('roles', [])):
            st.markdown(cls.no_acces)
            st.stop()
        return


class Login:

    @classmethod
    def logout(cls):
        st.session_state.authenticator.logout('Logout', 'sidebar')
        with st.sidebar:
            CountrySelector()
            st.caption(f'Welcome **{st.session_state.name}**')
        return

    @classmethod
    def login(cls, roles=None):
        if st.session_state.get('authentication_status') == None:
            # autheticate
            try:
                st.session_state.authenticator = Authenticate(dict(st.secrets.credentials), 'cookie_name', 'key', cookie_expiry_days=1)
                *_, username = st.session_state.authenticator.login('Login', 'main')
                print('Login ', st.session_state.name)
                try:
                    st.session_state['roles'] = st.session_state.authenticator.credentials['usernames'].get(username).get('roles')
                except AttributeError:
                    st.session_state['roles'] = []
            except KeyError:
                st.session_state.authentication_status = None
                st.warning('Try again something was wrong'), st.stop()
                print('Error in login with name key')
        try:
            # if authentication is successfull
            if st.session_state.authentication_status:
                cls.logout()
                Roles.allow_acces(roles)
                if st.session_state.get('conn') == None:
                    st.session_state.conn = st.connection('snow', type=SnowConnection)
            # if authentication fail
            elif st.session_state.authentication_status == False:
                st.session_state.authentication_status = None
                st.error('Username/password is incorrect'), st.stop()
            
            elif st.session_state.authentication_status == None:
                st.session_state.authentication_status = None
                st.warning('Please enter your username and password'), st.stop()
        except AttributeError:
            st.session_state.authentication_status = None
