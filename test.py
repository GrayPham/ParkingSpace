import joblib
import cv2

# Đọc lại mô hình SVM đã lưu
loaded_svm_model = joblib.load('svm_model2.pkl')

# Đọc ảnh mới
new_image_path = 'check\\1.png'  # Thay đổi đường dẫn tới ảnh mới của bạn
new_image = cv2.imread(new_image_path)
print(type(new_image))
# Xử lý ảnh mới (nếu cần)
# new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)  # Chuyển đổi sang ảnh xám (nếu mô hình yêu cầu)
new_image = cv2.resize(new_image, (15, 15))  # Resize ảnh (nếu cần)

# Chuyển đổi ảnh thành mảng NumPy (cần phù hợp với định dạng mô hình đã huấn luyện)
new_data = new_image.reshape(1, -1)

# Dự đoán lớp của ảnh mới
prediction = loaded_svm_model.predict(new_data)

# In ra dự đoán
print("Predicted class:", prediction[0])
