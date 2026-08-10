from supabase import create_client
from django.conf import settings

# Konekte ak Supabase
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def upload_video(file, filename):
    """
    Upload yon videyo nan bucket EXILE_VIDEOS.
    Presize MIME type pou evite erè 415 (invalid_mime_type).
    """
    res = supabase.storage.from_("Exile_videos").upload(
        filename,
        file,
        {"content-type": "video/mp4"}  # 👈 presize tip fichye a
    )
    return res  # retounen repons upload la pou debugging

def get_signed_url(filename, expire=3600):
    """
    Kreye yon signed URL pou videyo a.
    expire default = 3600 segonn (1 èdtan).
    """
    return supabase.storage.from_("Exile_videos").create_signed_url(filename, expire)
