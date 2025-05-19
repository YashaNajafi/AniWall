#---------< Libs >----------
import json, os, requests, re
from contextlib import closing
import threading
import time
import ctypes
import subprocess
import winreg
import sys
import shutil

#---------< Paths >---------
def ResourcePath(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

DataPath = ResourcePath(os.path.join(".","BackgroundsData","BackgroundsData.json"))
ORIGINAL_WALLPAPER_PATH = ResourcePath(os.path.join(".","BackgroundsData","original_wallpaper.jpg"))
wallpaper_process = None
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
    CoversFolderPath = ResourcePath(os.path.join(".","static","Images","Covers"))
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
    videos_dir = ResourcePath(os.path.join(base_dir, "Videos"))
    os.makedirs(videos_dir, exist_ok=True)
    file_path = ResourcePath(os.path.join(videos_dir, filename))
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
    base_dir = ResourcePath(os.path.dirname(os.path.dirname(current_file)))
    videos_dir = ResourcePath(os.path.join(base_dir, "Videos"))
    file_path = ResourcePath(os.path.join(videos_dir, BackgroundName))
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
        data_dir = os.path.dirname(ORIGINAL_WALLPAPER_PATH)
        os.makedirs(data_dir, exist_ok=True)
        wallpaper_path = GetCurrentWallpaperPath()
        if wallpaper_path and os.path.exists(wallpaper_path):
            shutil.copy2(wallpaper_path, ORIGINAL_WALLPAPER_PATH)
            print(f"Original wallpaper backed up successfully from {wallpaper_path} to {ORIGINAL_WALLPAPER_PATH}")
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
        if os.path.exists(ORIGINAL_WALLPAPER_PATH):
            absolute_path = os.path.abspath(ORIGINAL_WALLPAPER_PATH)
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
            print(f"Original wallpaper backup not found at {ORIGINAL_WALLPAPER_PATH}")
            return False
    except Exception as e:
        print(f"Error restoring original wallpaper: {e}")
        return False

def SetAnimatedWallpaper(video_path):
    global wallpaper_process
    try:
        if wallpaper_process and wallpaper_process.poll() is None:
            wallpaper_process.terminate()
            wallpaper_process.wait()
        current_file = os.path.abspath(__file__)
        base_dir = os.path.dirname(current_file)
        wallpaper_script = ResourcePath(os.path.join(base_dir, "Wallpaper.py"))
        wallpaper_process = subprocess.Popen([sys.executable, wallpaper_script, video_path])

        time.sleep(0.5)

        if wallpaper_process.poll() is None:
            print(f"Wallpaper process started with PID: {wallpaper_process.pid}")
            return True
        else:
            print("Wallpaper process failed to start")
            return False
    except Exception as e:
        print(f"Error setting wallpaper: {e}")
        return False

def DisableAnimatedWallpaper():
    global wallpaper_process
    try:
        print("Attempting to disable animated wallpaper...")

        wallpaper_restored = RestoreOriginalWallpaper()

        if wallpaper_process and wallpaper_process.poll() is None:
            print(f"Terminating wallpaper process with PID: {wallpaper_process.pid}")
            wallpaper_process.terminate()
            wallpaper_process.wait(timeout=5)
            wallpaper_process = None
            print("Wallpaper process terminated")
        else:
            print("No active wallpaper process found")

        return wallpaper_restored
    except Exception as e:
        print(f"Error disabling wallpaper: {e}")
        return False

def IsWallpaperRunning():
    global wallpaper_process
    try:
        is_running = wallpaper_process is not None and wallpaper_process.poll() is None
        print(f"Wallpaper process status: {'Running' if is_running else 'Not running'}")
        return is_running
    except Exception as e:
        print(f"Error checking if wallpaper is running: {e}")
        return False
