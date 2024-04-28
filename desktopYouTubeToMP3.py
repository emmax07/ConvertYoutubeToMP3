import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from pytube import Playlist
from moviepy.editor import VideoFileClip

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube Playlist Downloader')
        layout = QVBoxLayout()

        self.playlist_url_label = QLabel('Enter the URL of the YouTube playlist:')
        self.playlist_url_input = QLineEdit()
        self.save_directory_label = QLabel('Enter the directory where you want to save the downloaded files:')
        self.save_directory_input = QLineEdit()
        self.resolution_label = QLabel('Enter the desired resolution (e.g., 720p, 480p):')
        self.resolution_input = QLineEdit()
        self.download_button = QPushButton('Download Playlist')

        layout.addWidget(self.playlist_url_label)
        layout.addWidget(self.playlist_url_input)
        layout.addWidget(self.save_directory_label)
        layout.addWidget(self.save_directory_input)
        layout.addWidget(self.resolution_label)
        layout.addWidget(self.resolution_input)
        layout.addWidget(self.download_button)

        self.download_button.clicked.connect(self.download_playlist)

        self.setLayout(layout)

    def download_playlist(self):
        playlist_url = self.playlist_url_input.text()
        save_directory = self.save_directory_input.text()
        resolution = self.resolution_input.text()

        if not playlist_url or not save_directory:
            QMessageBox.warning(self, 'Warning', 'Please enter both playlist URL and save directory.')
            return

        try:
            playlist = Playlist(playlist_url)
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            
            for video in playlist.videos:
                try:
                    stream = video.streams.filter(only_audio=True, progressive=True, resolution=resolution).first()
                    if not stream:
                        stream = video.streams.filter(only_audio=True, progressive=True).order_by('resolution').desc().first()
                    stream.download(output_path=save_directory, filename=f"{video.title}.mp3")
                except Exception as e:
                    print(f"Error downloading {video.title}: {e}")
                    continue
            
            QMessageBox.information(self, 'Information', 'Playlist downloaded successfully!')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error downloading playlist: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec_())
