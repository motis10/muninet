import streamlit as st
from typing import Callable
from streamlit_image_gallery import streamlit_image_gallery

# Import i18n for translations
try:
    from app.utils.i18n import t
except ImportError:
    from utils.i18n import t

def create_grid_view(items, on_item_click, search_query="", search_fn: Callable = None, language="he"):
    if search_fn:
        items = search_fn(search_query)
    else:
        items = items   
    
    images = [
        {
            "src": item.image_url,
            "title": item.name,

        }
        for item in items
    ]

    clicked_index = streamlit_image_gallery(
        images=images,
        max_cols=2,
        gap=10,
        key="gallery"
    )

    if clicked_index is not None:
        clicked_item = items[clicked_index]
        on_item_click(clicked_item)

    return clicked_index