import streamlit as st
import json
from app.utils.models import UserData

# Try to import streamlit_local_storage, fallback to None if it fails
try:
    from streamlit_local_storage import LocalStorage
    local_storage = LocalStorage()
    HAS_LOCAL_STORAGE = True
except ImportError:
    print("streamlit_local_storage not available, using session state only")
    local_storage = None
    HAS_LOCAL_STORAGE = False

class StorageService:
    USER_KEY = "user_data"
    LANG_KEY = "language"
    TICKET_KEY = "ticket_history"

    def save_user_data(self, user_data: UserData):
        """Save user data to browser localStorage or session state."""
        data_json = json.dumps(user_data.__dict__)
        if HAS_LOCAL_STORAGE and local_storage:
            try:
                local_storage.setItem(self.USER_KEY, data_json)
                print("User data saved to localStorage")
            except Exception as e:
                print(f"Error saving to localStorage: {e}")
                st.session_state[self.USER_KEY] = data_json
        else:
            st.session_state[self.USER_KEY] = data_json
            print("User data saved to session state")

    def load_user_data(self) -> UserData:
        """Load user data from browser localStorage or session state."""
        if HAS_LOCAL_STORAGE and local_storage:
            try:
                data = local_storage.getItem(self.USER_KEY)
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
        if HAS_LOCAL_STORAGE and local_storage:
            try:
                local_storage.setItem(self.LANG_KEY, language)
            except Exception as e:
                st.session_state[self.LANG_KEY] = language
        else:
            st.session_state[self.LANG_KEY] = language

    def load_language(self) -> str:
        """Load language preference from browser localStorage or session state."""
        if HAS_LOCAL_STORAGE and local_storage:
            try:
                lang = local_storage.getItem(self.LANG_KEY)
                return lang if lang else "en"
            except Exception as e:
                return st.session_state.get(self.LANG_KEY, "en")
        else:
            return st.session_state.get(self.LANG_KEY, "en")

    def save_ticket(self, ticket_number: str):
        """Save ticket number to history in browser localStorage or session state."""
        if HAS_LOCAL_STORAGE and local_storage:
            try:
                tickets = self.get_ticket_history()
                tickets.append(ticket_number)
                local_storage.setItem(self.TICKET_KEY, json.dumps(tickets))
            except Exception as e:
                tickets = st.session_state.get(self.TICKET_KEY, [])
                tickets.append(ticket_number)
                st.session_state[self.TICKET_KEY] = json.dumps(tickets)
        else:
            tickets = st.session_state.get(self.TICKET_KEY, [])
            tickets.append(ticket_number)
            st.session_state[self.TICKET_KEY] = json.dumps(tickets)

    def get_ticket_history(self):
        """Get ticket history from browser localStorage or session state."""
        if HAS_LOCAL_STORAGE and local_storage:
            try:
                data = local_storage.getItem(self.TICKET_KEY)
                if data:
                    return json.loads(data)
            except Exception as e:
                data = st.session_state.get(self.TICKET_KEY)
                if data:
                    return json.loads(data)
        else:
            data = st.session_state.get(self.TICKET_KEY)
            if data:
                return json.loads(data)
        return []

    def clear_user_data(self):
        """Clear all user data from browser localStorage or session state."""
        if HAS_LOCAL_STORAGE and local_storage:
            try:
                for key in [self.USER_KEY, self.LANG_KEY, self.TICKET_KEY]:
                    local_storage.removeItem(key)
            except Exception as e:
                for key in [self.USER_KEY, self.LANG_KEY, self.TICKET_KEY]:
                    if key in st.session_state:
                        del st.session_state[key]
        else:
            for key in [self.USER_KEY, self.LANG_KEY, self.TICKET_KEY]:
                if key in st.session_state:
                    del st.session_state[key]