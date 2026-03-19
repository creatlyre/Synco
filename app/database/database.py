from app.database.supabase_store import SupabaseStore


# Backward-compatibility placeholders for modules that still import these names.
engine = None
Base = None


def get_db():
    yield SupabaseStore()
