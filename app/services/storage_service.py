import streamlit as st
import json
from app.utils.models import UserData

# Try to import streamlit_local_storage, fallback to None if it fails
try:
    from streamlit_local_storage import LocalStorage
    HAS_LOCAL_STORAGE = True
except ImportError:
    HAS_LOCAL_STORAGE = False

class StorageService:
    USER_KEY = "user_data"
    LANG_KEY = "language"
    TICKET_KEY = "ticket_history"
    
    def __init__(self):
        self._local_storage = None
        
    @property
    def local_storage(self):
        """Lazy initialization of LocalStorage only when needed."""
        if self._local_storage is None and HAS_LOCAL_STORAGE:
            try:
                self._local_storage = LocalStorage()
            except Exception as e:
                print(f"Failed to initialize LocalStorage: {e}")
                self._local_storage = False
        return self._local_storage if self._local_storage is not False else None

    def save_user_data(self, user_data: UserData):
        """Save user data to browser localStorage or session state."""
        data_json = json.dumps(user_data.__dict__)
        
        if HAS_LOCAL_STORAGE and self.local_storage:
            try:
                self.local_storage.setItem(self.USER_KEY, data_json)
                print("User data saved to localStorage")
                return
            except Exception as e:
                print(f"Error saving to localStorage: {e}")
        
        # Fallback to session state
        st.session_state[self.USER_KEY] = data_json
        print("User data saved to session state")

    def load_user_data(self) -> UserData:
        """Load user data from browser localStorage or session state."""
        
        if HAS_LOCAL_STORAGE and self.local_storage:
            try:
                data = self.local_storage.getItem(self.USER_KEY)
                if data:
                    d = json.loads(data)
                    return UserData(**d)
            except Exception as e:
                print(f"Error loading from localStorage: {e}")
        
        # Fallback to session state
        data = st.session_state.get(self.USER_KEY)
        if data:
            d = json.loads(data)
            return UserData(**d)
        return None

    def save_language(self, language: str):
        """Save language preference to browser localStorage or session state."""
        if HAS_LOCAL_STORAGE and self.local_storage:
            try:
                self.local_storage.setItem(self.LANG_KEY, language)
                return
            except Exception as e:
                print(f"Error saving language to localStorage: {e}")
        
        st.session_state[self.LANG_KEY] = language

    def load_language(self) -> str:
        """Load language preference from browser localStorage or session state."""
        if HAS_LOCAL_STORAGE and self.local_storage:
            try:
                lang = self.local_storage.getItem(self.LANG_KEY)
                if lang:
                    return lang
            except Exception as e:
                print(f"Error loading language from localStorage: {e}")
        
        return st.session_state.get(self.LANG_KEY, "en")

    def save_ticket(self, ticket_number: str):
        """Save ticket number to history in browser localStorage or session state."""
        tickets = self.get_ticket_history()
        tickets.append(ticket_number)
        
        if HAS_LOCAL_STORAGE and self.local_storage:
            try:
                self.local_storage.setItem(self.TICKET_KEY, json.dumps(tickets))
                return
            except Exception as e:
                print(f"Error saving ticket to localStorage: {e}")
        
        st.session_state[self.TICKET_KEY] = json.dumps(tickets)

    def get_ticket_history(self):
        """Get ticket history from browser localStorage or session state."""
        if HAS_LOCAL_STORAGE and self.local_storage:
            try:
                data = self.local_storage.getItem(self.TICKET_KEY)
                if data:
                    return json.loads(data)
            except Exception as e:
                print(f"Error loading ticket history from localStorage: {e}")
        
        data = st.session_state.get(self.TICKET_KEY)
        if data:
            return json.loads(data)
        return []

    def clear_user_data(self):
        """Clear all user data from browser localStorage or session state."""
        if HAS_LOCAL_STORAGE and self.local_storage:
            try:
                for key in [self.USER_KEY, self.LANG_KEY, self.TICKET_KEY]:
                    self.local_storage.removeItem(key)
                return
            except Exception as e:
                print(f"Error clearing localStorage: {e}")
        
        for key in [self.USER_KEY, self.LANG_KEY, self.TICKET_KEY]:
            if key in st.session_state:
                del st.session_state[key]