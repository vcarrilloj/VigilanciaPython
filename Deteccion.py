import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions
import cv2
import os

# Especificar la configuración del detector de objetos
options = vision.ObjectDetectorOptions(
    base_options=BaseOptions(model_asset_path="Modelo/efficientdet_lite0.tflite"),
    max_results=5,
    score_threshold=0.2,
    running_mode=vision.RunningMode.VIDEO)
detector = vision.ObjectDetector.create_from_options(options)

# Leer el video de entrada
input_path = "Capturas/ejemplo camara.mp4"
cap = cv2.VideoCapture(input_path)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

# Crear el objeto para guardar el video
output_path = "Capturas/video_procesado.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # o usa 'XVID' para AVI
video_writer = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

for frame_index in range(int(frame_count)):
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

    frame_timestamp_ms = int(1000 * frame_index / fps)

    detection_result = detector.detect_for_video(frame_rgb, frame_timestamp_ms)
    for detection in detection_result.detections:
        category = detection.categories[0]

        if (category.score * 100) >= 10:
            bbox = detection.bounding_box
            bbox_x, bbox_y, bbox_w, bbox_h = bbox.origin_x, bbox.origin_y, bbox.width, bbox.height
            score = (category.score * 100) + 30
            category_name = category.category_name
            cv2.rectangle(frame, (bbox_x, bbox_y), (bbox_x + bbox_w, bbox_y - 30), (100, 255, 0), -1)
            cv2.rectangle(frame, (bbox_x, bbox_y), (bbox_x + bbox_w, bbox_y + bbox_h), (100, 255, 0), 2)
            cv2.putText(frame, f"{category_name} {score:.2f}%", (bbox_x + 5, bbox_y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow('Video', frame)
    video_writer.write(frame)  # Guardar el frame en el video

    if cv2.waitKey(1) & 0xFF == 27:
        break

# Liberar recursos
cap.release()
video_writer.release()
cv2.destroyAllWindows()
