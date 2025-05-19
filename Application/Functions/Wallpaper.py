import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import win32gui
import win32con
import win32api

class VideoWallpaper(QMainWindow):
    def __init__(self, video_path):
        super().__init__()

        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        self.setWindowTitle("Video Wallpaper")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)

        self.video_widget = QVideoWidget()
        self.setCentralWidget(self.video_widget)

        self.media_player = QMediaPlayer(self)
        self.media_player.setVideoOutput(self.video_widget)

        video_url = QUrl.fromLocalFile(os.path.abspath(video_path))
        self.media_player.setMedia(QMediaContent(video_url))
        self.media_player.setVolume(0)

        self.media_player.mediaStatusChanged.connect(self.handle_media_status)
        self.media_player.error.connect(self.handle_error)

        self.showFullScreen()

        success = self.set_as_wallpaper()
        if success:
            self.media_player.play()
        else:
            print("Failed to set as wallpaper, exiting...")
            self.close()
            return

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_visibility)
        self.timer.start(1000)

    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()
        elif status == QMediaPlayer.LoadedMedia:
            print("Media loaded successfully")

    def handle_error(self, error):
        if error != QMediaPlayer.NoError:
            print(f"Media player error: {error} - {self.media_player.errorString()}")

    def set_as_wallpaper(self):
        try:
            progman = win32gui.FindWindow("Progman", None)
            if not progman:
                print("Could not find Progman window")
                return False

            win32gui.SendMessageTimeout(
                progman,
                0x052C,
                0,
                0,
                win32con.SMTO_NORMAL,
                1000
            )

            def find_worker_w():
                def callback(hwnd, results):
                    shellview = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", None)
                    if shellview:
                        workerw = win32gui.FindWindowEx(0, hwnd, "WorkerW", None)
                        if workerw:
                            results.append(workerw)
                    return True
                results = []
                win32gui.EnumWindows(callback, results)
                return results[0] if results else None

            workerw = find_worker_w()
            if not workerw:
                print("Could not find WorkerW window")
                return False

            hwnd = int(self.winId())
            win32gui.SetParent(hwnd, workerw)

            win32gui.InvalidateRect(workerw, None, True)

            print(f"Successfully set as wallpaper. WorkerW: {workerw}, Our window: {hwnd}")
            return True

        except Exception as e:
            print(f"Error setting as wallpaper: {e}")
            return False

    def check_visibility(self):
        try:
            foreground_hwnd = win32gui.GetForegroundWindow()
            if foreground_hwnd:
                window_placement = win32gui.GetWindowPlacement(foreground_hwnd)
                is_maximized = window_placement[1] == win32con.SW_SHOWMAXIMIZED

                if is_maximized:
                    if self.media_player.state() == QMediaPlayer.PlayingState:
                        self.media_player.pause()
                else:
                    if self.media_player.state() == QMediaPlayer.PausedState:
                        self.media_player.play()
        except Exception as e:
            print(f"Error checking visibility: {e}")

if __name__ == "__main__":
    video_path = "./Videos/Car In Ocean Night.mp4"
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
        print(f"Using video path from argument: {video_path}")
    else:
        print(f"Using default video path: {video_path}")

    app = QApplication(sys.argv)

    try:
        wallpaper = VideoWallpaper(video_path)
        sys.exit(app.exec_())
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
