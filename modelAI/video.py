import cv2
import time

from modelAI.lp_inference import LicensePlateRecognizer

# --- Mở video file ---
video_path = "D:/demoAI-1-001/demoAI/crop/xesang2.mp4"  # đổi thành đường dẫn video của bạn
vid = cv2.VideoCapture(video_path)
if not vid.isOpened():
    print(f"Không thể mở video {video_path}")
    exit()

prev_frame_time = 0

# Khởi tạo module AI (load model 1 lần)
lp_recognizer = LicensePlateRecognizer()

while True:
    ret, frame = vid.read()
    if not ret:
        break  # kết thúc video

    # --- Dò & đọc biển số bằng module đóng gói ---
    frame, list_read_plates = lp_recognizer.process_frame(frame)

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
