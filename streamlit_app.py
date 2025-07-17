"""
Streamlit Cloud entry point
This file serves as the main entry point for Streamlit Cloud deployment.
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Import and run the main application
from main import main

if __name__ == "__main__":
    main() 