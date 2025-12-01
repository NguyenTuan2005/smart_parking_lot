import torch
import cv2
import time
from modelAI.function import utils_rotate as utils_rotate
from modelAI.function import helper as helper

# --- Load YOLOv5 models ---
yolo_LP_detect = torch.hub.load('ultralytics/yolov5', 'custom', path='LP_detector_nano_61.pt', force_reload=True)
yolo_license_plate = torch.hub.load('ultralytics/yolov5', 'custom', path='LP_ocr_nano_62.pt', force_reload=True)
yolo_license_plate.conf = 0.6

# --- Mở video file ---
video_path = "D:/demoAI-1-001/demoAI/crop/xesang2.mp4"  # đổi thành đường dẫn video của bạn
vid = cv2.VideoCapture(video_path)
if not vid.isOpened():
    print(f"Không thể mở video {video_path}")
    exit()

prev_frame_time = 0

while True:
    ret, frame = vid.read()
    if not ret:
        break  # kết thúc video

    # --- Dò biển số ---
    results = yolo_LP_detect(frame)
    list_read_plates = set()

    for det in results.xyxy[0]:  # YOLOv5 trả về tensor [x1, y1, x2, y2, conf, cls]
        x1, y1, x2, y2, conf, cls = det
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

        # Cắt vùng biển số
        crop_img = frame[y1:y2, x1:x2]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,255), 2)

        # --- OCR đọc biển số ---
        lp = ""
        for cc in range(0, 2):
            for ct in range(0, 2):
                lp = helper.read_plate(yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
                if lp != "unknown":
                    list_read_plates.add(lp)
                    cv2.putText(frame, lp, (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                    break
            if lp != "unknown":
                break

    # --- Hiển thị FPS ---
    new_frame_time = time.time()
    fps = int(1 / (new_frame_time - prev_frame_time + 1e-6))
    prev_frame_time = new_frame_time
    cv2.putText(frame, f"FPS: {fps}", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)

    # --- Hiển thị video ---
    cv2.imshow('Video License Plate Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
