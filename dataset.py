import cv2
import numpy as np
import os
from util.util import get_parking_spots_bboxes
mask_data_path = './data/baixe2.png'
video_path = './data/parking1.mp4'
mask = cv2.imread(mask_data_path, 0)
cap = cv2.VideoCapture(video_path)



# Tìm các đối tượng riêng biệt trong kết quả
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
#spots = get_parking_spots_bboxes(connected_components)

# Tạo thư mục để lưu các đối tượng
output_folder = "dataset"
os.makedirs(output_folder, exist_ok=True)
num_image = 1
while True:
    ret, frame = cap.read()
    if not ret:
        print("Video kết thúc")
        break
    # Lặp qua từng contour và lưu các đối tượng vào các tệp riêng lẻ
    for idx, contour in enumerate(contours):
        # Tạo mặt nạ con dựa trên contour của đối tượng
        mask_roi = np.zeros_like(mask)
        cv2.drawContours(mask_roi, [contour], 0, 255, -1)
        x, y, w, h = cv2.boundingRect(contour)


        # Sử dụng phép toán bitwise để cắt ảnh gốc dựa trên mặt nạ con
        result = cv2.bitwise_and(frame, frame, mask=mask_roi)
        # Lưu đối tượng vào tệp riêng lẻ
        object_filename = os.path.join(output_folder, f"object_{num_image}.png")
        result_cropped = result[y:y+h, x:x+w]
        cv2.imwrite(object_filename, result_cropped)
        num_image = num_image  +1 
# Hiển thị số lượng đối tượng đã lưu
print(f"Số lượng đối tượng đã lưu: {len(contours)}")
