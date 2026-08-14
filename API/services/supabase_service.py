from supabase import create_client
from django.conf import settings

# Konekte ak Supabase
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def upload_video(file, filename):
    """
    Upload yon videyo nan bucket EXILE_VIDEOS.
    Presize MIME type pou evite erè 415 (invalid_mime_type).
    """
    try:
        # Convertir le fichier Django en bytes pour Supabase
        file_content = file.read()
        res = supabase.storage.from_("Exile_videos").upload(
            filename,
            file_content,
            {"content-type": "video/mp4"}  # 👈 presize tip fichye a
        )
        return res  # retounen repons upload la pou debugging
    except Exception as e:
        print(f"Erreur upload vidéo: {e}")
        raise

def upload_file(file, filename):
    """
    Upload yon fichye (photo oswa banner) nan bucket EXILE_IMAGES.
    Détecte automatiquement le MIME type selon l'extension du fichier.
    Supporte 7+ formats d'images: jpg, jpeg, png, gif, webp, bmp, tiff, svg
    """
    try:
        # Convertir le fichier Django en bytes pour Supabase
        file_content = file.read()
        
        # Détecter le MIME type selon l'extension
        content_type = "image/jpeg"  # Par défaut
        ext = filename.lower().split('.')[-1] if '.' in filename else ''

        if ext in ['jpg', 'jpeg']:
            content_type = "image/jpeg"
        elif ext == 'png':
            content_type = "image/png"
        elif ext == 'gif':
            content_type = "image/gif"
        elif ext == 'webp':
            content_type = "image/webp"
        elif ext == 'bmp':
            content_type = "image/bmp"
        elif ext in ['tiff', 'tif']:
            content_type = "image/tiff"
        elif ext == 'svg':
            content_type = "image/svg+xml"
        elif ext == 'ico':
            content_type = "image/x-icon"

        res = supabase.storage.from_("Exile_images").upload(
            filename,
            file_content,
            {"content-type": content_type}
        )
        return res
    except Exception as e:
        print(f"Erreur upload fichier: {e}")
        raise

def get_signed_url(filename, expire=3600):
    """
    Kreye yon signed URL pou videyo a.
    expire default = 3600 segonn (1 èdtan).
    """
    return supabase.storage.from_("Exile_videos").create_signed_url(filename, expire)
