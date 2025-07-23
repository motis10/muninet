import streamlit as st
import json
from app.utils.models import UserData
from app.utils.i18n import t
from app.components.header import render_header

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
        """Save user data to browser localStorage AND session state immediately."""
        data_json = json.dumps(user_data.__dict__)
        
        # CRITICAL: Save to session state FIRST for immediate access
        st.session_state[self.USER_KEY] = data_json
        st.session_state.user_data = user_data  # Also store the object directly
        print("✅ User data saved to session state immediately")
        
        # Then save to localStorage for persistence (async)
        if HAS_LOCAL_STORAGE and self.local_storage:
            try:
                self.local_storage.setItem(self.USER_KEY, data_json)
                print("✅ User data queued for localStorage")
            except Exception as e:
                print(f"❌ Error saving to localStorage: {e}")

    def load_user_data(self) -> UserData:
        """Load user data from session state first, then localStorage."""
        
        # Check session state first (immediate access)
        if hasattr(st.session_state, 'user_data') and st.session_state.user_data:
            print("✅ Loaded user data from session_state object")
            return st.session_state.user_data
        
        # Check session state JSON backup
        data = st.session_state.get(self.USER_KEY)
        if data:
            try:
                d = json.loads(data)
                user_data = UserData(**d)
                st.session_state.user_data = user_data  # Cache the object
                print("✅ Loaded user data from session_state JSON")
                return user_data
            except Exception as e:
                print(f"Error parsing session state data: {e}")
        
        # Finally try localStorage (for persistence across sessions)
        if HAS_LOCAL_STORAGE and self.local_storage:
            try:
                data = self.local_storage.getItem(self.USER_KEY)
                if data:
                    d = json.loads(data)
                    user_data = UserData(**d)
                    st.session_state.user_data = user_data  # Cache the object
                    print("✅ Loaded user data from localStorage")
                    return user_data
            except Exception as e:
                print(f"Error loading from localStorage: {e}")
        
        print("❌ No user data found")
        return None
        # print("❌ No user data found - generating random user data")
        # # Generate random user data as fallback
        # random_user = self._generate_random_user_data()
        
        # # Save the generated data for future use
        # self.save_user_data(random_user)
        
        # print(f"✅ Generated random user: {random_user.first_name} {random_user.last_name}")
        # return (random_user)


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

    def save_ticket(self, ticket):
        """Save a ticket to history (both localStorage and session state)."""
        # Get current history
        tickets = self.get_ticket_history()
        
        # Handle ticket as string (ticket number/ID)
        if isinstance(ticket, str):
            ticket_id = ticket
        elif isinstance(ticket, dict):
            ticket_id = ticket.get('ticket_id') or ticket.get('data') or str(ticket)
        else:
            ticket_id = str(ticket)  # Convert to string as fallback
        
        # Add new ticket (avoid duplicates)
        if ticket_id and ticket_id not in tickets:
            tickets.append(ticket_id)
            print(f"DEBUG: Added ticket {ticket_id} to history. Total tickets: {len(tickets)}")
        else:
            print(f"DEBUG: Ticket {ticket_id} already exists or is invalid")
        
        # Save to localStorage as JSON string (array of strings)
        if HAS_LOCAL_STORAGE and self.local_storage:
            try:
                self.local_storage.setItem(self.TICKET_KEY, json.dumps(tickets))
                print(f"DEBUG: Saved to localStorage: {tickets}")
            except Exception as e:
                print(f"Error saving to localStorage: {e}")
        
        # Also save to session state as backup (array of strings)
        st.session_state[self.TICKET_KEY] = tickets
        print(f"DEBUG: Saved to session state: {tickets}")

    def get_ticket_history(self):
        """Get ticket history from browser localStorage or session state."""
        if HAS_LOCAL_STORAGE and self.local_storage:
            try:
                data = self.local_storage.getItem(self.TICKET_KEY)
                print(f"DEBUG: Ticket history from localStorage: {data}")
                if data:
                    # localStorage stores as JSON string, parse to get the list
                    parsed = json.loads(data)
                    return parsed if isinstance(parsed, list) else []
            except Exception as e:
                print(f"Error loading ticket history from localStorage: {e}")
        
        # Fallback to session state
        data = st.session_state.get(self.TICKET_KEY, [])
        return data if isinstance(data, list) else []

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
