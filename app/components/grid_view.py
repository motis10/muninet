import streamlit as st
from typing import Callable
from streamlit_image_gallery import streamlit_image_gallery

# Import i18n for translations
try:
    from app.utils.i18n import t
except ImportError:
    from utils.i18n import t

def create_grid_view(items, on_item_click, search_query="", search_fn: Callable = None, language="he", page_key="default"):
    # Debug: Print search info
    # print(f"DEBUG grid_view {page_key}: search_query='{search_query}', has_search_fn={search_fn is not None}")
    
    if search_fn:
        filtered_items = search_fn(search_query)
        # print(f"DEBUG grid_view {page_key}: original_items={len(items)}, filtered_items={len(filtered_items)}")
        items = filtered_items
    else:
        items = items   
    
    images = [
        {
            "src": item.image_url,
            "title": item.name,

        }
        for item in items
    ]
    
    # print(f"DEBUG grid_view {page_key}: images: {len(images)}")

    # Create dynamic key based on search query and number of items to force re-render
    dynamic_key = f"gallery_{page_key}_{len(images)}_{hash(search_query) if search_query else 'empty'}"
    
    clicked_index = streamlit_image_gallery(
        images=images,
        max_cols=2,
        gap=10,
        key=dynamic_key
    )

    if clicked_index is not None:
        # print(f"DEBUG grid_view {page_key}: clicked_index={clicked_index}")
        clicked_item = items[clicked_index]
        on_item_click(clicked_item)

    return clicked_index