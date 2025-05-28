#---------< Libs >----------
import json, os, requests, re , logging
from contextlib import closing
import threading
import time
import ctypes
import subprocess
import winreg
import sys
import shutil
#---------< Paths >---------
DataPath = os.path.join(".","BackgroundsData","BackgroundsData.json")
OriginalWallpaperPath = os.path.join(".","BackgroundsData","OriginalWallpaperBackup.jpg")
UserDataPath = os.path.join(".","BackgroundsData","UserData.json")
WallpaperProcess = None
#---------< Classes >---------
class UserDataManagement:
    def __init__(self):
        self.UserDataPath = UserDataPath
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        if not os.path.exists(self.UserDataPath):
            with open(self.UserDataPath, 'w', encoding='utf-8') as file:
                JsonObject = {
                    "LastWallpaper": None,
                    "WallpaperStatus": False
                }
                json.dump(JsonObject, file, indent=3)

        with open(self.UserDataPath, 'r', encoding='utf-8') as file:
            self.UserData = json.load(file)

    def GetWallpaperStatus(self):
        return self.UserData

    def SetWallpaperStatus(self, WallpaperStatus: bool):
        self.UserData["WallpaperStatus"] = WallpaperStatus

        with open(self.UserDataPath, 'w', encoding='utf-8') as file:
            json.dump(self.UserData, file, indent=3)

    def SetLastWallpaper(self, LastWallpaper: str):
        self.UserData["LastWallpaper"] = LastWallpaper

        with open(self.UserDataPath, 'w', encoding='utf-8') as file:
            json.dump(self.UserData, file, indent=3)

#---------< Functions >---------
def GetMainData():
    with open(DataPath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def GetDataOfWallpaper(SearchType: str, SearchValue: str = None):
    with open(DataPath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    backgrounds = data.get("Backgrounds", [])
    if SearchType == "ByName":
        if not SearchValue:
            raise ValueError("SearchValue is required for ByName search.")
        result = [bg for bg in backgrounds if bg["Name"].lower() == SearchValue.lower()]
        return result[0] if result else None
    elif SearchType == "ByCategory":
        if not SearchValue:
            raise ValueError("SearchValue is required for ByCategory search.")
        result = [bg for bg in backgrounds if SearchValue.lower() in bg["Categories"].lower()]
        return result
    else:
        raise TypeError(f"Type {SearchType} Not Defined!")

def GetCoversPath(WithFolder: bool = True):
    Index = 0
    CoversFolderPath = os.path.join(".","static","Images","Covers")
    CoversPath = os.listdir(CoversFolderPath)
    if WithFolder:
        for Item in CoversPath:
            PathStructure = "Images/Covers/"
            Item = PathStructure + Item
            CoversPath[Index] = Item
            Index += 1
    return CoversPath

def GetBackgrounds():
    with open(DataPath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def DownloadBackground(BackgroundName: str, progress_tracker=None):
    filename = f"{BackgroundName}.mp4"
    Link = f"https://raw.githubusercontent.com/YashaNajafi/AniWall/refs/heads/main/Wallpapers/{filename}"
    current_file = os.path.abspath(__file__)
    base_dir = os.path.dirname(os.path.dirname(current_file))
    videos_dir = os.path.join(base_dir, "Videos")
    os.makedirs(videos_dir, exist_ok=True)
    file_path = os.path.join(videos_dir, filename)
    try:
        with open(file_path, 'wb') as _:
            pass
        session = requests.Session()
        try:
            head_response = session.head(Link)
            head_response.raise_for_status()
            total_size = int(head_response.headers.get('content-length', 0))
            if progress_tracker and BackgroundName in progress_tracker:
                progress_tracker[BackgroundName]['total_size'] = total_size
            try:
                with open(DataPath, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                for bg in data.get("Backgrounds", []):
                    if bg["Name"] == BackgroundName:
                        bg["FileSize"] = total_size
                        break
                with open(DataPath, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4)
            except Exception as e:
                print(f"Failed to update file size in background data: {e}")
        except Exception as e:
            print(f"Failed to get file size with HEAD request: {e}")
            total_size = 0
        with closing(session.get(Link, stream=True)) as response:
            response.raise_for_status()
            if total_size == 0:
                total_size = int(response.headers.get('content-length', 0))
                if progress_tracker and BackgroundName in progress_tracker:
                    progress_tracker[BackgroundName]['total_size'] = total_size
            chunk_size = 4096
            current_size = 0
            last_update_time = time.time()
            update_interval = 0.05
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        file.write(chunk)
                        current_size += len(chunk)
                        current_time = time.time()
                        if (current_time - last_update_time) > update_interval:
                            if progress_tracker and BackgroundName in progress_tracker:
                                progress_tracker[BackgroundName]['current_size'] = current_size
                                if total_size > 0:
                                    progress = (current_size / total_size) * 100
                                    progress_tracker[BackgroundName]['progress'] = progress
                            last_update_time = current_time
        if progress_tracker and BackgroundName in progress_tracker:
            progress_tracker[BackgroundName]['current_size'] = total_size
            progress_tracker[BackgroundName]['progress'] = 100
            progress_tracker[BackgroundName]['is_complete'] = True
        print("Download completed successfully.")
        return True
    except Exception as e:
        print(f"File Download Error: {e}")
        if progress_tracker and BackgroundName in progress_tracker:
            progress_tracker[BackgroundName]['error'] = str(e)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        return False

def CheckWallpaperExist(BackgroundName: str) -> bool:
    BackgroundName += ".mp4"
    current_file = os.path.abspath(__file__)
    base_dir = os.path.dirname(os.path.dirname(current_file))
    videos_dir = os.path.join(base_dir, "Videos")
    file_path = os.path.join(videos_dir, BackgroundName)
    return os.path.isfile(file_path)

def GetCategory(CategorySTR: str):
    Match = re.search(r'\(([^()]*)\)', CategorySTR)
    if Match:
        return Match.group(1).strip()
    return CategorySTR.strip()

def GetMainCategory(CategorySTR: str):
    Match = re.search(r'^([^(]+)', CategorySTR)
    if Match:
        return Match.group(1).strip()
    return CategorySTR.strip()

def BackupOriginalWallpaper():
    try:
        data_dir = os.path.dirname(OriginalWallpaperPath)
        os.makedirs(data_dir, exist_ok=True)
        wallpaper_path = GetCurrentWallpaperPath()
        if wallpaper_path and os.path.exists(wallpaper_path):
            shutil.copy2(wallpaper_path, OriginalWallpaperPath)
            print(f"Original wallpaper backed up successfully from {wallpaper_path} to {OriginalWallpaperPath}")
            return True
        else:
            print(f"Could not find current wallpaper at: {wallpaper_path}")
            return False
    except Exception as e:
        print(f"Error backing up original wallpaper: {e}")
        return False

def GetCurrentWallpaperPath():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop")
        wallpaper_path = winreg.QueryValueEx(key, 'WallPaper')[0]
        winreg.CloseKey(key)
        return wallpaper_path
    except Exception as e:
        print(f"Error getting current wallpaper path: {e}")
        return None

def RestoreOriginalWallpaper():
    try:
        if os.path.exists(OriginalWallpaperPath):
            absolute_path = os.path.abspath(OriginalWallpaperPath)
            print(f"Restoring wallpaper from: {absolute_path}")

            if os.path.getsize(absolute_path) > 0:
                result = ctypes.windll.user32.SystemParametersInfoW(
                    0x0014, 0, absolute_path, 3)

                if result:
                    try:
                        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_SET_VALUE)
                        winreg.SetValueEx(key, 'WallPaper', 0, winreg.REG_SZ, absolute_path)
                        winreg.CloseKey(key)
                    except Exception as reg_error:
                        print(f"Warning: Registry update failed: {reg_error}")

                    print("Original wallpaper restored successfully")
                    return True
                else:
                    print(f"SystemParametersInfoW failed with error code: {ctypes.GetLastError()}")
                    return False
            else:
                print("Original wallpaper file exists but is empty or corrupted")
                return False
        else:
            print(f"Original wallpaper backup not found at {OriginalWallpaperPath}")
            return False
    except Exception as e:
        print(f"Error restoring original wallpaper: {e}")
        return False

def SetAnimatedWallpaper(video_path):
    global WallpaperProcess
    try:
        if WallpaperProcess and WallpaperProcess.poll() is None:
            WallpaperProcess.terminate()
            WallpaperProcess.wait()
        current_file = os.path.abspath(__file__)
        base_dir = os.path.dirname(current_file)
        wallpaper_script = os.path.join(base_dir, "Wallpaper.py")
        WallpaperProcess = subprocess.Popen([sys.executable, wallpaper_script, video_path])

        time.sleep(0.5)

        if WallpaperProcess.poll() is None:
            print(f"Wallpaper process started with PID: {WallpaperProcess.pid}")
            return True
        else:
            print("Wallpaper process failed to start")
            return False
    except Exception as e:
        print(f"Error setting wallpaper: {e}")
        return False

def DisableAnimatedWallpaper():
    global WallpaperProcess
    try:
        print("Attempting to disable animated wallpaper...")

        wallpaper_restored = RestoreOriginalWallpaper()

        if WallpaperProcess and WallpaperProcess.poll() is None:
            print(f"Terminating wallpaper process with PID: {WallpaperProcess.pid}")
            WallpaperProcess.terminate()
            WallpaperProcess.wait(timeout=5)
            WallpaperProcess = None
            print("Wallpaper process terminated")
        else:
            print("No active wallpaper process found")

        return wallpaper_restored
    except Exception as e:
        print(f"Error disabling wallpaper: {e}")
        return False

def IsWallpaperRunning():
    global WallpaperProcess
    try:
        is_running = WallpaperProcess is not None and WallpaperProcess.poll() is None
        print(f"Wallpaper process status: {'Running' if is_running else 'Not running'}")
        return is_running
    except Exception as e:
        print(f"Error checking if wallpaper is running: {e}")
        return False
