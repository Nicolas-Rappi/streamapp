import streamlit as st
from .utils import page_selector

class CountrySelector:
    countries = {
        'CO': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Flag_of_Colombia.svg/255px-Flag_of_Colombia.svg.png',
        'AR': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Flag_of_Argentina.svg/2560px-Flag_of_Argentina.svg.png',
        'BR': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/1280px-Flag_of_Brazil.svg.png',
        'MX': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Flag_of_Mexico.svg/1280px-Flag_of_Mexico.svg.png',
        'CR': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Flag_of_Costa_Rica.svg/255px-Flag_of_Costa_Rica.svg.png',
        'PE': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Flag_of_Peru_%28state%29.svg/2560px-Flag_of_Peru_%28state%29.svg.png',
        'EC': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Flag_of_Ecuador.svg/2560px-Flag_of_Ecuador.svg.png',
        'CL': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Flag_of_Chile.svg/1200px-Flag_of_Chile.svg.png',
        'UY': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Flag_of_Uruguay.svg/2560px-Flag_of_Uruguay.svg.png'
    }

    def __init__(cls):
        st.session_state.country = st.session_state.get('country', 'UY')
        col1, col2 = st.container().columns([3,1])
        col1.selectbox(
            'Country Select',
            cls.countries.keys(),
            key='CountrySelect', 
            placeholder='Select Country',
            on_change=cls.change_country(),
            label_visibility='collapsed',
            index=list(cls.countries.keys()).index(
                st.session_state.get('CountrySelect', 'UY')
            )
        )
        with col2:
            cls.show_country()
        return

    def change_country(cls):
        st.session_state.country = st.session_state.get('CountrySelect', 'UY')

    def set_options(key, option):
        st.session_state[key] = option

    @classmethod
    def show_country(cls, width: int=40):
        return st.image(cls.countries.get(st.session_state.country), width=width)

    @classmethod
    def change_options(cls, key: str, page_options: dict, include_pages:bool = False, place_holder: str = None):
        col1, col2 = st.columns([7,1])
        with col1.expander(place_holder, expanded=False):
            st.selectbox(
                'Options',
                key=f'{key}_selected',
                options=page_options.keys(),
                label_visibility='hidden',
                placeholder=place_holder
            )
            st.button(
                'Select Option',
                on_click=cls.set_options,
                kwargs={'key': key, 'option': st.session_state.get(f'{key}_selected')},
                type='primary'
            )
        with col2:
            cls.show_country()

        if include_pages:
            page_selector(st.session_state, key, page_options)