import cv2

def extract_first_frame(video_path, image_name):
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    if success:
        cv2.imwrite(f"{image_name}.png", image)
        print("First frame extracted and saved as PNG.")
    else:
        print("Failed to extract the first frame.")

# Example usage
extract_first_frame("data//Khare_testvideo_03.mp4", "image_base_Khare_testvideo_03")
