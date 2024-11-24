from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.utils.text import get_valid_filename
import os, subprocess
from django.views.decorators.csrf import csrf_exempt

processed_files_to_delete = set()

@csrf_exempt
def index(request):
    global processed_files_to_delete

    if request.method == 'POST':
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"success": False, "error": "Файл не загружен"})
        
        if file.size > settings.MAX_UPLOAD_SIZE:
            return JsonResponse({"success": False, "error": f"Размер файла превышает допустимый: {settings.MAX_UPLOAD_SIZE_MESS}"})
        
        allowed_ext = [".mp4", ".avi", ".mkv", ".mov"]
        file_ext = os.path.splitext(file.name)[1].lower()
        if file_ext not in allowed_ext:
            return JsonResponse({"success": False, "error": f"Недопустимое расширений файла. Допустимые: {allowed_ext}"})
        
        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        valid_filename = get_valid_filename(file.name)
        input_file_path = os.path.join(upload_dir, valid_filename)
        with open(input_file_path, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        output_dir = os.path.join(settings.MEDIA_ROOT, "blured")
        os.makedirs(output_dir, exist_ok=True)
        output_file_path = os.path.join(output_dir, f"blured_{valid_filename}")

        if not os.path.exists(settings.PATH_TO_APP):
            return JsonResponse({"success": False, "error": f"Приложение не найдено: {settings.PATH_TO_APP}"}, status=500)


        command = [settings.PATH_TO_APP, input_file_path, output_file_path]
        try:
            result = subprocess.run(command, capture_output = True, text = True)
            exit_code = result.returncode
        except subprocess.CalledProcessError as e:
            # Обработка ошибок выполнения команды
            error_message = e.stderr.strip() if e.stderr else "Ошибка обработки файла."
            return JsonResponse({"success": False, "error": error_message}, status=500)
        except Exception as e:
            # Обработка общих ошибок
            return JsonResponse({"success": False, "error": f"Не удалось запустить процесс: {str(e)}"}, status=500)
        
        processed_files_to_delete.add(output_file_path)
        processed_files_to_delete.add(input_file_path)
        processed_file_url = f"{settings.MEDIA_URL}blured/blured_{valid_filename}"
        return JsonResponse({"success": True, "file_url": processed_file_url, "file_name": file.name})
    
    else:
        for file_path in processed_files_to_delete:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Не удалось удалить файл {file_path}: {e}")
        processed_files_to_delete.clear()

        return render(request, "mainApp/index.html")


