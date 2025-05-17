<<<<<<< HEAD
#---------< Libs >----------
import json,os,requests,re
from contextlib import closing
#---------< Paths >---------
DataPath = os.path.join(".","BackgroundsData","BackgroundsData.json")
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

def GetCoversPath(WithFolder : bool=True):
    Index = 0
    CoversFolderPath = os.path.join(".","static","Images","Covers")
    CoversPath = os.listdir(CoversFolderPath)

    if WithFolder:
        for Item in CoversPath:

            PathStructure = "Images/Covers/"
            Item = PathStructure+Item
            CoversPath[Index] = Item
            Index+=1
    else:
        return CoversPath

    return CoversPath

def GetBackgrounds():
    with open(DataPath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

def DownloadBackground(BackgroundName: str):
    BackgroundName += ".mp4"
    Link = f"https://raw.githubusercontent.com/YashaNajafi/AniWall/refs/heads/main/Wallpapers/{BackgroundName}"

    current_file = os.path.abspath(__file__)
    base_dir = os.path.dirname(os.path.dirname(current_file))
    videos_dir = os.path.join(base_dir, "Videos")
    os.makedirs(videos_dir, exist_ok=True)

    try:
        with closing(requests.get(Link, stream=True)) as Response:
            Response.raise_for_status()
            file_path = os.path.join(videos_dir, BackgroundName)
            with open(file_path, 'wb') as file:
                for chunk in Response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
        print("Download completed successfully.")
    except requests.exceptions.RequestException as e:
        print(f"File Download Error: {e}")

def CheckWallpaperExist(BackgroundName: str) -> bool:
    BackgroundName += ".mp4"

    current_file = os.path.abspath(__file__)
    base_dir = os.path.dirname(os.path.dirname(current_file))
    videos_dir = os.path.join(base_dir, "Videos")

    file_path = os.path.join(videos_dir, BackgroundName)

    return os.path.isfile(file_path)

def GetCategory(CategorySTR : str):
    Match = re.search(r'\(([^()]*)\)', CategorySTR)
    if Match:
        return Match.group(1).strip()
    return CategorySTR.strip()

def GetMainCategory(CategorySTR: str):
    Match = re.search(r'^([^(]+)', CategorySTR)
    if Match:
        return Match.group(1).strip()
    return CategorySTR.strip()
=======
<<<<<<< HEAD
#---------< Libs >----------
import json,os,requests,re
from contextlib import closing
#---------< Paths >---------
DataPath = os.path.join(".","BackgroundsData","BackgroundsData.json")
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

def GetCoversPath(WithFolder : bool=True):
    Index = 0
    CoversFolderPath = os.path.join(".","static","Images","Covers")
    CoversPath = os.listdir(CoversFolderPath)

    if WithFolder:
        for Item in CoversPath:

            PathStructure = "Images/Covers/"
            Item = PathStructure+Item
            CoversPath[Index] = Item
            Index+=1
    else:
        return CoversPath

    return CoversPath

def GetBackgrounds():
    with open(DataPath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

def DownloadBackground(BackgroundName: str):
    BackgroundName += ".mp4"
    Link = f"https://raw.githubusercontent.com/YashaNajafi/AniWall/refs/heads/main/Wallpapers/{BackgroundName}"

    current_file = os.path.abspath(__file__)
    base_dir = os.path.dirname(os.path.dirname(current_file))
    videos_dir = os.path.join(base_dir, "Videos")
    os.makedirs(videos_dir, exist_ok=True)

    try:
        with closing(requests.get(Link, stream=True)) as Response:
            Response.raise_for_status()
            file_path = os.path.join(videos_dir, BackgroundName)
            with open(file_path, 'wb') as file:
                for chunk in Response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
        print("Download completed successfully.")
    except requests.exceptions.RequestException as e:
        print(f"File Download Error: {e}")

def CheckWallpaperExist(BackgroundName: str) -> bool:
    BackgroundName += ".mp4"

    current_file = os.path.abspath(__file__)
    base_dir = os.path.dirname(os.path.dirname(current_file))
    videos_dir = os.path.join(base_dir, "Videos")

    file_path = os.path.join(videos_dir, BackgroundName)

    return os.path.isfile(file_path)

def GetCategory(CategorySTR : str):
    Match = re.search(r'\(([^()]*)\)', CategorySTR)
    if Match:
        return Match.group(1).strip()
    return CategorySTR.strip()

def GetMainCategory(CategorySTR: str):
    Match = re.search(r'^([^(]+)', CategorySTR)
    if Match:
        return Match.group(1).strip()
    return CategorySTR.strip()
=======
# #---------< Libs >----------
# import json, os, requests, re
# from contextlib import closing
# import threading
# import time
# import ctypes
# import subprocess
# import winreg
# import sys

# #---------< Paths >---------
# DataPath = os.path.join(".","BackgroundsData","BackgroundsData.json")
# ORIGINAL_WALLPAPER_PATH = os.path.join(".","BackgroundsData","original_wallpaper.jpg")

# #---------< Functions >---------
# def GetMainData():
#     with open(DataPath, 'r', encoding='utf-8') as file:
#         data = json.load(file)

#     return data

# def GetDataOfWallpaper(SearchType: str, SearchValue: str = None):
#     with open(DataPath, 'r', encoding='utf-8') as file:
#         data = json.load(file)

#     backgrounds = data.get("Backgrounds", [])

#     if SearchType == "ByName":
#         if not SearchValue:
#             raise ValueError("SearchValue is required for ByName search.")
#         result = [bg for bg in backgrounds if bg["Name"].lower() == SearchValue.lower()]
#         return result[0] if result else None

#     elif SearchType == "ByCategory":
#         if not SearchValue:
#             raise ValueError("SearchValue is required for ByCategory search.")
#         result = [bg for bg in backgrounds if SearchValue.lower() in bg["Categories"].lower()]
#         return result

#     else:
#         raise TypeError(f"Type {SearchType} Not Defined!")

# def GetCoversPath(WithFolder : bool=True):
#     Index = 0
#     CoversFolderPath = os.path.join(".","static","Images","Covers")
#     CoversPath = os.listdir(CoversFolderPath)

#     if WithFolder:
#         for Item in CoversPath:

#             PathStructure = "Images/Covers/"
#             Item = PathStructure+Item
#             CoversPath[Index] = Item
#             Index+=1
#     else:
#         return CoversPath

#     return CoversPath

# def GetBackgrounds():
#     with open(DataPath, 'r', encoding='utf-8') as file:
#         data = json.load(file)

#     return data

# def DownloadBackground(BackgroundName: str, progress_tracker=None):
#     filename = f"{BackgroundName}.mp4"
#     Link = f"https://raw.githubusercontent.com/YashaNajafi/AniWall/refs/heads/main/Wallpapers/{filename}"

#     current_file = os.path.abspath(__file__)
#     base_dir = os.path.dirname(os.path.dirname(current_file))
#     videos_dir = os.path.join(base_dir, "Videos")
#     os.makedirs(videos_dir, exist_ok=True)
#     file_path = os.path.join(videos_dir, filename)

#     try:
#         # First create an empty file that we'll write to in chunks
#         with open(file_path, 'wb') as _:
#             pass  # Create empty file

#         # Get file size and update background data
#         session = requests.Session()

#         # First make a HEAD request to get content length without downloading
#         try:
#             head_response = session.head(Link)
#             head_response.raise_for_status()
#             total_size = int(head_response.headers.get('content-length', 0))

#             # Update progress tracker with total size
#             if progress_tracker and BackgroundName in progress_tracker:
#                 progress_tracker[BackgroundName]['total_size'] = total_size

#             # Update the background data to store the file size
#             try:
#                 with open(DataPath, 'r', encoding='utf-8') as file:
#                     data = json.load(file)

#                 # Find the background in the data
#                 for bg in data.get("Backgrounds", []):
#                     if bg["Name"] == BackgroundName:
#                         bg["FileSize"] = total_size
#                         break

#                 # Save updated data
#                 with open(DataPath, 'w', encoding='utf-8') as file:
#                     json.dump(data, file, indent=4)
#             except Exception as e:
#                 print(f"Failed to update file size in background data: {e}")

#         except Exception as e:
#             print(f"Failed to get file size with HEAD request: {e}")
#             total_size = 0

#         # Download the file
#         with closing(session.get(Link, stream=True)) as response:
#             response.raise_for_status()

#             # If we didn't get the size from HEAD request, try to get it now
#             if total_size == 0:
#                 total_size = int(response.headers.get('content-length', 0))
#                 if progress_tracker and BackgroundName in progress_tracker:
#                     progress_tracker[BackgroundName]['total_size'] = total_size

#             # Use smaller chunks for more frequent updates
#             chunk_size = 4096  # Smaller chunk size for more granular updates
#             current_size = 0
#             last_update_time = time.time()
#             update_interval = 0.05  # Update progress more frequently (50ms)

#             with open(file_path, 'wb') as file:
#                 for chunk in response.iter_content(chunk_size=chunk_size):
#                     if chunk:
#                         file.write(chunk)
#                         current_size += len(chunk)

#                         # Update progress tracker more frequently
#                         current_time = time.time()
#                         if (current_time - last_update_time) > update_interval:
#                             if progress_tracker and BackgroundName in progress_tracker:
#                                 progress_tracker[BackgroundName]['current_size'] = current_size
#                                 if total_size > 0:
#                                     # Calculate exact percentage without rounding or limiting
#                                     progress = (current_size / total_size) * 100
#                                     progress_tracker[BackgroundName]['progress'] = progress
#                             last_update_time = current_time

#         # Mark download as complete
#         if progress_tracker and BackgroundName in progress_tracker:
#             progress_tracker[BackgroundName]['current_size'] = total_size
#             progress_tracker[BackgroundName]['progress'] = 100
#             progress_tracker[BackgroundName]['is_complete'] = True

#         print("Download completed successfully.")
#         return True

#     except Exception as e:
#         print(f"File Download Error: {e}")
#         # Update progress tracker with error
#         if progress_tracker and BackgroundName in progress_tracker:
#             progress_tracker[BackgroundName]['error'] = str(e)

#         # If download fails, delete the partially downloaded file
#         if os.path.exists(file_path):
#             try:
#                 os.remove(file_path)
#             except:
#                 pass
#         return False

# def CheckWallpaperExist(BackgroundName: str) -> bool:
#     BackgroundName += ".mp4"

#     current_file = os.path.abspath(__file__)
#     base_dir = os.path.dirname(os.path.dirname(current_file))
#     videos_dir = os.path.join(base_dir, "Videos")

#     file_path = os.path.join(videos_dir, BackgroundName)

#     return os.path.isfile(file_path)

# def GetCategory(CategorySTR : str):
#     Match = re.search(r'\(([^()]*)\)', CategorySTR)
#     if Match:
#         return Match.group(1).strip()
#     return CategorySTR.strip()

# def GetMainCategory(CategorySTR: str):
#     Match = re.search(r'^([^(]+)', CategorySTR)
#     if Match:
#         return Match.group(1).strip()
#     return CategorySTR.strip()

# # New functions for wallpaper management

# def BackupOriginalWallpaper():
#     """Backup the current desktop wallpaper"""
#     try:
#         # Create BackgroundsData directory if it doesn't exist
#         data_dir = os.path.dirname(ORIGINAL_WALLPAPER_PATH)
#         os.makedirs(data_dir, exist_ok=True)

#         # Get the current wallpaper path
#         wallpaper_path = GetCurrentWallpaperPath()

#         if wallpaper_path and os.path.exists(wallpaper_path):
#             # Copy the current wallpaper to our backup location
#             with open(wallpaper_path, 'rb') as src_file:
#                 with open(ORIGINAL_WALLPAPER_PATH, 'wb') as dst_file:
#                     dst_file.write(src_file.read())
#             return True
#         else:
#             print(f"Could not find current wallpaper at: {wallpaper_path}")
#             return False
#     except Exception as e:
#         print(f"Error backing up original wallpaper: {e}")
#         return False

# def GetCurrentWallpaperPath():
#     """Get the path of the current Windows wallpaper"""
#     try:
#         # Open registry key where wallpaper path is stored
#         key = winreg.OpenKey(
#             winreg.HKEY_CURRENT_USER,
#             r"Control Panel\Desktop"
#         )

#         # Read the wallpaper value
#         wallpaper_path = winreg.QueryValueEx(key, 'WallPaper')[0]
#         winreg.CloseKey(key)

#         return wallpaper_path
#     except Exception as e:
#         print(f"Error getting current wallpaper path: {e}")
#         return None

# def RestoreOriginalWallpaper():
#     """Restore the original wallpaper that was active before setting the animated one"""
#     try:
#         if os.path.exists(ORIGINAL_WALLPAPER_PATH):
#             # Use ctypes to change the wallpaper
#             ctypes.windll.user32.SystemParametersInfoW(
#                 20, 0, ORIGINAL_WALLPAPER_PATH, 3
#             )
#             print("Original wallpaper restored")
#             return True
#         else:
#             print("Original wallpaper backup not found")
#             return False
#     except Exception as e:
#         print(f"Error restoring original wallpaper: {e}")
#         return False

# def DisableAnimatedWallpaper():
#     """Terminates any running animated wallpaper processes and restores original wallpaper"""
#     try:
#         # Find and kill any running VideoWallpaper processes
#         # Since we're using PyQt, we'll look for python processes that might be our wallpaper
#         if sys.platform == 'win32':
#             # Use taskkill to forcefully terminate possible wallpaper processes
#             try:
#                 # Look for python processes that might be our wallpaper
#                 subprocess.run(['taskkill', '/F', '/IM', 'python.exe'],
#                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
#             except Exception as e:
#                 print(f"Error killing processes: {e}")

#         # Restore the original wallpaper
#         return RestoreOriginalWallpaper()
#     except Exception as e:
#         print(f"Error disabling animated wallpaper: {e}")
#         return False

# def IsWallpaperRunning():
#     """Check if the animated wallpaper is currently running"""
#     # This is a simplified check that could be improved
#     # A more robust solution would track the wallpaper process ID
#     try:
#         if sys.platform == 'win32':
#             # Check for WorkerW process running our app
#             # This is an approximation - in a full solution we would track the PID
#             result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'],
#                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             return b'python.exe' in result.stdout
#         return False
#     except Exception as e:
#         print(f"Error checking if wallpaper is running: {e}")
#         return False
import json, os, requests, re
from contextlib import closing
import threading
import time
import ctypes
import subprocess
import winreg
import sys

#---------< Paths >---------
DataPath = os.path.join(".","BackgroundsData","BackgroundsData.json")
ORIGINAL_WALLPAPER_PATH = os.path.join(".","BackgroundsData","original_wallpaper.jpg")

# Global variable to track wallpaper process
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
        data_dir = os.path.dirname(ORIGINAL_WALLPAPER_PATH)
        os.makedirs(data_dir, exist_ok=True)
        wallpaper_path = GetCurrentWallpaperPath()
        if wallpaper_path and os.path.exists(wallpaper_path):
            with open(wallpaper_path, 'rb') as src_file:
                with open(ORIGINAL_WALLPAPER_PATH, 'wb') as dst_file:
                    dst_file.write(src_file.read())
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
            ctypes.windll.user32.SystemParametersInfoW(20, 0, ORIGINAL_WALLPAPER_PATH, 3)
            print("Original wallpaper restored")
            return True
        else:
            print("Original wallpaper backup not found")
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
        wallpaper_script = os.path.join(base_dir, "Wallpaper.py")
        wallpaper_process = subprocess.Popen([sys.executable, wallpaper_script, video_path])
        return True
    except Exception as e:
        print(f"Error setting wallpaper: {e}")
        return False

def DisableAnimatedWallpaper():
    global wallpaper_process
    try:
        if wallpaper_process and wallpaper_process.poll() is None:
            wallpaper_process.terminate()
            wallpaper_process.wait()
            wallpaper_process = None
        return RestoreOriginalWallpaper()
    except Exception as e:
        print(f"Error disabling wallpaper: {e}")
        return False

def IsWallpaperRunning():
    global wallpaper_process
    try:
        return wallpaper_process is not None and wallpaper_process.poll() is None
    except Exception as e:
        print(f"Error checking if wallpaper is running: {e}")
        return False
>>>>>>> f0ac188 (Initial commit)
>>>>>>> c6a8d8e (Initial commit)
