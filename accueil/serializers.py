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

    class Meta:

        model = Video

        fields = [
            "id",
            "title",
            "description",
            "owner",
            "owner_username",
            "owner_id",
            "file",
            "file_url",
            "cover_url",
            "created_at",
            "is_public",
            "video_available",
        ]

        read_only_fields = [
            "id",
            "owner",
            "owner_username",
            "file_url",
            "cover_url",
            "created_at",
        ]

    def create(self, validated_data):
        owner_id = validated_data.pop('owner_id', None)
        if owner_id:
            validated_data['owner_id'] = owner_id
        return super().create(validated_data)

    # =========================================================
    # VIDEO URL
    # =========================================================

    def get_file_url(self, obj):

        if not obj.file:
            print(f"DEBUG: file_url - obj.file is None for video {obj.id}")
            return None

        try:
            print(f"DEBUG: Generating signed URL for file: {obj.file}")
            result = (
                supabase
                .storage
                .from_("Exile_videos")
                .create_signed_url(
                    obj.file,
                    3600,
                )
            )
            print(f"DEBUG: Supabase result: {result}")

            if isinstance(result, dict):

                # Supabase peut retourner différentes clés pour l'URL signée
                signed_url = result.get("signed_url") or result.get("signedUrl") or result.get("signedURL")
                print(f"DEBUG: Extracted signed_url: {signed_url}")
                return signed_url

            return result

        except Exception as e:
            print(f"DEBUG: Error generating file_url for video {obj.id}: {e}")
            # Fallback: retourner l'URL publique directe si le fichier n'existe pas dans Supabase
            # ou None si vraiment impossible
            return None

    # =========================================================
    # COVER URL
    # =========================================================

    def get_cover_url(self, obj):

        if not obj.cover:
            print(f"DEBUG: cover_url - obj.cover is None for video {obj.id}")
            return None

        try:
            print(f"DEBUG: Generating signed URL for cover: {obj.cover}")
            result = (
                supabase
                .storage
                .from_("Exile_images")
                .create_signed_url(
                    obj.cover,
                    3600,
                )
            )
            print(f"DEBUG: Supabase cover result: {result}")

            if isinstance(result, dict):
                signed_url = result.get("signed_url") or result.get("signedUrl") or result.get("signedURL")
                print(f"DEBUG: Extracted cover signed_url: {signed_url}")
                return signed_url

            return result

        except Exception as e:
            print(f"DEBUG: Error generating cover_url for video {obj.id}: {e}")
            import traceback
            traceback.print_exc()
            return None

    # =========================================================
    # VIDEO AVAILABLE
    # =========================================================

    def get_video_available(self, obj):
        """Indique si la vidéo est disponible (fichier existe dans Supabase)"""
        return bool(obj.file)
