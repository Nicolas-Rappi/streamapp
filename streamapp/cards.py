import streamlit.components.v1 as components
from streamlit import columns


class Card:
    html = """
        <div style="height: 300px; width: 300px; margin: 30px; border-radius: 30px; box-shadow: 5px 5px 20px black;
            position: relative; text-align: center; background-color: black">
        <a style="text-decoration: none;" href="{url}" target="_blank">   
        <img src="{img}"
            style="height: 100%; width: 100%; border-radius: 30px; transition: .5s; opacity: 0.3;">
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">
            <h1 style="color: white; font-size: 2.5rem; font-family: sans-serif">{title}</h1>
            <p style="color: white; font-size: 1.2rem; font-family: sans-serif; font-weight:bold;">{description}</p>
        </div>
        </a>
        
        </div>
    """

    def render(**kwargs):
        return Card.html.format(**kwargs)

    @classmethod
    def add_card(cls, url: str, title: str, img: str, description: str,  col: columns):
        with col:
            components.html(
                cls.render(url=url, title=title, img=img, description=description),
                width=400,
                height=400
            )