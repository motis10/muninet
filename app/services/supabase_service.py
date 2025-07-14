import os
import re
from supabase import create_client, Client
from app.utils.models import Category, StreetNumber

class SupabaseService:
    def __init__(self, supabase_url, supabase_key, ssl_cert=None, no_client=False):
        self.ssl_cert = ssl_cert
        self.client: Client = None
        if not no_client:
            self.client = create_client(supabase_url, supabase_key)

    def get_categories(self):
        if not self.client:
            raise RuntimeError("Supabase client not initialized.")
        try:
            data = self.client.table("categories").select("*").execute().data
            return [Category(**item) for item in data]
        except Exception as e:
            print(f"Supabase get_categories error: {e}")
            return []

    def get_street_numbers(self):
        if not self.client:
            raise RuntimeError("Supabase client not initialized.")
        try:
            data = self.client.table("street_numbers").select("*").execute().data
            return [StreetNumber(**item) for item in data]
        except Exception as e:
            print(f"Supabase get_street_numbers error: {e}")
            return []

    def search_categories(self, query: str, categories=None):
        """
        Search categories by name or text (case-insensitive, supports partial match).
        If categories is None, fetch from Supabase with server-side filtering.
        """
        if not query:
            return categories if categories is not None else self.get_categories()
        if categories is None:
            if not self.client:
                raise RuntimeError("Supabase client not initialized.")
            # Server-side search: ilike on name OR text
            try:
                data = self.client.table("categories").select("*") \
                    .or_(f"name.ilike.%{query}%,text.ilike.%{query}%") \
                    .execute().data
                return [Category(**item) for item in data]
            except Exception as e:
                print(f"Supabase search_categories error: {e}")
                return []
        # Fallback: local filtering
        import re
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        return [cat for cat in categories if pattern.search(cat.name) or pattern.search(cat.text)]

    def search_street_numbers(self, query: str, streets=None):
        """
        Search street numbers by name or house_number (case-insensitive, supports partial match).
        If streets is None, fetch from Supabase with server-side filtering.
        """
        if not query:
            return streets if streets is not None else self.get_street_numbers()
        if streets is None:
            if not self.client:
                raise RuntimeError("Supabase client not initialized.")
            try:
                data = self.client.table("street_numbers").select("*") \
                    .or_(f"name.ilike.%{query}%,house_number.ilike.%{query}%") \
                    .execute().data
                return [StreetNumber(**item) for item in data]
            except Exception as e:
                print(f"Supabase search_street_numbers error: {e}")
                return []
        # Fallback: local filtering
        import re
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        return [s for s in streets if pattern.search(s.name) or pattern.search(s.house_number)] 