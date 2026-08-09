
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.supabase_service import upload_video, get_signed_url

@api_view(["POST"])
def upload_video_view(request):
    file = request.FILES["video"]
    filename = file.name
    upload_video(file, filename)
    signed_url = get_signed_url(filename)
    return Response({"signed_url": signed_url})
