import streamlit as st
from typing import Callable

def create_grid_view(items, on_item_click, search_query="", search_fn: Callable = None):
    # Custom CSS for 2-column grid layout
    st.markdown(
        """
        <style>
        /* Grid container styling */
        .grid-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 10px 0;
        }
        
        /* Individual grid item styling */
        .grid-item {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            padding: 5px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
        }
        
        .grid-item:hover {
            background: #e9ecef;
            border-color: #1f77b4;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .grid-item-image {
            width: 160px;
            height: 160px;
            object-fit: cover;
            margin-bottom: 10px;
        }
        
        .grid-item-text {
            font-size: 16px;
            font-weight: 600;
            color: #333;
            text-align: center;
            line-height: 1.4;
            word-wrap: break-word;
        }
        
        /* Make Streamlit buttons invisible but clickable - ONLY for grid items */
        .stButton button {
            opacity: 0;
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            cursor: pointer;
            z-index: 10;
        }
        
        /* Ensure columns take equal space - ONLY for grid containers */
        .grid-container-wrapper div[data-testid="column"] {
            flex: 1 !important;
        }

                 @media (max-width: 640px) {
             .st-emotion-cache-ss04kk {
                 min-width: auto;
             }
         }
         
         /* Hide the parent container for this CSS-only markdown */
         div[data-testid="stElementContainer"]:has(.header-container3) {
             display: none !important;
             height: 0 !important;
             margin: 0 !important;
             padding: 0 !important;
         }
         </style>
         <div class="header-container3"></div>
         """,
        unsafe_allow_html=True,
    )
    
    if items is None:
        st.info("Loading...")
        return
        
    # Apply search filter
    if search_query:
        if search_fn:
            items = search_fn(search_query, items)
        else:
            items = [item for item in items if search_query.lower() in item.name.lower()]
    
    # Always 2 columns
    cols = st.columns(2)
    
    for idx, item in enumerate(items):
        with cols[idx % 2]:
            # Create a container for each grid item
            with st.container():
                # Create the visual box using HTML
                st.markdown(f"""
                <div class="grid-item">
                    <img src="{item.image_url}" class="grid-item-image" alt="{item.name}" />
                    <div class="grid-item-text">{item.name}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Invisible button that covers the entire box
                if st.button("", key=f"grid_{item.name}_{idx}", help=f"Click to select {item.name}"):
                    on_item_click(item) 