from ultralytics import YOLO
import cv2
import numpy as np

# Функция для блюра объектов
def blur_objects(frame, boxes, reduction_factor=0.05):
    for box in boxes:
        x1, y1, x2, y2 = map(int, box)  # Координаты бокса
        # Вычисляем ширину и высоту бокса
        box_width = x2 - x1
        box_height = y2 - y1

        # Уменьшаем размеры бокса
        x1 += int(box_width * reduction_factor)
        y1 += int(box_height * reduction_factor)
        x2 -= int(box_width * reduction_factor)
        y2 -= int(box_height * reduction_factor)

        # Убедимся, что координаты не выходят за границы кадра
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(frame.shape[1], x2), min(frame.shape[0], y2)

        # Извлечение ROI и применение блюра
        roi = frame[y1:y2, x1:x2]
        blurred = cv2.GaussianBlur(roi, (99, 99), 0)
        frame[y1:y2, x1:x2] = blurred
    return frame

# Обработка видео с веб-камеры с использованием YOLOv8
def process_webcam_yolo8():
    model = YOLO("yolov8n-face-lindevs.pt")  # Убедитесь, что используемая модель обучена для детекции лиц
    cap = cv2.VideoCapture(0)  # Захват видео с веб-камеры (индекс 0 - первая подключённая камера)

    if not cap.isOpened():
        print("Ошибка: Невозможно открыть веб-камеру.")
        return

    print("Начало обработки видео с веб-камеры. Нажмите 'q' для выхода.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка: Не удалось считать кадр с веб-камеры.")
            break

        # Детектирование объектов на текущем кадре
        results = model(frame)  # YOLOv8 автоматически возвращает результаты
        detections = results[0].boxes.data.cpu().numpy()  # Извлечение боксов и перевод в numpy
        boxes = []
        for detection in detections:
            # Фильтруем только лица (предполагая, что класс лица задан в модели)
            if int(detection[5]) == 0:  # Класс 0 — лицо (в зависимости от используемой модели)
                boxes.append(detection[:4])  # Координаты [x1, y1, x2, y2]

        # Применение блюра на обнаруженных лицах
        result_frame = blur_objects(frame, boxes)

        # Отображение текущего кадра
        cv2.imshow("Webcam Blur Faces", result_frame)

        # Нажмите 'q' для выхода из цикла
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Обработка завершена.")

# Запуск обработки веб-камеры
process_webcam_yolo8()
