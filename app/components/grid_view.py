import streamlit as st
from typing import Callable

def create_grid_view(items, on_item_click, search_query="", search_fn: Callable = None):
    st.markdown(
        """
        <style>
        div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"] {
            background: #f8f9fa;
            border-radius: 1em;
            width: 220px;
            height: 220px;
            min-width: 220px;
            min-height: 220px;
            max-width: 220px;
            max-height: 220px;
            margin: 0.5em auto 1em auto;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            box-sizing: border-box;
            text-align: center;
            flex: 1 0 220px;
        }
        .grid-img-area {
            width: 120px;
            height: 120px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 0.5em auto;
            background: transparent;
            border-radius: 0.5em;
            text-align: -webkit-center;
            text-align: center;
        }
        .grid-img-area img {
            max-width: 100%;
            max-height: 100%;
            display: block;
            margin: 0 auto;
        }
        div[data-testid="stHorizontalBlock"] button {
            width: 90%;
            height: 48px;
            min-height: 48px;
            font-size: 1.1em;
            border-radius: 0.5em;
            margin-bottom: 10px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        div[data-testid="stFullScreenFrame"] {
            text-align: -webkit-center;
        }


        
        </style>
        """,
        unsafe_allow_html=True,
    )
    if items is None:
        st.info("Loading...")
        return
    if search_query:
        if search_fn:
            items = search_fn(search_query, items)
        else:
            items = [item for item in items if search_query.lower() in item.name.lower()]
    cols_per_row = max(3, 4 if len(items) > 12 else 3 if len(items) > 6 else 2 if len(items) > 2 else 1)
    cols = st.columns(cols_per_row)
    for idx, item in enumerate(items):
        with cols[idx % cols_per_row]:
            with st.container(height=220):
                st.image(item.image_url, width=120)
                if st.button(item.name, key=f"grid_{item.name}_{idx}"):
                    on_item_click(item) 