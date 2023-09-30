import sys
from PyQt5.QtCore import Qt, QUrl  # Thêm QUrl
from PyQt5.QtGui import QPalette
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt5.QtMultimediaWidgets import QVideoWidget

class VideoPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Video Player")
        self.setGeometry(0, 0, 1920, 1080)  # Kích thước toàn màn hình

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        # Nút để chọn và hiển thị video
        self.video_button = QPushButton("Chọn Video", self)
        self.video_button.clicked.connect(self.load_and_play_video)
        layout.addWidget(self.video_button)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)
        layout.addWidget(self.video_widget)
        self.video_widget.hide()

    def load_and_play_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        video_file, _ = QFileDialog.getOpenFileName(self, "Chọn Video", "", "Video Files (*.mp4 *.avi *.mov *.mkv *.wmv);;All Files (*)", options=options)

        if video_file:
            self.video_widget.show()
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_file)))
            self.media_player.play()

def main():
    app = QApplication(sys.argv)
    window = VideoPlayerApp()
    window.showFullScreen()  # Hiển thị ứng dụng toàn màn hình
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
