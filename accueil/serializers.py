import mimetypes
import os

from rest_framework import serializers

from .models import Video
from API.services.supabase_service import supabase


class VideoSerializer(serializers.ModelSerializer):

    # ---------------------------------------------------------
    # Propriétaire - Séparation lecture/écriture
    # ---------------------------------------------------------

    owner = serializers.PrimaryKeyRelatedField(
        read_only=True  # Lecture seule
    )

    owner_username = serializers.CharField(
        source="owner.username",
        read_only=True,
    )

    owner_full_name = serializers.SerializerMethodField()

    owner_avatar = serializers.SerializerMethodField()

    # Champ interne pour l'écriture de l'ID
    owner_id = serializers.IntegerField(write_only=True, required=False)

    # ---------------------------------------------------------
    # URL vidéo
    # ---------------------------------------------------------

    file_url = serializers.SerializerMethodField()

    # ---------------------------------------------------------
    # URL couverture
    # ---------------------------------------------------------

    cover_url = serializers.SerializerMethodField()

    # ---------------------------------------------------------
    # Disponibilité vidéo
    # ---------------------------------------------------------

    video_available = serializers.SerializerMethodField()

    # ---------------------------------------------------------
    # Type MIME déduit de l'extension du fichier stocké
    # ---------------------------------------------------------

    mime_type = serializers.SerializerMethodField()

    class Meta:

        model = Video

        fields = [
            "id",
            "title",
            "description",
            "owner",
            "owner_username",
            "owner_full_name",
            "owner_avatar",
            "owner_id",
            "file",
            "file_url",
            "cover",
            "cover_url",
            "mime_type",
            "created_at",
            "is_public",
            "views",
            "video_available",
        ]

        read_only_fields = [
            "id",
            "owner",
            "owner_username",
            "owner_full_name",
            "owner_avatar",
            "file_url",
            "cover_url",
            "mime_type",
            "created_at",
            "views",
        ]

    def create(self, validated_data):
        owner_id = validated_data.pop('owner_id', None)
        if owner_id:
            validated_data['owner_id'] = owner_id
        return super().create(validated_data)

    # =========================================================
    # VIDEO URL
    # =========================================================

    def get_owner_full_name(self, obj):
        """Nom réel de l'auteur, avec repli sur le username."""
        owner = obj.owner
        if not owner:
            return None
        return (
            getattr(owner, "full_name", "")
            or owner.get_full_name()
            or owner.username
        )

    def get_owner_avatar(self, obj):
        """URL signée de la photo de profil de l'auteur (None si absente)."""
        owner = obj.owner
        profil = getattr(owner, "profil", None)
        if profil is None:
            from profil.models import Profil
            profil = Profil.objects.filter(user=owner).first()

        if not profil or not profil.photo:
            return None

        try:
            result = (
                supabase
                .storage
                .from_("Exile_images")
                .create_signed_url(profil.photo, 3600)
            )
            if isinstance(result, dict):
                return (
                    result.get("signed_url")
                    or result.get("signedUrl")
                    or result.get("signedURL")
                )
            return result
        except Exception:
            return None

    def get_mime_type(self, obj):
        """Type MIME déduit de l'extension, utile au lecteur vidéo."""
        if not obj.file:
            return None
        extension = os.path.splitext(obj.file)[1].lower()
        if extension == ".mov":
            # Les navigateurs refusent video/quicktime alors que le conteneur
            # (H.264/AAC) est lisible: on annonce video/mp4.
            return "video/mp4"
        guessed, _ = mimetypes.guess_type(obj.file)
        return guessed or "video/mp4"

    def get_file_url(self, obj):

        if not obj.file:
            return None

        try:
            result = (
                supabase
                .storage
                .from_("Exile_videos")
                .create_signed_url(
                    obj.file,
                    3600,
                )
            )

            if isinstance(result, dict):

                # Supabase peut retourner différentes clés pour l'URL signée
                return (
                    result.get("signed_url")
                    or result.get("signedUrl")
                    or result.get("signedURL")
                )

            return result

        except Exception as e:
            print(f"Erreur génération file_url pour la vidéo {obj.id}: {e}")
            # Fallback: retourner l'URL publique directe si le fichier n'existe pas dans Supabase
            # ou None si vraiment impossible
            return None

    # =========================================================
    # COVER URL
    # =========================================================

    def get_cover_url(self, obj):

        if not obj.cover:
            return None

        try:
            result = (
                supabase
                .storage
                .from_("Exile_images")
                .create_signed_url(
                    obj.cover,
                    3600,
                )
            )

            if isinstance(result, dict):
                return (
                    result.get("signed_url")
                    or result.get("signedUrl")
                    or result.get("signedURL")
                )

            return result

        except Exception as e:
            print(f"Erreur génération cover_url pour la vidéo {obj.id}: {e}")
            return None

    # =========================================================
    # VIDEO AVAILABLE
    # =========================================================

    def get_video_available(self, obj):
        """Indique si la vidéo est disponible (fichier existe dans Supabase)"""
        return bool(obj.file)
