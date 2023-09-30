import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib
# Đường dẫn đến thư mục chứa dữ liệu ảnh "good" và "bad"
data_dir = "dataset"

# Danh sách các thư mục con tương ứng với các lớp "good" và "bad"
classes = ["0", "1"]

# Khởi tạo danh sách để lưu dữ liệu và nhãn tương ứng
data = []
labels = []

# Đọc và xử lý dữ liệu hình ảnh
for class_idx, class_name in enumerate(classes):
    class_dir = os.path.join(data_dir, class_name)
    for image_file in os.listdir(class_dir):
        image_path = os.path.join(class_dir, image_file)
        image = cv2.imread(image_path)
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Chuyển đổi sang ảnh xám (nếu cần)
        resized_image = cv2.resize(image, (15,15))
        # Resize ảnh thành kích thước cố định (nếu cần)
        # image = cv2.resize(image, (width, height))
        data.append(resized_image)
        labels.append(class_idx)

# Chuyển danh sách dữ liệu và nhãn thành mảng NumPy
data = np.array(data)
labels = np.array(labels)

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Khởi tạo mô hình SVM
svm_model = SVC(kernel='linear')

# Huấn luyện mô hình
svm_model.fit(X_train.reshape(len(X_train), -1), y_train)

# Dự đoán trên tập kiểm tra
y_pred = svm_model.predict(X_test.reshape(len(X_test), -1))

# Đánh giá mô hình
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Lưu mô hình đã huấn luyện (nếu cần)
# import joblib
# joblib.dump(svm_model, 'svm_model.pkl')
joblib.dump(svm_model, 'svm_model2.pkl')