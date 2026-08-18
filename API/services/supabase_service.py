from supabase import create_client
from django.conf import settings
import mimetypes
import os
import uuid


# ============================================================
# CONNEXION SUPABASE
# ============================================================

supabase = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY,
)


# ============================================================
# UPLOAD VIDÉO
# ============================================================

def upload_video(file, filename=None):
    """
    Upload une vidéo dans le bucket Exile_videos.

    Le nom final est rendu unique afin d'éviter les erreurs
    Supabase 409 Duplicate.

    Args:
        file: fichier Django reçu par request.FILES
        filename: nom souhaité du fichier

    Returns:
        réponse Supabase
    """

    try:
        # ----------------------------------------------------
        # Lire le fichier
        # ----------------------------------------------------

        file_content = file.read()

        if not file_content:
            raise ValueError("Le fichier vidéo est vide.")

        # ----------------------------------------------------
        # Déterminer le nom original
        # ----------------------------------------------------

        if filename:
            original_name = os.path.basename(filename)
        else:
            original_name = os.path.basename(
                getattr(file, "name", "video.mp4")
            )

        # ----------------------------------------------------
        # Nettoyer le nom du fichier
        # ----------------------------------------------------

        name, extension = os.path.splitext(original_name)

        if not extension:
            extension = ".mp4"

        # Éviter les espaces et caractères problématiques
        safe_name = "".join(
            character if character.isalnum() or character in ("-", "_")
            else "_"
            for character in name
        )

        # ----------------------------------------------------
        # Générer un nom UNIQUE
        # ----------------------------------------------------

        unique_id = uuid.uuid4().hex

        final_filename = (
            f"{safe_name}_{unique_id}{extension.lower()}"
        )

        # ----------------------------------------------------
        # Déterminer le MIME type
        # ----------------------------------------------------

        content_type = getattr(file, "content_type", None)

        if not content_type:
            content_type, _ = mimetypes.guess_type(
                final_filename
            )

        if not content_type:
            content_type = "video/mp4"

        # ----------------------------------------------------
        # Upload Supabase
        # ----------------------------------------------------

        print(
            f"Upload vidéo Supabase: {final_filename}"
        )

        response = (
            supabase
            .storage
            .from_("Exile_videos")
            .upload(
                final_filename,
                file_content,
                {
                    "content-type": content_type,
                    "upsert": "false",
                },
            )
        )

        print(
            f"Vidéo uploadée avec succès: {final_filename}"
        )

        # ----------------------------------------------------
        # Retourner aussi le vrai nom du fichier
        # ----------------------------------------------------

        return {
            "response": response,
            "filename": final_filename,
        }

    except Exception as e:
        print(
            f"Erreur upload vidéo Supabase: {e}"
        )
        raise


# ============================================================
# UPLOAD IMAGE / FICHIER
# ============================================================

def upload_file(file, filename=None):
    """
    Upload une image dans Exile_images.
    """

    try:
        file_content = file.read()

        if not file_content:
            raise ValueError("Le fichier est vide.")

        if filename:
            original_name = os.path.basename(filename)
        else:
            original_name = os.path.basename(
                getattr(file, "name", "image")
            )

        name, extension = os.path.splitext(original_name)

        safe_name = "".join(
            character if character.isalnum() or character in ("-", "_")
            else "_"
            for character in name
        )

        unique_id = uuid.uuid4().hex

        final_filename = (
            f"{safe_name}_{unique_id}{extension.lower()}"
        )

        content_type = getattr(file, "content_type", None)

        if not content_type:
            content_type, _ = mimetypes.guess_type(
                final_filename
            )

        if not content_type:
            content_type = "application/octet-stream"

        response = (
            supabase
            .storage
            .from_("Exile_images")
            .upload(
                final_filename,
                file_content,
                {
                    "content-type": content_type,
                    "upsert": "false",
                },
            )
        )

        print(
            f"Fichier uploadé avec succès: {final_filename}"
        )

        return {
            "response": response,
            "filename": final_filename,
        }

    except Exception as e:
        print(
            f"Erreur upload fichier Supabase: {e}"
        )
        raise


# ============================================================
# URL SIGNÉE VIDÉO
# ============================================================

def get_signed_url(filename, expire=3600):
    """
    Génère une URL signée temporaire pour une vidéo.
    """

    try:
        response = (
            supabase
            .storage
            .from_("Exile_videos")
            .create_signed_url(
                filename,
                expire,
            )
        )

        if isinstance(response, dict):
            return response.get("signed_url")

        return response

    except Exception as e:
        print(
            f"Erreur génération URL vidéo: {e}"
        )
        return None

