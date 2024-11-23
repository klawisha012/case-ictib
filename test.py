from ultralytics import YOLO
import cv2
import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip

# Р¤СѓРЅРєС†РёСЏ РґР»СЏ Р±Р»СЋСЂР° РѕР±СЉРµРєС‚РѕРІ
def blur_objects(frame, boxes, reduction_factor=0.05):
    for box in boxes:
        x1, y1, x2, y2 = map(int, box)  # РљРѕРѕСЂРґРёРЅР°С‚С‹ Р±РѕРєСЃР°
        # Р’С‹С‡РёСЃР»СЏРµРј С€РёСЂРёРЅСѓ Рё РІС‹СЃРѕС‚Сѓ Р±РѕРєСЃР°
        box_width = x2 - x1
        box_height = y2 - y1

        # РЈРјРµРЅСЊС€Р°РµРј СЂР°Р·РјРµСЂС‹ Р±РѕРєСЃР°
        x1 += int(box_width * reduction_factor)
        y1 += int(box_height * reduction_factor)
        x2 -= int(box_width * reduction_factor)
        y2 -= int(box_height * reduction_factor)

        # РЈР±РµРґРёРјСЃСЏ, С‡С‚Рѕ РєРѕРѕСЂРґРёРЅР°С‚С‹ РЅРµ РІС‹С…РѕРґСЏС‚ Р·Р° РіСЂР°РЅРёС†С‹ РєР°РґСЂР°
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(frame.shape[1], x2), min(frame.shape[0], y2)

        # РР·РІР»РµС‡РµРЅРёРµ ROI Рё РїСЂРёРјРµРЅРµРЅРёРµ Р±Р»СЋСЂР°
        roi = frame[y1:y2, x1:x2]
        blurred = cv2.GaussianBlur(roi, (99, 99), 0)
        frame[y1:y2, x1:x2] = blurred
    return frame

# РћР±СЂР°Р±РѕС‚РєР° РІРёРґРµРѕ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј YOLOv8
def process_video_yolo8(video_path, output_path):
    model = YOLO("yolov8n-face-lindevs.pt")  # РЈР±РµРґРёС‚РµСЃСЊ, С‡С‚Рѕ РёСЃРїРѕР»СЊР·СѓРµРјР°СЏ РјРѕРґРµР»СЊ РѕР±СѓС‡РµРЅР° РґР»СЏ РґРµС‚РµРєС†РёРё Р»РёС†
    cap = cv2.VideoCapture(video_path)

    # РџСЂРѕРІРµСЂРєР° РѕС‚РєСЂС‹С‚РёСЏ РІРёРґРµРѕ
    if not cap.isOpened():
        print("РћС€РёР±РєР°: РќРµРІРѕР·РјРѕР¶РЅРѕ РѕС‚РєСЂС‹С‚СЊ РІРёРґРµРѕ.")
        return

    # РџРѕР»СѓС‡РµРЅРёРµ РїР°СЂР°РјРµС‚СЂРѕРІ РІРёРґРµРѕ
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps == 0 or frame_width == 0 or frame_height == 0:
        print("РћС€РёР±РєР°: РќРµРІРµСЂРЅС‹Рµ РїР°СЂР°РјРµС‚СЂС‹ РІС…РѕРґРЅРѕРіРѕ РІРёРґРµРѕ.")
        cap.release()
        return

    print(f"РџР°СЂР°РјРµС‚СЂС‹ РІРёРґРµРѕ: {frame_width}x{frame_height}, FPS: {fps}, РљР°РґСЂС‹: {total_frames}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # РљРѕРґРµРє РґР»СЏ Р·Р°РїРёСЃРё РІРёРґРµРѕ
    temp_video_path = "temp_output.mp4"  # Р’СЂРµРјРµРЅРЅРѕРµ РІРёРґРµРѕ РґР»СЏ РїРѕСЃР»РµРґСѓСЋС‰РµРіРѕ РґРѕР±Р°РІР»РµРЅРёСЏ Р·РІСѓРєР°
    out = cv2.VideoWriter(temp_video_path, fourcc, fps, (frame_width, frame_height))

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Р’СЃРµ РєР°РґСЂС‹ РѕР±СЂР°Р±РѕС‚Р°РЅС‹.")
            break

        # Р”РµС‚РµРєС‚РёСЂРѕРІР°РЅРёРµ РѕР±СЉРµРєС‚РѕРІ РЅР° С‚РµРєСѓС‰РµРј РєР°РґСЂРµ
        results = model(frame)  # YOLOv8 Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё РІРѕР·РІСЂР°С‰Р°РµС‚ СЂРµР·СѓР»СЊС‚Р°С‚С‹
        detections = results[0].boxes.data.cpu().numpy()  # РР·РІР»РµС‡РµРЅРёРµ Р±РѕРєСЃРѕРІ Рё РїРµСЂРµРІРѕРґ РІ numpy
        boxes = []
        for detection in detections:
            # Р¤РёР»СЊС‚СЂСѓРµРј С‚РѕР»СЊРєРѕ Р»РёС†Р° (РїСЂРµРґРїРѕР»Р°РіР°СЏ, С‡С‚Рѕ РєР»Р°СЃСЃ Р»РёС†Р° Р·Р°РґР°РЅ РІ РјРѕРґРµР»Рё)
            if int(detection[5]) == 0:  # РљР»Р°СЃСЃ 0 вЂ” Р»РёС†Рѕ (РІ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё РѕС‚ РёСЃРїРѕР»СЊР·СѓРµРјРѕР№ РјРѕРґРµР»Рё)
                boxes.append(detection[:4])  # РљРѕРѕСЂРґРёРЅР°С‚С‹ [x1, y1, x2, y2]

        # РџСЂРёРјРµРЅРµРЅРёРµ Р±Р»СЋСЂР° РЅР° РѕР±РЅР°СЂСѓР¶РµРЅРЅС‹С… Р»РёС†Р°С…
        result_frame = blur_objects(frame, boxes)

        # Р—Р°РїРёСЃСЊ РєР°РґСЂР° РІ РІС‹С…РѕРґРЅРѕРµ РІРёРґРµРѕ
        out.write(result_frame)

        frame_count += 1
        print(f"РћР±СЂР°Р±РѕС‚Р°РЅРѕ РєР°РґСЂРѕРІ: {frame_count}/{total_frames}")

        # РћС‚РѕР±СЂР°Р¶РµРЅРёРµ С‚РµРєСѓС‰РµРіРѕ РєР°РґСЂР° (РґР»СЏ С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏ)
        cv2.imshow("Processing Video", result_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Р”РѕР±Р°РІР»РµРЅРёРµ Р·РІСѓРєР° РІ С„РёРЅР°Р»СЊРЅРѕРµ РІРёРґРµРѕ
    add_audio_to_video(video_path, temp_video_path, output_path)
    print(f"РћР±СЂР°Р±РѕС‚РєР° РІРёРґРµРѕ Р·Р°РІРµСЂС€РµРЅР°. РЎРѕС…СЂР°РЅРµРЅРѕ РІ {output_path}.")

# Р”РѕР±Р°РІР»РµРЅРёРµ Р·РІСѓРєР° РІ РѕР±СЂР°Р±РѕС‚Р°РЅРЅРѕРµ РІРёРґРµРѕ
def add_audio_to_video(input_video, temp_video, output_video):
    original_video = VideoFileClip(input_video)
    processed_video = VideoFileClip(temp_video)

    # РџСЂРѕРІРµСЂРєР° РЅР°Р»РёС‡РёСЏ Р·РІСѓРєР°
    if original_video.audio is None:
        print("РџСЂРµРґСѓРїСЂРµР¶РґРµРЅРёРµ: РђСѓРґРёРѕ РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚ РІ РёСЃС…РѕРґРЅРѕРј РІРёРґРµРѕ.")
        processed_video.write_videofile(output_video, codec="libx264")
    else:
        # Р”РѕР±Р°РІР»РµРЅРёРµ Р·РІСѓРєР° Рє РѕР±СЂР°Р±РѕС‚Р°РЅРЅРѕРјСѓ РІРёРґРµРѕ
        final_video = processed_video.with_audio(original_video.audio)
        final_video.write_videofile(output_video, codec="libx264", audio_codec="aac")

    # РћС‡РёСЃС‚РєР° СЂРµСЃСѓСЂСЃРѕРІ
    original_video.close()
    processed_video.close()

# РћР±СЂР°Р±РѕС‚РєР° РІРёРґРµРѕ
process_video_yolo8("Хакатон/human_faces_1.mp4", "output_blurred_with_audio.mp4")