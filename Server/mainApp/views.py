import os
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.text import get_valid_filename
from .forms import UploadFileForm

#Сохраняет загруженный файл по указанному пути.
def save_uploaded_file(file, directory):
    os.makedirs(directory, exist_ok=True)
    valid_name = get_valid_filename(file.name)
    save_path = os.path.join(directory, valid_name)
    with open(save_path, "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)
    return save_path

def index(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"success": False, "error": "Нет файла"})
        
        if file.size > 2 * 1024 * 1024 * 1024: # > 2G
            return JsonResponse({"success": False, "error": "Размер файла превышает 2 Гб"})
        
        allowed_formats = [".mkv", ".avi", ".mp4", ".mov"]
        file_ext = os.path.splitext(file.name)[1].lower()
        if file_ext not in allowed_formats:
            return JsonResponse({"success": False, "error": "Недопустимый формат файла"})
        
        try:
            save_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
            save_path = save_uploaded_file(file, save_dir)
        except Exception as e:
            return JsonResponse({"success": False, "error": f"Ошибка сохранения файла: {str(e)}"})

        file_url = f"{settings.MEDIA_URL}uploads/{os.path.basename(save_path)}"
        return JsonResponse({"success": True, "file_url": file_url})
    else:
        form = UploadFileForm()

    return render(request, "mainApp/index.html", {"form": form})
