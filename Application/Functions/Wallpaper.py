<<<<<<< HEAD
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

        self.showFullScreen()

        self.media_player.play()

        self.set_as_wallpaper()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_visibility)
        self.timer.start(1000)

    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()

    def set_as_wallpaper(self):
        progman = win32gui.FindWindow("Progman", None)

        win32gui.SendMessageTimeout(
            progman,
            0x052C,
            0,
            0,
            win32con.SMTO_NORMAL,
            1000
        )

        def find_worker_w():
            def callback(hwnd, result):
                temp = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", None)
                if temp:
                    workerw = win32gui.FindWindowEx(0, hwnd, "WorkerW", None)
                    result.append(workerw)
                return True
            result = []
            win32gui.EnumWindows(callback, result)
            return result[0] if result else None

        workerw = find_worker_w()

        if workerw:
            hwnd = int(self.winId())
            win32gui.SetParent(hwnd, workerw)
        else:
            print("Could not find WorkerW window. Wallpaper setting failed.")

    def check_visibility(self):
        foreground_hwnd = win32gui.GetForegroundWindow()
        if foreground_hwnd:
            window_placement = win32gui.GetWindowPlacement(foreground_hwnd)
            is_maximized = window_placement[1] == win32con.SW_SHOWMAXIMIZED

            if is_maximized:
                if self.media_player.state() == QMediaPlayer.PlayingState:
                    self.media_player.pause()
                print("Wallpaper Status: Hidden (Maximized window detected), Player State: Paused")
            else:
                if self.media_player.state() == QMediaPlayer.PausedState:
                    self.media_player.play()
                print("Wallpaper Status: Visible, Player State: Playing")
        else:
            print("No foreground window detected.")

if __name__ == "__main__":
    video_path = "./Videos/Car In Ocean Night.mp4"
    if len(sys.argv) > 1:
        video_path = sys.argv[1]

    app = QApplication(sys.argv)

    try:
        wallpaper = VideoWallpaper(video_path)
        sys.exit(app.exec_())
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
=======
<<<<<<< HEAD
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

        self.showFullScreen()

        self.media_player.play()

        self.set_as_wallpaper()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_visibility)
        self.timer.start(1000)

    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()

    def set_as_wallpaper(self):
        progman = win32gui.FindWindow("Progman", None)

        win32gui.SendMessageTimeout(
            progman,
            0x052C,
            0,
            0,
            win32con.SMTO_NORMAL,
            1000
        )

        def find_worker_w():
            def callback(hwnd, result):
                temp = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", None)
                if temp:
                    workerw = win32gui.FindWindowEx(0, hwnd, "WorkerW", None)
                    result.append(workerw)
                return True
            result = []
            win32gui.EnumWindows(callback, result)
            return result[0] if result else None

        workerw = find_worker_w()

        if workerw:
            hwnd = int(self.winId())
            win32gui.SetParent(hwnd, workerw)
        else:
            print("Could not find WorkerW window. Wallpaper setting failed.")

    def check_visibility(self):
        foreground_hwnd = win32gui.GetForegroundWindow()
        if foreground_hwnd:
            window_placement = win32gui.GetWindowPlacement(foreground_hwnd)
            is_maximized = window_placement[1] == win32con.SW_SHOWMAXIMIZED

            if is_maximized:
                if self.media_player.state() == QMediaPlayer.PlayingState:
                    self.media_player.pause()
                print("Wallpaper Status: Hidden (Maximized window detected), Player State: Paused")
            else:
                if self.media_player.state() == QMediaPlayer.PausedState:
                    self.media_player.play()
                print("Wallpaper Status: Visible, Player State: Playing")
        else:
            print("No foreground window detected.")

if __name__ == "__main__":
    video_path = "./Videos/Car In Ocean Night.mp4"
    if len(sys.argv) > 1:
        video_path = sys.argv[1]

    app = QApplication(sys.argv)

    try:
        wallpaper = VideoWallpaper(video_path)
        sys.exit(app.exec_())
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
=======
# import sys
# import os
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
# from PyQt5.QtCore import Qt, QUrl, QTimer
# from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
# from PyQt5.QtMultimediaWidgets import QVideoWidget
# import win32gui
# import win32con
# import win32api

# class VideoWallpaper(QMainWindow):
#     def __init__(self, video_path):
#         super().__init__()

#         if not os.path.exists(video_path):
#             raise FileNotFoundError(f"Video file not found: {video_path}")

#         self.setWindowTitle("Video Wallpaper")
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)

#         self.video_widget = QVideoWidget()
#         self.setCentralWidget(self.video_widget)

#         self.media_player = QMediaPlayer(self)
#         self.media_player.setVideoOutput(self.video_widget)

#         video_url = QUrl.fromLocalFile(os.path.abspath(video_path))
#         self.media_player.setMedia(QMediaContent(video_url))
#         self.media_player.setVolume(0)

#         self.media_player.mediaStatusChanged.connect(self.handle_media_status)

#         self.showFullScreen()

#         self.media_player.play()

#         self.set_as_wallpaper()

#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.check_visibility)
#         self.timer.start(1000)

#     def handle_media_status(self, status):
#         if status == QMediaPlayer.EndOfMedia:
#             self.media_player.setPosition(0)
#             self.media_player.play()

#     def set_as_wallpaper(self):
#         progman = win32gui.FindWindow("Progman", None)

#         win32gui.SendMessageTimeout(
#             progman,
#             0x052C,
#             0,
#             0,
#             win32con.SMTO_NORMAL,
#             1000
#         )

#         def find_worker_w():
#             def callback(hwnd, result):
#                 temp = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", None)
#                 if temp:
#                     workerw = win32gui.FindWindowEx(0, hwnd, "WorkerW", None)
#                     result.append(workerw)
#                 return True
#             result = []
#             win32gui.EnumWindows(callback, result)
#             return result[0] if result else None

#         workerw = find_worker_w()

#         if workerw:
#             hwnd = int(self.winId())
#             win32gui.SetParent(hwnd, workerw)
#         else:
#             print("Could not find WorkerW window. Wallpaper setting failed.")

#     def check_visibility(self):
#         foreground_hwnd = win32gui.GetForegroundWindow()
#         if foreground_hwnd:
#             window_placement = win32gui.GetWindowPlacement(foreground_hwnd)
#             is_maximized = window_placement[1] == win32con.SW_SHOWMAXIMIZED

#             if is_maximized:
#                 if self.media_player.state() == QMediaPlayer.PlayingState:
#                     self.media_player.pause()
#                 print("Wallpaper Status: Hidden (Maximized window detected), Player State: Paused")
#             else:
#                 if self.media_player.state() == QMediaPlayer.PausedState:
#                     self.media_player.play()
#                 print("Wallpaper Status: Visible, Player State: Playing")
#         else:
#             print("No foreground window detected.")

# if __name__ == "__main__":
#     video_path = "./Videos/Car In Ocean Night.mp4"
#     if len(sys.argv) > 1:
#         video_path = sys.argv[1]

#     app = QApplication(sys.argv)

#     try:
#         wallpaper = VideoWallpaper(video_path)
#         sys.exit(app.exec_())
#     except FileNotFoundError as e:
#         print(f"Error: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
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

        self.showFullScreen()

        self.media_player.play()

        self.set_as_wallpaper()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_visibility)
        self.timer.start(1000)

    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()

    def set_as_wallpaper(self):
        progman = win32gui.FindWindow("Progman", None)

        win32gui.SendMessageTimeout(
            progman,
            0x052C,
            0,
            0,
            win32con.SMTO_NORMAL,
            1000
        )

        def find_worker_w():
            def callback(hwnd, result):
                temp = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", None)
                if temp:
                    workerw = win32gui.FindWindowEx(0, hwnd, "WorkerW", None)
                    result.append(workerw)
                return True
            result = []
            win32gui.EnumWindows(callback, result)
            return result[0] if result else None

        workerw = find_worker_w()

        if workerw:
            hwnd = int(self.winId())
            win32gui.SetParent(hwnd, workerw)
        else:
            print("Could not find WorkerW window. Wallpaper setting failed.")

    def check_visibility(self):
        foreground_hwnd = win32gui.GetForegroundWindow()
        if foreground_hwnd:
            window_placement = win32gui.GetWindowPlacement(foreground_hwnd)
            is_maximized = window_placement[1] == win32con.SW_SHOWMAXIMIZED

            if is_maximized:
                if self.media_player.state() == QMediaPlayer.PlayingState:
                    self.media_player.pause()
                print("Wallpaper Status: Hidden (Maximized window detected), Player State: Paused")
            else:
                if self.media_player.state() == QMediaPlayer.PausedState:
                    self.media_player.play()
                print("Wallpaper Status: Visible, Player State: Playing")
        else:
            print("No foreground window detected.")

if __name__ == "__main__":
    video_path = "./Videos/Car In Ocean Night.mp4"
    if len(sys.argv) > 1:
        video_path = sys.argv[1]

    app = QApplication(sys.argv)

    try:
        wallpaper = VideoWallpaper(video_path)
        sys.exit(app.exec_())
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
>>>>>>> f0ac188 (Initial commit)
>>>>>>> c6a8d8e (Initial commit)
