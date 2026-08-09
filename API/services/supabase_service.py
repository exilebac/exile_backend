from supabase import create_client
from django.conf import settings

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def upload_video(file, filename):
    supabase.storage.from_("EXILE_VIDEOS").upload(filename, file)
    return filename

def get_signed_url(filename, expire=3600):
    return supabase.storage.from_("EXILE_VIDEOS").create_signed_url(filename, expire)
